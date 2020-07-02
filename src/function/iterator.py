import os
import json


class TIterator:
    data = {}
    type_id = 0
    topic_id = 0
    user_id = -1  # 方便整体结构

    def __init__(self, root):
        file = open(root, encoding='utf-8')
        res = file.read()
        self.data = json.loads(res)

    def current(self):
        type = self.get_type()
        topic = self.get_topic()
        user = self.get_user()
        file = open('../../data/source/题目分析/' + type + '/' + topic + '/' + user + '/main.py', 'r',
                    encoding='utf-8')
        result = file.read()
        return result

    def next(self):
        type = self.get_type()
        topic = self.get_topic()
        self.user_id = self.user_id + 1
        if self.user_id == len(self.data[type][topic]):
            self.user_id = 0
            self.topic_id = self.topic_id + 1
            if self.topic_id == len(self.data[type]):
                self.topic_id = 0
                self.type_id = self.type_id + 1
                if self.type_id == len(self.data):
                    self.type_id = 0
                    return False
        return True

    def get_type(self):
        return list(self.data)[self.type_id]

    def get_topic(self):
        return list(self.data[self.get_type()])[self.topic_id]

    def get_user(self):
        return self.data[self.get_type()][self.get_topic()][self.user_id]


class UIterator:
    data = {}
    user_id = 0
    type_id = 0
    topic_id = -1  # 方便整体结构

    def __init__(self, root):
        file = open(root, 'r', encoding='utf-8')
        self.data = json.loads(file.read())

    def current(self):
        user = self.get_user()
        type = self.get_type()
        topic = self.get_topic()
        file = open('../../data/source/用户分析/' + user + '/' + type + '/' + topic + '/main.py', 'r',
                    encoding='utf-8')
        result = file.read()
        return result

    def next(self):
        user = self.get_user()
        type = self.get_type()
        self.topic_id = self.topic_id + 1
        if self.topic_id == len(self.data[user][type]):
            self.topic_id = 0
            self.type_id = self.type_id + 1
            if self.type_id == len(self.data[user]):
                self.type_id = 0
                self.user_id = self.user_id + 1
                if self.user_id == len(self.data):
                    self.user_id = 0
                    return False
        return True

    def get_user(self):
        return list(self.data)[self.user_id]

    def get_type(self):
        return list(self.data[self.get_user()])[self.type_id]

    def get_topic(self):
        return self.data[self.get_user()][self.get_type()][self.topic_id]


def generate_topic_iterator():
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


def getTIterator():
    return TIterator('../../data/analysis/topic_iterator.json')


def getUIterator():
    return UIterator('../../data/analysis/user_iterator.json')


def generate_user_iterator():
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
    generate_topic_iterator()
    generate_user_iterator()
