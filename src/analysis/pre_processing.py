from src.function.iterator import *
from src.function.file_operations import *
import os
import shutil


def generate_topic_iterator():
    result = {}
    topic_type = os.listdir('../../data/source/题目分析')
    topic_type.remove('.DS_Store')
    for type in topic_type:
        result[type] = {}
        topics = os.listdir('../../data/source/题目分析/' + type)
        if '.DS_Store' in topics:
            topics.remove('.DS_Store')
        for topic in topics:
            users = os.listdir('../../data/source/题目分析/' + type + '/' + topic)
            if not users:
                os.rmdir('../../data/source/题目分析/' + type + '/' + topic)
            else:
                result[type][topic] = users
    generate_json('../../data/analysis/topic_iterator.json', result)


def generate_user_iterator():
    result = {}
    users = os.listdir('../../data/source/用户分析')
    if '.DS_Store' in users:
        users.remove('.DS_Store')
    for user in users:
        result[user] = {}
        types = os.listdir('../../data/source/用户分析/' + user)
        if '.DS_Store' in types:
            types.remove('.DS_Store')
        for type in types:
            topics = os.listdir('../../data/source/用户分析/' + user + '/' + type)
            if not topics:
                os.rmdir('../../data/source/用户分析/' + user + '/' + type)
            else:
                result[user][type] = topics
    generate_json('../../data/analysis/user_iterator.json', result)


def check_topics():
    # 遍历检查下载内容是否被正确处理
    it = getTIterator()
    while it.next():
        try:
            if it.get_type() != '.DS_Store' and it.get_user() != '.DS_Store' and it.get_topic() != '.DS_Store':
                docs = os.listdir('../../data/source/题目分析/' + it.get_type() + '/' + it.get_topic() + '/' + it.get_user())
                # 检查目录内容是否为解压内容
                assert docs.count('.mooctest') != -1
                assert docs.count('.blocky.xml') != -1
                assert docs.count('main.py') != -1
                assert docs.count('properties') != -1
                assert docs.count('readme.md') != -1
        except AssertionError:
            print(it.get_type() + '/' + it.get_topic() + '/' + it.get_user())
            shutil.rmtree('../../data/source/题目分析/' + it.get_type() + '/' + it.get_topic() + '/' + it.get_user())


def check_users():
    # 遍历检查下载内容是否被正确处理
    it = getUIterator()
    while it.next():
        try:
            if it.get_type() != '.DS_Store' and it.get_user() != '.DS_Store' and it.get_topic() != '.DS_Store':
                docs = os.listdir('../../data/source/用户分析/' + it.get_user() + '/' + it.get_type() + '/' + it.get_topic())
                # 检查目录内容是否为解压内容
                assert docs.count('.mooctest') != -1
                assert docs.count('.blocky.xml') != -1
                assert docs.count('main.py') != -1
                assert docs.count('properties') != -1
                assert docs.count('readme.md') != -1
        except AssertionError:
            print(it.get_user() + '/' + it.get_type() + '/' + it.get_topic())
            shutil.rmtree('../../data/source/用户分析/' + it.get_user() + '/' + it.get_type() + '/' + it.get_topic())


def check_effective_answer():
    count = 0
    not_python = {}
    test_oriented = {}
    it = getUIterator()
    while it.next():
        if check_cpp(it):
            add_Uindex(not_python, it)
        elif check_test_cases(it):
            add_Uindex(test_oriented, it)
        print(count)
        count += 1
    generate_json('../../data/analysis/cpp_code.json', not_python)
    generate_json('../../data/analysis/test_oriented.json', test_oriented)


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
    while '' in sentences:
        sentences.remove('')
    for i in range(0, len(sentences)):
        words = sentences[i].split()
        sentence = ''.join(words)
        if sentence.startswith('#'):
            continue
        # 检查代码有无复杂逻辑，因为面向用例基本就是没脑子的if-else
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
    if num_of_if > 0 and (num_of_cases - 2 <= num_of_if <= num_of_cases + 2):  # 误差范围为1且if-else的数量不能为0
        return True
    return False


def remove_invalid(it):
    count = 0
    while it.next():
        src_1 = '../../data/source/用户分析/' + it.get_user() + '/' + it.get_type() + '/' + it.get_topic()
        dst_1 = '../../data/source/无效代码/用户分析/' + it.get_user() + '/' + it.get_type() + '/' + it.get_topic()
        src_2 = '../../data/source/题目分析/' + it.get_type() + '/' + it.get_topic() + '/' + it.get_user()
        dst_2 = '../../data/source/无效代码/题目分析/' + it.get_type() + '/' + it.get_topic() + '/' + it.get_user()
        try:
            shutil.move(src_1, dst_1)
            shutil.move(src_2, dst_2)
            print(count)
            count += 1
        except FileNotFoundError:
            continue
