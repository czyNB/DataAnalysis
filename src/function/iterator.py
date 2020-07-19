from src.function.file_operations import *


class TIterator:
    data = {}
    type_id = 0
    topic_id = 0
    user_id = -1  # 方便整体结构

    def __init__(self, root):
        self.data = read_json(root)

    def current(self):
        type = self.get_type()
        topic = self.get_topic()
        user = self.get_user()
        return read_filelines('../../data/source/题目分析/' + type + '/' + topic + '/' + user + '/main.py')

    def answer(self):
        type = self.get_type()
        topic = self.get_topic()
        user = self.get_user()
        return read_file('../../data/source/题目分析/' + type + '/' + topic + '/' + user + '/.mooctest/answer.py')

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
                    self.user_id = -1
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
        self.data = read_json(root)

    def current(self):
        user = self.get_user()
        type = self.get_type()
        topic = self.get_topic()
        return read_filelines('../../data/source/用户分析/' + user + '/' + type + '/' + topic + '/main.py')

    def now(self):
        user = self.get_user()
        type = self.get_type()
        if self.topic_id == len(self.data[user][type]):
            self.topic_id = 0
            self.type_id = self.type_id + 1
            if self.type_id == len(self.data[user]):
                self.type_id = 0
                self.user_id = self.user_id + 1
                if self.user_id == len(self.data):
                    self.user_id = 0
                    self.topic_id = -1
                    return False
        return True


    def next(self):
        # print(self.get_user())
        # topic = self.get_topic()
        type = self.get_type()
        user = self.get_user()
        self.topic_id = self.topic_id + 1
        if self.topic_id == len(self.data[user][type]):
            self.topic_id = 0
            self.type_id = self.type_id + 1
            if self.type_id == len(self.data[user]):
                self.type_id = 0
                self.user_id = self.user_id + 1
                if self.user_id == len(self.data):
                    self.user_id = 0
                    self.topic_id = -1
                    return False
        return True

    def get_user(self):
        # print('User: ',end='')
        # print(self.user_id)
        return list(self.data)[self.user_id]

    def get_type(self):
        # print('Type: ',end='')
        # print(self.type_id)
        return list(self.data[self.get_user()])[self.type_id]

    def get_topic(self):
        # print('Topic: ',end='')
        # print(self.topic_id)
        return self.data[self.get_user()][self.get_type()][self.topic_id]


def getTIterator():
    return TIterator('../../data/analysis/topic_iterator.json')  # topic_iterator.json


def getUIterator():
    return UIterator('../../data/analysis/user_iterator.json')  # user_iterator.json
