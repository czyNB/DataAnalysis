"""
本文件研究一篇代码变量初始化的混乱问题
"""
from decimal import Decimal

from src.analysis.pre_processing import generate_user_iterator
from src.function.iterator import *
from src.function.file_operations import *
from src.analysis.code_variable import *


def chaos_generator():
    code_variables_chaos = {}
    it = getUIterator()
    bigg = -1.0
    smal = 1.0
    while it.next():
        if it.get_user() not in code_variables_chaos.keys():
            code_variables_chaos[it.get_user()] = {}

        if it.get_type() not in code_variables_chaos[it.get_user()].keys():
            code_variables_chaos[it.get_user()][it.get_type()] = {}
        if it.get_topic() not in dict(code_variables_chaos[it.get_user()][it.get_type()]).keys():
            code_variables_chaos[it.get_user()][it.get_type()][it.get_topic()] = ''
        cur = chaos_each(it)
        print(cur)
        if cur != None:
            code_variables_chaos[it.get_user()][it.get_type()][it.get_topic()] = str((Decimal(100) - (Decimal(cur) * Decimal(200)).quantize(Decimal('0.0000'))))
        else:
            code_variables_chaos[it.get_user()][it.get_type()][it.get_topic()] = 'None'

        # if cur != None:
            # if cur > bigg:
            #     bigg = cur
            # if cur < smal:
            #     smal = cur
    # print(bigg)
    # print(smal)
    print(code_variables_chaos)
    generate_json('../../data/analysis/code_chaos.json', code_variables_chaos)



def chaos_each(it):
    with open('../../data/source/用户分析/' + it.get_user() + '/' + it.get_type() + '/' + it.get_topic() + '/main.py',
              'r') as f:
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
    print('../../data/source/用户分析/' + it.get_user() + '/' + it.get_type() + '/' + it.get_topic() + '/main.py')
    # print(num_of_lines, end=' ')
    # print(num_of_initiation_blocks, end=' ')
    if num_of_lines == 0.0:
        return None
    else:
        return num_of_initiation_blocks / num_of_lines

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


if __name__ == '__main__':
    # generate_user_iterator()
    chaos_generator()
