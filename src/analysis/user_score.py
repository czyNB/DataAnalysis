from src.analysis.user_evaluation import *
import numpy
import matplotlib.pyplot
import matplotlib

user_scores = {}
data = None
cpp_it = None
test_it = None
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


def get_all_scores():
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
    while cpp_it.next():
        result[cpp_it.get_user()][cpp_it.get_type()][cpp_it.get_topic()] = 0
    while test_it.next():
        result[test_it.get_user()][test_it.get_type()][test_it.get_topic()] = 0
    generate_json('../../data/analysis/user_score.json', result)
    print('Get All Scores Done!')


def get_radar(data, root, ceiling, name):
    matplotlib.rcParams['font.family'] = 'SimHei'
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    # numpy.array 高效的数组
    types = numpy.array(
        ['图结构\n' + str(round(data[0], 2)), '字符串\n' + str(round(data[1], 2)), '查找算法 ' + str(round(data[2], 2)),
         '排序算法\n' + str(round(data[3], 2)), '树结构\n' + str(round(data[4], 2)), '数组\n' + str(round(data[5], 2)),
         "数字操作 " + str(round(data[6], 2)), "线性表\n" + str(round(data[7], 2))])
    num_of_types = 8
    # numpy.linespace 在0-2pi之间划分八个区域
    angles = numpy.linspace(0, 2 * numpy.pi, num_of_types, endpoint=False)  # 弧度制
    # numpy.concatenate 拼接数组的方法
    # 首尾相连
    data = numpy.concatenate((data, [ceiling]))
    angles = numpy.concatenate((angles, [angles[0]]))
    figure = matplotlib.pyplot.figure(figsize=(5, 5), facecolor="white")
    # matplotlib.pyplot.subplot 绘制子图 111 意为在1*1中的第1个
    ax = figure.add_subplot(111, polar=True)
    # matplotlib.pyplot.plot 绘制点线图
    n_grids = numpy.linspace(0, ceiling, 6, endpoint=True)  # grid的网格数
    grids = [[i] * 9 for i in n_grids]  # grids的半径
    for i, grid in enumerate(grids[::-1]):  # 给grid 填充间隔色
        matplotlib.pyplot.plot(angles, grid, color='grey', linewidth=0.5)
        if (i > 0) & (i % 2 == 0):
            matplotlib.pyplot.fill_between(angles, grids[i], grids[i - 1], color='grey', alpha=0.1)
    ax.plot(angles, data, '.', color='black', linewidth=2)
    ax.plot(numpy.concatenate((angles[0:8], [angles[0]])), numpy.concatenate((data[0:8], [data[0]])),
            '.-', color='orange', linewidth=2)
    # matplotlib.pyplot.fill 填充点线图
    # matplotlib.pyplot.fill(angles[0:8], data[0:8], facecolor='g', alpha=0.2)
    # matplotlib.pyplot.thetagrids 绘制极轴
    ax.set_thetagrids(angles * 180 / numpy.pi, types)
    # matplotlib.pyplot.figtext 标题
    matplotlib.pyplot.figtext(0.5, 0.97, name, ha='center')
    # 坐标轴 matplotlib.pyplot.xticks or yticks
    # matplotlib.pyplot.set_xticks([])
    ax.set_yticks([])
    # matplotlib.pyplot.grid 生成网格
    ax.grid(axis='y')
    # 外圈不可见
    ax.spines['polar'].set_visible(False)
    matplotlib.pyplot.savefig(root)
    matplotlib.pyplot.show()


def get_weight():
    type_weights = {
        '图结构': 0,
        '字符串': 0,
        '排序算法': 0,
        '数字操作': 0,
        '数组': 0,
        '查找算法': 0,
        '树结构': 0,
        '线性表': 0,
    }

    for user in list(user_scores.keys()):
        for type in list(user_scores[user].keys()):
            if len(user_scores[user][type]) >= avg[type]:
                lost_scores = 100 - sum(user_scores[user][type].values()) / len(user_scores[user][type])
            else:
                lost_scores = 100 - sum(user_scores[user][type].values()) / avg[type]
            type_weights[type] += lost_scores
    s = sum(type_weights.values())
    for type in list(type_weights.keys()):
        type_weights[type] = type_weights[type] / s
    generate_json('../../data/analysis/type_weight.json', type_weights)
    print('Get Weight Done!')


def get_rank():
    users = list(read_json('../../data/analysis/iterator_user.json').keys())
    user_rank = {}

    for user in users:
        e = Evaluation(user)
        user_rank[user] = e.comprehensive_score
        get_radar(numpy.array(list(e.comprehensive_scores.values())), e.comprehensive_radar, 100, 'Python综合成绩分析图')

    user_rank = dict(sorted(user_rank.items(), key=lambda x: x[1], reverse=True))
    generate_json('../../data/analysis/user_rank.json', user_rank)
    print('Get Rank Done!')
