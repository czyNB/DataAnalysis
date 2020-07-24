from src.function.iterator import *
from src.function.file_operations import *
import os
import shutil

# 全局数据
test_data = read_json('../../data/origin/test_data.json')
test_cases = read_json('../../data/import/test_cases.json')


def generate_topic_iterator():
    result = {}
    topic_type = os.listdir('../../data/source/题目分析')
    if '.DS_Store' in topic_type:
        topic_type.remove('.DS_Store')
    for type in topic_type:
        result[type] = {}
        topics = os.listdir('../../data/source/题目分析/' + type)
        if '.DS_Store' in topics:
            topics.remove('.DS_Store')
        for topic in topics:
            users = os.listdir('../../data/source/题目分析/' + type + '/' + topic)
            if '.DS_Store' in users:
                users.remove('.DS_Store')
            if not users:
                os.rmdir('../../data/source/题目分析/' + type + '/' + topic)
            else:
                result[type][topic] = users
    generate_json('../../data/analysis/iterator_topic.json', result)
    print('    Iterator Topic Done!')


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
            if '.DS_Store' in topics:
                topics.remove('.DS_Store')
            if not topics:
                os.rmdir('../../data/source/用户分析/' + user + '/' + type)
            else:
                result[user][type] = topics
    generate_json('../../data/analysis/iterator_user.json', result)
    print('    Iterator User Done!')


def check_topics():
    # 遍历检查下载内容是否被正确处理
    it = getTIterator()
    while it.next():
        try:
            if it.get_type() != '.DS_Store' and it.get_user() != '.DS_Store' and it.get_topic() != '.DS_Store':
                docs = os.listdir(
                    '../../data/source/题目分析/' + it.get_type() + '/' + it.get_topic() + '/' + it.get_user())
                # 检查目录内容是否为解压内容
                assert docs.index('.mooctest') != -1
                assert docs.index('blockly.xml') != -1
                assert docs.index('main.py') != -1
                assert docs.index('properties') != -1
                assert docs.index('readme.md') != -1
        except ValueError:
            print(it.get_type() + '/' + it.get_topic() + '/' + it.get_user())
            shutil.rmtree('../../data/source/题目分析/' + it.get_type() + '/' + it.get_topic() + '/' + it.get_user())
    print('    Check Topics Done!')


def check_users():
    # 遍历检查下载内容是否被正确处理
    it = getUIterator()
    while it.next():
        try:
            if it.get_type() != '.DS_Store' and it.get_user() != '.DS_Store' and it.get_topic() != '.DS_Store':
                docs = os.listdir(
                    '../../data/source/用户分析/' + it.get_user() + '/' + it.get_type() + '/' + it.get_topic())
                # 检查目录内容是否为解压内容
                assert docs.index('.mooctest') != -1
                assert docs.index('blockly.xml') != -1
                assert docs.index('main.py') != -1
                assert docs.index('properties') != -1
                assert docs.index('readme.md') != -1
        except ValueError:
            print(it.get_user() + '/' + it.get_type() + '/' + it.get_topic())
            shutil.rmtree('../../data/source/用户分析/' + it.get_user() + '/' + it.get_type() + '/' + it.get_topic())
    print('    Check Users Done!')


def check_effective_answer():
    not_python = {}
    test_oriented = {}
    it = getUIterator()
    while it.next():
        if check_cpp(it):
            add_Uindex(not_python, it)
    test_oriented = check_test_cases(getUIterator())
    generate_json('../../data/analysis/pre_cpp.json', not_python)
    generate_json('../../data/analysis/pre_test.json', test_oriented)
    print('    Check Answer Done!')


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


def check_test_cases(it: UIterator) -> dict:
    result = {}
    while it.next():
        user = it.get_user().split('_')[2]
        cases = test_data[user]['cases']
        for case in cases:
            case_id = case['case_id']
            if case_id in list(test_cases):
                for user_id in test_cases[case_id]:
                    if 'user_id_' + str(user_id) in list(result):
                        pass
                    else:
                        result[user_id] = {}
                    if it.get_type() in list(result[user_id]):
                        result[user_id][it.get_type()].append(it.get_topic())
                    else:
                        result[user_id][it.get_type()] = [it.get_topic()]
                test_cases.pop(case_id)
    return result


def remove_invalid(it):
    while it.next():
        src_1 = '../../data/source/用户分析/' + it.get_user() + '/' + it.get_type() + '/' + it.get_topic()
        dst_1 = '../../data/source/无效代码/用户分析/' + it.get_user() + '/' + it.get_type() + '/' + it.get_topic()
        src_2 = '../../data/source/题目分析/' + it.get_type() + '/' + it.get_topic() + '/' + it.get_user()
        dst_2 = '../../data/source/无效代码/题目分析/' + it.get_type() + '/' + it.get_topic() + '/' + it.get_user()
        try:
            shutil.move(src_1, dst_1)
            shutil.move(src_2, dst_2)
        except FileNotFoundError:
            continue
        print('    Remove Invalid Done!')
