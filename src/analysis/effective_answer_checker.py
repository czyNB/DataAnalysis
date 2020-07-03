from src.function.iterator import *
from src.function.file_operations import *


def check_effective_answer():
    count = 0
    not_python = {}
    test_oriented = {}
    it = getUIterator()
    while it.next():
        if check_cpp(it):
            add_Uindex(not_python,it)
        elif check_test_cases(it):
            add_Uindex(test_oriented,it)
        print(count)
        count += 1
    generate_json('../../data/analysis/cpp_code.json',not_python)
    generate_json('../../data/analysis/test_oriented.json',test_oriented)


def check_cpp(it):
    user = it.get_user()
    type = it.get_type()
    topic = it.get_topic()
    # c++及其他不是Python语言 检查
    root = user + '/' + type + '/' + topic + '/properties'
    properties = read_json('../../data/source/用户分析/' + root)
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
    test_cases = read_json('../../data/source/用户分析/' + root)
    num_of_cases = len(test_cases)  # 获取用例的数量
    num_of_if = 0  # 获取if+print或elif+print组合的数量
    sentences = it.current()
    for i in range(0, len(sentences)):
        words = sentences[i].split()
        sentence = ''.join(words)
        if sentence.startswith('#'):
            continue
        # 检查代码有无复杂逻辑，因为面向用例基本就是没脑子的if-else
        elif 'while' in words or 'for' in words:  # 有无循环
            return False
        elif 'break' in words or 'continue' in words:  # 有无循环中断或循环继续
            return False
        elif 'def' in words or 'class' in words:  # 有无方法定义或类定义
            return False
        elif 'sorted(' in words or 'reversed(' in words:  # 有无使用排序或反转方法
            return False
        elif '*' in words or '/' in words:  # 有无计算（+、-保守考虑不算在范围内）
            return False
        # 检查代码里的if-else和print的数量是否和测试用例相似
        try:
            if sentence.startswith('if'):
                if ''.join(sentences[i + 1].split()).startswith('print'):
                    num_of_if += 1
            elif sentence.startswith('elif'):
                if ''.join(sentences[i + 1].split()).startswith('print'):
                    num_of_if += 1
        except IndexError:
            if sentence.find('print') != -1:
                num_of_if += 1
            else:
                return True
    if num_of_if > 0 and (num_of_cases - 1 <= num_of_if <= num_of_cases + 1):  # 误差范围为1且if-else的数量不能为0
        return True
    return False


if __name__ == '__main__':
    check_effective_answer()
