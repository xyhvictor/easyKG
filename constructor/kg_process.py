from config import conf
from kg_construct import mk_sub_file
import csv
import os


def is_attr(s):
    return s == 'BaiduTAG' or s == 'BaiduCARD'


def key_exist(d, e):
    return e in d


class LoadFile:
    def __init__(self):
        self.kg = dict()
        self.relation = list()

    def write_attr_relation(self):
        f_attr = open(conf.sys_attr_file, 'w')
        f_relation = open(conf.sys_relation_file, 'w')
        f_entity = open(conf.sys_leaf_file, 'w')
        f_new_node = open(conf.sys_new_node_file, 'w')

        writer_attr = csv.writer(f_attr)
        writer_relation = csv.writer(f_relation)
        writer_new_node = csv.writer(f_new_node)

        writer_attr.writerow(['Entity', 'Attribute', 'Attribute'])
        writer_relation.writerow(['HudongItem1', 'relation', 'HudongItem2'])
        writer_new_node.writerow(['title', 'lable'])
        try:
            for k, v in self.kg.items():
                # 写属性三元组和关系三元组
                for k_, v_ in v.items():
                    if is_attr(k_):
                        for tail in v_:
                            triple = [k, k_, tail]
                            writer_attr.writerow(triple)
                    else:
                        # 将关系进行保存
                        if k_ not in self.relation:
                            self.relation.append(k_)
                        for tail in v_:
                            triple = [k, k_, tail]
                            writer_relation.writerow(triple)
                # 写入实体和对应类型
                f_entity.write('金融' + '\t' + k + '\n')
                # 写入新增节点
                writer_new_node.writerow([k, 'newNode'])

        finally:
            f_attr.close()
            f_relation.close()
            f_entity.close()
            f_new_node.close()

    # 此函数需要在 write_attr_relation 后面执行
    def write_relation_tag(self):
        l = len(self.relation)
        tag = list(range(l))
        f = open(conf.sys_relation_tag_file, 'w')
        try:
            while len(self.relation) > 0:
                line = "('" + self.relation.pop() + "', " + str(tag.pop()) + ")\n"
                f.write(line)
        finally:
            f.close()

    def load(self, path):
        fin = open(path, 'r', encoding='utf-8')
        try:
            for line in fin:
                temps = line.split()
                head = temps[0]
                mid = temps[1]
                tail = temps[2]
                if not key_exist(self.kg, head):
                    self.kg[head] = dict()
                    self.kg[head][mid] = list()
                if not key_exist(self.kg[head], mid):
                    self.kg[head][mid] = list()
                self.kg[head][mid].append(tail)
        finally:
            fin.close()


if __name__ == '__main__':
    l = LoadFile()
    path = conf.out_file_dir + conf.out_file_name
    l.load(path)
    l.write_attr_relation()
    l.write_relation_tag()
