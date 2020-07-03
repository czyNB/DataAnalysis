import shutil
from src.function.iterator import *


def remove_invalid(it):
    count = 0
    while it.next():
        src_1 = '../../data/source/用户分析/' + it.get_user() + '/' + it.get_type() + '/' + it.get_topic()
        dst_1 = '../../data/source/无效代码/用户分析/' + it.get_user() + '/' + it.get_type() + '/' + it.get_topic()
        src_2 = '../../data/source/题目分析/' + it.get_type() + '/' + it.get_topic() + '/' + it.get_user()
        dst_2 = '../../data/source/无效代码/题目分析/' + it.get_type() + '/' + it.get_topic() + '/' + it.get_user()
        try:
            shutil.move(src_1, dst_1)
            shutil.move(src_2, dst_2)
            print(count)
            count += 1
        except FileNotFoundError:
            continue


if __name__ == '__main__':
    cpp_it = UIterator('../../data/analysis/cpp_code.json')
    test_it = UIterator('../../data/analysis/test_oriented.json')
    remove_invalid(cpp_it)
    remove_invalid(test_it)
