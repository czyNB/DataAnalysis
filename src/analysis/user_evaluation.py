import os
from src.function.file_operations import *
from src.analysis.user_score import *
import numpy


class Evaluation:
    user_id = None  # 用户ID
    # 各个类别的平均分，是做了的题的综合得分
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
    # 各个类别的完成率，默认同类别下所有题目的难度相同
    rates = {
        '图结构': 0,
        '字符串': 0,
        '查找算法': 0,
        '排序算法': 0,
        '树结构': 0,
        '数组': 0,
        '数字操作': 0,
        '线性表': 0,
    }
    # 各个类别的综合得分
    comprehensive_scores = {
        '图结构': 0,
        '字符串': 0,
        '查找算法': 0,
        '排序算法': 0,
        '树结构': 0,
        '数组': 0,
        '数字操作': 0,
        '线性表': 0,
    }
    score_radar = ''  # 得分雷达图路径
    rate_radar = ''  # 完成率雷达图路径
    comprehensive_radar = ''  # 综合雷达图路径
    comprehensive_score = 0  # 综合评分，各类别综合分 * 各类别权重
    num_of_upload = 0  # 提交的代码数量
    num_of_invalid = 0  # 无效的代码数量
    rate_of_valid = 0  # 提交代码有效率
    rate_of_completion = 0  # 200道题的完成率

    def __init__(self, user_id):
        self.user_id = user_id
        scores = read_json('../../data/analysis/user_score.json')[user_id]
        weights = read_json('../../data/analysis/type_weight.json')
        for type in scores.keys():
            if scores[type] == {}:
                continue
            self.scores[type] = sum(scores[type].values()) / len(scores[type])
            if len(scores[type]) >= avg[type]:
                self.rates[type] = 1
            else:
                self.rates[type] = len(scores[type]) / avg[type]
            self.comprehensive_scores[type] = self.scores[type] * self.rates[type]
            self.comprehensive_score += self.comprehensive_scores[type] * weights[type]
            self.num_of_upload += 1
        print(self.comprehensive_score)
        del scores, type, weights

        self.score_radar = '../../data/image/score/' + user_id + '.png'
        self.rate_radar = '../../data/image/rate/' + user_id + '.png'
        self.comprehensive_radar = '../../data/image/' + user_id + '.png'
        get_radar(numpy.array(list(self.scores.values())), self.score_radar, 100, 'Python提交成绩分析图')
        get_radar(numpy.array(list(self.rates.values())), self.rate_radar, 1, 'Python提交率成绩分析图')
        get_radar(numpy.array(list(self.comprehensive_scores.values())), self.comprehensive_radar, 100, 'Python综合成绩分析图')

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
        self.rate_of_completion = (self.num_of_upload - self.num_of_invalid) / 200

    def compare(self, e):
        if self.comprehensive_score > e.comprehensive_score:
            return True
        elif self.comprehensive_score < e.comprehensive_score:
            return False
        else:
            if self.comprehensive_scores['图结构'] > e.comprehensive_scores['图结构']:
                return True
            elif self.comprehensive_scores['图结构'] < e.comprehensive_scores['图结构']:
                return False
            else:
                if self.comprehensive_scores['树结构'] > e.comprehensive_scores['树结构']:
                    return True
                elif self.comprehensive_scores['树结构'] < e.comprehensive_scores['树结构']:
                    return False
                else:
                    if self.comprehensive_scores['字符串'] > e.comprehensive_scores['字符串']:
                        return True
                    elif self.comprehensive_scores['字符串'] < e.comprehensive_scores['字符串']:
                        return False
                    else:
                        return True
