# #Thử nghiêm doc du lieu xml
from bs4 import BeautifulSoup
with open ('../dataset/SalesTransactions/SalesTransactions.xml','r') as f:
    data = f.read()
#Passing the stored data inside the beautifulsoup parser
bs_data = BeautifulSoup(data,'xml')
#Finding all instance of tag
UelSample = bs_data.find_all('UelSample')
print(UelSample)