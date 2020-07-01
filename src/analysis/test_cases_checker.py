import json
import os


def test_cases_checker():
    result = {}
    f1 = open('../../data/analysis/topic_iterator.json', encoding='utf-8')  # f1为题目分析
    data = json.loads(f1.read())  # 加载json数据
    for type in data.keys():
        for topic in data[type].keys():
            for user in data[type][topic]:
                print()


if __name__ == '__main__':
    test_cases_checker()
