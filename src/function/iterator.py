import os
import json


def topic_iterator():
    result = {}
    topic_type = os.listdir('../../data/source/题目分析')
    for type in topic_type:
        result[type] = {}
        topics = os.listdir('../../data/source/题目分析/' + type)
        for topic in topics:
            users = os.listdir('../../data/source/题目分析/' + type + '/' + topic)
            result[type][topic] = users
    json_data = json.dumps(result, indent=4, separators=(',', ': '), ensure_ascii=False)
    f = open('../../data/analysis/topic_iterator.json', 'w', encoding='utf-8')
    f.write(json_data)
    f.close()


def user_iterator():
    result = {}
    users = os.listdir('../../data/source/用户分析')
    for user in users:
        result[user] = {}
        types = os.listdir('../../data/source/用户分析/' + user)
        for type in types:
            topics = os.listdir('../../data/source/用户分析/' + user + '/' + type)
            result[user][type] = topics
    json_data = json.dumps(result, indent=4, separators=(',', ': '), ensure_ascii=False)
    f = open('../../data/analysis/user_iterator.json', 'w', encoding='utf-8')
    f.write(json_data)
    f.close()


if __name__ == '__main__':
    topic_iterator()
    user_iterator()
