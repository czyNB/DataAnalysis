from src.function.iterator import *
from src.analysis.code_variable import *
from src.analysis.code_reuse import *
from src.analysis.code_initiation import *


def code_evaluation():
    # evaluate_user_rmarks()
    # code_reuse(getUIterator())
    # chaos_generator()
    # evaluate_user_detailed()
    variable_dict = read_json('../../data/analysis/code_variable.json')
    reuse_dict = read_json('../../data/analysis/code_reuse.json')
    confusion_dict = read_json('../../data/analysis/code_chaos.json')
    users = list(read_json('../../data/analysis/iterator_user.json').keys())
    result = {}
    for user in users:
        score = variable_dict[user] * 0.35 + reuse_dict[user] * 0.55 + confusion_dict[user] * 0.1
        result[user] = score
    result = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
    generate_json('../../data/analysis/code_evaluation.json', result)
