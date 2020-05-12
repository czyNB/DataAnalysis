directory = "../.data/题目分析/查找算法/俄罗斯套娃信封问题_1580656269392/user_id_49823"
answer_file = open(directory + "/.mooctest/answer.py", "r")
text = answer_file.readlines()
words = []
for sentence in text:
    words += sentence.strip().split(" ")
