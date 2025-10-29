from flask import Flask
from flaskext.mysql import MySQL
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
import numpy as np
from sklearn.preprocessing import StandardScaler
import threading, webbrowser
from flask import render_template_string
app = Flask(__name__)

def getConnect(server, port, database, username, password):
    try:
        mysql = MySQL()
        #Mysql confirgurations
        app.config['MYSQL_DATABASE_HOST']=server
        app.config['MYSQL_DATABASE_PORT']=port
        app.config['MYSQL_DATABASE_USER']=username
        app.config['MYSQL_DATABASE_PASSWORD']=password
        app.config['MYSQL_DATABASE_DB'] = database
        mysql.init_app(app)
        conn = mysql.connect()
        return conn
    except mysql.connector.Error as e:
        print("Error = ", e)
    return None
def closeConnect(conn):
    if conn != None:
        conn.close()
def queryDataset(conn,sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    df=pd.DataFrame(cursor.fetchall())
    return df
conn=getConnect('localhost', 3306, 'salesdatabase','root','@Obama123')
sql1="select * from customer"
df1=queryDataset(conn,sql1)
print(df1)
sql2="select distinct customer.CustomerId, Age, Annual_Income, Spending_Score "\
     "from customer, customer_spend_score "\
     "where customer.CustomerId=customer_spend_score.customerId"
df2=queryDataset(conn,sql2)
df2.columns=['CustomerId','Age','Annual_Income','Spending_Score']
print(df2)
print(df2.head())
print(df2.describe())
def showHistogram(df,columns):
    plt.figure(1, figsize=(7,8))
    n=0
    for column in columns:
        n +=1
        plt.subplot(3, 1, n)
        plt.subplots_adjust(hspace=0.5, wspace=0.5)
        sns.distplot(df[column], bins=32)
        plt.title(f'Histogram of {column}')
    plt.show()
showHistogram(df2,df2.columns[1:])

def elbowMethod(df, columnsForElbow):
    X = df.loc[:, columnsForElbow].values
    inertia = []
    for n in range(1, 11):
        model = KMeans(n_clusters = n,
                       init = 'k-means++',
                       max_iter = 500,
                       random_state = 42)
        model.fit(X)
        inertia.append(model.inertia_)

    plt.figure(1, figsize = (15, 6))
    plt.plot(np.arange(1, 11), inertia, 'o')
    plt.plot(np.arange(1, 11), inertia, '-', alpha = 0.5)
    plt.xlabel('Number of Clusters'), plt.ylabel('Cluster sum of squared distances')
    plt.show()

columns = ['Age', 'Spending_Score']
elbowMethod(df2, columns)

def runKMeans(X, cluster):
    model = KMeans(n_clusters = cluster,
                   init = 'k-means++',
                   max_iter = 500,
                   random_state = 42)
    model.fit(X)
    labels = model.labels_
    centroids = model.cluster_centers_
    y_kmeans = model.fit_predict(X)
    return y_kmeans, centroids, labels

X = df2.loc[:, columns].values
cluster = 4
colors = ["red", "green", "blue", "purple", "black", "pink", "orange"]
y_kmeans, centroids, labels = runKMeans(X, cluster)
print(y_kmeans)
print(centroids)
print(labels)
df2["cluster"] = labels

def visualizeKMeans(X, _kmeans, cluster, title, xlabel, ylabel, colors):
    plt.figure(figsize = (10, 10))
    for i in range(cluster):
        plt.scatter(X[y_kmeans == i, 0],
                    X[y_kmeans == i, 1],
                    s = 100,
                    c = colors[i],
                    label = 'Cluster %i' %(i + 1))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

visualizeKMeans(X,
                y_kmeans,
                cluster,
                "Cluster of Customers - Age X Spending Score",
                "Age",
                "Spending Score",
                colors)

#K=5

columns = ['Annual_Income', 'Spending_Score',]
elbowMethod(df2, columns)
X = df2.loc[:, columns].values
cluster = 5

y_kmeans, centroids, labels = runKMeans(X, cluster)

print(y_kmeans)
print(centroids)
print(labels)
df2["cluster"] = labels
visualizeKMeans(X,
                y_kmeans,
                cluster,
                "Cluster of Customers - Annual Income X Spending Score",
                "Annual Income",
                "Spending Score",
                colors)
#k=6
columns = ['Age','Annual_Income', 'Spending_Score',]
elbowMethod(df2, columns)
X = df2.loc[:, columns].values
cluster = 6

y_kmeans, centroids, labels = runKMeans(X, cluster)

print(y_kmeans)
print(centroids)
print(labels)
df2["cluster"] = labels
print(df2)
def visualize3DKmeans(df,columns, hover_data, cluster):
    fig = px.scatter_3d(df, x=columns[0], y=columns[1], z=columns[2],color='cluster',hover_data=hover_data, category_orders={"cluster": range(0,cluster)})
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    fig.show()
hover_data = df2.columns
visualize3DKmeans(df2, columns, hover_data, cluster)

#in danh sách customer ra màn hình console
def showClustersConsole(df):
    print("\n===== DANH SÁCH KHÁCH HÀNG THEO TỪNG CỤM =====")
    for cid in sorted(df['cluster'].unique()):
        print(f"\n--- CLUSTER {cid} ---")
        print(df[df['cluster'] == cid])
        print("----------------------------------------")

showClustersConsole(df2)
#in danh sách màn hình ra web
def showClustersWeb(k):
    sql = """
        SELECT c.Id, c.CustomerID, c.Name, c.Gender, c.Age,
               cs.Annual_Income, cs.Spending_Score
        FROM customer c
        JOIN customer_spend_score cs ON c.CustomerID = cs.CustomerID
    """
    df = queryDataset(conn, sql)
    df.columns = ['Id', 'CustomerID', 'Name', 'Gender', 'Age',
                  'Annual Income', 'Spending Score']

    # Chạy KMeans phân cụm
    X = df[['Age', 'Annual Income', 'Spending Score']].values
    y_kmeans, centroids, labels = runKMeans(X, k)
    df['cluster'] = labels

    clusters = {cid: df[df['cluster'] == cid] for cid in sorted(df['cluster'].unique())}

    html_template = """
    <html>
    <head>
        <title>Customer Clusters (k = {{k}})</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                margin: 30px;
                background: linear-gradient(120deg, #e0f7fa, #fce4ec);
            }
            h1 {
                color: #5b21b6;
                text-align: center;
                margin-bottom: 20px;
            }
            h2 {
                color: #ef6c00;
                margin-top: 40px;
                border-left: 6px solid #ffb74d;
                padding-left: 10px;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
                background-color: white;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 3px 8px rgba(0,0,0,0.1);
            }
            th {
                background-color: #ba68c8;
                color: white;
                padding: 10px;
                text-align: center;
                font-weight: 600;
            }
            td {
                border-bottom: 1px solid #f0f0f0;
                padding: 8px;
                text-align: center;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            tr:hover {
                background-color: #f1f8e9;
                transition: 0.2s;
            }
        </style>
    </head>
    <body>
        <h1> Customer Clusters (k = {{k}})</h1>
        {% for cid, g in clusters.items() %}
            <h2>Cluster {{cid}}</h2>
            {{ g.to_html(index=False) | safe }}
        {% endfor %}
    </body>
    </html>
    """
    return render_template_string(html_template, k=k, clusters=clusters)
@app.route('/clusters/<int:k>')
def clusters(k):
    return showClustersWeb(k)


def open_browser():
    """Tự động mở trình duyệt khi Flask khởi động."""
    webbrowser.open_new("http://127.0.0.1:5000/clusters/6")  # Mặc định k=6


if __name__ == '__main__':
    print("\nTrình duyệt đang mở")
    threading.Timer(1.5, open_browser).start()
    app.run(debug=True)