import math
import re


def simple_difficulty_evaluation(content):
    distinct_operator = 0.0
    distinct_operands = 0.0
    total_operands = 0.0
    total_operators = 0.0
    # 标准答案阅读，得到指标
    dic_operator = {}
    dic_operand = {}
    dist = []
    content_of_the_file = content.replace('\n', ' ')
    the_file = content_of_the_file.split(' ')
    the_file = list(filter(None, the_file))
    if the_file is []:
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
                        # if ii != ',':
                        if ii not in dist:
                            dist = dist + [ii]
                            dic_operator.update({ii: 1})
                        else:
                            dic_operator[ii] = dic_operator[ii] + 1
                    elif not check_operand(current_token + ii) and current_token == '':
                        # if ii != ',':
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
        for k in dic_operator.values():
            total_operators = total_operators + k
        # 计算分值
        if distinct_operands != 0:
            difficulty = distinct_operator / 2 + total_operands / distinct_operands
        else:
            difficulty = 0.0
        if (distinct_operands + distinct_operator != 0):
            volume = (total_operators + total_operands) * math.log2(distinct_operator + distinct_operands)
        else:
            volume = 0
        if difficulty * volume != 0:
            effort = math.log2(difficulty * (volume ** 2))
        else:
            effort = 0
        return difficulty


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