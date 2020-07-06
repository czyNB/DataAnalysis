import numpy
import matplotlib.pyplot
import matplotlib


def generate_score_radar():
    matplotlib.rcParams['font.family'] = 'SimHei'
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    # numpy.array 高效的数组
    types = numpy.array(['图结构', '字符串', '排序算法', '数字操作', '数组', '查找算法', "树结构", "线性表"])
    num_of_types = 8
    scores = numpy.array([88.7, 85, 90, 95, 70, 96, 78, 45])
    # numpy.linespace 在0-2pi之间划分八个区域
    angles = numpy.linspace(0, 2 * numpy.pi, num_of_types, endpoint=False)  # 弧度制
    # numpy.concatenate 拼接数组的方法
    # 首尾相连
    scores = numpy.concatenate((scores, [scores[0]]))
    angles = numpy.concatenate((angles, [angles[0]]))
    figure = matplotlib.pyplot.figure(facecolor="white")
    # matplotlib.pyplot.subplot 绘制子图 111 意为在1*1中的第1个
    matplotlib.pyplot.subplot(111, polar=True)
    # matplotlib.pyplot.plot 绘制点线图
    matplotlib.pyplot.plot(angles, scores, 'bo-', color='g', linewidth=2)
    # matplotlib.pyplot.fill 填充点线图
    matplotlib.pyplot.fill(angles, scores, facecolor='g', alpha=0.2)
    # matplotlib.pyplot.thetagrids 绘制极轴
    matplotlib.pyplot.thetagrids(angles * 180 / numpy.pi, types)
    # matplotlib.pyplot.figtext 标题
    matplotlib.pyplot.figtext(0.52, 0.95, 'Python成绩分析图', ha='center')
    # matplotlib.pyplot.grid 生成网格
    matplotlib.pyplot.grid(True)
    matplotlib.pyplot.show()


if __name__ == '__main__':
    generate_score_radar()
