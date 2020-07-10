from src.function.file_operations import *


class Evaluation:
    user_scores = read_json('../../data/analysis/user_score.json')
    weights = read_json('../../data/analysis/type_weight.json')
    test_codes = read_json('../../data/analysis/test_oriented.json')
    cpp_codes = read_json('../../data/analysis/cpp_code.json')
    avg = {
        '图结构': 12,
        '字符串': 18,
        '排序算法': 11,
        '数字操作': 34,
        '数组': 46,
        '查找算法': 20,
        '树结构': 29,
        '线性表': 30,
    }

    def __init__(self, user_id):
        self.num_of_invalid = 0
        self.num_of_upload = 0
        self.comprehensive_score = 0
        self.scores = {
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
        self.rates = {
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
        self.comprehensive_scores = {
            '图结构': 0,
            '字符串': 0,
            '查找算法': 0,
            '排序算法': 0,
            '树结构': 0,
            '数组': 0,
            '数字操作': 0,
            '线性表': 0,
        }
        self.user_id = user_id
        scores = Evaluation.user_scores[user_id]
        for type in scores.keys():
            if scores[type] == {}:
                continue
            self.scores[type] = sum(scores[type].values()) / len(scores[type])
            if len(scores[type]) >= Evaluation.avg[type]:
                self.rates[type] = 1
            else:
                self.rates[type] = len(scores[type]) / Evaluation.avg[type]
            self.comprehensive_scores[type] = self.scores[type] * self.rates[type]
            self.comprehensive_score += self.comprehensive_scores[type] * Evaluation.weights[type]
            self.num_of_upload += 1

        self.score_radar = '../../data/image/upload_score/' + user_id + '.png'
        self.comprehensive_radar = '../../data/image/' + user_id + '.png'

        try:
            cpp_code = Evaluation.cpp_codes[user_id]
            test_code = Evaluation.test_codes[user_id]
            topics = list(cpp_code.values()) + list(test_code.values())
            for i in range(0, len(topics)):
                self.num_of_invalid += len(topics[i])
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
