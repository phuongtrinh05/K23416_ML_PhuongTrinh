from MLBAProject.Connectors.Connector import Connector
from MLBAProject.Models.PurchaseMLModel import PurchaseMLModel

connector=Connector(server="localhost",port=3306,database="lecturer_retails",username="root",password="@Obama123")
connector.connect()
pm=PurchaseMLModel(connector)
pm.execPurchaseHistory()

dfTransform=pm.processTransform()
print(dfTransform.head())
pm.buildCorrelationMatrix(dfTransform)