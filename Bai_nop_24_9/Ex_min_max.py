import pandas as pd
def find_orders_within_range(df,minValue,maxValue):
    #Tổng gia tri don hàng
    order_totals = df.groupby('OrderID').apply(lambda x: (x['UnitPrice']*x['Quantity']*(1-x['Discount'])).sum())
    #loc don hang trong range
    orders_within_range = order_totals[(order_totals >= minValue) & (order_totals <= maxValue)]
    # danh sach cac ma don hang khong trung nhau
    unique_orders = df[df['OrderID'].isin(orders_within_range.index)]['OrderID'].drop_duplicates().tolist()
    return unique_orders
df=pd.read_csv('../dataset/SalesTransactions/SalesTransactions.csv')
minValue = float(input("Nhập giá trị min:"))
maxValue = float(input("Nhập giá trị max:"))
result = find_orders_within_range(df, minValue, maxValue)
print('Danh sách các hóa đơn trong phạm vi giá trị từ', minValue, 'đến', maxValue, 'la', result)
