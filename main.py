import argparse
import re
import sys
import yaml


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path", type=str, help="Путь к файлу с конфигурацией")
    return parser.parse_args()

def read_input_file(input_file_path):
    with open(input_file_path, "r", encoding="utf-8") as file:
        return file.read()

def remove_comments(input_data):
    input_data = re.sub(r'\\.*', '', input_data)
    input_data = re.sub(r'<!--.*?-->', '', input_data, flags=re.DOTALL)
    return input_data

def parse_value(value, constants_dict):
    if value.isdigit():
        return int(value)
    elif value == "true":
        return True
    elif value == "false":
        return False
    elif value.startswith('@"') and value.endswith('"'):
        return value[2:-1]
    elif value.startswith('!(') and value.endswith(')'):
        const_name = value[2:-1]
        return constants_dict.get(const_name, None)
    elif value.startswith('{') and value.endswith('}'):
        return [parse_value(v.strip(), constants_dict) for v in value[1:-1].split('.')]
    elif value.startswith('([') and value.endswith('])'):
        dict_content = value[2:-2]
        return parse_dict(dict_content, constants_dict)
    return value

def parse_dict(input_data, constants_dict):
    output = {}
    items = re.findall(r'([a-zA-Z][_a-zA-Z0-9]*)\s*:\s*(.*?)\s*(?=,|\])', input_data)
    for key, value in items:
        output[key] = parse_value(value, constants_dict)
    return output

def parse_constants(input_data):
    constants_dict = {}
    matches = re.findall(r'([a-zA-Z][_a-zA-Z0-9]*)\s*:=\s*(.*?)\s*(?=\n|$)', input_data)
    for name, value in matches:
        constants_dict[name] = value.strip()
    return constants_dict

def convert_to_yaml(input_data, constants_dict):
    config = parse_dict(input_data, constants_dict)
    return yaml.dump(config, default_flow_style=False, allow_unicode=True)

def main():
    args = parse_args()
    try:
        input_data = read_input_file(args.input_file_path)
        input_data = remove_comments(input_data)
        constants_dict = parse_constants(input_data)
        yaml_data = convert_to_yaml(input_data, constants_dict)
        print(yaml_data)
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)

if __name__ == '__main__':
    main()