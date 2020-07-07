import os

from src.function.file_operations import *
from src.analysis.user_score import *
import numpy


class Evaluation:
    user_id = None  # 用户ID
    # 各个类别的平均分
    scores = {
        '图结构': 0,
        '字符串': 0,
        '查找算法': 0,
        '排序算法': 0,
        '树结构': 0,
        '数组': 0,
        '数字操作': 0,
        '线性表': 0,
    }
    radar_graph = ''  # 雷达图路径
    comprehensive_score = 0  # 综合评分，通过各类别平均分加权得到
    num_of_upload = 0  # 提交的代码数量
    num_of_invalid = 0  # 无效的代码数量
    rate_of_valid = 0  # 提交代码有效率

    def __init__(self, user_id):
        self.user_id = user_id

        difficulties = read_json('../../data/analysis/difficulty_of_exercises.json')
        scores = read_json('../../data/analysis/user_score.json')[user_id]
        for type in scores.keys():
            for topic in scores[type]:
                difficulty = float(difficulties[type + '/' + topic].split(';')[1])
                score = scores[type][topic]
                self.scores[type] += score * difficulty
                self.num_of_upload += 1
        del difficulties, scores, type, topic, difficulty, score

        self.radar_graph = get_score_radar(self.user_id, numpy.array(list(self.scores.values())))

        try:
            cpp_code = read_json('../../data/analysis/cpp_code.json')[user_id]
            test_code = read_json('../../data/analysis/test_oriented.json')[user_id]
            topics = list(cpp_code.values()) + list(test_code.values())
            for i in range(0, len(topics)):
                self.num_of_invalid += len(topics[i])
            del cpp_code, test_code, topics
        except KeyError:
            pass
        self.rate_of_valid = (self.num_of_upload - self.num_of_invalid) / self.num_of_upload
