# class Sql_Param:
#     def __init__(self):
#         # 对于 SQLite3，通常只需要指定数据库文件的路径
#         self.dbname = '/home/jimmy/roar/roar/db.sqlite3'  # 替换为 SQLite 数据库文件的实际路径
        
#         # SQLite 不需要用户名、密码、主机和端口，因此可以将它们留空或删除
#         self.host = None
#         self.user = None
#         self.password = None
#         self.port = None



class Sql_Param:
    def __init__(self):
        self.dbname = 'roar'
        self.host = 'localhost'
        self.user = 'root'
        self.port = 3306
        self.password = 'password'
    
    def __str__(self):
        return 'SQL params'