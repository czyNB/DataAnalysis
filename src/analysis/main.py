from src.download.download import *
from src.analysis.pre_processing import *
from src.function.iterator import *
from src.function.file_operations import *
import os


def initialize():
    try:
        os.mkdir('../../data')
        os.mkdir('../../data/analysis')
        os.mkdir('../../data/origin')
        os.mkdir('../../data/source')
    except FileExistsError:
        pass
    #
    topic_download()
    #
    user_download()
    #
    generate_topic_iterator()
    #
    generate_user_iterator()
    #
    check_topics()
    #
    check_users()
    #
    generate_topic_iterator()
    #
    generate_user_iterator()
    #
    check_effective_answer()
    #
    cpp_it = UIterator('../../data/analysis/cpp_code.json')
    #
    test_it = UIterator('../../data/analysis/test_oriented.json')
    #
    remove_invalid(cpp_it)
    #
    remove_invalid(test_it)
    #
    generate_topic_iterator()
    #
    generate_user_iterator()
    print("Done!")





