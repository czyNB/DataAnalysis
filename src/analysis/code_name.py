"""
此文件根据log中的命名标准对每个学生在命名方面的规范程度进行打分
"""

from src.function.iterator import *
from src.function.file_operations import *
import os


# 该方法提供评估所有用户的命名规范程度的接口
def format():
    it = getUIterator();
    while it.next():
        str = "../../data/source/用户分析/" + it.get_user() + '/' + it.get_type() + '/' + it.get_topic() + '/main.py'
        result = os.system("autopep8" + " --in-place " + '"' + str + '"')
        print(it.get_user())
    print("format_over")


def evaluate_users():
    # format()
    it = getUIterator()
    it.next()
    content = {}
    while it.now():
        score_in_codename = evaluate_user(it)
        if it.get_user() not in content.keys():
            content.update({it.get_user(): '%3f' % score_in_codename})
        else:
            break
    generate_json('../../data/analysis/code_name.json',content)


# 该方法提供单个用户的命名规范程度的接口
def evaluate_user(it):
    user = it.get_user()
    right_name = 0
    all_name = 0
    flag = True
    user_score=0
    while flag:
        all_name += int(get_all(it)[0])
        right_name += int(get_all(it)[1])
        if (it.next() and it.get_user() != user):
            flag = False
    print(all_name)
    print(right_name)
    print(user)
    if all_name!=0:
       user_score = right_name * 100 / all_name
    return user_score


# 该题全部命名数量,该题正确命名数量形成一个列表
def get_all(it):
    num_all = 0
    num_right = 0

    content_of_file = read_file('../../data/source/用户分析/' + it.get_user() + '/' + it.get_type()
                                + '/' + it.get_topic() + '/main.py')
    content_of_file = list(content_of_file.replace('\n', ' ').split())
    for element in content_of_file:
        if check_operator(element):
            num_all += 1
    for i in range(0, len(content_of_file)):
        if check_variable(content_of_file[i]):
            variable = content_of_file[i - 1]
            v_list = variable.split('_')
            for j in v_list:
                if not j.islower():
                    break
            num_right += 1
        elif check_func(content_of_file[i]):
            f = content_of_file[i + 1]
            f_list = f.split('_')
            for k in f_list:
                if not k.islower():
                    break
            num_right += 1
        elif check_module(content_of_file[i]):
            m = content_of_file[i + 1]
            if m.islower():
                num_right += 1
        elif check_class(content_of_file[i]):
            cl = content_of_file[i + 1]
            if not cl.isupper() and cl[0].isupper():
                num_right += 1

    return [num_all, num_right]


def check_operator(the_char):
    the_set = ['def', 'class', 'module', '=', '==', '!=', '+=', '-=']
    if the_char in the_set:
        return True


def check_variable(the_char):
    the_set = ['module', '=', '==', '!=', '+=', '-=']
    if the_char in the_set:
        return True
    return False


def check_class(the_char):
    if the_char == 'class':
        return True


def check_func(the_char):
    if the_char == 'def':
        return True


def check_module(the_char):
    if the_char == 'module':
        return True
