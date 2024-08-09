import requests
from pymongo import MongoClient
import json
from .SQL_database import MySql_Database
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
    
    def stmt_select_active_id(self):
        stmt = f""""""
    
    def insert_data_into_active_category_info(self,category,show_unit,master_unit,
                                              sub_unit,support_unit,other_unit,active_id):
        stmt = f"""INSERT INTO active_category_info(
        category, show_unit, master_unit, sub_unit, 
        support_unit, other_unit, active_id
        )VALUES(
        '{category}','{show_unit}','{master_unit}','{sub_unit}','{support_unit}',
        '{other_unit}','{active_id}'
        )"""
        rows = self.execute_update(stmt)
        return rows

    def insert_data_into_active_show_info(self,show_start_time,show_end_time,show_location,
                                          show_location_addr,on_sale,price,active_info_id):
        stmt = f"""INSERT INTO active_show_info(
        show_start_time, show_end_time, show_location, 
        show_location_addr, on_sale, price, active_info_id
        )VALUES(
        '{show_start_time}','{show_end_time}','{show_location}','{show_location_addr}'
        ,'{on_sale}','{price}','{active_info_id}'
        )"""
        rows = self.execute_update(stmt)
        return rows

    def insert_data_into_active_info(self,id,title,discount_info,active_description,
                                     active_promo_image,source_web_name,webSales,
                                     start_date,end_date,comment,hitRate):
        stmt = f"""INSERT INTO active_info(
        id, title, discount_info, active_description, 
        active_promo_image, source_web_name, webSales, 
        start_date, end_date, comment, hitRate
        )VALUES(
        '{id}','{title}','{discount_info}','{active_description}','{active_promo_image}',
        '{source_web_name}','{webSales}','{start_date}','{end_date}','{comment}','{hitRate}'
        )"""
        rows = self.execute_update(stmt)
        return rows


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

def api_schedule_for_mongod():
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

def data_tidy():
    
    dbh = SQL_Datamend()
    data_need_check = list()
    inSQL_active_id = dbh.stmt_select_active_id()
    for data in inSQL_active_id:
        data_need_check.append(data['id'])
    data_need_insert = list()
    mongodb_data = collection.find()
    for data in mongodb_data:
        if data['UID'] not in data_need_check:
            data_need_insert.append(data)
    
    active_info_dict = dict()
    show_info_dict = dict()
    active_category_info = dict()
    for data in data_need_insert:
        active_id = data['UID']
        title = data['title']
        category = data['category']
        #array
        show_info = data['showInfo']
        show_unit = data['showUnit'] if data['showUnit'] else ''
        discount_info = data['discountInfo'] if data['discountInfo'] else ''
        active_description = data['descriptionFilterHtml'] if data['descriptionFilterHtml'] else ''
        active_image = data['imageUrl'] if data['imageUrl'] else ''
        #array
        master_unit = data['masterUnit'] if data['masterUnit'] else []
        #array
        sub_unit = data['subUnit'] if data['subUnit'] else []
        #array    
        support_unit = data['supportUnit'] if data['supportUnit'] else []
        #array
        other_unit = data['otherUnit'] if data['otherUnit'] else []
        webSales = data['webSales'] if data['webSales'] else ''
        comment = data['comment'] if data['comment'] else ''
        source_web_name = data['sourceWebName']
        activate_start_date_obj = datetime.strptime(data['startDate'], "%Y/%m/%d").date()
        active_start_date = activate_start_date_obj.strftime('%Y-%m-%d')
        activate_end_date_obj = datetime.strptime(data['endDate'],"%Y/%m/%d").date()
        active_end_date = activate_end_date_obj.strftime('%Y-%m-%d')
        #int
        hitRate = data['hitRate'] if data['hitRate'] else 0
        active_info_dict[active_id] = {
            'title':title,'discount_info':discount_info,'active_description':active_description,
            'active_image':active_image,'source_web_name':source_web_name,'webSales':webSales,
            'active_start_date':active_start_date,'active_end_date':active_end_date,
            'comment':comment,'hitRate':hitRate
        }
        if show_info:
            for i in range(0,len(show_info)):
                key = (active_id,i)
                start_time_obj = datetime.strptime(show_info[i]['time'], "%Y/%m/%d %H:%M:%S")
                start_time_datetime = start_time_obj.strftime("%Y-%m-%d %H:%M:%S")
                end_time_obj = datetime.strptime(show_info[i]['endTime'],"%Y/%m/%d %H:%M:%S")
                end_time_datetime = end_time_obj.strftime("%Y-%m-%d %H:%M:%S")
                show_info_dict[key] = {
                    'show_start_time':start_time_datetime,
                    'show_end_time':end_time_datetime,
                    'show_location':show_info[i]['locationName'],
                    'show_location_addr':show_info[i]['location'],
                    'on_sale':show_info[i]['onSales'],
                    'price':show_info[i]['price']
                }
        if category:
            active_category_info[active_id] = {
                'category':category,
                'show_unit':'',
                'master_unit':'',
                'sub_unit':'',
                'support_unit':'',
                'other_unit':''
            }
        if master_unit:
           for i in range(0,len(master_unit)):
                if i == len(master_unit) -1 :
                    active_category_info[active_id]['master_unit'] += master_unit[i]
                else:
                    active_category_info[active_id]['master_unit'] += master_unit[i]+','
               
        
        if sub_unit:
            for i in range(0,len(sub_unit)):
                if i == len(sub_unit)-1:
                    active_category_info[active_id]['sub_unit']+=sub_unit[i]
                else:
                    active_category_info[active_id]['sub_unit']+=sub_unit[i]+','
        
        if support_unit:
            for i in range(0,len(support_unit)):
                if i == len(support_unit)-1:
                    active_category_info[active_id]['support_unit']+=support_unit[i]
                else:
                    active_category_info[active_id]['support_unit']+=support_unit[i]+','
        if other_unit:
            for i in range(0,len(other_unit)):
                if i == len(other_unit)-1:
                    active_category_info[active_id]['other_unit']+=other_unit[i]
                else:
                    active_category_info[active_id]['other_unit']+=other_unit[i]+','
        if show_unit:
            for i in range(0,len(show_unit)):
                if i == len(show_unit)-1:
                    active_category_info[active_id]['show_unit']+=show_unit[i]
                else:
                    active_category_info[active_id]['show_unit']+=show_unit[i]+','
    return active_info_dict,show_info_dict,active_category_info





def api_schedule_for_sql():
    pass

def print_result():
    msg,msg1 = api_schedule_for_mongod()
    data_tidy()

    print(msg)
    print(msg1)
