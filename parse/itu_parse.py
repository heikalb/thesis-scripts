"""
Send context sentences containing verbs to ITU to get morphological parses
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import pipeline_caller


def main():
    results = []
    sents = open('../data/all_sents_spellchecked.txt', 'r').read().split('\n')

    caller = pipeline_caller.PipelineCaller()
    tool_name = "morphanalyzer"
    api_token = "sQj6zxcVt7JzWXHNTdRu3QRzc6i8KZz7"

    start_i = 346
    i = 0
    for s in sents[start_i:]:
        try:
            print(s)
            curr_result = []

            for w in s.split():
                r = caller.call(tool_name, w, api_token)
                r = ' '.join(r.split('\n'))
                curr_result.append(r)

            curr_result = '\n'.join(curr_result)
            results.append('<S> <S>+BSTag\n{0}\n</S> </S>+ESTag'.format(curr_result))
            i += 1
            print(curr_result)
        except ConnectionResetError:
            True

        if i % 1000 == 0 or i == len(sents[start_i:]):
            with open('parsed_sents_{0}.txt'.format(i), 'w') as f:
                f.write('\n'.join(results))

if __name__ == '__main__':
    main()
    exit(0)