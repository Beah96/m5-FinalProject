from unittest import TestCase
from courses.models import Course
from courses.models import Course
from django.db.models import ForeignKey, ManyToManyField
from django.db.models.fields.reverse_related import ManyToManyRel


class TestCourseModel(TestCase):
    def test_name_field(self):
        expected = 100
        result = Course._meta.get_field("name").max_length
        message = "Atributo 'name' possui 'max_length' diferente do esperado."
        self.assertEqual(expected, result, message)

        result = Course._meta.get_field("name").unique
        message = "Atributo 'name' não foi configurado como único."
        self.assertTrue(result, message)

        result = Course._meta.get_field("name").null
        message = "Atributo 'name' deve ser obrigatório."
        self.assertFalse(result, message)

    def test_status_field(self):
        expected = 11
        result = Course._meta.get_field("status").max_length
        message = "Atributo 'status' possui 'max_length' diferente do esperado."
        self.assertEqual(expected, result, message)

        result = Course._meta.get_field("status").choices
        message = "Atributo 'status' não foi configurado como fieldchoice."
        self.assertTrue(result, message)

        expected = 3
        result = Course._meta.get_field("status").choices
        message = "Atributo 'status' está com um número menor que o esperado de choices/escolhas."
        self.assertEqual(expected, len(result), message)

        expected = ["not started", "in progress", "finished"]
        result = [choice[0] for choice in Course._meta.get_field("status").choices]
        message = (
            "Atributo 'status' está com choices/escolhas diferentes do que o esperado."
        )
        for expected_choice in expected:
            self.assertIn(expected_choice, result, message)

        expected = "not started"
        result = Course._meta.get_field("status").default
        message = "Atributo 'status' está com valor padrão diferente do esperado."
        self.assertEqual(expected, result.value, message)

    def test_start_date(self):
        result = Course._meta.get_field("start_date").null
        message = "Atributo 'start_date' deve ser obrigatório."
        self.assertFalse(result, message)

    def test_start_date(self):
        result = Course._meta.get_field("end_date").null
        message = "Atributo 'start_date' deve ser obrigatório."
        self.assertFalse(result, message)


class TestRelationshipTest(TestCase):
    def test_one_to_many_between_account_course(self):
        result = Course._meta.get_field("instructor")
        message = "Atributo 'instructor' do relacionamento 1:N não foi declarado corretamente."
        self.assertIsInstance(result, ForeignKey, message)

    def test_many_to_many_between_account_course(self):
        result = Course._meta.get_field("students")

        message = (
            "Relacionamento N:N não foi declarado corretamente."
            "O comportamento esperado é: os cursos terão a chave 'students' "
            "e os usuários terão uma chave 'my_courses'."
        )
        self.assertIsInstance(result, ManyToManyField | ManyToManyRel, message)
