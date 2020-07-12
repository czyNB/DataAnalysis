from src.analysis import user_score
from src.download.download import *
from src.analysis.pre_processing import *
from src.analysis.user_score import *
from src.analysis.topic_difficulty import *
from src.analysis.user_evaluation import *
import os


def initialize():
    # 下载题目分析
    # topic_download()
    # 下载用户分析
    # user_download()
    # 生成初代题目分析迭代文件
    generate_topic_iterator()
    # 生成初代用户分析迭代文件
    generate_user_iterator()
    # 检查题目分析中下载是否出错
    # check_topics()
    # 检查用户分析中下载是否出错
    # check_users()
    # 生成二代题目分析迭代文件
    # generate_topic_iterator()
    # 生成二代用户分析迭代文件
    # generate_user_iterator()
    # 检查无效作答代码
    # check_effective_answer()
    # 生成cpp代码迭代器
    # cpp_it = UIterator('../../data/analysis/cpp_code.json')
    # 生成面向用例代码迭代器
    # test_it = UIterator('../../data/analysis/test_oriented.json')
    # 移除cpp代码
    # remove_invalid(cpp_it)
    # 移除面向用例代码
    # remove_invalid(test_it)
    # 生成终代题目分析迭代文件
    # generate_topic_iterator()
    # 生成终代题目分析迭代文件
    # generate_user_iterator()
    # 生成数据
    # user_score.data = read_json('../../data/origin/test_data.json')
    # user_score.cpp_it = UIterator('../../data/analysis/cpp_code.json')
    # user_score.test_it = UIterator('../../data/analysis/test_oriented.json')
    # Evaluation.test_codes = read_json('../../data/analysis/test_oriented.json')
    # Evaluation.cpp_codes = read_json('../../data/analysis/cpp_code.json')
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
    shutil.copy('../../doc/origin/sample.json', '../../data/origin/sample.json.json')
    # 预创建文件
    try:
        open('../../data/analysis/user_iterator.json', 'r')
    except FileNotFoundError:
        open('../../data/analysis/user_iterator.json', 'w')
    try:
        open('../../data/analysis/topic_iterator.json', 'r')
    except FileNotFoundError:
        open('../../data/analysis/topic_iterator.json', 'w')
    try:
        open('../../data/analysis/test_oriented.json', 'r')
    except FileNotFoundError:
        open('../../data/analysis/test_oriented.json', 'w')
    try:
        open('../../data/analysis/cpp_code.json', 'r')
    except FileNotFoundError:
        open('../../data/analysis/cpp_code.json', 'w')
    try:
        open('../../data/analysis/user_score.json', 'r')
    except FileNotFoundError:
        open('../../data/analysis/user_score.json', 'w')
    try:
        open('../../data/analysis/topic_difficulty.json', 'r')
    except FileNotFoundError:
        open('../../data/analysis/topic_difficulty.json', 'w')
    try:
        open('../../data/analysis/type_weight.json', 'r')
    except FileNotFoundError:
        open('../../data/analysis/type_weight.json', 'w')
    try:
        open('../../data/analysis/user_rank.json', 'r')
    except FileNotFoundError:
        open('../../data/analysis/user_rank.json', 'w')


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
    evaluate_exercises()
    print('Done!')


def code_analysis():
    print('Done!')


if __name__ == '__main__':
    initialize()
    # user_analysis()
    # topic_analysis()
    # code_analysis()
