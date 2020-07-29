from decimal import Decimal
from src.function.iterator import *
from src.function.file_operations import *
import math
import re


def topic_eval_generator():
    content_difficulty = {}
    content_volume = {}
    content_effort = {}
    it = getTIterator()
    count = 0.0
    counter = 0.0
    curr = ""
    is_start = True
    biggest = Decimal(-1.0)
    smallest = Decimal(99999.99)
    mark = 1
    while it.next():
        current = it.get_type() + '/' + it.get_topic() + '/'
        answer = topic_eval(it)
        if answer != 0:
            if not is_start:
                if curr != current:
                    if counter != 0.0:
                        last_answer = Decimal(count / counter).quantize(Decimal('0.00'))
                    else:
                        last_answer = ""
                    count = answer[0]
                    counter = 1.0
                    former = curr.split('/')
                    curr = current
                    if former[0] not in content_difficulty.keys():
                        content_difficulty[former[0]] = {}
                    if former[1] not in content_difficulty.keys():
                        if last_answer > biggest:
                            biggest = last_answer
                        if last_answer < smallest:
                            smallest = last_answer
                        content_difficulty[former[0]].update(
                            {former[1]: str(last_answer * Decimal(4.0) / Decimal(100.0))})
                else:
                    count = count + answer[0]
                    counter = counter + 1
            else:
                count = answer[0]
                counter = 0.0
                curr = current
                is_start = False
        print(mark, end=' ')
        mark += 1
    print()
    generate_json('../../data/analysis/topic_difficulty.json', content_difficulty)
    print('Topic Evaluation Done!')


def topic_eval(it: TIterator):
    # 计算所需要的指标
    distinct_operator = 0.0
    distinct_operands = 0.0
    total_operands = 0.0
    total_operators = 0.0
    # 标准答案阅读，得到指标
    dic_operator = {}
    dic_operand = {}
    dist = []
    content_of_the_file = it.answer_by_user()
    content_of_the_file = content_of_the_file.replace('\n', ' ')
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
