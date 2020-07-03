"""
add_Uindex方法，用于收集迭代器中的数据以便生成符合用户分析的迭代文件
add_Tindex方法，用于收集迭代器中的数据以便生成符合题目分析的迭代文件
generate_json，生成json文件
read_json，读取json文件
read_file，读取普通文件
read_filelines，按行读取普通文件
"""
import json


def add_Uindex(result, it):
    if it.get_user() not in list(result):
        result[it.get_user()] = {it.get_type(): [it.get_topic()]}
    elif it.get_type() not in list(result[it.get_user()]):
        result[it.get_user()][it.get_type()] = [it.get_topic()]
    else:
        result[it.get_user()][it.get_type()].append(it.get_topic())


def add_Tindex(result, it):
    if it.get_type() not in list(result):
        result[it.get_type()] = {it.get_topic(): [it.get_user()]}
    elif it.get_topic() not in list(result[it.get_type()]):
        result[it.get_type()][it.get_topic()] = [it.get_user()]
    else:
        result[it.get_type()][it.get_topic()].append(it.user())


def generate_json(root, data):
    json_data = json.dumps(data, indent=4, separators=(',', ': '), ensure_ascii=False)
    f = open(root, 'w', encoding='utf-8')
    f.write(json_data)
    f.close()


def read_json(root):
    file = open(root, 'r', encoding='utf-8')
    res = file.read()
    data = json.loads(res)
    return data


def read_file(root):
    file = open(root, 'r', encoding='utf-8')
    return file.read()


def read_filelines(root):
    file = open(root, 'r', encoding='utf-8')
    return file.readlines()
