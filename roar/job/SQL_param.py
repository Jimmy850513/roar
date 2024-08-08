
class Sql_Param:
    def __init__(self):
        self.dbname = 'roar'
        self.host = 'localhost'
        self.user = 'root'
        self.port = '3306'
        self.password = 'password'
    
    def __str__(self):
        return 'SQL params'