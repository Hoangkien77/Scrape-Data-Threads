from pymongo.mongo_client import MongoClient
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')
# Kết nối tới MongoDB
client = MongoClient('mongodb+srv://Hoangkien77:Hoangkien77@cluster0.vdw6x.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['Scrape_data']
collection = db['Threads_data']

# Đọc file JSON
with open('Post_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
unique_data=list({frozenset(item.items()): item for item in data}.values())
# Chèn dữ liệu vào MongoDB
if isinstance(unique_data, list):  # Kiểm tra nếu dữ liệu là danh sách
    result = collection.insert_many(data)
    print(f"Đã thêm {len(result.inserted_ids)} tài liệu vào MongoDB!")
else:
    print("Dữ liệu JSON không phải dạng danh sách.")