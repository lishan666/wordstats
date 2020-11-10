#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# function 自动统计英语单词词频，带翻译
import re
import os
import time
import json
import urllib.request
import urllib.parse
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QFileDialog, QMessageBox
from matplotlib import pyplot as plt

file_library = "./file_library_txt"
txt_file_name = 'combine.txt'
result_file_name = 'result.txt'
cwd = os.getcwd()


def translate(content):
    """
    功能：有道词典翻译
        content:要翻译的内容，可以是单词，可以是中文
    """
    # 翻译地址
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    data = {'i': content, 'doctype': 'json'}
    data = urllib.parse.urlencode(data).encode('utf-8')
    response = urllib.request.urlopen(url, data)
    html = response.read().decode('utf-8')
    target = json.loads(html)
    # 返回第一个翻译结果
    result = (target['translateResult'][0][0]['tgt'])
    return result


def find_txt(folder, files):
    """
    功能：寻找指定文件夹下的所有txt文档路径
        folder:指定文件夹
        files:保存找到的txt文件路径的列表
    """
    file_list = os.listdir(folder)
    for filename in file_list:
        de_path = os.path.join(folder, filename)
        if os.path.isfile(de_path):
            if de_path.endswith(".txt"):
                files.append(de_path)
        else:
            find_txt(de_path, files)


def creat_time_folder(root_path):
    """
   功能：在指定文件路径下，新建一个以时间命名的文件夹
       root_path:指定文件夹路径
       path:返回的最终路径
   """
    # 获取当前时间
    now = time.strftime("%Y-%m-%d_%H-%M", time.localtime(time.time()))
    # 生成统计结果保存的文件名
    path = root_path + now + '/'
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)
    return path


class WordStats:
    def __init__(self, folder, combine, result):
        """
        功能：初始化实例对象
            folder:要统计的文件夹
            combine:合成txt文件名
            result:返回统计结果txt文件名
        """
        self.path = cwd + "/result/"
        self.folder = folder
        self.combine = combine
        self.result = result
        self.files = []
        self.content = " "
        self.ui = QUiLoader().load(cwd + "./ui/stats.ui")
        self.ui.button_stats_file.clicked.connect(self.button_stats_file_handle_calc)
        self.ui.button_stats_para.clicked.connect(self.button_stats_para_handle_calc)
        self.ui.button_loadfolder.clicked.connect(self.button_load_folder_handle_calc)

    def button_stats_para_handle_calc(self):
        self.ui.progressBar.setRange(0, 5)
        path = creat_time_folder(self.path)
        self.path = path
        self.combine = path + txt_file_name
        self.result = path + result_file_name
        self.ui.progressBar.setValue(0)
        content = self.ui.plainTextEdit.toPlainText()
        self.content = content.lower()
        self.ui.progressBar.setValue(1)
        WordStats.stat_freq(self)
        self.ui.textBrowser_result.clear()
        WordStats.preview_result(self)
        self.ui.progressBar.setValue(5)
        QMessageBox.about(self.ui,
                          '统计结束', '前往result目录查看详细结果')

    def button_stats_file_handle_calc(self):
        self.ui.progressBar.setRange(0, 5)
        path = creat_time_folder(self.path)
        self.path = path
        self.combine = path + txt_file_name
        self.result = path + result_file_name
        self.ui.progressBar.setValue(0)
        WordStats.combine_txt(self)
        self.content = WordStats.gettext(self.combine)
        self.ui.progressBar.setValue(1)
        WordStats.stat_freq(self)
        self.ui.textBrowser_result.clear()
        WordStats.preview_result(self)
        self.ui.progressBar.setValue(5)
        QMessageBox.about(self.ui,
                          '统计结束', '前往result目录查看详细结果')

    def button_load_folder_handle_calc(self):
        files = []
        folder = QFileDialog.getExistingDirectory(self.ui, "选择统计文件夹")
        find_txt(folder, files)
        self.folder = folder
        self.files = files
        self.ui.textBrowser.clear()
        for file in files:
            self.ui.textBrowser.append(file)
            self.ui.textBrowser.ensureCursorVisible()

    def preview_result(self):
        result = self.result
        f = open(result, 'r', encoding="utf-8")
        for i in range(13):
            line = f.readline()
            self.ui.textBrowser_result.append(line)
            self.ui.textBrowser_result.ensureCursorVisible()

    def combine_txt(self):
        """
        功能：合并指定文件夹下的所有txt文件
            files:要合并的文件路径列表
            combine_file_name:合并后的txt文件名
        """
        files = self.files
        combine_file_name = self.combine
        # 打开当前目录下的result.txt文件，如果没有则创建
        f = open(combine_file_name, 'w', encoding='utf-8')
        for filepath in files:
            # 遍历单个txt文件，读取行数
            for line in open(filepath, 'r', encoding='utf-8'):
                f.writelines(line)
                f.write('\n')
        # 关闭文件
        f.close()

    @staticmethod
    def gettext(file_name):
        """
            功能：获取txt文件内容,并将英语单词全部转换为小写字母
            file_name:txt文件名
        """
        f = open(file_name, "r", errors='ignore', encoding='utf-8')
        txt = f.read().lower()
        f.close()
        return txt

    def stat_freq(self, min_len=2, max_len=20):
        """
        功能：统计txt文件中英文单词出现频率
            content:要统计的内容
            result_name：统计结果保存txt文件名
            min_len:单词最小长度，默认值2
            max_len:单词最大长度，默认值20
        """
        result_name = self.result
        save_path = self.path
        content = self.content
        words = re.split(r'[^A-Za-z\'\-]+', content)
        new_words = []
        for word in words:
            word_len = len(word)
            if (word_len >= min_len) and (word_len <= max_len):
                new_words.append(word)
        total_word = len(new_words)
        counts = {}
        for word in new_words:
            counts[word] = counts.get(word, 0) + 1
        items = list(counts.items())
        items.sort(key=lambda w: w[1], reverse=True)
        self.ui.progressBar.setValue(2)
        f = open(result_name, 'w', encoding='utf-8')
        f.writelines("{0:<6}\t{1:<20}\t{2:<20}\t{3:<6}\t{4:<5}\t{5:>5}".format
                     ("No",
                      "Word",
                      "Translate",
                      "Count",
                      "Freq",
                      "Cum_Freq"))
        f.write('\n')
        f.writelines("{0:<6}\t{1:<20}\t{2:<20}\t{3:<6}\t{4:<5}\t{5:>5}".format
                     (len(items),
                      "all_word",
                      "翻译",
                      total_word,
                      "100%",
                      "100%"))
        f.write('\n')
        f.writelines(
            "___________________________________________________"
            "___________________________________________________")
        f.write('\n')
        # 单词出现次数列表
        cnt = []
        # 单词累计出现次数列表
        cum_cnt = []
        # 单词累计出现次数
        cum_count = 0
        # 单词累计频率列表
        cum_fre = []
        for i in range(len(items)):
            word, count = items[i]
            cum_count = cum_count + count
            freq = count / total_word
            cum_freq = cum_count / total_word
            f.writelines("{0:<6}\t{1:<20}\t{2:<20}\t{3:<6}\t{4:.4%}\t{5:.4%}".format
                         (i + 1,
                          word,
                          # translate(word),  # 此语句可以对英语单词进行翻译
                          " ",                # 此语句不进行翻译，翻译部分显示为空
                          count,
                          freq,
                          cum_freq))
            f.write('\n')
            cnt.append(count)
            cum_cnt.append(cum_count)
            cum_fre.append(cum_freq * 100)
        # 关闭文件
        f.close()
        self.ui.progressBar.setValue(3)

        cnt_len = len(cnt)
        # 绘制频率图
        plt.bar(list(range(1, cnt_len + 1)), cnt, align='center')
        plt.axis([1, cnt_len + 1, 1, cnt[cnt_len // 30]])
        plt.title('Word frequency')
        plt.xlabel('X axis')
        plt.ylabel('Y axis')
        plt.savefig(save_path + 'freq.png')
        plt.show()

        # 绘制累计频率图
        bins = range(0, 101, 5)
        plt.hist(cum_fre, bins=bins, rwidth=0.9)
        plt.title("Word cumulative frequency")
        plt.savefig(save_path + 'cumfreq.png')
        plt.show()

        result = dict()
        for a in set(cnt):
            result[a] = cnt.count(a)
        key = []
        value = []
        for k in result:
            key.append(k)
            value.append(result[k])
        self.ui.progressBar.setValue(4)


if __name__ == "__main__":
    start = time.time()
    app = QApplication([])
    stats = WordStats(file_library, txt_file_name, result_file_name)
    stats.ui.show()
    app.exec_()
    end = time.time()
    # print("程序运行" + str(end - start) + "s")
