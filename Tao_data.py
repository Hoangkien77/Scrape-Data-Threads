from pymongo.mongo_client import MongoClient
import json
import sys

# Đảm bảo mã nguồn sử dụng UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Kết nối tới MongoDB
client = MongoClient('mongodb+srv://Hoangkien77:Hoangkien77@cluster0.vdw6x.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['Scrape_data']
collection = db['Threads_data']

# Đọc file JSON
with open('Post_data2.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Loại bỏ phần tử trùng lặp trong dữ liệu
# Sử dụng json.dumps để chuyển đối tượng thành chuỗi JSON để so sánh
unique_data = list({json.dumps(item, sort_keys=True): item for item in data}.values())

# Kiểm tra và chèn dữ liệu vào MongoDB nếu dữ liệu là danh sách
if isinstance(unique_data, list):
    # Chèn các tài liệu vào MongoDB
    result = collection.insert_many(unique_data)
    print(f"Đã thêm {len(result.inserted_ids)} tài liệu vào MongoDB!")
else:
    print("Dữ liệu JSON không phải dạng danh sách.")
