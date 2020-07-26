from src.function.iterator import *
from src.analysis.code_variable import *
from src.analysis.code_reuse import *
from src.analysis.code_initiation import *


def code_evaluation():
    variable_dict = evaluate_user_rmarks()
    reuse_dict = code_reuse(getUIterator())
    confusion_dict = chaos_generator()
    users = list(read_json('../../data/analysis/iterator_user.json').keys())
    result = {}
    for user in users:
        score = variable_dict[user] * 0.4 + reuse_dict[user] * 0.4 + confusion_dict[user] * 0.2
        result[user] = score
    generate_json('../../data/analysis/code_evaluation.json', result)
