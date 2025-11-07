from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd

class PurchaseStatistic:
    def __init__(self, connector=None):
        self.connector = connector
        self.lasted_df = None

    # =========================
    # 1️⃣ Thống kê Holiday Description
    # =========================
    def processHolidayDescription(self):
        """
        Lấy dữ liệu description từ bảng holidays_events
        và trả về top 12 description xuất hiện nhiều nhất.
        """
        sql = "SELECT description FROM holidays_events;"
        df = self.connector.queryDataset(sql)
        if df is None or df.empty:
            print("⚠️ Không có dữ liệu holidays_events hoặc truy vấn lỗi.")
            return None

        desc_freq = (
            df.groupby('description')
            .size()
            .reset_index(name='count')
            .sort_values('count', ascending=False)
            .head(12)
        )
        self.lasted_df = desc_freq
        return desc_freq

    # =========================
    # 2️⃣ Vẽ biểu đồ Top 12 Description
    # =========================
    def visualizeHolidayDescription(self, df):
        if df is None or df.empty:
            print("⚠️ Không có dữ liệu để vẽ biểu đồ.")
            return
        sns.set(style="whitegrid")
        plt.figure(figsize=(8, 5))
        sns.barplot(
            data=df,
            y='description',
            x='count',
            color='skyblue'
        )
        plt.title("Top 12 Most Frequent Holiday Descriptions",
                  fontsize=13, weight='bold')
        plt.xlabel("Frequency")
        plt.ylabel("Holiday Description")
        plt.tight_layout()
        plt.show()
