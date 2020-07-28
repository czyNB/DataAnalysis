# 统计数据
import numpy as np
from src.function.file_operations import *
from src.function.iterator import *
from numpy import ndarray


# 方差
def variance(list_a: list) -> float:
    list_a = list(map(float, list_a))
    return np.var(list_a)


# 标准差
def deviation(list_b: list) -> float:
    list_b = list(map(float, list_b))
    return np.std(list_b)


# 平均值
def average(list_c: list) -> float:
    list_c = list(map(float, list_c))
    return np.mean(list_c)


# 协方差
def coveriance(list_a: list, list_b: list) -> float:
    list_a = list(map(float, list_a))
    list_b = list(map(float, list_b))
    list_ab = []
    for i in range(0, len(list_a)):
        list_ab.append(float(list_a[i] * list_b[i]))
    return average(list_ab) - average(list_a) * average(list_b)


# 相关系数
def r_reference(list_a: list, list_b: list) -> float:
    list_a = list(map(float, list_a))
    list_b = list(map(float, list_b))
    r_reference = coveriance(list_a, list_b) / deviation(list_a) / deviation(list_b)
    return r_reference


def yyy():
    scores = read_json('../../data/analysis/user_rank.json')
    codes = read_json('../../data/analysis/code_evaluation.json')
    users = list(read_json('../../data/analysis/iterator_user.json'))
    a = []
    b = []
    for user in users:
        a.append(scores[user])
        b.append(codes[user])
    print(r_reference(a, b))
