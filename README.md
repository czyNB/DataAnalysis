# DataAnalysis
> 大二下数据科学基础大作业
>
> czyNB



## 项目结构

* 根目录
  * 源文件
    * 下载文件：用于通过原始数据将具体数据下载到源数据中
    * 分析文件：用于分析源数据并将分析结果放到分析数据中
    * 产品文件：用于整合分析结果制作代码分析工具
    * 功能文件：用于开发辅助功能简化分析过程
  * 数据
    * 原始数据
    * 源数据
    * 分析数据
  * 日志
    * 会议记录
    * 日程表
    * 问题交流



## 注意事项

* clone之后的初始流程：
  * 确认项目结构所有的文件夹都已经存在（data文件夹不算在git库中）
  * 用Pycharm打开项目，打开项目设置。Pycharm中项目结构要将data文件夹设置为excluded，否则每次扫描代码要花很久的时间
  * 依次运行topic_download.py、user_download.py、iterator.py、file_checker.py，删除下载失败的文件夹，重新运行iterator.py

* 导入到json文件的代码段

  ```python
  json_data = json.dumps(result, indent=4, separators=(',', ': '), ensure_ascii=False)
  f = open('../../data/analysis/cppCode.json', 'w', encoding='utf-8')
  f.write(json_data)
  f.close()
  ```