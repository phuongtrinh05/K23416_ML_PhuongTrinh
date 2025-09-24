import sqlite3
import pandas as pd

try:
    # Kết nối database
    sqliteConnection = sqlite3.connect('../databases/Chinook_Sqlite.sqlite')
    cursor = sqliteConnection.cursor()
    print('DB Init')

    # Câu query: tổng tiền theo khách hàng
    query = """
    SELECT c.CustomerId, c.FirstName || ' ' || c.LastName AS CustomerName, 
           SUM(i.Total) AS TotalSpent
    FROM Customer c
    JOIN Invoice i ON c.CustomerId = i.CustomerId
    GROUP BY c.CustomerId
    ORDER BY TotalSpent DESC
    LIMIT 7;
    """

    # Đọc kết quả vào DataFrame
    df = pd.read_sql_query(query, sqliteConnection)
    print(df)

    cursor.close()

except sqlite3.Error as error:
    print('Error occurred - ', error)

finally:
    if sqliteConnection:
        sqliteConnection.close()
        print('SQLite Connection closed')
