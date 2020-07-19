"""
此文件根据资料中给出的标准答案的代码内容的困难程度
目的是根据同学们写书的代码的实际难度来为该题目所得分数加权，计算得每位同学的得分，而且此得分是与**代码难度**相关联的（而非单纯的**题目难度**）
因为那种题目巨难而解答代码简洁的代码，在解题书写代码过程中命名的影响力不那么大

计算得原本题目难度：最难79.21,最易2.00；按照0～80的比例放大到范围为1，均匀分布，以此为难度系数
"""

from decimal import Decimal
from src.function.iterator import *
from src.function.file_operations import *
import re
import os


def evaluate_exercises():
    count =  0
    it = getTIterator()
    content = {}
    while it.next():
        # print(it.get_type() + it.get_topic() + it.get_user() + ':', end="")
        score_in_difficulty = Decimal(evaluate_certain_exercise(it)).quantize(Decimal('0.00'))
        # if score_in_difficulty > biggest:
        #     biggest = score_in_difficulty
        # if score_in_difficulty < smallest and score_in_difficulty > 0:
        #     smallest = score_in_difficulty
        # print(score_in_difficulty)
        if it.get_type() + '/' + it.get_topic() not in content.keys():
            content.update({it.get_type() + '/' + it.get_topic(): str(score_in_difficulty) + ";" + str(
                (score_in_difficulty * Decimal(5.0) / Decimal(4.0) / Decimal(100)).quantize(Decimal('0.00')))})

        # content[it.get_type() + '/' + it.get_topic()][0] = score_in_difficulty * 5.0 / 4.0 / 100
        print(count)
        count += 1
    generate_json('../../data/analysis/topic_difficulty.json', content)


def evaluate_certain_exercise(it):
    # 这个方法计算每个题目的代码难度，根据给出的标准答案

    # 计算所需要的指标
    distinct_operator = 0.0
    distinct_operands = 0.0
    total_operands = 0.0

    # 标准答案阅读，得到指标
    dic_operator = {}
    dic_operand = {}
    dist = []
    content_of_the_file = it.answer()
    content_of_the_file = content_of_the_file.replace('\n', ' ')
    the_file = content_of_the_file.split(' ')
    the_file = list(filter(None, the_file))

    if the_file == []:
        return 0.0
    try:
        for i in the_file:
            if check_operand(i):
                if i in dist:
                    dic_operand[i] = dic_operand[i] + 1
                else:
                    dist = dist + [i]
                    dic_operand.update({i: 1})
            else:
                current_token = ''
                all_chars = list(i)
                for ii in all_chars:
                    if not check_operand(current_token + ii) and current_token != '':
                        if current_token not in dist:
                            dist = dist + [current_token]
                            dic_operand.update({current_token: 1})
                        else:
                            dic_operand[current_token] = dic_operand[current_token] + 1
                        current_token = ''
                        if ii != ',':
                            if ii not in dist:
                                dist = dist + [ii]
                                dic_operator.update({ii: 1})
                            else:
                                dic_operator[ii] = dic_operator[ii] + 1
                    elif not check_operand(current_token + ii) and current_token == '':
                        if ii != ',':
                            if ii not in dist:
                                dist = dist + [ii]
                                dic_operator.update({ii: 1})
                            else:
                                dic_operator[ii] = dic_operator[ii] + 1
                    else:
                        current_token = current_token + ii
    finally:
        distinct_operator = distinct_operator + len(dic_operator)
        distinct_operands = distinct_operands + len(dic_operand)
        for j in dic_operand.values():
            total_operands = total_operands + j

        # 计算分值
        return distinct_operator / 2 + total_operands / distinct_operands


def check_operator(the_char):
    the_set = ['+', '-', '*', '/', '%', '=', '!', '<', '>', '&', '|', '^', '~', '{', '}', '[', ']', '(', ')', '#', '$',
               '\\', '?', '\'', '"', ';', ':', '`', ' ', '\n', ',', '.']
    if the_char in the_set:
        return True


def check_operand(the_string):
    no_slash = the_string.split('_')
    the_str = "".join(no_slash)
    if len(the_str) == 1:
        if not the_str.isalpha() and not the_str.isdigit():
            return False
    if (re.match('^[a-zA-Z0-9]{0,}', the_str).span() != (0, len(the_str))):
        return False
    else:
        return True
