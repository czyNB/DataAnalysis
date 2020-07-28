import math
import re
from src.analysis.code_reuse import *
from src.analysis.code_initiation import *
from src.analysis.code_variable import *
from src.function.format import *


# def simple_difficulty_evaluation(content):
#     distinct_operator = 0.0
#     distinct_operands = 0.0
#     total_operands = 0.0
#     total_operators = 0.0
#     # 标准答案阅读，得到指标
#     dic_operator = {}
#     dic_operand = {}
#     dist = []
#     content_of_the_file = content.replace('\n', ' ')
#     the_file = content_of_the_file.split(' ')
#     the_file = list(filter(None, the_file))
#     if the_file is []:
#         return 0.0
#     try:
#         for i in the_file:
#             if check_operand(i):
#                 if i in dist:
#                     dic_operand[i] = dic_operand[i] + 1
#                 else:
#                     dist = dist + [i]
#                     dic_operand.update({i: 1})
#             else:
#                 current_token = ''
#                 all_chars = list(i)
#                 for ii in all_chars:
#                     if not check_operand(current_token + ii) and current_token != '':
#                         if current_token not in dist:
#                             dist = dist + [current_token]
#                             dic_operand.update({current_token: 1})
#                         else:
#                             dic_operand[current_token] = dic_operand[current_token] + 1
#                         current_token = ''
#                         # if ii != ',':
#                         if ii not in dist:
#                             dist = dist + [ii]
#                             dic_operator.update({ii: 1})
#                         else:
#                             dic_operator[ii] = dic_operator[ii] + 1
#                     elif not check_operand(current_token + ii) and current_token == '':
#                         # if ii != ',':
#                         if ii not in dist:
#                             dist = dist + [ii]
#                             dic_operator.update({ii: 1})
#                         else:
#                             dic_operator[ii] = dic_operator[ii] + 1
#                     else:
#                         current_token = current_token + ii
#     finally:
#         distinct_operator = distinct_operator + len(dic_operator)
#         distinct_operands = distinct_operands + len(dic_operand)
#         for j in dic_operand.values():
#             total_operands = total_operands + j
#         for k in dic_operator.values():
#             total_operators = total_operators + k
#         # 计算分值
#         if distinct_operands != 0:
#             difficulty = distinct_operator / 2 + total_operands / distinct_operands
#         else:
#             difficulty = 0.0
#         if (distinct_operands + distinct_operator != 0):
#             volume = (total_operators + total_operands) * math.log2(distinct_operator + distinct_operands)
#         else:
#             volume = 0
#         if difficulty * volume != 0:
#             effort = math.log2(difficulty * (volume ** 2))
#         else:
#             effort = 0
#         return difficulty
#
#
# def check_operator(the_char):
#     the_set = ['+', '-', '*', '/', '%', '=', '!', '<', '>', '&', '|', '^', '~', '{', '}', '[', ']', '(', ')', '#', '$',
#                '\\', '?', '\'', '"', ';', ':', '`', ' ', '\n', ',', '.']
#     if the_char in the_set:
#         return True
#
#
# def check_operand(the_string):
#     no_slash = the_string.split('_')
#     the_str = "".join(no_slash)
#     if len(the_str) == 1:
#         if not the_str.isalpha() and not the_str.isdigit():
#             return False
#     if (re.match('^[a-zA-Z0-9]{0,}', the_str).span() != (0, len(the_str))):
#         return False
#     else:
#         return True


def evaluation(content: str) -> {}:
    f = open('main.py', 'w')
    f.write(content)
    f.close()
    GUI_format()
    result = {'variable': get_variable_score(), 'reuse': get_reuse_score(), 'initiation': get_variable_score(), 'all': 0.0}
    result['all'] = result['variable'] * 0.4 + result['reuse'] * 0.4 + result['initiation'] * 0.2
    return result


def get_variable_score() -> float:
    f = open('main.py','r')
    content = f.read()
    return evaluate_one_file2(content)


def get_reuse_score() -> float:
    code = read_filelines('main.py')
    content = read_file('main.py')
    classes = class_list2(content)
    funcs = fun_list2(content)
    variables = variable_list2(content)
    variables = sorted(variables, key=lambda x: len(x))
    while len(variables) > 0 and len(variables[0]) == 1:
        variables = variables[1:]
        if len(variables) == 0:
            break
    variables = list(reversed(variables))
    result = {
        'class_num': 0,
        'func_num': 0,
        'my_func': 0,
        'normal': 0
    }
    try:
        code = clean(clean_init(code))
        res = clean_class(code, classes)
        result['class_num'] = res[1]
        code = clean(res[0])
        res = clean_func(code, funcs)
        result['func_num'] = res[1]
        result['my_func'] = res[2]
        code = clean(res[0])
        code = clean(clean_variable(code, variables))
    except IndexError:
        return 0
    result['normal'] = len((' '.join(code)).split(' '))
    del res
    return min(100, (result['class_num'] * 5 + result['my_func'] * 3.5 + result['func_num'] * 1.5) / (result['normal'] * 1.05) * 100)


def get_initiation_score() -> float:
    with open('main.py',
              'r', encoding='utf-8') as f:
        content = list(f)
    num_of_lines = 0.0
    num_of_initiation_blocks = 0
    appeared_variables = []
    whether_current_block = False
    for line in content:
        num_of_lines = num_of_lines + 1
        line = str(line).replace('==', '+')
        if '=' not in list(line) and whether_current_block == True:
            num_of_initiation_blocks = num_of_initiation_blocks + 1
            whether_current_block = False
        elif '=' in list(line):
            the_chars = list(line)
            is_start = True
            num_of_blanks = 0
            for i in the_chars:
                if i == ' ' and is_start:
                    num_of_blanks = num_of_blanks + 1
                elif i != ' ':
                    break
            for i in range(num_of_blanks):
                the_chars.pop(0)
            current_string = the_chars[0]
            for i in range(1, len(the_chars)):
                if not check_operand(current_string + the_chars[i]):
                    break
                else:
                    current_string = current_string + the_chars[i]
            if current_string not in appeared_variables and not check_special(current_string):
                whether_current_block = True
                appeared_variables = appeared_variables + [current_string]
            elif current_string in appeared_variables:
                if whether_current_block == True:
                    num_of_initiation_blocks = num_of_initiation_blocks + 1
                whether_current_block = False
            else:
                whether_current_block = False
    # print('../../data/source/用户分析/' + it.get_user() + '/' + it.get_type() + '/' + it.get_topic() + '/main.py')
    # print(num_of_lines, end=' ')
    # print(num_of_initiation_blocks, end=' ')
    if num_of_lines == 0.0:
        return None
    else:
        return 100.0 - (num_of_initiation_blocks / num_of_lines) * 200


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


def check_special(the_string):
    the_set = [
        '',
        'and',
        'as',
        'assert',
        'break',
        'class',
        'continue',
        'def',
        'elif',
        'else',
        'except',
        'finally',
        'for',
        'from',
        'if',
        'import',
        'in',
        'is',
        'lambda',
        'not',
        'or',
        'pass',
        'raise',
        'return',
        'try',
        'while',
        'with',
        'yield',
        'del',
        'global',
        'nonlocal',
        'True',
        'False',
        'None'
    ]
    if the_string in the_set:
        return True
    else:
        return False
