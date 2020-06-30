import json
import urllib.request, urllib.parse
import os
import zipfile

f = open('../../data/origin/test_data.json', encoding='utf-8')  # 打开'test_data.json'的json文件
res = f.read()
data = json.loads(res)  # 加载json数据
indexes = list(data)
'''cases = data[indexes[0]]['cases'] 
# print(cases)'''  # 取出json中第一个学生的cases数据
# 遍历做题信息
try:
    os.mkdir('../../data/source/用户分析')
except FileExistsError:
    pass
directory = "../../data/source/用户分析/"
for index in indexes:
    cases = data[index]['cases']
    user_id = 'user_id_' + index
    for case in cases:
        case_id = case['case_id']
        case_type = case['case_type']
        final_score = case['final_score']
        upload_records = sorted(case["upload_records"], key=lambda x: x["score"], reverse=True)
        try:
            upload_record = upload_records[0]
        except IndexError:
            continue
        upload_id = upload_record["upload_id"]
        upload_time = upload_record["upload_time"]
        code_url = upload_record["code_url"]
        name = urllib.parse.unquote(os.path.basename(case["case_zip"]))  # 获取文件名，ur1里对中文会urlencode,解个码

        print(case_id, case_type)
        if "*" in name:
            name = name.replace("*", "_")
        try:
            os.mkdir(directory + user_id)
        except FileExistsError:
            pass
        try:
            os.mkdir(directory + user_id + '/' + case_type)
        except FileExistsError:
            pass
        try:
            os.mkdir(directory + user_id + '/' + case_type + '/' + name[:len(name) - 4])
        except FileExistsError:
            if not os.listdir(directory + user_id + '/' + case_type + '/' + name[:len(name) - 4]):
                pass
            else:
                continue

        filename = directory + user_id + '/' + case_type + '/' + name[:len(name) - 4] + '/' + name
        print(filename)
        urllib.request.urlretrieve(code_url, filename)  # 下载题目包到本地

        zf_1 = zipfile.ZipFile(filename)
        try:
            zf_1.extractall(path=directory + user_id + '/' + case_type + '/' + name[:len(name) - 4])
        except RuntimeError as e:
            print(e)
        zf_1.close()
        os.remove(filename)

        filename = directory + user_id + '/' + case_type + '/' + name[:len(name) - 4] + '/' + \
                   os.listdir(directory + user_id + '/' + case_type + '/' + name[:len(name) - 4])[0]
        zf_2 = zipfile.ZipFile(filename)
        try:
            zf_2.extractall(path=directory + user_id + '/' + case_type + '/' + name[:len(name) - 4])
        except RuntimeError as e:
            print(e)
        zf_2.close()
        os.remove(filename)
