from rest_framework.test import APITestCase
from model_bakery import baker
from rest_framework_simplejwt.tokens import RefreshToken
from courses.models import Course
from students_courses.models import StudentCourse
from uuid import uuid4 as v4
from datetime import datetime


class TestCreateCourseView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/courses/"
        cls.superuser = baker.make("accounts.Account", is_superuser=True)
        cls.common_user = baker.make("accounts.Account", is_superuser=False)

        cls.superuser_token = str(
            RefreshToken.for_user(cls.superuser).access_token,
        )
        cls.common_user_token = str(
            RefreshToken.for_user(cls.common_user).access_token,
        )

    def test_can_not_create_a_course_without_token(self):
        expected = 401
        course_data = {
            "name": "Python",
            "start_date": "2023-08-28",
            "end_date": "2023-10-28",
        }
        response = self.client.post(self.BASE_URL, course_data, format="json")

        message = (
            f"\n<{self.BASE_URL}> status code da rota está diferente de {expected}."
        )
        self.assertEqual(expected, response.status_code, message)

    def test_can_not_create_a_course_with_common_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.common_user_token)
        course_data = {
            "name": "Python",
            "start_date": "2023-08-28",
            "end_date": "2023-10-28",
        }
        response = self.client.post(self.BASE_URL, course_data, format="json")
        expected_status = 403
        result_status = response.status_code
        message = f"\n<{self.BASE_URL}> status code da rota está diferente de {expected_status}."
        self.assertEqual(expected_status, result_status, message)

    def test_can_not_create_course_missing_body(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.superuser_token)
        expected = 400
        course_data = {}
        response = self.client.post(self.BASE_URL, course_data, format="json")
        message = (
            f"\n<{self.BASE_URL}> status code da rota está" f" diferente de {expected}."
        )
        self.assertEqual(expected, response.status_code, message)

        expected_keys = {"name", "start_date", "end_date"}
        result = set(response.json().keys())
        message = (
            f"\n<{self.BASE_URL}> retorno diferente do esperado."
            f"\nAs chaves obrigatórias são: {expected_keys}"
        )
        self.assertSetEqual(expected_keys, result, message)

        expected_values = [
            ["This field is required."],
            ["This field is required."],
            ["This field is required."],
        ]

        result = list(response.json().values())
        message = (
            f"\n<{self.BASE_URL}> retorno diferente do esperado."
            f"\nO valor de cada chave obrigatória deve ser: {expected_values}"
        )
        self.assertListEqual(expected_values, result, message)

    def test_can_not_create_course_with_duplicate_name(self):
        baker.make("courses.Course", name="Python")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.superuser_token)

        course_data = {
            "name": "Python",
            "start_date": "2023-08-28",
            "end_date": "2023-10-28",
        }
        response = self.client.post(
            self.BASE_URL,
            course_data,
            format="json",
        )
        expected = 400
        result = response.status_code
        message = (
            f"\n<{self.BASE_URL}> status code da rota está diferente de {expected}."
        )
        self.assertEqual(expected, result, message)

        expected = {"name": ["course with this name already exists."]}
        result = response.json()
        message = f"\n<{self.BASE_URL}> corpo de retorna da rota está diferente de {expected}."
        self.assertDictEqual(expected, result, message)

    def test_can_create_course_without_instructor_using_superuser_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.superuser_token)
        expected_status = 201
        course_data = {
            "name": "Python",
            "start_date": "2023-08-28",
            "end_date": "2023-10-28",
        }
        response = self.client.post(
            self.BASE_URL,
            course_data,
            format="json",
        )
        message = f"\n<{self.BASE_URL}> status code da rota está diferente de {expected_status}."
        self.assertEqual(expected_status, response.status_code, message)

        expected_keys = {
            "id",
            "name",
            "status",
            "start_date",
            "end_date",
            "instructor",
            "contents",
            "students_courses",
        }
        result = set(response.json().keys())
        message = (
            f"\n<{self.BASE_URL}> retorno diferente do esperado."
            f"\nA resposta deve ter somente estas chaves: {expected_keys}."
        )
        self.assertSetEqual(expected_keys, result, message)

        result = response.json()["instructor"]
        message = (
            f"<{self.BASE_URL}> o valor retornado da chave "
            "instructor"
            " deve ser nulo."
        )
        self.assertIsNone(result, message)

        expected = 1
        result = Course.objects.all().count()
        message = (
            f"\n<{self.BASE_URL}> não foi feito o salvamento correto"
            " do curso no banco de dados."
        )
        self.assertEqual(
            expected,
            result,
        )

    def test_can_create_course_with_instructor_using_superuser_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.superuser_token)
        expected = 201
        course_data = {
            "name": "Python",
            "start_date": "2023-08-28",
            "end_date": "2023-10-28",
            "instructor": self.superuser.id,
        }
        response = self.client.post(
            self.BASE_URL,
            course_data,
            format="json",
        )
        message = (
            f"\n<{self.BASE_URL}> status code da rota está diferente de {expected}."
        )
        self.assertEqual(expected, response.status_code, message)

        expected_keys = {
            "id",
            "name",
            "status",
            "start_date",
            "end_date",
            "instructor",
            "contents",
            "students_courses",
        }
        result = set(response.json().keys())
        message = (
            f"\n<{self.BASE_URL}> retorno diferente do esperado."
            f"\nA resposta deve ter somente estas chaves: {expected_keys}."
        )
        self.assertSetEqual(expected_keys, result, message)

        result = response.json()["instructor"]
        expected_value = str(self.superuser.id)
        message = (
            f"<{self.BASE_URL}> o valor retornado da chave "
            "instructor"
            f" não está igual ao valor do id do usuário"
        )
        self.assertEqual(expected_value, result, message)

        expected = 1
        result = Course.objects.all().count()
        message = (
            f"\n<{self.BASE_URL}> não foi feito o salvamento correto"
            " do curso no banco de dados."
        )
        self.assertEqual(
            expected,
            result,
        )


class TestReadCourseView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/courses/"
        cls.superuser = baker.make("accounts.Account", is_superuser=True)
        cls.common_user = baker.make("accounts.Account", is_superuser=False)

        cls.superuser_token = str(
            RefreshToken.for_user(cls.superuser).access_token,
        )
        cls.common_user_token = str(
            RefreshToken.for_user(cls.common_user).access_token,
        )
        cls.courses_without_students = baker.make("courses.Course", _quantity=3)

    def test_can_read_all_courses_using_superuser_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.superuser_token)
        response = self.client.get(self.BASE_URL)
        expected_status_code = 200
        result_status_code = response.status_code
        message = f"<{self.BASE_URL}> status code retornado diferente de {expected_status_code}."
        self.assertEqual(expected_status_code, result_status_code, message)

        expected_course_quantity = len(self.courses_without_students)
        result_course_quantity = len(response.json())
        message = f"<{self.BASE_URL}> listagem não está retornando todos os cursos."
        self.assertEqual(expected_course_quantity, result_course_quantity, message)

    def test_can_read_only_own_courses_using_common_token(self):
        course = baker.make("courses.Course")
        course.students.add(self.common_user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.common_user_token)
        response = self.client.get(self.BASE_URL)
        expected_status_code = 200
        result_status_code = response.status_code
        message = f"<{self.BASE_URL}> status code retornado diferente de {expected_status_code}."
        self.assertEqual(expected_status_code, result_status_code, message)

        expected_course_quantity = 1
        result_course_quantity = len(response.json())
        message = f"<{self.BASE_URL}> listagem não está retornando somente os cursos que o usuário participa."
        self.assertEqual(expected_course_quantity, result_course_quantity, message)


class TestDeleteCourseView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/courses/"
        cls.superuser = baker.make("accounts.Account", is_superuser=True)
        cls.common_user = baker.make("accounts.Account", is_superuser=False)

        cls.superuser_token = str(
            RefreshToken.for_user(cls.superuser).access_token,
        )
        cls.common_user_token = str(
            RefreshToken.for_user(cls.common_user).access_token,
        )

    def test_can_delete_course_using_superuser_token(self):
        course = baker.make("courses.Course")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.superuser_token)
        response = self.client.delete(self.BASE_URL + str(course.id) + "/")
        expected_status_code = 204
        result_status_code = response.status_code
        message = f"<{self.BASE_URL}{course.id}/> status code retornado está diferente de {expected_status_code}."
        self.assertEqual(expected_status_code, result_status_code, message)

        expected_count = 0
        result_count = Course.objects.all().count()
        message = f"<{self.BASE_URL}{course.id}/> deleção não removeu o curso do banco de dados."
        self.assertEqual(expected_count, result_count, message)

    def test_can_not_delete_course_using_common_user_token(self):
        course = baker.make("courses.Course")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.common_user_token)
        response = self.client.delete(self.BASE_URL + str(course.id) + "/")
        expected_status_code = 403
        result_status_code = response.status_code
        message = f"<{self.BASE_URL}{course.id}/> status code retornado está diferente de {expected_status_code}."
        self.assertEqual(expected_status_code, result_status_code, message)

        expected_count = 1
        result_count = Course.objects.all().count()
        message = f"<{self.BASE_URL}{course.id}/> não foi impedido que o curso fosse excluído do banco de dados."
        self.assertEqual(expected_count, result_count, message)


class TestRetrieveCourseView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/courses/"
        cls.superuser = baker.make("accounts.Account", is_superuser=True)
        cls.common_user = baker.make("accounts.Account", is_superuser=False)

        cls.superuser_token = str(
            RefreshToken.for_user(cls.superuser).access_token,
        )
        cls.common_user_token = str(
            RefreshToken.for_user(cls.common_user).access_token,
        )

    def test_can_retrieve_course_using_superuser_token(self):
        course = baker.make("courses.Course")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.superuser_token)
        response = self.client.get(self.BASE_URL + str(course.id) + "/")
        expected_status_code = 200
        result_status_code = response.status_code
        message = f"<{self.BASE_URL}{course.id}/> status code retornado diferente de {expected_status_code}."
        self.assertEqual(expected_status_code, result_status_code, message)

        expected_body = {
            "id": str(course.id),
            "name": course.name,
            "status": "not started",
            "start_date": datetime.strftime(course.start_date, "%Y-%m-%d"),
            "end_date": datetime.strftime(course.end_date, "%Y-%m-%d"),
            "instructor": course.instructor,
            "students_courses": [],
            "contents": [],
        }
        result_body = response.json()
        message = (
            f"<{self.BASE_URL}{course.id}/> corpo de resposta está diferente do esperado."
            f"Deve ser semelhante a este {expected_body}."
        )
        self.assertEqual(expected_body, result_body, message)

    def test_can_not_retrieve_a_course_which_not_exists_using_superuser_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.superuser_token)
        response = self.client.get(self.BASE_URL + str(v4()) + "/")
        expected_status_code = 404
        result_status_code = response.status_code
        message = f"<{self.BASE_URL}{v4()}/> status code retornado diferente de {expected_status_code}."
        self.assertEqual(expected_status_code, result_status_code, message)


class TestUpdateCourseView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/courses/"
        cls.superuser = baker.make("accounts.Account", is_superuser=True)
        cls.common_user = baker.make("accounts.Account", is_superuser=False)

        cls.superuser_token = str(
            RefreshToken.for_user(cls.superuser).access_token,
        )
        cls.common_user_token = str(
            RefreshToken.for_user(cls.common_user).access_token,
        )

    def test_can_update_course_using_superuser_token(self):
        course = baker.make("courses.Course")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.superuser_token)
        course_data = {"name": "React"}
        response = self.client.patch(
            self.BASE_URL + str(course.id) + "/", course_data, format="json"
        )
        expected_status_code = 200
        result_status_code = response.status_code
        message = f"<{self.BASE_URL}{course.id}/> status code retornado diferente de {expected_status_code}."
        self.assertEqual(expected_status_code, result_status_code, message)

        expected_count = 1
        result_count = Course.objects.filter(name=course_data["name"]).count()
        message = f"<{self.BASE_URL}{course.id}/> atualização não foi persistida no banco de dados."
        self.assertEqual(expected_count, result_count, message)

    def test_can_not_update_course_using_common_user_token(self):
        course = baker.make("courses.Course")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.common_user_token)
        course_data = {"name": "React"}
        response = self.client.patch(
            self.BASE_URL + str(course.id) + "/", course_data, format="json"
        )
        expected_status_code = 403
        result_status_code = response.status_code
        message = f"<{self.BASE_URL}{course.id}/> status code retornado diferente de {expected_status_code}."
        self.assertEqual(expected_status_code, result_status_code, message)

    def test_can_add_student_into_course_using_superuser_token(self):
        course = baker.make("courses.Course")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.superuser_token)
        course_data = {"students_courses": [{"student_email": self.common_user.email}]}
        response = self.client.put(
            f"{self.BASE_URL}{course.id}/students/", course_data, format="json"
        )
        expected_status_code = 200
        result_status_code = response.status_code
        message = f"\n<{self.BASE_URL}{course.id}/students/> status code da rota está diferente de {expected_status_code}."
        self.assertEqual(expected_status_code, result_status_code, message)

        expected_keys = {"id", "name", "students_courses"}
        result_keys = set(response.json().keys())
        message = (
            f"\n<{self.BASE_URL}{course.id}/students/> retorno diferente do esperado."
            f"\nA resposta deve ter estas chaves principais: {expected_keys}."
        )
        self.assertSetEqual(expected_keys, result_keys, message)

        pivot = StudentCourse.objects.filter(course=course)
        expected_count = pivot.count()
        result_count = len(response.json()["students_courses"])
        message = f"<{self.BASE_URL}{course.id}/students/> Criação não foi salva no banco de dados corretamente."
        self.assertEqual(expected_count, result_count, message)

        expected_body = {
            "id": str(course.id),
            "name": course.name,
            "students_courses": [
                {
                    "id": str(pivot.first().id),
                    "student_id": str(self.common_user.id),
                    "student_username": self.common_user.username,
                    "student_email": self.common_user.email,
                    "status": "pending",
                }
            ],
        }
        result_body = response.json()
        message = (
            f"\n<{self.BASE_URL}{course.id}/students/> retorno diferente do esperado."
            f"\nCorpo de resposta deve ser semelhante a este {expected_body}."
        )
        self.assertDictEqual(expected_body, result_body, message)

    def test_can_not_add_invalid_student_into_course_using_superuser_token(self):
        course = baker.make("courses.Course")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.superuser_token)
        course_data = {
            "students_courses": [{"student_email": "email@quenaoexiste.com.br"}]
        }
        response = self.client.put(
            f"{self.BASE_URL}{course.id}/students/", course_data, format="json"
        )
        expected_status_code = 400
        result_status_code = response.status_code
        message = f"\n<{self.BASE_URL}{course.id}/students/> status code da rota está diferente de {expected_status_code}."
        self.assertEqual(expected_status_code, result_status_code, message)

        expected_key = {"detail"}
        result_key = set(response.json().keys())
        message = (
            f"\n<{self.BASE_URL}{course.id}/students/> retorno diferente do esperado."
            f"\nCorpo de resposta deve conter somente as chaves: {expected_key}"
        )
        self.assertSetEqual(expected_key, result_key, message)
        expected_body = {
            "detail": (
                "No active accounts was found: "
                f"{course_data['students_courses'][0]['student_email']}."
            )
        }
        result_body = response.json()
        message = (
            f"\n<{self.BASE_URL}{course.id}/students/> retorno diferente do esperado."
            f"\nCorpo de resposta deve ser semelhante a este {expected_body}."
        )
        self.assertDictEqual(expected_body, result_body, message)
