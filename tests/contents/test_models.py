from unittest import TestCase
from contents.models import Content


class TestContentModel(TestCase):
    def test_name_field(self):
        expected = 150
        result = Content._meta.get_field("name").max_length
        message = "Atributo 'name' possui 'max_length' diferente do esperado."
        self.assertEqual(expected, result, message)

        result = Content._meta.get_field("name").null
        message = "Atributo 'name' deve ser obrigatório."
        self.assertFalse(result, message)

    def test_content_field(self):
        result = Content._meta.get_field("content").null
        message = "Atributo 'content' deve ser obrigatório."
        self.assertFalse(result, message)

    def test_video_url_field(self):
        expected = 200
        result = Content._meta.get_field("video_url").max_length
        message = "Atributo 'video_url' possui 'max_length' diferente do esperado."
        self.assertEqual(expected, result, message)
