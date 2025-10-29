import os
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from flaskext.mysql import MySQL
from flask import Flask

app = Flask(__name__)

# ==========================================
# KẾT NỐI DATABASE
# ==========================================
def getConnect(server, port, database, username, password):
    try:
        mysql = MySQL()
        app.config['MYSQL_DATABASE_HOST'] = server
        app.config['MYSQL_DATABASE_PORT'] = port
        app.config['MYSQL_DATABASE_USER'] = username
        app.config['MYSQL_DATABASE_PASSWORD'] = password
        app.config['MYSQL_DATABASE_DB'] = database
        mysql.init_app(app)
        conn = mysql.connect()
        return conn
    except Exception as e:
        print("❌ Lỗi kết nối:", e)
    return None

def queryDataset(conn, sql: str) -> pd.DataFrame:
    cur = conn.cursor()
    cur.execute(sql)
    df = pd.DataFrame(cur.fetchall())
    return df

# ==========================================
# XÂY DỰNG DỮ LIỆU ĐẶC TRƯNG
# ==========================================
def build_interest_features(conn) -> pd.DataFrame:
    sql = """
    SELECT
        c.customer_id,
        CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
        COUNT(r.rental_id)                       AS total_rentals,
        COUNT(DISTINCT f.film_id)                AS unique_films,
        COUNT(DISTINCT fc.category_id)           AS unique_categories,
        AVG(f.rental_rate)                       AS avg_rental_rate,
        SUM(f.length)                            AS total_length,
        MIN(r.rental_date)                       AS first_rental_date,
        MAX(r.rental_date)                       AS last_rental_date
    FROM sakila.customer c
    LEFT JOIN sakila.rental r         ON c.customer_id = r.customer_id
    LEFT JOIN sakila.inventory i      ON r.inventory_id = i.inventory_id
    LEFT JOIN sakila.film f           ON i.film_id     = f.film_id
    LEFT JOIN sakila.film_category fc ON f.film_id     = fc.film_id
    GROUP BY c.customer_id, customer_name
    ORDER BY c.customer_id;
    """
    df = queryDataset(conn, sql)
    df.columns = ["customer_id","customer_name","total_rentals","unique_films",
                  "unique_categories","avg_rental_rate","total_length",
                  "first_rental_date","last_rental_date"]

    # Xử lý thời gian & các đặc trưng phát sinh
    df["last_rental_date"]  = pd.to_datetime(df["last_rental_date"])
    df["first_rental_date"] = pd.to_datetime(df["first_rental_date"])
    today = pd.Timestamp.today().normalize()
    df["recency_days"] = (today - df["last_rental_date"]).dt.days.fillna(9999)

    days_active = (df["last_rental_date"] - df["first_rental_date"]).dt.days
    months_active = (days_active / 30.0).clip(lower=1.0)  # tránh chia 0
    df["rentals_per_month"] = (df["total_rentals"] / months_active).fillna(0)

    # Fill NA các đặc trưng số
    fill_cols = ["total_rentals","unique_films","unique_categories",
                 "avg_rental_rate","total_length","rentals_per_month"]
    df[fill_cols] = df[fill_cols].fillna(0)
    return df

# ==========================================
# GOM CỤM KMEANS & IN CONSOLE
# ==========================================
def runKMeansAndPrint(df: pd.DataFrame, feature_cols, n_clusters: int = 4) -> pd.DataFrame:
    X = df.loc[:, feature_cols].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=500, n_init=10, random_state=42)
    labels = model.fit_predict(X_scaled)
    df = df.copy()
    df["cluster"] = labels

    print("\n===== KẾT QUẢ PHÂN CỤM =====")
    for cid in sorted(df["cluster"].unique()):
        print(f"\n--- CỤM {cid} ---")
        print(df[df["cluster"] == cid][["customer_name","total_rentals","unique_films","avg_rental_rate"]])
        print("----------------------------------")
    return df

# ==========================================
# XUẤT FILE EXCEL (lưu cùng thư mục với file .py)
# ==========================================
def exportClustersToExcel(df, filename="CustomerClusters_FilmInventory_k4.xlsx"):
    """
    Xuất toàn bộ dữ liệu DataFrame df ra file Excel
    (lưu trực tiếp vào thư mục Bai_nop_29_10)
    """
    # Lấy đường dẫn thư mục cha của file hiện tại
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Tạo đường dẫn đến thư mục Bai_nop_29_10
    save_dir = os.path.join(current_dir, "Bai_nop_29_10")

    # Nếu thư mục chưa tồn tại thì tạo mới
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Tạo đường dẫn đầy đủ tới file Excel
    save_path = os.path.join(save_dir, filename)

    # Xuất DataFrame ra Excel
    df.to_excel(save_path, index=False)

    print(f"\n📁 Dữ liệu đã được lưu vào file: {save_path}")

# ==========================================
# CHƯƠNG TRÌNH CHÍNH
# ==========================================
if __name__ == "__main__":
    print("\nPHÂN CỤM KHÁCH HÀNG THEO FILM & INVENTORY (k=4)")

    conn = getConnect("localhost", 3306, "sakila", "root", "@Obama123")
    df_feat = build_interest_features(conn)
    features = ["total_rentals", "unique_films", "avg_rental_rate"]
    df_clustered = runKMeansAndPrint(df_feat, features, n_clusters=4)

    exportClustersToExcel(df_clustered)
    try:
        conn.close()
    except Exception:
        pass

    print("\n Hoàn tất phân cụm và lưu file Excel!")
