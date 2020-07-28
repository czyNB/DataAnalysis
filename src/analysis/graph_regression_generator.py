"""使用scatter()绘制散点图"""
import matplotlib.pyplot as plt
from src.function.file_operations import *


def xxx():
    x_content = dict(read_json('../../data/analysis/user_rank.json'))
    code_eval = dict(read_json('../../data/analysis/code_evaluation.json'))
    x_values = []
    y_values = []

    x_content = dict(sorted(x_content.items(), key=lambda kv: (kv[1], kv[0])))
    for i in x_content.keys():
        x_values = x_values + [i]

    for j in x_content.keys():
        y_values = y_values + [code_eval[j]]

    '''
    scatter() 
    x:横坐标 y:纵坐标 s:点的尺寸
    '''
    plt.scatter(x_values, y_values, s=5)

    # 设置图表标题并给坐标轴加上标签
    plt.title('Users\' rank vs. users\' code quality', fontsize=24)
    plt.xlabel('user_rank', fontsize=14)
    plt.ylabel('code_evaluation', fontsize=14)

    # 设置刻度标记的大小
    plt.tick_params(axis='both', which='major', labelsize=1)
    plt.savefig('../../data/analysis/graph_regression.png')
    plt.show()


if __name__ == '__main__':
    xxx()
