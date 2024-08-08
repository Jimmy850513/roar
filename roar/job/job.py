import requests
from pymongo import MongoClient
import json
from SQL_database import MySql_Database
#mongodb的資訊
client = MongoClient('mongodb://localhost:27017/')
db = client['music_active']
collection = db['music_active']
#pymysql的資訊
class SQL_Datamend(MySql_Database):
    def __init__(self):
        super().__init__()
    
    


#confirm data is not inside
def data_check(check_data):
    data_list = collection.find({},{"UID": 1, "_id": 0})
    check_id = [data.get('UID') for data in data_list]
    data_need_insert = list()
    for data in check_data:
        u_id = data.get('UID')
        if u_id and u_id not in check_id:
            data_need_insert.append(data)
    return data_need_insert

def api_schedule():
    url = 'https://cloud.culture.tw/frontsite/trans/SearchShowAction.do?method=doFindTypeJ&category=1'
    data_json = requests.get(url)
    try:
        data_list = data_json.json()
    except Exception as e:
        data_list = None
        return f'資料錯誤,錯誤原因：{e}'
    
    data_need_insert = data_check(data_list)
    if data_need_insert:
        collection.insert_many(data_need_insert)
        msg = 'mongodb文檔插入成功'
        msg1 = ''
        return msg,msg1
    else:
        msg = '目前無需要插入的資料'
        msg1 = ''
        return msg,msg1

def print_result():
    msg,msg1 = api_schedule()
    print(msg)
    print(msg1)
