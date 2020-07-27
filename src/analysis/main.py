import sys
sys.path.append('C:/南大软院/DataAnalysis')
from src.analysis import user_score
from src.analysis.pre_processing import *
from src.analysis.code_evaluation import *
from src.analysis.topic_evaluation import *
from src.analysis.topic_sequence import *
from src.analysis.user_score import *


def initialize():
    print('Initialize Start!')
    generate_dir()
    generate_file()
    code_format()
    print("Initialize Done!")


def user_analysis():
    print('User Analysis Start!')
    # 生成数据
    user_score.data = read_json('../../data/origin/test_data.json')
    user_score.cpp_it = UIterator('../../data/analysis/pre_cpp.json')
    user_score.test_it = UIterator('../../data/analysis/pre_test.json')
    Evaluation.test_codes = read_json('../../data/analysis/pre_test.json')
    Evaluation.cpp_codes = read_json('../../data/analysis/pre_cpp.json')
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
    print('User Analysis Done!')


def topic_analysis():
    print('Topic Analysis Start!')
    topic_eval_generator()
    sort_topics_by_difficulty()
    print('Topic Analysis Done!')


def code_analysis():
    print('Code Analysis Start!')
    code_evaluation()
    print('Code Analysis Done!')


def get_data():
    print('Data Start!')
    # initialize()
    # user_analysis()
    # topic_analysis()
    code_analysis()
    print('Data Done!')


if __name__ == '__main__':
    get_data()
    print('All Done!')
