from src.function.file_operations import *
from src.function.iterator import *
import numpy
import matplotlib.pyplot
import matplotlib


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
        result[cpp_it.get_user()][cpp_it.get_type()][cpp_it.get_topic()] = 0
    while test_it.next():
        result[test_it.get_user()][test_it.get_type()][test_it.get_topic()] = 0
    generate_json('../../data/analysis/user_score.json', result)


def get_score_radar(user_id, scores):
    matplotlib.rcParams['font.family'] = 'SimHei'
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    # numpy.array 高效的数组
    types = numpy.array(
        ['图结构\n' + str(round(scores[0], 2)), '字符串\n' + str(round(scores[1], 2)), '排序算法 ' + str(round(scores[2], 2)),
         '数字操作\n' + str(round(scores[3], 2)), '数组\n' + str(round(scores[4], 2)), '查找算法\n' + str(round(scores[5], 2)),
         "树结构 " + str(round(scores[6], 2)), "线性表\n" + str(round(scores[7], 2))])
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
    matplotlib.pyplot.savefig('../../data/image/' + user_id + '.png')
    matplotlib.pyplot.show()
    return '../../data/image/' + user_id + '.png'
