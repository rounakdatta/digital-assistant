import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["digitalAssistant"]

# get the names of all the DBs under the same IP
# print(myclient.list_database_names())

# create a new collection aka DB
shopData = mydb["shopData"]

# put some values into the collection
firstEverData = [{"item": "iPhone X 64GB", "code": "iphonex64", "seller": "One Electronics", "sellerAddress": "501, Andheri Kurla Road, Mumbai, MH, India", "availableQuantity": 4, "sellingPrice": 94000, "maxDiscountPercent": 5, "cod": False, "tags": ["iphone x", "iphone", "iphone 10", "apple", "apple iphone x", "apple iphone 10", "apple iphone", "latest iphone", "iphone 2018"]}, 
				{"item": "Redmi Note 5", "code": "redminote5", "seller": "Tamil Resellers", "sellerAddress": "Potheri Market, Chennai, TN, India", "availableQuantity": 10, "sellingPrice": 14000, "maxDiscountPercent": 2, "cod": True, "tags": ["redmi note 5", "redmi 5", "note 5", "redmi note", "xiaomi redmi note 5", "xiaomi redmi", "mi note 5", "mi note", "xiaomi note 5"]},
				{"item": "Redmi Note 3", "code": "redminote3", "seller": "The Mobile Store", "sellerAddress": "Station Rd, Rishra, WB, India", "availableQuantity": 14, "sellingPrice": 9999, "maxDiscountPercent": 6, "cod": True, "tags": ["redmi note 3", "redmi 3", "note 3", "redmi note", "xiaomi redmi note 3", "xiaomi redmi", "xiaomi note 3", "mi note 3", "mi note", "kenzo"]},
				{"item": "Xiaomi Mi A1", "code": "mia1", "seller": "eKart Logistics", "sellerAddress": "Great Eastern, JPN, Bengaluru, KA, India", "availableQuantity": 8, "sellingPrice": 15000, "maxDiscountPercent": 0, "cod": True, "tags": ["xiaomi mi a1", "mi a1", "android one", "xiaomi android one", "mi one"]}
				]

# use insert_one for a single value
shopData.insert_many(firstEverData)

# get values from collection
# for x in shopData.find():
# 	print(x)

for y in shopData.find({"tags": "iphone"}):
	print(y['availableQuantity'])