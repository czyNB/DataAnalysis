import os
from src.function.file_operations import *


def generate_topic_iterator():
    result = {}
    topic_type = os.listdir('../../data/source/题目分析')
    for type in topic_type:
        result[type] = {}
        topics = os.listdir('../../data/source/题目分析/' + type)
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
    for user in users:
        result[user] = {}
        types = os.listdir('../../data/source/用户分析/' + user)
        for type in types:
            topics = os.listdir('../../data/source/用户分析/' + user + '/' + type)
            if not topics:
                os.rmdir('../../data/source/用户分析/' + user + '/' + type)
            else:
                result[user][type] = topics
    generate_json('../../data/analysis/user_iterator.json', result)


if __name__ == '__main__':
    generate_topic_iterator()
    generate_user_iterator()
