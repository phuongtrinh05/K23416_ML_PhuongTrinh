import pandas as pd


def find_orders_within_range(df, minValue, maxValue, SortType=True):
    # Tính tổng giá trị mỗi OrderID
    order_totals = (df.assign(Total=df['UnitPrice'] * df['Quantity'] * (1 - df['Discount']))
                    .groupby('OrderID')['Total']
                    .sum()
                    .reset_index())

    # Lọc theo khoảng giá trị
    filtered = order_totals[(order_totals['Total'] >= minValue) & (order_totals['Total'] <= maxValue)]

    # Sắp xếp theo SortType (True = tăng dần, False = giảm dần)
    filtered = filtered.sort_values(by='Total', ascending=SortType)

    return filtered


# --- Chạy thử ---
df = pd.read_csv('../dataset/SalesTransactions/SalesTransactions.csv')

minValue = float(input("Nhập giá trị min: "))
maxValue = float(input("Nhập giá trị max: "))
sortType = input("Sort tăng dần? (y/n): ").lower() == 'y'

result = find_orders_within_range(df, minValue, maxValue, sortType)

print("Danh sách hóa đơn trong khoảng giá trị từ", minValue, "đến", maxValue, "là:")
print(result)
