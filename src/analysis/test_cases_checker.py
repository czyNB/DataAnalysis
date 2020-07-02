from src.function.iterator import TIterator, UIterator
import json


def check_effective_answer():
    result = []
    it = UIterator('../../data/analysis/user_iterator.json')
    while it.next():
        code = it.current()
        sentences = code.split('\n')
        words = code.split()

        if '#include' in words:  # c++检查
            result.append([it.get_user(), it.get_type(), it.get_topic()])

    json_data = json.dumps(result, indent=4, separators=(',', ': '), ensure_ascii=False)
    f = open('../../data/analysis/cppCode.json', 'w', encoding='utf-8')
    f.write(json_data)
    f.close()


if __name__ == '__main__':
    check_effective_answer()
