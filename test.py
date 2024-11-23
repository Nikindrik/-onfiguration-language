import unittest
from unittest.mock import patch, mock_open
import sys
from main import *


class TestConfigurationParser(unittest.TestCase):
    @patch('sys.argv', ['main.py', 'test_config.txt'])
    def test_parse_args(self):
        args = parse_args()
        self.assertEqual(args.input_file_path, 'test_config.txt')

    @patch("builtins.open", new_callable=mock_open, read_data="input data")
    def test_read_input_file(self, mock_file):
        input_data = read_input_file("test_config.txt")
        self.assertEqual(input_data, "input data")
        mock_file.assert_called_with("test_config.txt", "r", encoding="utf-8")

    def test_remove_comments(self):
        input_data = """\ Это комментарий
                        <!-- это многострочный
                        комментарий -->
                        значение 1 { 1 . 2 . 3 }"""
        cleaned_data = remove_comments(input_data)
        expected_output = "                        значение 1 { 1 . 2 . 3 }"
        self.assertEqual(cleaned_data.strip(), expected_output.strip())

    def test_parse_dict(self):
        input_data = "([name: value, age: 30])"
        constants_dict = {}
        result = parse_dict(input_data, constants_dict)
        expected_result = {'name': 'value', 'age': 30}
        self.assertEqual(result, expected_result)

    def test_parse_constants(self):
        input_data = """name := value
                        age := 30"""
        constants_dict = parse_constants(input_data)
        expected_constants = {'name': 'value', 'age': '30'}
        self.assertEqual(constants_dict, expected_constants)

    def test_convert_to_yaml(self):
        input_data = "([name: value, age: 30])"
        constants_dict = {}
        yaml_data = convert_to_yaml(input_data, constants_dict)
        expected_yaml = "age: 30\nname: value\n"
        self.assertEqual(yaml_data, expected_yaml)


if __name__ == '__main__':
    unittest.main()