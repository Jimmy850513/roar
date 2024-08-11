# import sqlite3
# from .SQL_param import Sql_Param

# class SQLite3_Database(Sql_Param):
#     def __init__(self):
#         super().__init__()
#         self.conn = None
#         self.curs = None
#         try:
#             self.conn = sqlite3.connect(self.dbname)  # 使用 SQLite 数据库文件路径
#             self.curs = self.conn.cursor()
#             print("Database connected successfully")
#         except Exception as e:
#             print("Database connection failed")
#             raise

#     def execute_query(self, stmt):
#         self.curs.execute(stmt)
#         result = self.curs.fetchall()
#         columns = [desc[0] for desc in self.curs.description]
#         return [dict(zip(columns, row)) for row in result]

#     def execute_update(self, query, params=None):
#         try:
#             self.curs.execute(query, params or ())
#             self.conn.commit()
#         except sqlite3.Error as e:
#             print(f"Error executing update: {e}")
#             self.conn.rollback()
#             raise

#     def close(self):
#         if self.curs:
#             self.curs.close()
#         if self.conn:
#             self.conn.close()
#         print("Database connection closed")



import pymysql
from .SQL_param import Sql_Param
class MySql_Database(Sql_Param):
    def __init__(self):
        super().__init__() 
        self.conn = None
        self.curs = None
        try:
            self.conn = pymysql.connect(
                database=self.dbname,
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port
            )
            self.curs = self.conn.cursor()
            print("database正常連接")
        except Exception as e:
            print("database 未正常連接")
            raise
        
    def execute_query(self, stmt):
        self.curs.execute(stmt)
        result = self.curs.fetchall()
        # 获取列名
        columns = [desc[0] for desc in self.curs.description]
        # 将结果转换为字典列表
        return [dict(zip(columns, row)) for row in result]

    def execute_update(self, query, params=None):
        """
        执行 SQL 更新/插入/删除
        """
        try:
            self.curs.execute(query, params or ())
            self.conn.commit()
        except pymysql.MySQLError as e:
            print(f"Error executing update: {e}")
            self.conn.rollback()
            raise

    def close(self):
        if self.curs:
            self.curs.close()
        if self.conn:
            self.conn.close()
        print("Database connection closed")