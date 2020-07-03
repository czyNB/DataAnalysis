from src.function.iterator import *
import os


def check_topics():
    # 遍历检查下载内容是否被正确处理
    it = TIterator('../../data/analysis/topic_iterator.json')
    while it.next():
        try:
            docs = os.listdir('../../data/source/题目分析/' + it.get_type() + '/' + it.get_topic() + '/' + it.get_user())
            assert docs == ['.mooctest', 'blockly.xml', 'main.py', 'properties', 'readme.md']  # 检查目录内容是否为解压内容
        except AssertionError:
            print(it.get_type() + '/' + it.get_topic() + '/' + it.get_user())


def check_users():
    # 遍历检查下载内容是否被正确处理
    it = UIterator('../../data/analysis/user_iterator.json')
    while it.next():
        try:
            docs = os.listdir('../../data/source/用户分析/' + it.get_user() + '/' + it.get_type() + '/' + it.get_topic())
            assert docs == ['.mooctest', 'blockly.xml', 'main.py', 'properties', 'readme.md']  # 检查目录内容是否为解压内容
        except AssertionError:
            print(it.get_user() + '/' + it.get_type() + '/' + it.get_topic())


if __name__ == '__main__':
    check_topics()
    check_users()
