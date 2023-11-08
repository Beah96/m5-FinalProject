from rest_framework.test import APITestCase
from model_bakery import baker
from rest_framework_simplejwt.tokens import RefreshToken
from contents.models import Content

from uuid import uuid4 as v4


class TestCreateContentView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/courses/{}/contents/"
        cls.superuser = baker.make("accounts.Account", is_superuser=True)
        cls.common_user = baker.make("accounts.Account", is_superuser=False)

        cls.superuser_token = str(
            RefreshToken.for_user(cls.superuser).access_token,
        )
        cls.common_user_token = str(
            RefreshToken.for_user(cls.common_user).access_token,
        )

    def test_can_create_content_using_superuser_token(self):
        course = baker.make("courses.Course")
        content_data = {
            "name": "Estruturas de repetição",
            "content": "...",
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.superuser_token)
        url = self.BASE_URL.format(course.id)
        response = self.client.post(url, content_data, format="json")
        expected_status_code = 201
        result_status_code = response.status_code
        message = (
            f"<{url}> status code retornado está diferente de {expected_status_code}."
        )
        self.assertEqual(expected_status_code, result_status_code, message)

        expected_keys = {"id", "name", "content", "video_url"}
        result_body = set(response.json().keys())
        message = (
            f"<{url}> corpo de resposta deve trazer somente as chaves {expected_keys}."
        )
        self.assertEqual(expected_keys, result_body, message)

    def test_can_not_create_content_using_superuser_token_missing_body(self):
        course = baker.make("courses.Course")
        content_data = {}
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.superuser_token)
        url = self.BASE_URL.format(course.id)
        response = self.client.post(url, content_data, format="json")
        expected_status_code = 400
        result_status_code = response.status_code
        message = (
            f"<{url}> status code retornado está diferente de {expected_status_code}."
        )
        self.assertEqual(expected_status_code, result_status_code, message)

        expected_body = {
            "name": ["This field is required."],
            "content": ["This field is required."],
        }
        result_body = response.json()
        message = f"<{url}> corpo de resposta deve ser semelhante a {expected_body}."
        self.assertEqual(expected_body, result_body, message)

    def test_can_not_create_content_using_common_user_token(self):
        content_data = {
            "name": "Estruturas de repetição",
            "content": "...",
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.common_user_token)
        url = self.BASE_URL.format(v4())
        response = self.client.post(url, content_data, format="json")
        expected_status_code = 403
        result_status_code = response.status_code
        message = (
            f"<{url}> status code retornado está diferente de {expected_status_code}."
        )
        self.assertEqual(expected_status_code, result_status_code, message)


class TestRetrieveContentView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/courses/{}/contents/"
        cls.superuser = baker.make("accounts.Account", is_superuser=True)
        cls.common_user = baker.make("accounts.Account", is_superuser=False)

        cls.superuser_token = str(
            RefreshToken.for_user(cls.superuser).access_token,
        )
        cls.common_user_token = str(
            RefreshToken.for_user(cls.common_user).access_token,
        )

    def test_can_retrieve_content_using_superuser_token(self):
        content = baker.make("contents.Content")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.superuser_token)
        url = self.BASE_URL.format(content.course_id) + str(content.id) + "/"
        response = self.client.get(url)
        expected_status_code = 200
        result_status_code = response.status_code
        message = (
            f"<{url}> status code retornado está diferente de {expected_status_code}."
        )
        self.assertEqual(expected_status_code, result_status_code, message)

        expected_keys = {"id", "name", "content", "video_url"}
        result_body = set(response.json().keys())
        message = (
            f"<{url}> corpo de resposta deve trazer somente as chaves {expected_keys}."
        )
        self.assertEqual(expected_keys, result_body, message)

    def test_can_not_retrieve_content_using_common_user_token(self):
        content = baker.make("contents.Content")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.common_user_token)
        url = self.BASE_URL.format(content.course_id) + str(content.id) + "/"
        response = self.client.get(url)
        expected_status_code = 403
        result_status_code = response.status_code
        message = (
            f"<{url}> status code retornado está diferente de {expected_status_code}."
        )
        self.assertEqual(expected_status_code, result_status_code, message)

    def test_can_retrieve_content_using_participant_user_token(self):
        content = baker.make("contents.Content")
        content.course.students.add(self.common_user)
        current_student_token = str(
            RefreshToken.for_user(self.common_user).access_token,
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + current_student_token)
        url = self.BASE_URL.format(content.course_id) + str(content.id) + "/"
        response = self.client.get(url)
        expected_status_code = 200
        result_status_code = response.status_code
        message = (
            f"<{url}> status code retornado está diferente de {expected_status_code}."
        )
        self.assertEqual(expected_status_code, result_status_code, message)

        expected_keys = {"id", "name", "content", "video_url"}
        result_body = set(response.json().keys())
        message = (
            f"<{url}> corpo de resposta deve trazer somente as chaves {expected_keys}."
        )
        self.assertEqual(expected_keys, result_body, message)

    def test_can_not_retrieve_content_with_invalid_course_id(self):
        content = baker.make("contents.Content")
        random_course_uuid = str(v4())
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.superuser_token)
        url = self.BASE_URL.format(random_course_uuid) + str(content.id) + "/"
        response = self.client.get(url)
        expected_status_code = 404
        result_status_code = response.status_code
        message = (
            f"<{url}> status code retornado está diferente de {expected_status_code}."
        )
        self.assertEqual(expected_status_code, result_status_code, message)

        expected_body = {"detail": "course not found."}
        result_body = response.json()
        message = f"<{url}> retorno está diferente do esperado."
        self.assertEqual(expected_body, result_body, message)

    def test_can_not_retrieve_content_with_invalid_content_id(self):
        course = baker.make("courses.Course")
        random_content_uuid = str(v4())
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.superuser_token)
        url = self.BASE_URL.format(str(course.id)) + str(random_content_uuid) + "/"
        response = self.client.get(url)
        expected_status_code = 404
        result_status_code = response.status_code
        message = (
            f"<{url}> status code retornado está diferente de {expected_status_code}."
        )
        self.assertEqual(expected_status_code, result_status_code, message)

        expected_body = {"detail": "content not found."}
        result_body = response.json()
        message = f"<{url}> retorno está diferente do esperado."
        self.assertEqual(expected_body, result_body, message)


class TestUpdateContentView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/courses/{}/contents/"
        cls.superuser = baker.make("accounts.Account", is_superuser=True)
        cls.common_user = baker.make("accounts.Account", is_superuser=False)

        cls.superuser_token = str(
            RefreshToken.for_user(cls.superuser).access_token,
        )
        cls.common_user_token = str(
            RefreshToken.for_user(cls.common_user).access_token,
        )

    def test_can_update_content_using_superuser_token(self):
        content = baker.make("contents.Content")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.superuser_token)
        url = self.BASE_URL.format(content.course_id) + str(content.id) + "/"
        content_data = {"content": "Conteúdo atualizado."}
        response = self.client.patch(url, content_data, format="json")
        expected_status_code = 200
        result_status_code = response.status_code
        message = (
            f"<{url}> status code retornado está diferente de {expected_status_code}."
        )
        self.assertEqual(expected_status_code, result_status_code, message)

        expected_keys = {"id", "name", "content", "video_url"}
        result_keys = set(response.json().keys())
        message = (
            f"<{url}> corpo de resposta deve trazer somente as chaves {expected_keys}."
        )
        self.assertEqual(expected_keys, result_keys, message)

        expected_body = {
            "id": str(content.id),
            "name": content.name,
            "content": content_data["content"],
            "video_url": content.video_url,
        }
        result_body = response.json()
        message = (
            f"<{url}> corpo de resposta deve ser semelhante a este {expected_body}."
        )
        self.assertDictEqual(expected_body, result_body, message)

    def test_can_not_update_content_using_common_user_token(self):
        content = baker.make("contents.Content")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.common_user_token)
        url = self.BASE_URL.format(content.course_id) + str(content.id) + "/"
        content_data = {"content": "Conteúdo atualizado."}
        response = self.client.patch(url, content_data, format="json")
        expected_status_code = 403
        result_status_code = response.status_code
        message = (
            f"<{url}> status code retornado está diferente de {expected_status_code}."
        )
        self.assertEqual(expected_status_code, result_status_code, message)


class TestDeleteContentView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/courses/{}/contents/"
        cls.superuser = baker.make("accounts.Account", is_superuser=True)
        cls.common_user = baker.make("accounts.Account", is_superuser=False)

        cls.superuser_token = str(
            RefreshToken.for_user(cls.superuser).access_token,
        )
        cls.common_user_token = str(
            RefreshToken.for_user(cls.common_user).access_token,
        )

    def test_can_not_delete_content_using_common_user_token(self):
        content = baker.make("contents.Content")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.common_user_token)
        url = self.BASE_URL.format(content.course_id) + str(content.id) + "/"
        response = self.client.delete(url)
        expected_status_code = 403
        result_status_code = response.status_code
        message = (
            f"<{url}> status code retornado está diferente de {expected_status_code}."
        )
        self.assertEqual(expected_status_code, result_status_code, message)

        expected_count = 1
        result_count = Content.objects.all().count()
        message = (
            f"<{url}> a deleção usando token de estudante não está sendo bloqueada."
        )
        self.assertEqual(expected_count, result_count, message)

    def test_can_delete_content_using_superuser_token(self):
        content = baker.make("contents.Content")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.superuser_token)
        url = self.BASE_URL.format(content.course_id) + str(content.id) + "/"
        response = self.client.delete(url)
        expected_status_code = 204
        result_status_code = response.status_code
        message = (
            f"<{url}> status code retornado está diferente de {expected_status_code}."
        )
        self.assertEqual(expected_status_code, result_status_code, message)

        expected_count = 0
        result_count = Content.objects.all().count()
        message = f"<{url}> a deleção usando token de administrador/instrutor não está apagando do banco de dados."
        self.assertEqual(expected_count, result_count, message)
