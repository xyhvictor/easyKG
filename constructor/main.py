class KGProcessor:
    finance_words = {'金融', '经济', '财经', '货币', '贷款', '资金','股票','期货','银行','股市','保险','并购','证券',
                   '上市公司','利益','基金','上市','证交所','债券','储蓄','知识产权','预算','赤字','会计','审计',
                   '物价','美联储','通货','信贷','外汇','交易','股息','资本','杠杆','兼并','收购','产权',
                   '破产','下跌','大跌','资产','套利'}
    finance_entity_set = set()
    csv = []
    financeKG = []
    all = False
    count = 0

    def openFile(self, path):
        c = 0
        with open(path,'r') as file:
            for line in file:
                c += 1
                ans = line.split()
                self.csv.append(ans)
                if self.all is False and c > self.count:
                    break
        file.close()

    def first_extract_finance_line_fromCSV(self):
        for members in self.csv:
            for member in members:
                for i in self.finance_words:
                    if i in member:
                        self.financeKG.append(members)

    def second_extract_finance_entity_from_financeKG(self):
        for i in self.financeKG:
            self.finance_entity_set.add(i[0])

    def third_extract_all_finance_line_fromCSV_according_finance_entity(self):
        for line in self.csv:
            for i in line:
                if i[0] in self.finance_entity_set:
                    self.financeKG.append(line)

    def KGConstruction(self,input_path, output_path,count="all",toFile = False):
        if count == "all":
            self.all = True
        else:
            self.count = count
        self.openFile(input_path)
        self.first_extract_finance_line_fromCSV()
        self.second_extract_finance_entity_from_financeKG()
        self.third_extract_all_finance_line_fromCSV_according_finance_entity()
        if not toFile:
            return self.financeKG
        else:
            f = open(output_path, 'w')
            for line in self.financeKG:
                str = ""
                for i in line:
                    str += i
                    str += " "
                str = str[:-1]
                f.write(str+'\n')
            f.close()


if __name__ == '__main__':
    intput_file = "./file/kg.txt"
    output_file = "./file/finance_kg.txt"
    kgp = KGProcessor()
    kgp.KGConstruction(intput_file, output_file, toFile=True)
