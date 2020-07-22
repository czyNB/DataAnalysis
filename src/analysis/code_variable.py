# 代码变量的分析
from src.function.file_operations import *
import re

#it为UIterator 返回代码中所有变量
def variable_list(it):
    v_list=[]
    content_of_file = read_file('../../data/source/用户分析/' + it.get_user() + '/' + it.get_type()
                                + '/' + it.get_topic() + '/main.py')
    content_of_file = list(content_of_file.replace('\n', ' ').split())
    for i in range(0, len(content_of_file)):
        if check_variable(content_of_file[i]):
            variable = content_of_file[i - 1]
            if check_others(variable):
                v_list.append(variable)
    return list(set(v_list))

# 返回所有类名
def class_list(it):
    c_list=[]
    content_of_file = read_file('../../data/source/用户分析/' + it.get_user() + '/' + it.get_type()
                                + '/' + it.get_topic() + '/main.py')
    content_of_file = list(content_of_file.replace('\n', ' ').split())
    for i in range(0, len(content_of_file)):
        if check_class(content_of_file[i]):
            variable = content_of_file[i + 1]
            variable = variable[0:-1]
            c_list.append(variable)
    return  c_list

# 返回所有函数名
def func_list(it):
    f_list = []
    content_of_file = read_file('../../data/source/用户分析/' + it.get_user() + '/' + it.get_type()
                                + '/' + it.get_topic() + '/main.py')
    content_of_file = list(content_of_file.replace('\n', ' ').split())
    for i in range(0, len(content_of_file)):
        if check_func(content_of_file[i]):
            variable = content_of_file[i + 1]
            pattern=".*?(?=\\()"
            variable=re.match(pattern,variable).group()
            f_list.append(variable)
    return  f_list


# 以下皆为上面返回列表所需方法


def check_variable(the_char):
    the_set = [ '=' ,'in']
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
    the_set = ['[',']','(',')']
    for element in the_set:
        if element in the_char:
            return False
    return True


