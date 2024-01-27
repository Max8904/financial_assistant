# 載入 selenium 相關模組
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import bs4
import time
import csv
from datetime import datetime
from tqdm import tqdm


# 設定 Chrome Driver 的執行檔路徑
options = Options()
options.chrome_executable_path = "D:/Python Project/financial_assistant/chromedriver.exe"
# 建立 Driver 物件實體，用程式操作瀏覽器運作
driver = webdriver.Chrome(options=options)

def crawler_scrollDown_NTime(link, time):
    # 連線到 Yahoo! 新聞 / 財金版
    driver.get(link)
    # 捲動視窗並等待瀏覽器載入更多內容
    n = 0
    while n < time:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(5) # 等待載入
        # 等待載入新內容
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//h3[@class='Mb(5px)']")))
        n += 1

    # 取得網頁內容
    page_source = driver.page_source

    # 使用 Beautiful Soup 解析 HTML
    soup = bs4.BeautifulSoup(page_source, 'html.parser')

    # 找到文章標題元素
    title_elements = soup.find_all('h3', class_='Mb(5px)')

    # 紀錄所有文章的 ID、標題、連結
    link_list = []
    # 取得網頁中新聞的標題
    for i, title_element in enumerate(title_elements):
        title = title_element.text.strip()
        # print(title)

        # 直接使用 BeautifulSoup 的方法找到 <a> 元素
        a_element = title_element.find('a')

        # 確認是否找到了 <a> 元素
        if a_element:
            # 如果找到，取得 href 屬性的值
            href_value = a_element.get('href')
            link = "https://tw.news.yahoo.com" + href_value
            # print(link)

            link_dict = {"ID": i, "Title": title, "Link": link}
            link_list.append(link_dict)

    # print(link_list)
    return link_list

# def crawler_scrollDown_ToBottom():
#     # 設定 Chrome Driver 的執行檔路徑
#     options = Options()
#     options.chrome_executable_path = "D:/Python Project/financial_assistant/chromedriver.exe"

#     # 建立 Driver 物件實體，用程式操作瀏覽器運作
#     driver = webdriver.Chrome(options=options)

#     # 連線到 Yahoo! 新聞 / 財金版
#     driver.get("https://tw.news.yahoo.com/finance/")
#     time.sleep(5)

#     # 循環捲動直到底部
#     while True:
#         # 記錄頁面高度
#         last_height = driver.execute_script("return document.body.scrollHeight")

#         # 捲動至底部
#         # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#         # 等待載入新內容
#         # 模擬按下 PAGE_DOWN 鍵
#         driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
#         time.sleep(5)
#         # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h3[@class='Mb(5px)']")))

#         # 再次取得新的頁面高度
#         new_height = driver.execute_script("return document.body.scrollHeight")

#         # 如果新的頁面高度和之前的相同，表示已經到達底部，退出循環
#         if new_height == last_height:
#             break

#     # 取得網頁內容
#     page_source = driver.page_source

#     # 使用 Beautiful Soup 解析 HTML
#     soup = bs4.BeautifulSoup(page_source, 'html.parser')

#     # 找到文章標題元素，這可能需要根據實際 HTML 結構進行調整
#     title_elements = soup.find_all('h3', class_='Mb(5px)')

#     # 取得網頁中新聞的標題
#     for title_element in title_elements:
#         print(title_element.text.strip())

#     # 關閉瀏覽器
#     driver.quit()

def get_article(link):
    # 連線到特定文章網址
    driver.get(link)

    # 循環捲動直到底部
    while True:
        # 記錄頁面高度
        last_height = driver.execute_script("return document.body.scrollHeight")

        # 捲動至底部
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 等待載入新內容
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//p")))

        # 再次取得新的頁面高度
        new_height = driver.execute_script("return document.body.scrollHeight")

        # 如果新的頁面高度和之前的相同，表示已經到達底部，退出循環
        if new_height == last_height:
            break

    # 取得網頁內容
    page_source = driver.page_source

    # 使用 Beautiful Soup 解析 HTML
    root = bs4.BeautifulSoup(page_source, 'html.parser')

    # 取得網頁中新聞的標題
    title = root.title.string
    # print(title)

    # 取得文章內容
    body = root.find('div', class_ = "caas-body")
    paragraph_list = body.find_all('p')
    # print(paragraph_list)

    # 過濾文章內容: 去除空白字串、去除標籤
    paragraph_list_filitered = []
    for paragraph in paragraph_list:
        if paragraph.text == "":
            continue
        paragraph_list_filitered.append(paragraph.text)
    # print(paragraph_list_filitered)
    paragraph = "\n".join(paragraph_list_filitered)
    # print(paragraph)

    # 回傳 output
    output_dict = {"Title": title, "Link": link, "Paragraph": paragraph}
    # print(output_dict)
    return output_dict

def crawler_output_csv(filename_out):
    with open(filename_out, "a", encoding="utf-8", newline='') as f_out:
        writer = csv.writer(f_out)
        cols_name = ["ID", "Title", "Link", "Paragraph"]
        writer.writerow(cols_name)

        # 連線到 Yahoo! 新聞 / 財金版
        link = "https://tw.news.yahoo.com/finance/"
        link_list = crawler_scrollDown_NTime(link, 3)

        print("Crawler Processing ... ")
        for link_dict in tqdm(link_list):
            link = link_dict["Link"]
            output_dict = get_article(link)

            content = [link_dict["ID"], output_dict["Title"], output_dict["Link"], output_dict["Paragraph"]]
            writer.writerow(content)



if __name__ == "__main__":
    # # 連線到 Yahoo! 新聞 / 財金版
    # link = "https://tw.news.yahoo.com/finance/"
    # crawler_scrollDown_NTime(link, 3)


    # crawler_scrollDown_ToBottom()


    # link = "https://tw.news.yahoo.com/%E5%87%BA%E5%B8%AD%E8%BC%9D%E9%81%94%E5%8F%B0%E7%81%A3%E5%88%86%E5%85%AC%E5%8F%B8%E5%B0%BE%E7%89%99-%E9%BB%83%E4%BB%81%E5%8B%B3%E5%BC%B7%E8%AA%BF-%E6%BA%96%E5%82%99%E9%9D%9E%E5%B8%B8%E5%A4%9A%E7%B4%85%E5%8C%85-134055932.html"
    # get_article(link)


    
    # 獲取當前日期、時間
    current_date = str(datetime.now().date())
    current_time = str(datetime.now().time()).split(".")[0].replace(":", "-")
    current_date_time = current_date + "_" + current_time
    # print(current_date_time)

    filename_out = f"crawler_file/crawler_{current_date_time}.csv"
    crawler_output_csv(filename_out)