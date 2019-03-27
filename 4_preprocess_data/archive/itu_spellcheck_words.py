"""
Send list of verbs to ITU for spellchecking and correction
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import pipeline_caller


def main():
    caller = pipeline_caller.PipelineCaller()
    tool_name = "spellcheck"
    api_token = "sQj6zxcVt7JzWXHNTdRu3QRzc6i8KZz7"
    result = ''

    text = open('../1_data/all_verbs.txt', 'r').read()
    result += caller.call(tool_name, text, api_token)

    with open('../1_data/all_verbs_spellchecked.txt', 'w') as f:
        f.write(result)


if __name__ == '__main__':
    main()
    exit(0)