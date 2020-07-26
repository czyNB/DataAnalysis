# 代码操作的分析
import re
from src.function.iterator import *
from src.analysis.code_variable import *


def code_reuse(it: UIterator):
    result = {}
    current_user = it.get_user()
    while it.next():
        classification = classify(it)
    print('Code Reuse Done!')


def classify(it: UIterator) -> dict:
    variables = variable_list(it)
    while
        variables = sorted(variables, key=lambda x: len(x), reverse=True)
    funcs = func_list(it)
    classes = class_list(it)
    root = '../../data/source/用户分析/' + it.get_user() + '/' + it.get_type() + '/' + it.get_topic() + '/main.py'
    code = read_filelines(root)
    result = {
        'advanced': 0,
        'normal': 0,
    }
    code = clean(clean_variable(clean(clean_init(code)), variables))
    return result


def clean_init(code: []) -> []:
    i = 0
    while i < len(code):
        if code[i] == '':
            code.remove(code[i])
            i -= 1
        elif code[i].startswith('import') or code[i].startswith('def') or code[i].startswith('class') or code[
            i].startswith('#') or code[i].startswith('return'):
            code.remove(code[i])
            i -= 1
        elif code[i].find('=') != -1 and code[i][code[i].find('=') + 1] != '=' and code[i][
            code[i].find('=') - 1] != '!':
            code[i] = code[i][code[i].find('=') + 1:].strip()
        elif code[i].find('__main__') != -1:
            code.remove(code[i])
            i -= 1
        i += 1
    return code


def clean(code: []) -> []:
    i = 0
    while i < len(code):
        while code[i].endswith(':'):
            code[i] = code[i][:len(code[i]) - 1]
        while code[i].startswith('.'):
            code[i] = code[i][1:]
        i += 1
    return code


def clean_variable(code: [], variables: []) -> []:
    i = 0
    content = '\n'.join(code)
    for variable in variables:
        content = ''.join(content.split(variable))
    code = content.split('\n')
    return code


if __name__ == '__main__':
    code_reuse(getUIterator())
