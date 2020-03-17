import os
import re
from config import conf


def merge_sub_file(in_dir, out_file):
    fout = open(out_file, 'w')
    file_list = os.listdir(in_dir)
    for i in file_list:
        fin = open(in_dir + i, 'r')
        try:
            for line in fin:
                fout.writelines(line)
        finally:
            fin.close()
    fout.close()


def mk_sub_file(buf, out_file_path, sub):
    if sub != -1:
        [des_filename, extname] = os.path.splitext(out_file_path)
        out_file_path = des_filename + '_' + str(sub) + extname
    print('make file: %s' % out_file_path)
    fout = open(out_file_path, 'w')
    try:
        fout.writelines(buf)
        return sub + 1 if sub != -1 else -1
    finally:
        fout.close()


def split_by_line_count(in_file_path, out_file_path, count=500000):
    fin = open(in_file_path, encoding="utf-8")
    try:
        buf = []
        sub = 1
        for line in fin:
            buf.append(line)
            if len(buf) == count:
                sub = mk_sub_file(buf, out_file_path, sub)
                buf = []
        if len(buf) != 0:
            sub = mk_sub_file(buf, out_file_path, sub)
    finally:
        return sub
        fin.close()


class Controller:
    def __init__(self):
        self.kgp = KGProcessor()
        self.in_out_file_path = dict()
        self.in_cache = conf.in_sub_file_dir
        self.out_cache = conf.out_sub_file_dir
        self.prepare()

    def prepare(self):
        split_by_line_count(conf.in_file_dir + conf.in_file_name, self.in_cache + conf.in_file_name)
        file_name = os.listdir(self.in_cache)
        for name in file_name:
            in_path = self.in_cache + name
            sub = re.findall(r"\d", in_path)
            out_path = self.out_cache + conf.out_file_name
            [des_filename, extname] = os.path.splitext(out_path)
            out_path = des_filename + '_' + ''.join(sub) + extname
            self.in_out_file_path[in_path] = out_path

    def run(self):
        while self.in_out_file_path:
            _in, _out = self.in_out_file_path.popitem()
            self.kgp.run_extracting_roughly(_in, _out)
        if conf.clear_cache is True:
            merge_sub_file(self.out_cache, conf.out_file_dir + conf.out_file_name)
            self.clear_cache()

    def clear_cache(self):
        in_cache_file = os.listdir(self.in_cache)
        out_cache_file = os.listdir(self.out_cache)
        for name in in_cache_file:
            os.remove(self.in_cache + name)
        for name in out_cache_file:
            os.remove(self.out_cache + name)


class KGProcessor:
    """ 从知识图谱三元组文件中提取新的知识图谱。

    第一步为粗略的提取，主要查找三元组的头实体或者尾实体中是否含有指定关键词和黑名单中的词语。

    Attributes:
        conf: 参数信息，在config.py中设置
        csv: 用于存储源知识图谱中的数据
        finance_entity_set: 从源知识图谱中根据指定条件（关键词和黑名单）提取出的实体集合
        financeKG: 用于存储从csv中根据finance_entity_set集合中实体提取的数据
        finance_words: 领域关键词集合
        black_list: 黑名单集合

    """

    def __init__(self):
        self.finance_entity_set = set()
        self.csv = []
        self.financeKG = []
        self.conf = conf
        self.finance_words = self.conf.finance_words
        self.black_list = self.conf.black_list

    def is_in_finance_words(self, pattern):
        for i in self.finance_words:
            if i in pattern:
                return True
        return False

    def is_in_black_list(self, pattern):
        for i in self.black_list:
            if i in pattern:
                return True
        return False

    def first_open_file(self, path):
        self.csv = []
        with open(path, 'r') as file:
            for line in file:
                self.csv.append(line)
        file.close()

    def second_extract_finance_line_fromCSV(self):
        self.financeKG = []
        for members in self.csv:
            member = members.split()
            if self.is_in_finance_words(member[0]) is True and self.is_in_black_list(member[0]) is False:
                self.financeKG.append(members)
            elif self.is_in_finance_words(member[2]) is True and self.is_in_black_list(member[2]) is False:
                self.financeKG.append(members)

    def third_extract_finance_entity_from_financeKG(self):
        self.finance_entity_set = set()
        for i in self.financeKG:
            container = i.split()
            self.finance_entity_set.add(container[0])

    def fourth_extract_all_finance_line_fromCSV_according_finance_entity(self):
        self.financeKG = []
        for line in self.csv:
            container = line.split()
            if container[0] in self.finance_entity_set:
                self.financeKG.append(line)

    def run_extracting_roughly(self, in_file_path, out_file_path):
        self.first_open_file(in_file_path)
        self.second_extract_finance_line_fromCSV()
        self.third_extract_finance_entity_from_financeKG()
        self.fourth_extract_all_finance_line_fromCSV_according_finance_entity()
        mk_sub_file(self.financeKG, out_file_path, -1)


if __name__ == '__main__':
    controller = Controller()
    controller.run()
