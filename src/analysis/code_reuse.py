# 代码操作的分析
import re
from src.function.iterator import *
from src.analysis.code_variable import *


def code_reuse(it: UIterator):
    result = {}
    count = 1
    while it.next():
        reuse_score = classify(it)
        if it.get_user() in list(result.keys()):
            pass
        else:
            result[it.get_user()] = {}
        if it.get_type() in list(result[it.get_user()].keys()):
            pass
        else:
            result[it.get_user()][it.get_type()] = {}
        result[it.get_user()][it.get_type()][it.get_topic()] = reuse_score
        print(count, end=' ')
        count += 1
    print()
    generate_json('../../data/analysis/code_reuse_detailed.json', result)
    for user in result.keys():
        s = 0
        l = 0
        for type in list(result[user].keys()):
            for topic in list(result[user][type].keys()):
                s += result[user][type][topic]
                l += 1
        if l > 50:
            result[user] = s / l * 100
        elif l > 20:
            result[user] = s / (l * 5) * 100
        else:
            result[user] = s / (l * 15) * 100
    result = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
    # highest = sorted(list(result.values()), reverse=True)[1]
    # for item in result.items():
    #     result[item[0]] = min(100, item[1] / highest * 100)
    generate_json('../../data/analysis/code_reuse.json', result)
    print('Code Reuse Done!')


def classify(it: UIterator) -> float:
    variables = variable_list1(it)
    variables = sorted(variables, key=lambda x: len(x))
    while len(variables) > 0 and len(variables[0]) == 1:
        variables = variables[1:]
        if len(variables) == 0:
            break
    variables = list(reversed(variables))
    funcs = func_list1(it)
    classes = class_list1(it)
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
        # print(it.get_user(), it.get_type(), it.get_topic())
        return 0
    result['normal'] = len((' '.join(code)).split(' '))
    del res, root
    return (result['class_num'] * 5 + result['my_func'] * 3.5 + result['func_num'] * 1.5) / (result['normal'] * 1.05)


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
