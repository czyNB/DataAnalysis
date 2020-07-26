from src.function.file_operations import *
import operator
import numpy as np
from matplotlib import pyplot as plt

plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['font.sans-serif'] = ['SimHei']


def sort_topics_by_difficulty():
    reader = read_json('../../data/analysis/topic_difficulty.json')
    temp = {}
    for type in reader:
        for topic in reader[type]:
            k = str(list(reader).index(type)) + '\n' + str(list(reader[type]).index(topic))
            temp.update({k: float(reader[type][topic])})
    sorted_x = sorted(temp.items(), key=operator.itemgetter(1))
    generate_json('../../data/analysis/topic_sequence.json', dict(sorted_x))
    print('    Topic Sequence Done!')
    set_color()
    generate_the_form()


def set_color():
    f = read_json('../../data/analysis/topic_sequence.json')
    t = {}
    counter = 0
    for w in f.keys():
        counter = counter + 1
        w = str(w).split('\n')[0]
        # print(w)
        if w == '0':
            t.update({counter: 'Red'})
        elif w == '1':
            t.update({counter: 'Blue'})
        elif w == '2':
            t.update({counter: 'Green'})
        elif w == '3':
            t.update({counter: 'Teal'})
        elif w == '4':
            t.update({counter: 'Yellow'})
        elif w == '5':
            t.update({counter: 'Orange'})
        elif w == '6':
            t.update({counter: 'Purple'})
        elif w == '7':
            t.update({counter: 'Pink'})
    # print(t)
    generate_json('../../data/analysis/topic_color.json', t)


def generate_the_form():
    data = read_json('../../data/analysis/topic_sequence.json')
    # 创建窗口, 并设置分辨率
    fig = plt.figure(figsize=(300, 10), dpi=100)
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
    width = 0.6
    # 绘制柱状图
    ff = read_json('../../data/analysis/topic_color.json')
    co = []
    for www in ff.values():
        co = co + [www]
    plt.bar(index, values, width, color=co)
    plt.bar(index, [values[0]] + [0] * (len(values) - 1), width, label='图结构', color='Red')
    plt.bar(index, [0, values[1]] + [0] * (len(values) - 2), width, label='字符串', color='Blue')
    plt.bar(index, [0] * 20 + [values[20]] + [0] * (len(values) - 21), width, label='排序算法', color='Green')
    plt.bar(index, [0] * 2 + [values[2]] + [0] * (len(values) - 3), width, label='数字操作', color='Teal')
    plt.bar(index, [0] * 10 + [values[10]] + [0] * (len(values) - 11), width, label='数组', color='Yellow')
    plt.bar(index, [0] * 6 + [values[6]] + [0] * (len(values) - 7), width, label='查找算法', color='Orange')
    plt.bar(index, [0] * 14 + [values[14]] + [0] * (len(values) - 15), width, label='树结构', color='Purple')
    plt.bar(index, [0] * 3 + [values[3]] + [0] * (len(values) - 4), width, label='线性表', color='Pink')
    # 设置横轴标签
    plt.xlabel('题目名称')
    # 设置纵轴标签
    plt.ylabel('题目难度')
    # 添加标题
    plt.title('题目名称-难度柱形图')
    # 添加纵横轴的刻度
    plt.xticks(index, list(data))
    plt.legend(loc="upper right")
    plt.savefig('../../data/analysis/graph_difficulty.png')
    print('    Graph Difficulty Done!')
