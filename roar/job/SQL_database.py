import pymysql
from .SQL_param import Sql_Param
class MySql_Database(Sql_Param):
    def __init__(self):
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
        
    def execute_query(self, query, params=None):
        """
        执行 SQL 查询
        """
        try:
            self.curs.execute(query, params or ())
            return self.curs.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error executing query: {e}")
            raise

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