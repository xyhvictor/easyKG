import os
from config import conf


def merge_sub_file(src_dir, dest_file):
    fout = open(dest_file, 'w')
    file_list = os.listdir(src_dir)
    for i in file_list:
        fin = open(src_dir + i, 'r')
        try:
            for line in fin:
                fout.writelines(line)
        finally:
            fin.close()
    fout.close()


def mk_sub_file(buf, out_dir, file_name, sub):
    [des_filename, extname] = os.path.splitext(file_name)
    filename = des_filename + '_' + str(sub) + extname
    filename = out_dir + filename
    print('make file: %s' % filename)
    fout = open(filename, 'w')
    try:
        fout.writelines(buf)
        return sub + 1
    finally:
        fout.close()


def split_by_line_count(in_path=conf.src_file_dir + conf.in_file_name, out_dir=conf.sub_src_file_dir,
                        out_file_name=conf.in_file_name, count=500000):
    fin = open(in_path, encoding="utf-8")
    try:
        buf = []
        sub = 1
        for line in fin:
            buf.append(line)
            if len(buf) == count:
                sub = mk_sub_file(buf, out_dir, out_file_name, sub)
                buf = []
        if len(buf) != 0:
            sub = mk_sub_file(buf, out_dir, out_file_name, sub)
    finally:
        fin.close()


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
        sub: 用于控制生成子文件

    """
    def __init__(self):
        self.finance_entity_set = set()
        self.csv = []
        self.financeKG = []
        self.conf = conf
        self.finance_words = self.conf.finance_words
        self.black_list = self.conf.black_list
        self.sub = 1

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

    def run_extracting_roughly(self, file_path):
        self.first_open_file(file_path)
        self.second_extract_finance_line_fromCSV()
        self.third_extract_finance_entity_from_financeKG()
        self.fourth_extract_all_finance_line_fromCSV_according_finance_entity()
        self.sub = mk_sub_file(self.financeKG, self.conf.sub_dest_file_dir, self.conf.out_file_name, self.sub)

    def KGConstruction_first_step(self):
        print('-'*50 + '\n' + 'start extracting\n' + '-'*50)
        split_by_line_count()
        file_list = os.listdir(self.conf.sub_src_file_dir)
        for i in file_list:
            self.run_extracting_roughly(self.conf.sub_src_file_dir + i)
        merge_sub_file(self.conf.sub_dest_file_dir, self.conf.dest_file_dir + self.conf.out_file_name)
        print('-'*50 + '\n' + 'all files have been extracted\n' + '-'*50)
        if self.conf.clear_cache is True:
            print('-'*50 + '\n' + 'clearing file cache....\n' + '-'*50)
            src_cache = os.listdir(self.conf.sub_src_file_dir)
            dest_cache = os.listdir(self.conf.sub_dest_file_dir)
            for i in src_cache:
                os.remove(self.conf.sub_src_file_dir + i)
            for i in dest_cache:
                os.remove(self.conf.sub_dest_file_dir + i)
            print('-'*50 + '\n' + 'finished\n' + '-'*50)


if __name__ == '__main__':
    kgp = KGProcessor()
    kgp.KGConstruction_first_step()
