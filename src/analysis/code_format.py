"""
此文件根据log中的命名标准对每个学生在命名方面的规范程度进行打分
"""

from src.function.iterator import *
from src.function.file_operations import *
from src.analysis.code_variable import *
import os
import enchant



# 该方法提供评估所有用户的命名规范程度的接口
def format():
    it = getUIterator()
    while it.next():
        str = "../../data/source/用户分析/" + it.get_user() + '/' + it.get_type() + '/' + it.get_topic() + '/main.py'
        result = os.system("autopep8" + " --in-place " + '"' + str + '"')
        print(it.get_user())
    print("format_over")


def evaluate_user_rmarks():
    # format()
    it = getUIterator()
    it.next()
    content = {}
    while it.now():
        score_in_codename = evaluate_one(it)
        if it.get_user() not in content.keys():
            content.update({it.get_user(): '%3f' % score_in_codename})
        else:
            break
    # generate_json('../../data/analysis/code_format.json', content)
    print(content)
    return content


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
        if (it.next() and it.get_user() != user):
            flag = False
    # print(all_name)
    # print(right_name)
    # print(user)
    if all_name != 0:
        user_score = right_name * 100 / all_name
    print(str(user)+' '+str(user_score))
    return user_score


# 该题全部命名数量,该题正确命名数量形成一个列表

def check_operator(the_char):
    the_set = ['def', 'class', 'module', '=', '==', '!=', '+=', '-=']
    if the_char in the_set:
        return True

def check_reasonable(variables: list) ->list:
    check = enchant.Dict("en_US")
    b_list=[]
    if len(variables)>0:
        for element in variables:
            e_list=list(element.split('_'))
            for letter in e_list:
                if letter!='':
                    if check.check(letter):
                        b_list.append(True)
                        break
    return  b_list













