# 代码操作的分析
import re
from src.function.iterator import *
from src.analysis.code_variable import *


def code_reuse(it: UIterator):
    result = {}
    while it.next():
        reuse_score = classify(it)
        if it.get_user() in result:
            result[it.get_user()].append(reuse_score)
        else:
            result[it.get_user()] = [reuse_score]
    for item in result.items():
        result[item[0]] = sum(item[1]) / len(item[1])
    generate_json('code_reuse.json', result)
    print('Code Reuse Done!')


def classify(it: UIterator) -> float:
    variables = variable_list(it)
    variables = sorted(variables, key=lambda x: len(x))
    while len(variables) > 0 and len(variables[0]) == 1:
        variables = variables[1:]
        if len(variables) == 0:
            break
    variables = list(reversed(variables))
    funcs = func_list(it)
    classes = class_list(it)
    root = '../../data/source/用户分析/' + it.get_user() + '/' + it.get_type() + '/' + it.get_topic() + '/main.py'
    code = read_filelines(root)
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
        print(it.get_user(),it.get_type(),it.get_topic())
        return 0
    result['normal'] = len((' '.join(code)).split(' '))
    del res, root
    return (result['class_num'] * 5 + result['my_func'] * 2 + result['func_num'] * 2) / result['normal']


def clean_init(code: []) -> []:
    code = '\n'.join(code).split('\'\'\'')
    i = 0
    j = 0
    while i < len(code):
        if i % 2 != j % 2:
            code.remove(code[i])
            i -= 1
            j += 1
        i += 1
    code = ''.join(code).split('\n')
    i = 0
    while i < len(code):
        if code[i].find('#') != -1:
            code[i] = code[i][:code[i].find('#')]
        if code[i].startswith('import') or code[i].startswith('def') or code[i].startswith('class'):
            code.remove(code[i])
            i -= 1
        if code[i].find('=') != -1 and code[i][code[i].find('=') - 1] == ' ' and code[i][code[i].find('=') + 1] == ' ':
            code[i] = code[i][code[i].find('=') + 1:].strip()
        if code[i].find('__main__') != -1:
            code.remove(code[i])
            i -= 1
        if code[i].startswith('return'):
            code[i] = ' '.join(code[i].split(' ')[1:])
        i += 1
    return code


def clean(code: []) -> []:
    i = 0
    while i < len(code):
        if code[i] == '':
            code.remove(code[i])
            i -= 1
        while code[i].endswith(':'):
            code[i] = ''.join(code[i].split(':'))
        while code[i].startswith('.'):
            code[i] = ''.join(code[i].split('.'))
        while code[i].find(',') != -1:
            code[i] = ''.join(code[i].split(','))
        i += 1
    return code


def clean_variable(code: [], variables: []) -> []:
    content = '\n'.join(code)
    for variable in variables:
        content = ''.join(content.split(variable))
    code = content.split('\n')
    return code


def clean_func(code: [], funcs: []) -> []:
    funcs_num = len(re.findall('[a-zA-z]\(', '\n'.join(code)))
    my_func_num = 0
    content = '\n'.join(code)
    for func in funcs:
        content = re.split(func + r'[(](.*?)[)]', content)
        my_func_num += int((len(content) - 1) / 2)
        content = ''.join(content)
    code = content.split('\n')
    return [code, funcs_num, my_func_num]


def clean_class(code: [], classes: []) -> []:
    content = '\n'.join(code)
    class_num = 0
    for class_ in classes:
        class_ = class_[:len(class_) - 1]
        content = re.split(class_ + r'[(](.*?)[)]', content)
        class_num += int((len(content) - 1) / 2)
        content = ''.join(content)
    code = content.split('\n')
    return [code, class_num]


if __name__ == '__main__':
    code = read_filelines('../../data/source/用户分析/user_id_60747/排序算法/餐厅过滤器_1580557412562/main.py')
    clean(clean_init(code))

