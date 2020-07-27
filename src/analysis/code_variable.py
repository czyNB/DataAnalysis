# 代码变量的分析
"""
此文件根据log中的命名标准对每个学生在命名方面的规范程度进行打分
"""
from src.function.file_operations import *
from src.function.iterator import *
import os
import enchant
import re


def variable_list(it: UIterator) -> list:
    v_list = []
    content_of_file = read_file('../../data/source/用户分析/' + it.get_user() + '/' + it.get_type()
                                + '/' + it.get_topic() + '/main.py')
    content_of_file = list(content_of_file.replace('\n', ' ').split())
    for i in range(0, len(content_of_file)):
        if check_variable(content_of_file[i]):
            variable = content_of_file[i - 1]
            if check_others(variable):
                v_list.append(variable)
        elif check_func(content_of_file[i]):
            func_v = content_of_file[i + 1]
            flag = True
            j = 2
            while flag:
                letter = content_of_file[i + j]
                func_v += letter
                j += 1
                if ')' in letter:
                    flag = False
            func_v_list = re.findall(r'[(](.*?)[)]', func_v)
            if len(func_v_list) > 0 and '' not in func_v_list:
                for element in func_v_list:
                    if element != 'self':
                        e_list = element.split(',')
                        for j in range(0, len(e_list)):
                            if ':' in e_list[j]:
                                e_list[j] = e_list[j].split(':')[0]
                            elif '=' in e_list[j]:
                                e_list[j] = e_list[j].split('=')[0]
                            elif '(' in e_list[j]:
                                e_list[j] += ')'
                            elif '+' in e_list[j]:
                                e_list[j] = e_list[j].split('+')[0]
                        v_list.extend(e_list)
    return list(set(v_list))


# 返回所有类名
def class_list(it: UIterator) -> list:
    c_list = []
    content_of_file = read_file('../../data/source/用户分析/' + it.get_user() + '/' + it.get_type()
                                + '/' + it.get_topic() + '/main.py')
    content_of_file = list(content_of_file.replace('\n', ' ').split())
    for i in range(0, len(content_of_file)):
        if check_class(content_of_file[i]):
            variable = content_of_file[i + 1]
            c_list.append(variable)
    return c_list


# 返回所有函数名
def func_list(it: UIterator) -> list:
    f_list = []
    content_of_file = read_file('../../data/source/用户分析/' + it.get_user() + '/' + it.get_type()
                                + '/' + it.get_topic() + '/main.py')
    content_of_file = list(content_of_file.replace('\n', ' ').split())
    for i in range(0, len(content_of_file)):
        if check_func(content_of_file[i]):
            variable = content_of_file[i + 1]
            pattern = ".*?(?=\\()"
            variable = re.match(pattern, variable).group()
            f_list.append(variable)
    return f_list


# 以下皆为上面返回列表所需方法


def check_variable(the_char):
    the_set = ['=', 'in']
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


def check_others(the_char):
    the_set = ['[', ']', '(', ')']
    for element in the_set:
        if element in the_char:
            return False
    if check_int(the_char):
        return False
    if the_char == 'i' or the_char == 'j' or the_char == 'k':
        return False
    return True


def check_int(the_char):
    try:
        num = int(the_char)
        return True
    except ValueError:
        return False


# 该方法提供评估所有用户的命名规范程度的接口
# def format():
#     it = getUIterator()
#     count = 1
#     while it.next():
#         str = "../../data/source/用户分析/" + it.get_user() + '/' + it.get_type() + '/' + it.get_topic() + '/main.py'
#         result = os.system("autopep8" + " --in-place " + '"' + str + '"')
#         print(count, end=' ')
#         count += 1
#     print()
#     print("Format Done!")


def evaluate_user_rmarks():
    # format()
    it = getUIterator()
    it.next()
    content = {}
    count = 1
    while it.now():
        score_in_codename = evaluate_one(it)
        if it.get_user() not in content.keys():
            content.update({it.get_user(): score_in_codename})
        else:
            break
        print(count, end=' ')
        count += 1
    print()
    generate_json('../../data/analysis/code_variable.json', content)
    print('Code Variable Done!')


# 该方法提供单个用户的命名规范程度的接口
def evaluate_one(it):
    user = it.get_user()
    right_name = 0
    all_name = 0
    flag = True
    user_score = 0
    while flag:
        all_name += len(variable_list(it))
        right_name += len(check_reasonable(variable_list(it)))
        if it.next() and it.get_user() != user:
            flag = False
    if all_name != 0:
        user_score = right_name * 100 / all_name
    return user_score


# 该题全部命名数量,该题正确命名数量形成一个列表
def check_operator(the_char):
    the_set = ['def', 'class', 'module', '=', '==', '!=', '+=', '-=']
    if the_char in the_set:
        return True


def check_reasonable(variables: list) -> list:
    check = enchant.Dict("en_US")
    b_list = []
    if len(variables) > 0:
        for element in variables:
            e_list = list(element.split('_'))
            for letter in e_list:
                if letter != '':
                    if check.check(letter):
                        b_list.append(True)
                        break
    return b_list
