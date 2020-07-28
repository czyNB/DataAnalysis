from src.function.iterator import *
import os


def format():
    it = getUIterator()
    count = 1
    while it.next():
        str = "../../data/source/用户分析/" + it.get_user() + '/' + it.get_type() + '/' + it.get_topic() + '/main.py'
        result = os.system("autopep8" + " --in-place " + '"' + str + '"')
        print(count, end=' ')
        count += 1
    print()
    print("Format Done!")


def GUI_format():
    os.system('autopep8 --in-place "../GUI/main.py"')
