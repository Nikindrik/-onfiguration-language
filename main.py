import argparse
import yaml
import re


def remove_comments(input_text):
    input_text = re.sub(r'\\.*$', '', input_text, flags=re.MULTILINE)  # Однострочные комментарии
    input_text = re.sub(r'<!--.*?-->', '', input_text, flags=re.DOTALL)  # Многострочные комментарии
    return input_text


def tokenize(input_text):
    token_patterns = [
        (r'(\()|\)', 'PARENTHESIS'),  # Скобки
        (r'(\[\])|(\[)', 'BRACKETS'),  # Словари
        (r'\{|\}', 'BRACES'),  # Массивы
        (r'\:=', 'ASSIGN_OPERATOR'),  # :=
        (r'!(\()', 'EXCLAMATION'),  # Вычисление констант....
        (r'\"[^\"]*\"', 'STRING'),  # @"строка"
        (r'[\d]+', 'NUMBER'),  # Числа
        (r'[_a-zA-Z][_a-zA-Z0-9]*', 'IDENTIFIER'),  # Имена переменных
        (r'\s+', 'WHITESPACE')  # Пробелы
    ]
    token_regex = '|'.join([f'(?P<{name}>{pattern})' for pattern, name in token_patterns])  # Составляем один общий шаблон для поиска всех токенов
    tokens = []
    for match in re.finditer(token_regex, input_text):
        for name, group in match.groupdict().items():
            if group and name != 'WHITESPACE':
                tokens.append(group)
    return tokens


def parse_config(input_text):
    input_text = remove_comments(input_text)
    tokens = tokenize((input_text))
    print(tokens)

    arrays = [
        {"name": [1, 2, 3]}
    ]
    consts = []
    dicts = []

    # TODO: Для список и словарей, обрабатывать их внутри и считать смещения, а потом прибовлять к i
    for i in len(tokens):
        if re.match(r'[_a-zA-Z][_a-zA-Z0-9]*', tokens[i]) and tokens[i + 1] == ':=' and tokens[i + 2] != '{' \
                and tokens[i + 2] != '([':
            consts.append({tokens[i] : tokens[i + 2]})  # Добовляю константы
            i += 3
        elif re.match(r'[_a-zA-Z][_a-zA-Z0-9]*', tokens[i]) and tokens[i + 1] == ':=' and tokens[i + 2] == '{':
            pass
        elif re.match(r'[_a-zA-Z][_a-zA-Z0-9]*', tokens[i]) and tokens[i + 1] == ':=' and tokens[i + 2] == '([':
            pass
        elif re.match(r'[_a-zA-Z][_a-zA-Z0-9]*', tokens[i]) and tokens[i + 1] == ':=' and tokens[i + 2] != '{':
            pass
        # TODO: Понять Вычисление константы на этапе трансляции !(имя)


    # return yaml.safe_load(input_text)


def main():
    parser = argparse.ArgumentParser(description="Parser for a custom configuration language to YAML")
    parser.add_argument("input_file", help="Path to the input .txt configuration file")
    parser.add_argument("output_file", help="Path to the output YAML file")
    args = parser.parse_args()

    if not args.input_file.endswith(".txt"):
        print("Error: Input file must have a .txt extension")
        exit(1)
    try:
        with open(args.input_file, "r") as infile:
            input_text = infile.read()
        parsed_data = parse_config(input_text)

        with open(args.output_file, "w") as outfile:
            yaml.dump(parsed_data, outfile, allow_unicode=True, default_flow_style=False)
        print(f"Conversion completed. Output saved to {args.output_file}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()