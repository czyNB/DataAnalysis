from src.function.file_operations import *
from src.function.iterator import *
import numpy


def generate_all():
    count = 0
    data = read_json('../../data/origin/test_data.json')
    result = {}
    users = list(data)
    for user in users:
        result['user_id_' + user] = {
            '图结构': {},
            '字符串': {},
            '排序算法': {},
            '数字操作': {},
            '数组': {},
            '查找算法': {},
            '树结构': {},
            '线性表': {}
        }
        cases = data[user]['cases']
        for case in cases:
            type = case['case_type']
            s = case['case_zip'].split('/')[4]
            topic = s[0:len(s) - 4].replace('*', '_')
            upload_records = case['upload_records']
            try:
                score = sorted(upload_records, key=lambda x: x["score"], reverse=True)[0]['score']
            except IndexError:
                continue
            result['user_id_' + user][type][topic] = score
            print(count)
            count += 1
    cpp_it = UIterator('../../data/analysis/cpp_code.json')
    test_it = UIterator('../../data/analysis/test_oriented.json')
    while cpp_it.next():
        del result[cpp_it.get_user()][cpp_it.get_type()][cpp_it.get_topic()]
    while test_it.next():
        del result[test_it.get_user()][test_it.get_type()][test_it.get_topic()]
    generate_json('../../data/analysis/user_score.json', result)


def average_score(user_id):
    scores = [0, 0, 0, 0, 0, 0, 0, 0]
    data = read_json('../../data/analysis/user_score.json')[user_id]
    types = list(data)
    for i in range(0,8):
        if data[types[i]] == {}:
            continue
        else:
            scores[i] = sum(data[types[i]].values()) / len(data[types[i]])
    return numpy.array(scores)


if __name__ == '__main__':
    generate_all()
