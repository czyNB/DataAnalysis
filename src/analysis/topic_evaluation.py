"""
此文件根据资料中给出的标准答案的代码内容的困难程度
目的是根据同学们写书的代码的实际难度来为该题目所得分数加权，计算得每位同学的得分，而且此得分是与**代码难度**相关联的（而非单纯的**题目难度**）
因为那种题目巨难而解答代码简洁的代码，在解题书写代码过程中命名的影响力不那么大

生成文件：topic_difficulty.json：代码难度
        topic_volume.json：代码量
        topic_effort.json：对代码的解析、理解、书写所需精力投入的量化
"""

from decimal import Decimal
from src.function.iterator import *
from src.function.file_operations import *
import re
import math


def evaluate_exercises():
    count = 0
    it = getTIterator()
    content_difficulty = {}
    content_volume = {}
    content_effort = {}
    # biggestD = Decimal(-1.0)
    # smallestD = Decimal(9999999.99)
    # biggestV = Decimal(-1.0)
    # biggestE = Decimal(-1.0)
    # smallestV = Decimal(9999999.99)
    # smallestE = Decimal(9999999.99)
    # biggestD, biggestE, biggestV = -1.0, -1.0, -1.0
    # smallestD, smallestE, smallestV = 99999999.99, 99999999.99, 99999999.99
    while it.next():
        # print(it.get_type() + it.get_topic() + it.get_user() + ':')
        answer = evaluate_certain_exercise(it)
        if answer != 0:
            score_in_difficulty = Decimal(evaluate_certain_exercise(it)[0]).quantize(Decimal('0.00'))
            volume = Decimal(evaluate_certain_exercise(it)[1]).quantize(Decimal('0.00'))
            effort = Decimal(evaluate_certain_exercise(it)[2]).quantize(Decimal('0.00'))
            # print(it.get_user())
            # print(it.get_topic())
            # print(it.get_type())
            # answer = evaluate_certain_exercise(it)
            # print(answer)
            # score_in_difficulty = answer[0]
            # volume = answer[1]
            # effort = answer[2]
            # if score_in_difficulty > biggestD:
            #     biggestD = score_in_difficulty
            # if score_in_difficulty < smallestD and score_in_difficulty > 0:
            #     smallestD = score_in_difficulty
            # if effort > biggestE:
            #     biggestE = effort
            # if effort < smallestE and effort > 0:
            #     smallestE = effort
            # if volume > biggestV:
            #     biggestV = volume
            # if volume < smallestV and volume > 0:
            #     smallestV = volume
            # print('Difficulty: ',end='')
            # print(smallestD,end=' ')
            # print(biggestD)
            # print('Volume: ',end='')
            # print(smallestV,end=' ')
            # print(biggestV)
            # print('Effort: ', end='')
            # print(smallestE, end=' ')
            # print(biggestE)
            if it.get_type() not in content_difficulty.keys():
                content_difficulty[it.get_type()] = {}
            if it.get_type() not in content_volume.keys():
                content_volume[it.get_type()] = {}
            if it.get_type() not in content_effort.keys():
                content_effort[it.get_type()] = {}
            if it.get_topic() not in content_difficulty.keys():
                # content.update({it.get_type() + '/' + it.get_topic(): str(score_in_difficulty) + ";" + str(
                #     (score_in_difficulty * Decimal(5.0) / Decimal(4.0) / Decimal(100)).quantize(Decimal('0.00')))})
                content_difficulty[it.get_type()].update({it.get_topic(): str(score_in_difficulty)})
            if it.get_topic() not in content_volume.keys():
                content_volume[it.get_type()].update({it.get_topic(): str(volume)})
            if it.get_topic() not in content_effort.keys():
                content_effort[it.get_type()].update({it.get_topic(): str(effort)})
            # content[it.get_type() + '/' + it.get_topic()][0] = score_in_difficulty * 5.0 / 4.0 / 100
            print(count)
            count += 1
    generate_json('../../data/analysis/topic_difficulty.json', content_difficulty)
    generate_json('../../data/analysis/topic_volume.json', content_volume)
    generate_json('../../data/analysis/topic_effort.json', content_effort)
    print('Topic Difficulty:')
    calculate_the_average('../../data/analysis/topic_difficulty.json')
    print('Topic Volume:')
    calculate_the_average('../../data/analysis/topic_volume.json')
    print('Topic Effort:')
    calculate_the_average('../../data/analysis/topic_effort.json')


def evaluate_certain_exercise(it):
    # 这个方法计算每个题目的代码难度，根据给出的标准答案

    # 计算所需要的指标
    distinct_operator = 0.0
    distinct_operands = 0.0
    total_operands = 0.0
    total_operators = 0.0

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
        difficulty = distinct_operator / 2 + total_operands / distinct_operands
        volume = (total_operators + total_operands) * math.log2(distinct_operator + distinct_operands)
        effort = math.log2(difficulty * (volume ** 2))
        return [difficulty, volume, effort]


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


def calculate_the_average(root):
    total = 0.0
    count = 0
    f = read_json(root)
    for i in f["数字操作"]:
        total = total + float(f["数字操作"][i])
        count = count + 1
    print("数字操作:", end='')
    print(total / count)
    total = 0.0
    count = 0
    for j in f["查找算法"]:
        total = total + float(f["查找算法"][j])
        count = count + 1
    print("查找算法:", end='')
    print(total / count)
    total = 0.0
    count = 0
    for k in f['字符串']:
        total = total + float(f["字符串"][k])
        count = count + 1
    print("字符串:", end='')
    print(total / count)
    total = 0.0
    count = 0
    for l in f["线性表"]:
        total = total + float(f["线性表"][l])
        count = count + 1
    print("线性表:", end='')
    print(total / count)
    total = 0.0
    count = 0
    for m in f['数组']:
        total = total + float(f["数组"][m])
        count = count + 1
    print("数组:", end='')
    print(total / count)
    total = 0.0
    count = 0
    for n in f['树结构']:
        total = total + float(f["树结构"][n])
        count = count + 1
    print("树结构:", end='')
    print(total / count)
    total = 0.0
    count = 0
    for o in f['排序算法']:
        total = total + float(f["排序算法"][o])
        count = count + 1
    print("排序算法:", end='')
    print(total / count)
    total = 0.0
    count = 0
    for p in f['图结构']:
        total = total + float(f["图结构"][p])
        count = count + 1
    print("图结构:", end='')
    print(total / count)