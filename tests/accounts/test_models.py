from unittest import TestCase
from accounts.models import Account


class TestAccountModel(TestCase):
    def test_username_field(self):
        expected = 150
        result = Account._meta.get_field("username").max_length
        message = "Atributo 'username' possui 'max_length' diferente do esperado."
        self.assertEqual(expected, result, message)

        result = Account._meta.get_field("username").unique
        message = "Atributo 'username' não foi configurado como único."
        self.assertTrue(result, message)

        result = Account._meta.get_field("username").null
        message = "Atributo 'username' deve ser obrigatório."
        self.assertFalse(result, message)

    def test_password_field(self):
        expected = 128
        result = Account._meta.get_field("password").max_length
        message = "Atributo 'password' possui 'max_length' diferente do esperado."
        self.assertEqual(expected, result, message)

        result = Account._meta.get_field("password").null
        message = "Atributo 'password' deve ser obrigatório."
        self.assertFalse(result, message)

    def test_email_field(self):
        expected = 100
        result = Account._meta.get_field("email").max_length
        message = "Atributo 'email' possui 'max_length' diferente do esperado."
        self.assertEqual(expected, result, message)

        result = Account._meta.get_field("email").unique
        message = "Atributo 'email' não foi configurado como único."
        self.assertTrue(result, message)

        result = Account._meta.get_field("email").null
        message = "Atributo 'email' deve ser obrigatório."
        self.assertFalse(result, message)

    def test_is_superuser_field(self):
        result = Account._meta.get_field("is_superuser").default
        message = "Atributo 'is_superuser' está com valor padrão diferente do esperado."
        self.assertFalse(result, message)
