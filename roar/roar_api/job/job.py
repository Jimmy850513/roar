import requests
from pymongo import MongoClient
import json
from .SQL_database import MySql_Database
# from .SQL_database import SQLite3_Database
import asyncio
from datetime import datetime
#mongodb的資訊
client = MongoClient('mongodb://localhost:27017/')
db = client['music_active']
collection = db['music_active']
#pymysql的資訊
class SQL_Datamend(MySql_Database):
    def __init__(self):
        super().__init__()

    def stmt_select_active_id(self):
        stmt = f"""SELECT id FROM active_info"""
        rows = self.execute_query(stmt)
        return rows
    
    def insert_data_into_active_category_info(self,category,show_unit,master_unit,
                                              sub_unit,support_unit,other_unit,active_id):
        stmt = """INSERT INTO active_category_info (
        category, show_unit, master_unit, sub_unit, 
            support_unit, other_unit, active_id,
            is_deleted
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s,0
        )"""
        params = (category, show_unit, master_unit, sub_unit, support_unit, other_unit, active_id)
        rows = self.execute_update(stmt,params)
        return rows

    def insert_data_into_active_show_info(self,show_start_time,show_end_time,show_location,
                                          show_location_addr,on_sale,price,active_info_id):
        stmt = """INSERT INTO active_show_info (
            show_start_time, show_end_time, show_location, 
            show_location_addr, on_sale, price, active_info_id,
            is_deleted
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s,0
        )"""
        params = (show_start_time, show_end_time, show_location,
                show_location_addr, on_sale, price, active_info_id)
        rows = self.execute_update(stmt,params)
        return rows

    def insert_data_into_active_info(self,id,title,discount_info,active_description,
                                     active_promo_image,source_web_name,webSales,
                                     start_date,end_date,comment,hitRate):
        stmt = """INSERT INTO active_info (
            id, title, discount_info, active_description, 
            active_promo_image, source_web_name, webSales, 
            start_date, end_date, comment, hitRate, is_deleted
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0
        )"""
        params = (id, title, discount_info, active_description,
                  active_promo_image, source_web_name, webSales,
                  start_date, end_date, comment, hitRate)
        rows = self.execute_update(stmt,params)
        return rows
# class SQL_Datamend(SQLite3_Database):
#     def __init__(self):
#         super().__init__()

#     def stmt_select_active_id(self):
#         stmt = f"""SELECT id FROM active_info"""
#         rows = self.execute_query(stmt)
#         return rows
    
#     def insert_data_into_active_category_info(self,category,show_unit,master_unit,
#                                               sub_unit,support_unit,other_unit,active_id):
#         stmt = """INSERT INTO active_category_info (
#         category, show_unit, master_unit, sub_unit, 
#             support_unit, other_unit, active_id,
#             is_deleted
#         ) VALUES (
#             ?, ?, ?, ?, ?, ?, ?,0
#         )"""
#         params = (category, show_unit, master_unit, sub_unit, support_unit, other_unit, active_id)
#         rows = self.execute_update(stmt,params)
#         return rows

#     def insert_data_into_active_show_info(self,show_start_time,show_end_time,show_location,
#                                           show_location_addr,on_sale,price,active_info_id):
#         stmt = """INSERT INTO active_show_info (
#             show_start_time, show_end_time, show_location, 
#             show_location_addr, on_sale, price, active_info_id,
#             is_deleted
#         ) VALUES (
#             ?, ?, ?, ?, ?, ?, ?,0
#         )"""
#         params = (show_start_time, show_end_time, show_location,
#                 show_location_addr, on_sale, price, active_info_id)
#         rows = self.execute_update(stmt,params)
#         return rows

#     def insert_data_into_active_info(self,id,title,discount_info,active_description,
#                                      active_promo_image,source_web_name,webSales,
#                                      start_date,end_date,comment,hitRate):
#         stmt = """INSERT INTO active_info (
#             id, title, discount_info, active_description, 
#             active_promo_image, source_web_name, webSales, 
#             start_date, end_date, comment, hitRate, is_deleted
#         ) VALUES (
#             ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0
#         )"""
#         params = (id, title, discount_info, active_description,
#                   active_promo_image, source_web_name, webSales,
#                   start_date, end_date, comment, hitRate)
#         rows = self.execute_update(stmt,params)
#         return rows

# MongoDB 配置
client = MongoClient('mongodb://localhost:27017/')
db = client['music_active']
collection = db['music_active']

# 数据检查函数
def data_check(check_data):
    existing_ids = [data.get('UID') for data in collection.find({}, {"UID": 1, "_id": 0})]
    return [data for data in check_data if data.get('UID') not in existing_ids]

# 从 API 获取数据并处理
def api_schedule_for_mongod():
    url = 'https://cloud.culture.tw/frontsite/trans/SearchShowAction.do?method=doFindTypeJ&category=1'
    try:
        response = requests.get(url)
        data_list = response.json()
    except Exception as e:
        return f'數據獲取失敗: {e}', '', False

    data_to_insert = data_check(data_list)
    if data_to_insert:
        collection.insert_many(data_to_insert)
        return 'MongoDB 數據插入成功', '', True
    else:
        return '無需插入数据', '', False

# 数据整理
def data_tidy():
    dbh = SQL_Datamend()
    existing_ids = [data['id'] for data in dbh.stmt_select_active_id()]
    
    new_data = [data for data in collection.find() if data['UID'] not in existing_ids]

    active_info_dict = {}
    show_info_dict = {}
    active_category_info = {}

    for data in new_data:
        active_id = data['UID']
        active_info_dict[active_id] = {
            'title': data.get('title', ''),
            'discount_info': data.get('discountInfo', ''),
            'active_description': data.get('descriptionFilterHtml', ''),
            'active_image': data.get('imageUrl', ''),
            'source_web_name': data.get('sourceWebName', ''),
            'webSales': data.get('webSales', ''),
            'active_start_date': datetime.strptime(data.get('startDate', ''), "%Y/%m/%d").strftime('%Y-%m-%d'),
            'active_end_date': datetime.strptime(data.get('endDate', ''), "%Y/%m/%d").strftime('%Y-%m-%d'),
            'comment': data.get('comment', ''),
            'hitRate': data.get('hitRate', 0)
        }

        show_info_dict.update({
            (active_id, i): {
                'show_start_time': datetime.strptime(show['time'], "%Y/%m/%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S"),
                'show_end_time': datetime.strptime(show['endTime'], "%Y/%m/%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S"),
                'show_location': show['locationName'],
                'show_location_addr': show['location'],
                'on_sale': 1 if show['onSales'] == 'Y' else 0,
                'price': show['price']
            } for i, show in enumerate(data.get('showInfo', []))
        })

        active_category_info[active_id] = {
            'category': data.get('category', ''),
            'show_unit': data.get('showUnit', ''),
            'master_unit': ','.join(data.get('masterUnit', [])),
            'sub_unit': ','.join(data.get('subUnit', [])),
            'support_unit': ','.join(data.get('supportUnit', [])),
            'other_unit': ','.join(data.get('otherUnit', []))
        }

    return active_info_dict, show_info_dict, active_category_info

# 插入数据到 SQL
def api_schedule_for_sql():
    dbh = SQL_Datamend()
    active_info, show_info_dict, active_category_info = data_tidy()

    if not active_info:
        return '無需插入活動信息', '', ''
    next_step = False
    try:
        for k, v in active_info.items():
            dbh.insert_data_into_active_info(k, v['title'], v['discount_info'], v['active_description'],
                                              v['active_image'], v['source_web_name'], v['webSales'],
                                              v['active_start_date'], v['active_end_date'],
                                              v['comment'], v['hitRate'])
        msg1 = '活動信息插入成功'
        next_step = True
    except Exception as e:
        msg1 = f'活動信息插入失败: {e}'
        
    if next_step:
        try:
            for k, v in active_category_info.items():
                dbh.insert_data_into_active_category_info(v['category'], v['show_unit'], v['master_unit'], 
                                                        v['sub_unit'], v['support_unit'], v['other_unit'], k)
            msg2 = '活動分類信息插入成功'
        except Exception as e:
            msg2 = f'活動分類信息插入失败: {e}'

        try:
            for k, v in show_info_dict.items():
                dbh.insert_data_into_active_show_info(v['show_start_time'], v['show_end_time'], v['show_location'],
                                                    v['show_location_addr'], v['on_sale'], v['price'], k[0])
            msg3 = '表演信息插入成功'
        except Exception as e:
            msg3 = f'表演信息插入失败: {e}'
    else:
        msg2 = ''
        msg3 = ''
    return msg1, msg2, msg3

# 主任务函数
def print_result():
    msg1, msg2, msg3 = api_schedule_for_mongod()
    if msg3:
        msg4, msg5, msg6 = api_schedule_for_sql()
        print(msg1, msg2, msg3)
        print(msg4, msg5, msg6)
    else:
        print(msg1, msg2, msg3)
