from rest_framework.test import APITestCase
from accounts.models import Account
from model_bakery import baker
from django.contrib.auth.hashers import (
    make_password,
)


class TestCreateAccountView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/accounts/"

    def test_can_create_superuser_with_success(self):
        expected = 201
        url = self.BASE_URL
        user_data = {
            "username": "bob",
            "password": "1234",
            "email": "bob@kenzie.com.br",
            "is_superuser": True,
        }
        response = self.client.post(url, user_data, format="json")
        message = f"\n<{url}> status code da rota {url} está diferente de {expected}."
        self.assertEqual(expected, response.status_code, message)

        expected_keys = {
            "id",
            "username",
            "email",
            "is_superuser",
        }
        result = set(response.json().keys())
        message = (
            f"\n<{url}> retorno diferente do esperado."
            f"\nA resposta deve ter somente estas chaves: {expected_keys}."
        )
        self.assertSetEqual(expected_keys, result, message)

        result = response.json()["is_superuser"]
        message = (
            f"<{url}> o valor retornado da chave 'is_superuser' deve ser verdadeiro."
        )
        self.assertTrue(result, message)

        expected = 1
        result = Account.objects.all().count()
        message = f"\n<{url}> não foi feito o salvamento correto do usuário no banco de dados."
        self.assertEqual(
            expected,
            result,
        )

    def test_can_create_common_user_with_success(self):
        expected = 201
        url = self.BASE_URL
        user_data = {
            "username": "bob",
            "password": "1234",
            "email": "bob@kenzie.com.br",
            "is_superuser": False,
        }
        response = self.client.post(url, user_data, format="json")
        message = f"\n<{url}> status code da rota {url} está diferente de {expected}."
        self.assertEqual(expected, response.status_code, message)

        expected_keys = {
            "id",
            "username",
            "email",
            "is_superuser",
        }
        result = set(response.json().keys())
        message = (
            f"\n<{url}> retorno diferente do esperado."
            f"\nA resposta deve ter somente estas chaves: {expected_keys}."
        )
        self.assertSetEqual(expected_keys, result, message)

        result = response.json()["is_superuser"]
        message = (
            f"<{url}> o valor retornado da chave 'is_superuser' deve ser verdadeiro."
        )
        self.assertFalse(result, message)

        expected = 1
        result = Account.objects.all().count()
        message = f"\n<{url}> não foi feito o salvamento correto do usuário no banco de dados."
        self.assertEqual(
            expected,
            result,
        )

    def test_can_not_create_account_missing_body(self):
        expected = 400
        url = self.BASE_URL
        user_data = {}
        response = self.client.post(url, user_data, format="json")
        message = f"\n<{url}> status code da rota {url} está diferente de {expected}."
        self.assertEqual(expected, response.status_code, message)

        expected_keys = {"email", "username", "password"}
        result = set(response.json().keys())
        message = (
            f"\n<{url}> retorno diferente do esperado."
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
            f"\n<{url}> retorno diferente do esperado."
            f"\nO valor de cada chave obrigatória deve ser: {expected_values}"
        )
        self.assertListEqual(expected_values, result, message)

    def test_can_not_create_a_duplicate_username_and_email(self):
        expected = 400
        url = self.BASE_URL
        user_data = {
            "username": "bob",
            "password": "1234",
            "email": "bob@kenzie.com.br",
            "is_superuser": True,
        }
        self.client.post(url, user_data, format="json")
        response = self.client.post(url, user_data, format="json")
        message = f"\n<{url}> status code da rota {url} está diferente de {expected}."
        self.assertEqual(expected, response.status_code, message)

        expected_keys = {"email", "username"}
        result = set(response.json().keys())
        message = (
            f"\n<{url}> retorno diferente do esperado."
            f"\nA resposta deve ter somente estas chaves: {expected_keys}."
        )
        self.assertSetEqual(expected_keys, result, message)

        result = response.json()

        expected_response_email = ["user with this email already exists."]
        message = (
            f"\n<{url}> retorno diferente do esperado."
            f"\nA resposta de unicidade referente ao email deve ser {expected_response_email}."
        )
        self.assertEqual(result["email"], expected_response_email, message)

        expected_response_username = ["A user with that username already exists."]
        message = (
            f"\n<{url}> retorno diferente do esperado."
            f"\nA resposta de unicidade referente ao email deve ser {expected_response_username}."
        )
        self.assertEqual(result["username"], expected_response_username, message)


class TestLoginAccountView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/login/"

    def test_login_with_incorrect_credentials(self):
        URL = self.BASE_URL
        account_data = {
            "username": "account_1111",
            "password": "1111",
        }
        response = self.client.post(URL, account_data, format="json")
        expected_status_code = 401
        result_status_code = response.status_code
        message = (
            f"<{URL}>: Status code retornado está diferente de {expected_status_code}."
        )
        self.assertEqual(expected_status_code, result_status_code, message)

        expected_body = {"detail": "No active account found with the given credentials"}
        result_body = response.json()
        message = f"<{URL}>: corpo de retorno está diferente de {expected_body}."
        self.assertEqual(expected_body, result_body, message)

    def test_login_without_required_fields(self):
        URL = self.BASE_URL
        account_data = {}
        response = self.client.post(URL, account_data, format="json")
        expected_status_code = 400
        result_status_code = response.status_code
        message = (
            f"<{URL}>: Status code retornado está diferente de {expected_status_code}."
        )
        self.assertEqual(expected_status_code, result_status_code, message)

    def test_login_with_correct_credentials(self):
        baker.make(
            "accounts.Account",
            username="account_1111",
            password=make_password("1234"),
        )
        URL = self.BASE_URL
        account_data = {
            "username": "account_1111",
            "password": "1234",
        }
        response = self.client.post(URL, account_data, format="json")
        expected_status_code = 200
        result_status_code = response.status_code
        message = (
            f"<{URL}>: Status code retornado está diferente de {expected_status_code}."
        )
        self.assertEqual(expected_status_code, result_status_code, message)

        expected_keys = {"access", "refresh"}
        result_keys = set(response.json().keys())
        message = (
            f"<{URL}>: corpo de retorno deve conter somente as chaves: {expected_keys}."
        )
        self.assertSetEqual(expected_keys, result_keys, message)
