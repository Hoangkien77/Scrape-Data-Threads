from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo.mongo_client import MongoClient
import time
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')




# Khởi tạo trình duyệt
driver = webdriver.Chrome()

# Truy cập trang Threads
driver.get('https://www.threads.net/@maianh230896/post/DCq9hVST7H0?hl=vi')

# Chờ đợi trang tải xong
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'div')))

# Cuộn trang (nếu cần thiết)
def scroll_to_bottom():
    previous_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    return new_height != previous_height

for _ in range(3):  # Cuộn 3 lần (tùy theo số lượng bạn muốn)
    if not scroll_to_bottom():
        break

# Thu thập dữ liệu
posts = driver.find_elements(By.TAG_NAME, 'div')

print(f"Số lượng bài viết thu thập được: {len(posts)}")

post_data = []

# Lặp qua các bài viết
for post in posts:
    try:
        # Tìm username
        username = post.find_element(By.CSS_SELECTOR, 'div > div > a > span').text
        
        # Tìm thời gian đăng
        Time = post.find_element(By.CSS_SELECTOR, 'div.xqcrz7y span > a > time > span').text
        
        # Tìm nội dung bài viết
        Content = post.find_element(By.CSS_SELECTOR, 'div.x1xdureb.xkbb5z.x13vxnyz > div > div.x1a6qonq.x6ikm8r.x10wlt62.xj0a0fe.x126k92a.x6prxxf.x7r5mf7 > span').text
        Like = post.find_element(By.CSS_SELECTOR, "div.x1xdureb svg > path").text
        Comment = post.find_element(By.CSS_SELECTOR, "div.x1xdureb.xkbb5z.x13vxnyz div.x6s0dn4.x78zum5.xl56j7k.xezivpi > div > div").text

        # Thêm dữ liệu vào danh sách
        post_data.append({"username": username, "Time": Time, 'Content': Content})
    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu: {e}")

# Lưu dữ liệu vào file JSON
with open('Post_data.json', 'w', encoding='utf-8') as f:
    json.dump(post_data, f, ensure_ascii=False, indent=4)

# Đóng trình duyệt
driver.quit()
