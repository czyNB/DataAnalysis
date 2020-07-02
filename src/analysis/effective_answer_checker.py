from src.function.iterator import TIterator, UIterator
import json


def check_effective_answer():
    count = 0
    not_python = []
    test_oriented = []
    it = UIterator('../../data/analysis/user_iterator.json')
    while it.next():
        if check_cpp(it):
            not_python.append([it.get_user(), it.get_type(), it.get_topic()])
        elif check_test_cases(it):
            test_oriented.append([it.get_user(), it.get_type(), it.get_topic()])
    json_data1 = json.dumps(not_python, indent=4, separators=(',', ': '), ensure_ascii=False)
    f1 = open('../../data/analysis/invalid/cpp_code.json', 'w', encoding='utf-8')
    f1.write(json_data1)
    f1.close()
    json_data2 = json.dumps(test_oriented, indent=4, separators=(',', ': '), ensure_ascii=False)
    f2 = open('../../data/analysis/invalid/test_oriented.json', 'w', encoding='utf-8')
    f2.write(json_data2)
    f2.close()


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
    user = it.get_user()
    type = it.get_type()
    topic = it.get_topic()
    root = user + '/' + type + '/' + topic + '/.mooctest/testCases.json'
    f = open('../../data/source/用户分析/' + root, 'r', encoding='utf-8')
    test_cases = json.loads(f.read())
    num_of_cases = len(test_cases)  # 获取用例的数量
    num_of_if = 0  # 获取if+print组合的数量
    code = it.current()
    sentences = (''.join(code.split(' '))).split('\n')
    for i in range(0, len(sentences)):
        try:
            if sentences[i].startswith('if'):
                if sentences[i + 1].startswith('print'):
                    num_of_if += 1
            elif sentences[i].startswith('elif'):
                if sentences[i + 1].startswith('print'):
                    num_of_if += 1
        except IndexError:
            if sentences[i].find('print') != -1:
                num_of_if += 1
            else:
                return True
    if num_of_cases == num_of_if:
        return True
    return False


if __name__ == '__main__':
    check_effective_answer()
