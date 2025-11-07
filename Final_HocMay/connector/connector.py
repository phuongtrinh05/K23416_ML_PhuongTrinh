#python -m pip install mysql-connector-python
import mysql.connector
import traceback
import pandas as pd



class Connector:
    def __init__(self,server="localhost", port=3306, database="data", username="root", password="@Obama123"):
        self.server=server
        self.port=port
        self.database=database
        self.username=username
        self.password=password
    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.server,
                port=self.port,
                database=self.database,
                user=self.username,
                password=self.password,
            use_pure=True)
            return self.conn
        except:
            self.conn=None
            traceback.print_exc()
        return None

    def disConnect(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
            self.conn = None
    # Kiểm tra email đã tồn tại trong bảng customer chưa
    def email_exists(self, email: str) -> bool:
        self.connect()
        cursor = self.conn.cursor()
        sql = "SELECT 1 FROM customer WHERE Email = %s LIMIT 1"
        cursor.execute(sql, (email,))
        row = cursor.fetchone()
        cursor.close()
        return row is not None

    # Đăng ký khách hàng mới
    def register_customer(self, username: str, email: str,
                          password_hash: str, confirm_hash: str = None) -> int:
        """
        Trả về số dòng bị ảnh hưởng (1 = thành công, 0 = thất bại)
        """
        self.connect()
        if confirm_hash is None:
            confirm_hash = password_hash

        sql = """
            INSERT INTO customer (UserName, Email, Password, ConfirmPassword)
            VALUES (%s, %s, %s, %s)
        """
        val = (username, email, password_hash, confirm_hash)
        cursor = self.conn.cursor()
        cursor.execute(sql, val)
        self.conn.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected

    # Kiểm tra email tồn tại
    def email_exists(self, email: str) -> bool:
        self.connect()
        cursor = self.conn.cursor()
        sql = "SELECT 1 FROM customer WHERE Email = %s LIMIT 1"
        cursor.execute(sql, (email,))
        row = cursor.fetchone()
        cursor.close()
        return row is not None

    # Lưu user mới
    def register_customer(self, username: str, email: str,
                          password_hash: str) -> int:
        self.connect()

        sql = """
            INSERT INTO customer (UserName, Email, Password)
            VALUES (%s, %s, %s)
        """
        cursor = self.conn.cursor()
        cursor.execute(sql, (username, email, password_hash))
        self.conn.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected

    def queryDataset(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            df = pd.DataFrame(cursor.fetchall())
            if not df.empty:
                df.columns = cursor.column_names
            return df
        except:
            traceback.print_exc()
        return None

    # def getTablesName(self):
    #     cursor = self.conn.cursor()
    #     cursor.execute("Show tables;")
    #     results = cursor.fetchall()
    #     tablesName = []
    #     for item in results:
    #         tablesName.append([tableName for tableName in item][0])
    #     return tablesName
    #
    # def fetchone(self, sql, val):
    #     try:
    #         cursor = self.conn.cursor()
    #         cursor.execute(sql, val)
    #         dataset = cursor.fetchone()
    #         cursor.close()
    #         return dataset
    #     except:
    #         traceback.print_exc()
    #     return None
    #
    # def fetchall(self, sql, val):
    #     try:
    #         cursor = self.conn.cursor()
    #         cursor.execute(sql, val)
    #         dataset = cursor.fetchall()
    #         cursor.close()
    #         return dataset
    #     except:
    #         traceback.print_exc()
    #     return None
    #
    # def insert_one(self, sql, val):
    #     cursor = self.conn.cursor()
    #     cursor.execute(sql, val)
    #     self.conn.commit()
    #     result = cursor.rowcount
    #     cursor.close()
    #     return result

