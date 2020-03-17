class Conf:
    data_dir = '../data/'
    in_file_dir = data_dir + 'src/'
    out_file_dir = data_dir + 'dest/'
    in_sub_file_dir = in_file_dir + 'subfile/'
    out_sub_file_dir = out_file_dir + 'subfile/'

    out_file_name = 'finance_triples.txt'
    in_file_name = 'baike_triples.txt'

    finance_words = {'金融', '经济', '财经', '货币', '贷款', '资金', '股票', '期货', '银行', '股市', '保险', '并购', '证券',
                     '上市公司', '基金', '上市', '证交所', '债券', '储蓄', '预算', '赤字', '会计', '审计',
                     '物价', '美联储', '通货', '信贷', '外汇', '交易', '股息', '资本', '杠杆', '兼并', '收购',
                     '破产', '资产', '套利'}
    black_list = {'Ace', 'Aoc', 'CECT', 'HP'}

    attribute_black_list = {'餐厅', '书籍'}
    attribute_white_list = {'公司'}

    clear_cache = True


conf = Conf()
