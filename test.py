from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Khởi tạo trình duyệt
driver = webdriver.Chrome()

# Truy cập trang Threads
driver.get('https://www.threads.net')

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
        
        # Thu thập hình ảnh và video
        images = post.find_elements(By.TAG_NAME, 'img')
        videos = post.find_elements(By.TAG_NAME, 'video')
        
        image_urls = [img.get_attribute('src') for img in images if img.get_attribute('src')]
        video_urls = [video.get_attribute('src') for video in videos if video.get_attribute('src')]
        
        # Thu thập bình luận (comments)
        comments = []
        comment_elements = post.find_elements(By.CSS_SELECTOR, 'div[data-testid="post-comment"]')  # Cập nhật selector cho bình luận
        
        for comment in comment_elements:
            try:
                comment_text = comment.text
                comments.append(comment_text)
            except Exception as e:
                print(f"Lỗi khi lấy bình luận: {e}")
        
        # Thu thập dữ liệu bài viết
        post_data.append({
            "username": username,
            "Time": Time,
            "Content": Content,
            "images": image_urls,  # Danh sách các URL hình ảnh
            "videos": video_urls,  # Danh sách các URL video
            "comments": comments   # Danh sách các bình luận
        })
    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu bài viết: {e}")

# Lưu dữ liệu vào file JSON
with open('Post_data3.json', 'w', encoding='utf-8') as f:
    json.dump(post_data, f, ensure_ascii=False, indent=4)

# Đóng trình duyệt
driver.quit()

