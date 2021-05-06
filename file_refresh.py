import os


def new_report(test_report):
    lists = os.listdir(test_report)                                     # 列出目录的下所有文件和文件夹保存到lists
    lists.sort(key=lambda fn: os.path.getmtime(test_report + "\\" + fn))  # 按时间排序
    file_new = os.path.join(test_report, lists[-1])                      # 获取最新的文件保存到file_new
    file_new = file_new.replace('\\', '/')
    return file_new
