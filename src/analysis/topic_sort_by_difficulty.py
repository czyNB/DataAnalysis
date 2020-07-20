from src.function.file_operations import *
import operator
import numpy as np
from matplotlib import pyplot as plt
plt.rcParams['font.sans-serif']=['Arial Unicode MS']



def sort_topics_by_difficulty():
    reader = read_json('../../data/analysis/topic_difficulty.json')
    temp = {}
    for i in reader:
        current_item = i
        for j in reader[i]:
            k = i + '-' + j.split('_')[0]
            temp.update({k: float(reader[i][j])})
    sorted_x = sorted(temp.items(), key=operator.itemgetter(1))
    generate_json('../../data/analysis/topic_difficulty_sorted.json', dict(sorted_x))
    print('Done!')
    generate_the_form()


def generate_the_form():
    data = read_json('../../data/analysis/topic_difficulty_sorted.json')
    # 创建窗口, 并设置分辨率
    fig = plt.figure(figsize=(200, 10), dpi=100)
    # 柱子总数
    N = len(data)
    # 包含每个柱子对应值的序列
    values = []
    for ii in data:
        values = values + [data[ii]]
        # print(data[ii])
    # print(values)
    # 包含每个柱子下标的序列
    index = np.arange(N)
    # 柱子的宽度
    width = 0.45
    # 绘制柱状图, 每根柱子的颜色为紫罗兰色
    p2 = plt.bar(index, values, width, label="num", color="#87CEFA")
    # 设置横轴标签
    plt.xlabel('题目名称')
    # 设置纵轴标签
    plt.ylabel('题目难度')
    # 添加标题
    plt.title('题目名称-难度柱形图')
    # 添加纵横轴的刻度
    plt.xticks(index, tuple(dict(data).keys()))
    # plt.yticks(np.arange(0, 10000, 10))
    # 添加图例
    plt.legend(loc="upper right")
    fig.autofmt_xdate()
    plt.show()
    print('Done!')