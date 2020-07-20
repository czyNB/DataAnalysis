from src.analysis import user_score
from src.analysis.code_name import *
from src.download.download import *
from src.analysis.pre_processing import *
from src.analysis.user_score import *
from src.analysis.topic_evaluation import *
from src.analysis.user_evaluation import *
import os


def initialize():
    # 预生成文件夹
    generate_dir()
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
    cpp_it = UIterator('../../data/analysis/pre_cpp.json')
    # 生成面向用例代码迭代器
    test_it = UIterator('../../data/analysis/pre_test.json')
    # 移除cpp代码
    remove_invalid(cpp_it)
    # 移除面向用例代码
    remove_invalid(test_it)
    # 生成终代题目分析迭代文件
    generate_topic_iterator()
    # 生成终代题目分析迭代文件
    generate_user_iterator()
    # 生成数据
    user_score.data = read_json('../../data/origin/test_data.json')
    user_score.cpp_it = UIterator('../../data/analysis/pre_cpp.json')
    user_score.test_it = UIterator('../../data/analysis/pre_test.json')
    Evaluation.test_codes = read_json('../../data/analysis/pre_test.json')
    Evaluation.cpp_codes = read_json('../../data/analysis/pre_cpp.json')
    print("Done!")


def generate_dir():
    try:
        os.mkdir('../../data')
    except FileExistsError:
        pass
    try:
        os.mkdir('../../data/analysis')
    except FileExistsError:
        pass
    try:
        os.mkdir('../../data/analysis')
    except FileExistsError:
        pass
    try:
        os.mkdir('../../data/origin')
    except FileExistsError:
        pass
    try:
        os.mkdir('../../data/source')
    except FileExistsError:
        pass
    try:
        os.mkdir('../../data/image')
    except FileExistsError:
        pass
    try:
        os.mkdir('../../data/source/题目分析')
    except FileExistsError:
        pass
    try:
        os.mkdir('../../data/source/用户分析')
    except FileExistsError:
        pass
    try:
        os.mkdir('../../data/source/无效代码')
    except FileExistsError:
        pass
    shutil.copy('../../doc/origin/test_data.json', '../../data/origin/test_data.json')
    shutil.copy('../../doc/origin/sample.json', '../../data/origin/sample.json')


def user_analysis():
    # 分析数据
    get_all_scores()
    # 生成数据
    user_score.user_scores = read_json('../../data/analysis/user_score.json')
    Evaluation.user_scores = read_json('../../data/analysis/user_score.json')
    # 分析数据
    get_weight()
    # 生成数据
    Evaluation.weights = read_json('../../data/analysis/type_weight.json')
    # 分析数据
    get_rank()
    print('Done!')


def topic_analysis():
    topic_eval_generator()
    print('Done!')


def code_analysis():
    evaluate_users()
    print('Done!')


if __name__ == '__main__':
    # initialize()
    # user_analysis()
    topic_analysis()
    # code_analysis()