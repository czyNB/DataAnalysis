import json
import urllib.request, urllib.parse
import os
import zipfile

f = open('../test_data.json', encoding='utf-8')  # 打开'data.json'的json文件
res = f.read()
data = json.loads(res)  # 加载json数据
# print(data)
# 取出json中第一个学生的cases数据
indexes = list(data)
# cases = data[indexes[0]]['cases']
# print(cases)
# 遍历做题信息
try:
    os.mkdir('../.data/题目分析')
except FileExistsError:
    pass
directory = "../.data/"
for index in indexes:
    cases = data[index]['cases']
    user_id = 'user_id_' + index
    for case in cases:
        case_id = case['case_id']
        case_type = case['case_type']
        case_zip_url = case['case_zip']
        final_score = case['final_score']
        print(case_id, case_type)
        name = urllib.parse.unquote(os.path.basename(case_zip_url))
        if "*" in name:
            name = name.replace("*", "_")
        try:
            os.mkdir(directory + case_type)
        except FileExistsError:
            pass
        try:
            os.mkdir(directory + case_type + '/' + name[:len(name) - 4])
        except FileExistsError:
            pass
        try:
            os.mkdir(directory + case_type + '/' + name[:len(name) - 4] + '/' + user_id)
        except FileExistsError:
            continue
        filename = directory + case_type + '/' + name[:len(name) - 4] + '/' + user_id + '/' + name
        print(filename)
        urllib.request.urlretrieve(case_zip_url, directory + case_type + '/' + name[:len(name) - 4] + '/' + user_id + '/' + name)  # 下载题目包到本地
        zf = zipfile.ZipFile(filename)
        try:
            zf.extractall(path=directory + case_type + '/' + name[:len(name) - 4] + '/' + user_id)
        except RuntimeError as e:
            print(e)
        zf.close()
        os.remove(filename)

directory = "../.data/用户分析/user_id_"
for index in indexes:
    cases = data[index]['cases']
    case_dir = directory + index
    try:
        os.mkdir(case_dir)
    except FileExistsError:
        pass
    for case in cases:
        print(case["case_id"], case["case_type"])
        case_type_dir = case_dir + "/" + case["case_type"]
        try:
            os.mkdir(case_type_dir)
        except FileExistsError:
            pass
        name = urllib.parse.unquote(os.path.basename(case["case_zip"]))  # 获取文件名，ur1里对中文会urlencode,解个码
        filename = case_type_dir + "/" + name
        if "*" in filename:
            filename = filename.replace("*", "_")
        print(filename)
        urllib.request.urlretrieve(case["case_zip"], filename)  # 下载题目包到本地
        zf = zipfile.ZipFile(filename)
        try:
            try:
                os.mkdir(filename[0:len(filename) - 4])
            except FileExistsError:
                pass
            zf.extractall(filename[0:len(filename) - 4])
        except RuntimeError as e:
            print(e)
        zf.close()
        os.remove(filename)
