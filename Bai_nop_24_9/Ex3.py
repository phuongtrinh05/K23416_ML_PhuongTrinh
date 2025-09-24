#đầu vào là df, đầu ra là top 3 sản phẩm bán ra có giá trị bán ra cao nhất

import pandas as pd
# Đọc dữ liệu
df = pd.read_csv("../dataset/SalesTransactions/SalesTransactions.csv")

# Tạo cột giá trị bán ra
df['Total'] = df['UnitPrice'] * df['Quantity'] * (1 - df['Discount'])

# Tổng giá trị theo ProductID
product_sales = df.groupby('ProductID')['Total'].sum()

# Top 3 sản phẩm có doanh thu cao nhất
top3_products = product_sales.sort_values(ascending=False).head(3)

# In kết quả với số thứ tự
print("Top 3 sản phẩm có giá trị bán cao nhất:")
for i, (product_id, total) in enumerate(top3_products.items(), start=1):
    print(f"{i}. ProductID {product_id}: {total:.2f}")
