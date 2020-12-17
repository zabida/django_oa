import json
import xlrd, xlwt
import pymysql
try:
    from xlutils.copy import copy
except:
    pass

# mysql -u shgov -h 172.31.236.60 -p shgov
# Gb!OLLHm%G67*wyV0b0r55mR!fc*!x0a

# db = pymysql.connect('172.31.236.60', 'shgov', 'Gb!OLLHm%G67*wyV0b0r55mR!fc*!x0a', 'shgov')
db = pymysql.connect('10.101.12.34', 'root', 'Chinadep@123', 'shgov_outnet_test')
cur = db.cursor()


def read_excel(name, sheet):
    data = xlrd.open_workbook(name)
    table = data.sheet_by_name(sheet)
    data_set_ids = []
    for i in range(1, table.nrows):
        r = table.row_values(i)
        data_set_ids.append(r[0])
    return data_set_ids


def get_res_url(out='shenji.json'):
    data_set_ids = read_excel('shenji.xlsx', 'Sheet2')
    datas = dict()
    for id in data_set_ids:
        try:
            id = str(int(id))
        except:
            print(id)
            id = str(id)
        datas[id] = dict()
        sql_ = "select * from data_set where dataset_id='{}'".format(id)
        print(11, sql_)
        cur.execute(sql_)
        set_data = cur.fetchone()
        d_id = set_data[0]
        cur.execute('select * from data_set_resources where data_set_id={} and status=3'.format(d_id))
        res_data = cur.fetchall()
        for res in res_data:
            datas[id][res[0]] = res[5]
    print(datas)
    with open(out, 'w') as f:
        json.dump(datas, f)
    return datas


class settings(object):
    INTERNAL_IPS = ["10.83.66.127", "172.27.148.162", "172.27.148.163"]
    INTERFACE_ADDR = 'https://data.sh.gov.cn/interface/{}'


def deal_res_url(res_url, obj_did, res_id):

    if not res_url:   # res.res_url可能为None
        return ''

    for ip in settings.INTERNAL_IPS:
        if ip in res_url:
            return settings.INTERFACE_ADDR.format('/'.join([obj_did, str(res_id)]))
    return res_url


def update_excel(data_source='local', local_source='shenji.json'):
    if data_source == 'local':
        with open(local_source, 'r') as f:
            trans = json.load(f)
    else:
        trans = get_res_url()
    r_book = xlrd.open_workbook('shenji.xlsx')
    r_sheet = r_book.sheet_by_name('Sheet2')
    w_book = copy(r_book)
    w_sheet = w_book.get_sheet(1)
    for i in range(1, r_sheet.nrows):
        try:
            set_id = str(int(r_sheet.row_values(i)[0]))
        except:
            set_id = str(r_sheet.row_values(i)[0])
        print(set_id)
        res_d = trans.get(set_id)
        if len(res_d.items()) > 2:
            print('数据有误{}'.format(set_id))

        res_d = list(res_d.items())
        xml_no, json_no = 0, 0
        for res_id, res_url in res_d:

            if isinstance(res_url, str) and (
            res_url[-5: -1] if res_url.endswith('/') else res_url[-4:]).lower() == '/xml':
                url_type = 'XML'
                xml_no += 1
            else:
                url_type = 'JSON'
                json_no += 1

            res_url = deal_res_url(res_url, set_id, res_id)
            if url_type == 'JSON':
                w_sheet.write(i, 2*(json_no-1) + 3, res_url)
            else:
                w_sheet.write(i, 2*(xml_no-1) + 2, res_url)

    w_book.save('审计第一批.xls')


# get_res_url()
update_excel()
