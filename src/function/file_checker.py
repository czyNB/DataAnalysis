import os
import json


def check_topics():
    # 遍历检查下载内容是否被正确处理
    f1 = open('../../data/analysis/topic_iterator.json', encoding='utf-8')  # f1为题目分析
    data = json.loads(f1.read())  # 加载json数据
    for type in data.keys():
        for topic in data[type].keys():
            for user in data[type][topic]:
                try:
                    docs = os.listdir('../../data/source/题目分析/' + type + '/' + topic + '/' + user)
                    assert docs == ['.mooctest', 'blockly.xml', 'main.py', 'properties', 'readme.md']  # 检查目录内容是否为解压内容
                except AssertionError:
                    print(type + '/' + topic + '/' + user)


def check_users():
    # 遍历检查下载内容是否被正确处理
    f2 = open('../../data/analysis/user_iterator.json', encoding='utf-8')  # f2为用户分析
    data = json.loads(f2.read())  # 加载json数据
    for user in data.keys():
        for type in data[user].keys():
            for topic in data[user][type]:
                try:
                    docs = os.listdir('../../data/source/用户分析/' + user + '/' + type + '/' + topic)
                    assert docs == ['.mooctest', 'blockly.xml', 'main.py', 'properties', 'readme.md']  # 检查目录内容是否为解压内容
                except AssertionError:
                    print(user + '/' + type + '/' + topic)


if __name__ == '__main__':
    check_topics()
    check_users()
