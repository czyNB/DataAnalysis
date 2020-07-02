from src.function.iterator import TIterator, UIterator
import json


def check_effective_answer():
    result = []
    it = UIterator('../../data/analysis/user_iterator.json')
    while it.next():
        if check_cpp(it):
            result.append([it.get_user(),it.get_type(),it.get_topic()])
    json_data = json.dumps(result, indent=4, separators=(',', ': '), ensure_ascii=False)
    f = open('../../data/analysis/invalid_code.json', 'w', encoding='utf-8')
    f.write(json_data)
    f.close()


def check_cpp(it):
    user = it.get_user()
    type = it.get_type()
    topic = it.get_topic()
    # c++及其他不是Python语言 检查
    root = user + '/' + type + '/' + topic + '/properties'
    f = open('../../data/source/用户分析/' + root, 'r', encoding='utf-8')
    properties = json.loads(f.read())
    if properties['lang'] == 'Python':
        return False
    elif properties['lang'] == 'Python3':
        return False
    else:
        return True


def check_test_cases(it):
    return False


if __name__ == '__main__':
    check_effective_answer()
