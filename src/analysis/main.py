from src.download.download import *
from src.analysis.pre_processing import *
from src.analysis.user_score import *
from src.analysis.topic_difficulty import *
from src.analysis.user_evaluation import *
import os


def initialize():
    try:
        os.mkdir('../../data')
        os.mkdir('../../data/analysis')
        os.mkdir('../../data/origin')
        os.mkdir('../../data/source')
    except FileExistsError:
        pass
    # 下载题目分析
    topic_download()
    # 下载用户分析
    user_download()
    # 生成初代题目分析迭代文件
    generate_topic_iterator()
    # 生成初代用户分析迭代文件
    generate_user_iterator()
    # 检查题目分析中下载是否出错
    check_topics()
    # 检查用户分析中下载是否出错
    check_users()
    # 生成二代题目分析迭代文件
    generate_topic_iterator()
    # 生成二代用户分析迭代文件
    generate_user_iterator()
    # 检查无效作答代码
    check_effective_answer()
    # 生成cpp代码迭代器
    cpp_it = UIterator('../../data/analysis/cpp_code.json')
    # 生成面向用例代码迭代器
    test_it = UIterator('../../data/analysis/test_oriented.json')
    # 创建所需要的文件夹
    try:
        os.mkdir('../../data/source/无效代码')
    except FileExistsError:
        pass
    # 移除cpp代码
    remove_invalid(cpp_it)
    # 移除面向用例代码
    remove_invalid(test_it)
    # 生成终代题目分析迭代文件
    generate_topic_iterator()
    # 生成终代题目分析迭代文件
    generate_user_iterator()
    print("Done!")


def user_analysis():
    # generate_all()
    # get_weight()
    e = Evaluation('user_id_60641')
    print('Done!')


def topic_analysis():
    evaluate_exercises()
    print('Done!')


def code_analysis():
    print('Done!')


if __name__ == '__main__':
    # initialize()
    user_analysis()
    # topic_analysis()
    code_analysis()
