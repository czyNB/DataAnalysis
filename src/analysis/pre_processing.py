from src.function.iterator import *
from src.function.file_operations import *
from src.download.download import *
import os
import shutil
import zipfile


def generate_dir():
    try:
        os.mkdir('../../data')
    except FileExistsError:
        pass
    try:
        os.mkdir('../../data/analysis')
    except FileExistsError:
        pass
    try:
        os.mkdir('../../data/analysis')
    except FileExistsError:
        pass
    try:
        os.mkdir('../../data/origin')
    except FileExistsError:
        pass
    try:
        os.mkdir('../../data/source')
    except FileExistsError:
        pass
    try:
        os.mkdir('../../data/image')
    except FileExistsError:
        pass
    try:
        os.mkdir('../../data/source/题目分析')
    except FileExistsError:
        pass
    try:
        os.mkdir('../../data/source/用户分析')
    except FileExistsError:
        pass
    try:
        os.mkdir('../../data/source/无效代码')
    except FileExistsError:
        pass
    try:
        os.mkdir('../../data/import')
    except FileExistsError:
        pass
    shutil.copy('../../doc/origin/test_data.json', '../../data/origin/test_data.json')
    shutil.copy('../../doc/origin/sample.json', '../../data/origin/sample.json')
    shutil.copy('../../doc/origin/test_cases.json', '../../data/import/test_cases.json')  # 感谢王崇羽小组的大力支持
    shutil.copy('../../doc/origin/code_chaos.json', '../../data/analysis/code_chaos.json')
    shutil.copy('../../doc/origin/code_reuse.json', '../../data/analysis/code_reuse.json')
    shutil.copy('../../doc/origin/code_variable.json', '../../data/analysis/code_variable.json')
    shutil.copy('../../doc/origin/graph_difficulty.png', '../../data/analysis/graph_difficulty.png')
    shutil.copy('../../doc/origin/iterator_topic.json', '../../data/analysis/iterator_topic.json')
    shutil.copy('../../doc/origin/iterator_user.json.json', '../../data/analysis/iterator_user.json')
    shutil.copy('../../doc/origin/pre_cpp.json', '../../data/analysis/pre_cpp.json')
    shutil.copy('../../doc/origin/pre_test.json', '../../data/analysis/pre_test.json')
    shutil.copy('../../doc/origin/topic_color.json', '../../data/analysis/topic_color.json')
    shutil.copy('../../doc/origin/topic_difficulty.json', '../../data/analysis/topic_difficulty.json')
    shutil.copy('../../doc/origin/topic_sequence.json', '../../data/analysis/topic_sequence.json')
    shutil.copy('../../doc/origin/type_weight.json', '../../data/analysis/type_weight.json')
    shutil.copy('../../doc/origin/user_rank.json', '../../data/analysis/user_rank.json')
    shutil.copy('../../doc/origin/user_score.json', '../../data/analysis/user_score.json')
    image = zipfile.ZipFile('../../doc/data/image.zip')
    image.extractall(path='../../data/image')
    print('Generate Dir Done!')


def generate_file():
    topic_download()
    user_download()
    generate_topic_iterator()
    generate_user_iterator()
    check_topics()
    check_users()
    generate_topic_iterator()
    generate_user_iterator()
    check_effective_answer()
    remove_invalid(UIterator('../../data/analysis/pre_cpp.json'))
    remove_invalid(UIterator('../../data/analysis/pre_test.json'))
    generate_topic_iterator()
    generate_user_iterator()


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
    print('Iterator Topic Done!')


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
    print('Iterator User Done!')


def check_topics():
    # 遍历检查下载内容是否被正确处理
    it = getTIterator()
    count = 1
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
            print()
            print(it.get_type() + '/' + it.get_topic() + '/' + it.get_user())
            shutil.rmtree('../../data/source/题目分析/' + it.get_type() + '/' + it.get_topic() + '/' + it.get_user())
        print(count, end=' ')
        count += 1
    print()
    print('Check Topics Done!')


def check_users():
    # 遍历检查下载内容是否被正确处理
    it = getUIterator()
    count = 1
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
            print()
            print(it.get_user() + '/' + it.get_type() + '/' + it.get_topic())
            shutil.rmtree('../../data/source/用户分析/' + it.get_user() + '/' + it.get_type() + '/' + it.get_topic())
        print(count, end=' ')
        count += 1
    print()
    print('Check Users Done!')


def check_effective_answer():
    not_python = {}
    it = getUIterator()
    count = 1
    while it.next():
        if check_cpp(it):
            add_Uindex(not_python, it)
        print(count, end=' ')
        count += 1
    test_oriented = check_test_cases(find_topic())
    generate_json('../../data/analysis/pre_cpp.json', not_python)
    generate_json('../../data/analysis/pre_test.json', test_oriented)
    print()
    print('Check Answer Done!')


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


def check_test_cases(topic_list: dict) -> dict:
    test_cases = read_json('../../data/import/test_cases.json')
    result = {}
    for item in test_cases.items():
        if item[1] is not []:
            users = item[1]
            for user in users:
                if 'user_id_' + user in list(result.keys()):
                    pass
                else:
                    result['user_id_' + user] = {}
                type, topic = topic_list[item[0]].split('/')
                if type in list(result['user_id_' + user].keys()):
                    pass
                else:
                    result['user_id_' + user][type] = []
                if topic in result['user_id_' + user][type]:
                    pass
                else:
                    result['user_id_' + user][type].append(topic)
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
    print('Remove Invalid Done!')


def find_topic() -> dict:
    test_data = read_json('../../data/origin/test_data.json')
    result = {}
    for item in test_data.items():
        cases = dict(item[1])
        for case in cases['cases']:
            if case['case_id'] in list(result.keys()):
                continue
            else:
                type = case['case_type']
                topic = case['case_zip'].split('/')[4]
                topic = topic[:len(topic) - 4]
                topic = topic.replace('*', '_')
                result[case['case_id']] = type + '/' + topic
    return result

# 该方法提供评估所有用户的命名规范程度的接口
def code_format():
    it = getUIterator()
    count = 1
    while it.next():
        str = "../../data/source/用户分析/" + it.get_user() + '/' + it.get_type() + '/' + it.get_topic() + '/main.py'
        result = os.system("autopep8" + " --in-place " + '"' + str + '"')
        print(count, end=' ')
        count += 1
    print()
    print("    Format Done!")
