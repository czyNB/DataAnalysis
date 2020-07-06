import numpy
import matplotlib.pyplot
import matplotlib
from src.analysis.user_score import *


def generate_score_radar(scores):
    matplotlib.rcParams['font.family'] = 'SimHei'
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    # numpy.array 高效的数组
    types = numpy.array(
        ['图结构\n' + str(round(scores[0], 1)), '字符串\n' + str(round(scores[1], 1)), '排序算法' + str(round(scores[2], 1)),
         '数字操作\n' + str(round(scores[3], 1)), '数组\n' + str(round(scores[4], 1)), '查找算法\n' + str(round(scores[5], 1)),
         "树结构 " + str(round(scores[6], 1)), "线性表\n" + str(round(scores[7], 1))])
    num_of_types = 8
    # numpy.linespace 在0-2pi之间划分八个区域
    angles = numpy.linspace(0, 2 * numpy.pi, num_of_types, endpoint=False)  # 弧度制
    # numpy.concatenate 拼接数组的方法
    # 首尾相连
    scores = numpy.concatenate((scores, [scores[0]]))
    angles = numpy.concatenate((angles, [angles[0]]))
    figure = matplotlib.pyplot.figure(figsize=(5, 5), facecolor="white")
    # matplotlib.pyplot.subplot 绘制子图 111 意为在1*1中的第1个
    matplotlib.pyplot.subplot(111, polar=True)
    # matplotlib.pyplot.plot 绘制点线图
    matplotlib.pyplot.plot(angles, scores, 'bo-', color='g', linewidth=2)
    # matplotlib.pyplot.fill 填充点线图
    matplotlib.pyplot.fill(angles, scores, facecolor='g', alpha=0.2)
    # matplotlib.pyplot.thetagrids 绘制极轴
    matplotlib.pyplot.thetagrids(angles * 180 / numpy.pi, types)
    # matplotlib.pyplot.figtext 标题
    matplotlib.pyplot.figtext(0.5, 0.97, 'Python成绩分析图', ha='center')
    # matplotlib.pyplot.grid 生成网格
    matplotlib.pyplot.grid(True)
    matplotlib.pyplot.show()


if __name__ == '__main__':
    generate_score_radar(average_score('user_id_60641'))
