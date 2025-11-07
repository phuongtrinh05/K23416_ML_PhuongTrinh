from Final_HocMay.connector.connector import Connector
from Final_HocMay.Models.PurchaseStatistic import PurchaseStatistic

# =========================
# 1️⃣ KẾT NỐI DATABASE
# =========================
connector = Connector(
    server="localhost",
    port=3306,
    database="data",
    username="root",
    password="@Obama123"
)
connector.connect()

# =========================
# 2️⃣ TẠO ĐỐI TƯỢNG VÀ GỌI HÀM
# =========================
pm = PurchaseStatistic(connector)
df_desc = pm.processHolidayDescription()
print(df_desc)

pm.visualizeHolidayDescription(df_desc)
connector.disConnect()

