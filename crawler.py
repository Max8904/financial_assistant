# 載入 selenium 相關模組
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request as req
import bs4
import time
import csv
from datetime import datetime
from tqdm import tqdm
import json


# 設定 Chrome Driver 的執行檔路徑
options = Options()
# 設定 headless 模式 (不顯示瀏覽器運作畫面)
# options.add_argument("--headless")
options.chrome_executable_path = "D:/Python Project/financial_assistant/chromedriver.exe"
# 建立 Driver 物件實體，用程式操作瀏覽器運作
driver = webdriver.Chrome(options=options)

def crawler_scrollDown_NTime(link, times):
    # 連線到 Yahoo! 新聞 / 財金版
    driver.get(link)

    # 捲動視窗並等待瀏覽器載入更多內容
    n = 0
    while n < times:
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

def crawler_scrollDown_ToBottom(link):
    # 連線到 Yahoo! 新聞 / 財金版
    driver.get(link)

    # 捲動視窗並等待瀏覽器載入更多內容
    # 等待載入新內容
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@id='app']")))

    while True:
        # 記錄頁面高度
        last_height = driver.execute_script("return document.body.scrollHeight")

        # 捲動至底部
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 等待載入新內容
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//h3[@class='Mb(5px)']")))

        # 再次取得新的頁面高度
        new_height = driver.execute_script("return document.body.scrollHeight")

        # 如果新的頁面高度和之前的相同，表示已經到達底部，退出循環
        if new_height == last_height:
            break

    # 取得網頁內容
    page_source = driver.page_source

    # 使用 Beautiful Soup 解析 HTML
    soup = bs4.BeautifulSoup(page_source, 'html.parser')

    # 找到文章標題元素
    # title_elements = soup.find_all('li', class_='Pos(r) Lh(1.5) H(24px) Mb(8px)')
    # title_elements.extend(soup.find_all('h3', class_='Mb(5px)'))
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
            # link = href_value
            # if "https://" not in href_value:
            #     link = "https://tw.news.yahoo.com" + href_value
            link = "https://tw.news.yahoo.com" + href_value
            # print(link)

            link_dict = {"ID": i, "Title": title, "Link": link}
            link_list.append(link_dict)

    # print(link_list)
    return link_list

def crawler_Yahoo(link):
    requestData = """{"requests":{"g0":{"resource":"StreamService","operation":"read","params":{"ui":{"comments":true,"editorial_featured_count":1,"image_quality_override":true,"link_out_allowed":true,"ntk_bypassA3c":true,"pubtime_maxage":0,"relative_links":true,"show_comment_count":true,"smart_crop":true,"storyline_count":2,"storyline_enabled":true,"storyline_min":2,"summary":true,"thumbnail_size":100,"view":"mega","editorial_content_count":0,"finance_upsell_threshold":4},"category":"LISTID:a8a208bf-23e1-4950-8aba-8a8d1c0c2da5","forceJpg":true,"releasesParams":{"limit":20,"offset":0},"offnet":{"include_lcp":true},"use_content_site":true,"useNCP":true,"ads":{"ad_polices":true,"contentType":"video/mp4,application/x-shockwave-flash","count":25,"frequency":3,"inline_video":true,"pu":"https://tw.news.yahoo.com","se":5419954,"spaceid":2144404919,"start_index":1,"timeout":450,"type":"STRM","useHqImg":true,"useResizedImages":true},"batches":{"pagination":true,"size":20,"timeout":1300,"total":170},"enableAuthorBio":true,"max_exclude":0,"min_count":3,"service":{"specRetry":{"enabled":false}},"pageContext":{"site":"news","section":"finance","topic":"default","electionPageType":"default","electionTvType":"default","pageType":"minihome","renderTarget":"default"},"content_type":"section","ncpParams":{"body":{"gqlVariables":{"main":{"pagination":{"requestedCount":20,"contentOverrides":{"7ec60ff6-fab6-343b-bdf7-284506e7514d":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"8fc7caa0-6053-3fba-a151-4397c548254a":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"dc6839c5-11ea-353a-8499-30f50914d8cf":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"ba53e00a-73b9-3ea5-b512-37f29ca78484":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"ce2c8f3b-6abd-3633-9e4a-e7cbfa22e7c8":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"9c744572-a023-3eaf-8701-7e041f43ebe8":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"3efeecb3-b6dc-37ac-b1d2-279175939296":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"b13b63b5-5f94-3b19-8184-58f12c14b728":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"6fe342e2-0890-3a12-8fe3-f27cadb1f1c3":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"2d481caf-d166-301e-8b45-474118b5f41e":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"a3249a35-46b6-3f7b-bc11-c62b5e1ff858":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"a5a6ecc7-04a4-3956-8c7f-30e2831c5065":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"400d491d-d84b-37e2-82e4-91c97901ba26":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"783d0a5b-cc17-3bc7-8750-a1625ef31fc5":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"d66a5cad-025f-32eb-b14d-7dc475a10230":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"216788a7-aa81-398c-8d72-6ec60bffa060":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"e9f44ab8-a500-3353-b7d8-d8e439c60288":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"cad5f4fe-fe18-35ce-be6b-19c8136f9fda":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"238f9743-36aa-36f6-ba7f-70137841ecba":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"fae8ff21-5e9b-3fe9-a18d-24a17546099d":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"ab5d8430-1b41-3594-a100-67e4997d2145":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"4c2a4cbb-03ba-37a0-b443-976f0c79250b":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"363ee9ae-d261-3ce4-845b-07563c56136f":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"f6023048-ee81-4fb8-8d8d-b9cd180ce010":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"73195a29-afba-37a0-8050-7e4f76a4bf85":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"a9a2b100-a260-4c98-8835-b7ab917c45b4":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"3e8766d6-8ebd-3b83-a85b-0f710f2a4281":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"8a2cfc2d-b652-3cad-8966-c35473e50376":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"b2af510d-1254-3fa2-a981-7ba5bafd9b7a":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"f9144bc3-525a-3f95-9a30-7b83b1c7536a":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"e048b749-0c6c-3c02-b70c-1c6aaf81a538":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"1774563c-5910-3ceb-a1f4-e9a5bdd3521c":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"823b24a7-a5a7-3b46-95b5-f23910e58e78":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"6c4093e5-60f3-3306-8c3f-671ae2760b16":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"a699c379-36eb-3555-8036-99fce551f810":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"eb4ba695-5e58-3e14-a616-8e1a163e486b":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"116e6d97-2461-3df8-aa20-6abb9f9bcc49":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"418a79aa-9028-46a4-a393-d931dfd5105f":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"75641b37-463d-3934-a763-5197ecdab8e2":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"dd0de705-ea3b-34e3-827a-99ce69686680":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"7545a945-29e3-3270-953b-343e5efb6056":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"92b0e51f-1d41-376a-bc3a-9d734f859b3c":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"0c932b58-3e48-3fc9-9a85-982a1297a155":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"ed785146-c48e-3585-911c-c38341cbe610":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"96d8f598-3b64-3acc-9946-52855ddbe172":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"c5474ab8-50c7-3dfe-99b5-2f9a2c894e18":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"83575ffb-25e0-3424-a411-e59fc1f08aac":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"803a34d5-39ba-3c5d-a6e4-a9ed06a2aba0":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"a1a4326a-3c20-3cc2-83f0-993f5e11c466":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"0d152139-830a-3112-a576-3df539e9c449":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"245df971-2944-3a17-913b-aad0cca51d0f":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"b99750c5-0366-36f0-be61-51c37dc07473":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"b6ae6ee5-6204-3908-b9f1-0cc0a08c7f89":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"924cb8d3-a5aa-4237-a657-77ce2380488b":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"68efda5b-6675-3a3a-aafa-48077f294242":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"caf2bf47-f2af-3469-9d83-9c8d73a3fc3a":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"855fbef5-d7da-39b5-bf60-40717aa4bed0":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"b6081089-6916-3912-8881-32b5acc18b87":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"d917186e-94bd-3bfc-b0f4-1ec0473d3dae":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"0c071939-46c6-3e9c-9ca9-c2f4cdf86e68":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"093bf3a0-bdc7-3f6c-9224-290673f4ab3f":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"37af5015-9abc-34a4-9cd2-f6295d3325f0":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"93392a16-ec3c-39bb-987c-dd0dd0e5cf71":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"9b2d4d6c-2c3d-44e6-ab80-16518f232ced":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"5c09ff3a-0271-3fac-8e54-b22916b0d3ad":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"f27af463-46e8-3fd2-970e-a564e1d49a20":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"921412cc-66e0-3e2a-a820-b5d0c40982ca":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"78dc9210-f589-3e81-9ae1-791667cebfac":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"0678f5af-c799-3fe2-9ad3-f2f2c82d77dd":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"ace62879-b9d1-3511-9e0e-d07e2eb28498":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"16d59f76-21cd-3e75-a334-78115ace1201":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"e6ba95ae-d58c-3eb6-b119-fe5cb6128a46":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"01dc99ee-edca-3b4b-990e-6ca3d49b9a39":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"9ac04312-6119-3588-b5ed-12f3625dc988":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"b2955ab8-68de-3785-95d3-78357d766f5f":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"182e1b3d-0418-37d7-8592-88e8036e8486":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"60b94ba1-ae33-3fb9-99c1-a0128e58f1bb":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"31966810-83d9-3148-a405-d323bd0229cd":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"29863330-3113-3ebd-8f4d-ac9bffa3edec":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"8e6f5c44-43c1-345b-9198-58cf03b26fb7":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"9b672209-95c4-34f4-82c4-55c18f32bce2":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"7d778304-c465-32a4-834c-310845557d83":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"7805dac9-f3ad-302c-a03d-aeb1d9e7aa35":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"0a28c785-b33a-48e5-975e-70a71a62838f":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"b55d7d43-740e-30a5-ba22-d5ef5be70e21":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"fb238b7f-10f9-3e3c-910b-67013673a689":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"0d697eec-d087-383e-8077-b2b6c0a118d9":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"c2439d56-9a37-3bfe-9bf4-8be8229cfa6c":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"e7cd992a-9ab5-3d72-b7d5-4f593a6ff8ab":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"b4246feb-e50e-32f0-b4aa-db107f54c823":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"43353d5f-36a1-3c98-9c02-20fb2e0930c1":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"36ada6fc-963d-3273-94e3-211afbdb2bff":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"cd6c0603-f0a0-30a6-bf55-b18c853f33ed":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"056a1234-6067-39e6-a16f-6cf85f787a8d":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"03945464-f3dc-3fd0-ad1a-695bd774f3f4":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"a8a7057c-bba4-3ed9-9f91-274692d5040d":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"756f1846-215a-3abd-9538-84b14411037d":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"57201007-b744-32ea-8357-e85460407fd4":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"fe0a8187-e188-3f26-8ef2-2f3c27918ed2":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"8361120c-678c-3196-bb4e-d71ca44c3a81":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"142ffc1a-67d4-35ac-b1d2-427df4595ba4":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"c3daebe3-2388-3d92-bffc-86290098e525":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"9c128916-85a4-35ed-9956-2e4d482deaac":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"21817a84-f7ac-3863-b5fb-0090bfb92329":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"ec23112a-91ad-3e1e-a17d-c839ab34a68c":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"437bc430-20b6-3510-b288-83e570e396a4":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"66bac2f9-d3cf-326b-9210-724b5596ef0a":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"6e3d6942-7aaa-3a52-9b5f-07a131dcb1d3":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"dc692250-1b0c-32ff-abbf-cdfa3708e7f4":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"725c549d-94ee-3426-82b0-5326d5caa556":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"335646ba-9a29-4b6a-823c-d85928719109":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"397f1804-46f7-3c25-85b5-be958f7ee337":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"7c7ddd0a-4324-39a7-9f9f-fe01d35f696e":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"022e000b-65e1-3461-a118-fc08153a5505":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"c871b0de-2719-3e17-b0aa-c78c55100642":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"c49962af-bbbb-353b-bb6a-05e1ef11b3ce":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"7a71cc82-b323-3934-8ddd-848a88d3efbc":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"80a2413c-dfb9-3d84-9b7e-b674d0f26524":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"88747c16-1f35-39ce-8d28-44368ceec4b3":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"c7f80aa5-f290-3f93-84a9-12ea4e74ed0b":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"5f9e050d-c86e-3873-bde5-16f88cba51ba":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"f9da52be-6282-3408-9648-41f8ea12f677":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"8e341f45-4634-4ec2-ad9e-1d2d164a5060":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"929cd985-a756-3d31-9786-211647d5d8cd":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"17b33176-3f79-3c0f-beed-d1dc9449b2ba":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"6877a1b6-6585-3f3a-a7f5-46b44a5041ff":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"99a351f9-a52b-3f22-a9d4-04db917f74e6":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"ec065603-1f4e-4ca4-a75c-1d90a2300ff7":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"dbb41487-a2c2-3028-bc14-0f66876a3c75":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"},"845a954e-df67-312a-86c9-71d8abc5b698":{"list":"a8a208bf-23e1-4950-8aba-8a8d1c0c2da5"}},"remainingCount":130,"geminiToken":"{\"geminiDedupeToken\":\"ChM4MDE2Nzg1NzEzMDQ0NDkzMzEyEv0DCj4I3b-PARD5pK7y1qC7-C0Y14yKroOr1uk_IJHF28uwpa33fioJSGVybyBXYXJzMP_O0w84k_mjzPfgvpyLAQo4CN2_jwEQz6Ditev-9pQiGIj38OfF7qX7ZSDNhN-SmvGnqiMqBEF1ZGkwi-i9DzjayIHX35HBugkKSQjdv48BEJGP6KD0vIOl9gEYkY_ooPS8g6X2ASDthJ-W3_L66eoBKhFCdXp6RGFpbHkgV2lubmVyczD7rfUPOLOdivPZvrTCgwEKPAjdv48BEMbIoIfwzsD9ZxjP_OGbu5GOgGEgl7P6k4OchdBsKgdTYW1zdW5nMKrRhBA43cfIsL-6ioyGAQpNCN2_jwEQjq78g-u59LUrGK-a07jbnvPLzQEg2ZX4o-e6vMoVKhjkuK3oj6_pm7vkv6HkvIHmpa3os4flrokww__BDziD8fzSjd2ToFIKPAjdv48BELjes9_hxNKiMBiq0tShnPTogkMgh4jMwqfEi_H5ASoGU1VCQVJVMLfz-g84o4rQ2vbm4sTfAQpPCN2_jwEQ5pGk5t3Ztt0UGP7H86bV7cKO_wEghLfiw7CYlZvoASoY5aGU5oGp5Yqg77ya5bO25ba86L6y5aC0MIH2hA84zsmss83krt7OARITNDM0MTAxOTUwMzcwODM2Mjc1MhgHILLnygI\",\"adsStartIndex\":\"2\"}","uuids":"783d0a5b-cc17-3bc7-8750-a1625ef31fc5:STORY,43353d5f-36a1-3c98-9c02-20fb2e0930c1:STORY,01dc99ee-edca-3b4b-990e-6ca3d49b9a39:STORY,5f9e050d-c86e-3873-bde5-16f88cba51ba:STORY,a5a6ecc7-04a4-3956-8c7f-30e2831c5065:STORY,36ada6fc-963d-3273-94e3-211afbdb2bff:STORY,9ac04312-6119-3588-b5ed-12f3625dc988:STORY,d917186e-94bd-3bfc-b0f4-1ec0473d3dae:STORY,9c744572-a023-3eaf-8701-7e041f43ebe8:STORY,c5474ab8-50c7-3dfe-99b5-2f9a2c894e18:STORY,73195a29-afba-37a0-8050-7e4f76a4bf85:STORY,88747c16-1f35-39ce-8d28-44368ceec4b3:STORY,855fbef5-d7da-39b5-bf60-40717aa4bed0:STORY,99a351f9-a52b-3f22-a9d4-04db917f74e6:STORY,0d697eec-d087-383e-8077-b2b6c0a118d9:STORY,803a34d5-39ba-3c5d-a6e4-a9ed06a2aba0:STORY,929cd985-a756-3d31-9786-211647d5d8cd:STORY,9b672209-95c4-34f4-82c4-55c18f32bce2:STORY,16d59f76-21cd-3e75-a334-78115ace1201:STORY,a8a7057c-bba4-3ed9-9f91-274692d5040d:STORY,f9da52be-6282-3408-9648-41f8ea12f677:STORY,ed785146-c48e-3585-911c-c38341cbe610:STORY,d66a5cad-025f-32eb-b14d-7dc475a10230:STORY,29863330-3113-3ebd-8f4d-ac9bffa3edec:STORY,0c071939-46c6-3e9c-9ca9-c2f4cdf86e68:STORY,116e6d97-2461-3df8-aa20-6abb9f9bcc49:STORY,c2439d56-9a37-3bfe-9bf4-8be8229cfa6c:STORY,c871b0de-2719-3e17-b0aa-c78c55100642:STORY,238f9743-36aa-36f6-ba7f-70137841ecba:STORY,fe0a8187-e188-3f26-8ef2-2f3c27918ed2:STORY,7a71cc82-b323-3934-8ddd-848a88d3efbc:STORY,83575ffb-25e0-3424-a411-e59fc1f08aac:STORY,80a2413c-dfb9-3d84-9b7e-b674d0f26524:STORY,056a1234-6067-39e6-a16f-6cf85f787a8d:STORY,f27af463-46e8-3fd2-970e-a564e1d49a20:STORY,e7cd992a-9ab5-3d72-b7d5-4f593a6ff8ab:STORY,ce2c8f3b-6abd-3633-9e4a-e7cbfa22e7c8:STORY,17b33176-3f79-3c0f-beed-d1dc9449b2ba:STORY,f9144bc3-525a-3f95-9a30-7b83b1c7536a:STORY,b2af510d-1254-3fa2-a981-7ba5bafd9b7a:STORY,8fc7caa0-6053-3fba-a151-4397c548254a:STORY,0c932b58-3e48-3fc9-9a85-982a1297a155:STORY,60b94ba1-ae33-3fb9-99c1-a0128e58f1bb:STORY,7805dac9-f3ad-302c-a03d-aeb1d9e7aa35:STORY,dc6839c5-11ea-353a-8499-30f50914d8cf:STORY,96d8f598-3b64-3acc-9946-52855ddbe172:STORY,ace62879-b9d1-3511-9e0e-d07e2eb28498:STORY,6877a1b6-6585-3f3a-a7f5-46b44a5041ff:STORY,ab5d8430-1b41-3594-a100-67e4997d2145:STORY,8e6f5c44-43c1-345b-9198-58cf03b26fb7:STORY,03945464-f3dc-3fd0-ad1a-695bd774f3f4:STORY,725c549d-94ee-3426-82b0-5326d5caa556:STORY,37af5015-9abc-34a4-9cd2-f6295d3325f0:STORY,e9f44ab8-a500-3353-b7d8-d8e439c60288:STORY,0678f5af-c799-3fe2-9ad3-f2f2c82d77dd:STORY,dc692250-1b0c-32ff-abbf-cdfa3708e7f4:STORY,142ffc1a-67d4-35ac-b1d2-427df4595ba4:STORY,92b0e51f-1d41-376a-bc3a-9d734f859b3c:STORY,b99750c5-0366-36f0-be61-51c37dc07473:STORY,b6081089-6916-3912-8881-32b5acc18b87:STORY,9c128916-85a4-35ed-9956-2e4d482deaac:STORY,397f1804-46f7-3c25-85b5-be958f7ee337:STORY,093bf3a0-bdc7-3f6c-9224-290673f4ab3f:STORY,e6ba95ae-d58c-3eb6-b119-fe5cb6128a46:STORY,dbb41487-a2c2-3028-bc14-0f66876a3c75:STORY,363ee9ae-d261-3ce4-845b-07563c56136f:STORY,f6023048-ee81-4fb8-8d8d-b9cd180ce010:STORY,fae8ff21-5e9b-3fe9-a18d-24a17546099d:STORY,8a2cfc2d-b652-3cad-8966-c35473e50376:STORY,eb4ba695-5e58-3e14-a616-8e1a163e486b:STORY,57201007-b744-32ea-8357-e85460407fd4:STORY,0a28c785-b33a-48e5-975e-70a71a62838f:STORY,a699c379-36eb-3555-8036-99fce551f810:STORY,216788a7-aa81-398c-8d72-6ec60bffa060:STORY,68efda5b-6675-3a3a-aafa-48077f294242:STORY,a3249a35-46b6-3f7b-bc11-c62b5e1ff858:STORY,21817a84-f7ac-3863-b5fb-0090bfb92329:STORY,9b2d4d6c-2c3d-44e6-ab80-16518f232ced:STORY,7d778304-c465-32a4-834c-310845557d83:STORY,924cb8d3-a5aa-4237-a657-77ce2380488b:STORY,31966810-83d9-3148-a405-d323bd0229cd:STORY,335646ba-9a29-4b6a-823c-d85928719109:STORY,5c09ff3a-0271-3fac-8e54-b22916b0d3ad:STORY,b6ae6ee5-6204-3908-b9f1-0cc0a08c7f89:STORY,ec23112a-91ad-3e1e-a17d-c839ab34a68c:STORY,93392a16-ec3c-39bb-987c-dd0dd0e5cf71:STORY,3efeecb3-b6dc-37ac-b1d2-279175939296:STORY,418a79aa-9028-46a4-a393-d931dfd5105f:STORY,caf2bf47-f2af-3469-9d83-9c8d73a3fc3a:STORY,fb238b7f-10f9-3e3c-910b-67013673a689:STORY,7c7ddd0a-4324-39a7-9f9f-fe01d35f696e:STORY,ec065603-1f4e-4ca4-a75c-1d90a2300ff7:STORY,2d481caf-d166-301e-8b45-474118b5f41e:STORY,cad5f4fe-fe18-35ce-be6b-19c8136f9fda:STORY,022e000b-65e1-3461-a118-fc08153a5505:STORY,182e1b3d-0418-37d7-8592-88e8036e8486:STORY,1774563c-5910-3ceb-a1f4-e9a5bdd3521c:STORY,921412cc-66e0-3e2a-a820-b5d0c40982ca:STORY,66bac2f9-d3cf-326b-9210-724b5596ef0a:STORY,b55d7d43-740e-30a5-ba22-d5ef5be70e21:STORY,8e341f45-4634-4ec2-ad9e-1d2d164a5060:STORY,6fe342e2-0890-3a12-8fe3-f27cadb1f1c3:STORY,b13b63b5-5f94-3b19-8184-58f12c14b728:STORY,c49962af-bbbb-353b-bb6a-05e1ef11b3ce:STORY,75641b37-463d-3934-a763-5197ecdab8e2:STORY,7545a945-29e3-3270-953b-343e5efb6056:STORY,400d491d-d84b-37e2-82e4-91c97901ba26:VIDEO,6c4093e5-60f3-3306-8c3f-671ae2760b16:VIDEO,823b24a7-a5a7-3b46-95b5-f23910e58e78:STORY,e048b749-0c6c-3c02-b70c-1c6aaf81a538:STORY,845a954e-df67-312a-86c9-71d8abc5b698:STORY,6e3d6942-7aaa-3a52-9b5f-07a131dcb1d3:STORY,a9a2b100-a260-4c98-8835-b7ab917c45b4:STORY,8361120c-678c-3196-bb4e-d71ca44c3a81:VIDEO,7ec60ff6-fab6-343b-bdf7-284506e7514d:STORY,ba53e00a-73b9-3ea5-b512-37f29ca78484:STORY,c3daebe3-2388-3d92-bffc-86290098e525:STORY,dd0de705-ea3b-34e3-827a-99ce69686680:STORY,437bc430-20b6-3510-b288-83e570e396a4:STORY,b2955ab8-68de-3785-95d3-78357d766f5f:STORY,756f1846-215a-3abd-9538-84b14411037d:STORY,c7f80aa5-f290-3f93-84a9-12ea4e74ed0b:STORY,a1a4326a-3c20-3cc2-83f0-993f5e11c466:STORY,b4246feb-e50e-32f0-b4aa-db107f54c823:STORY,0d152139-830a-3112-a576-3df539e9c449:STORY,4c2a4cbb-03ba-37a0-b443-976f0c79250b:STORY,78dc9210-f589-3e81-9ae1-791667cebfac:STORY,cd6c0603-f0a0-30a6-bf55-b18c853f33ed:STORY,3e8766d6-8ebd-3b83-a85b-0f710f2a4281:STORY,245df971-2944-3a17-913b-aad0cca51d0f:STORY"}}}}}}}},"context":{"feature":"oathPlayer,enableEvPlayer,enableGAMAds,enableGAMEdgeToEdge,videoDocking","bkt":"news-TW-zh-Hant-TW-def","crumb":"m3BeptrhSf3","device":"desktop","intl":"tw","lang":"zh-Hant-TW","partner":"none","prid":"2h00c7tirkomq","region":"TW","site":"news","tz":"Asia/Taipei","ver":"2.3.2669","ecma":"modern"}}"""

    request = req.Request(link, headers={
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
    }, data = requestData)

    with req.urlopen(request) as response:
        data = json.load(response)
        print(data)
    
    
    # 紀錄所有文章的 ID、標題、連結
    link_list = []
    # # 取得網頁中新聞的標題
    # for i, title_element in enumerate(title_elements):
    #     title = title_element.text.strip()
    #     # print(title)

    #     # 直接使用 BeautifulSoup 的方法找到 <a> 元素
    #     a_element = title_element.find('a')

    #     # 確認是否找到了 <a> 元素
    #     if a_element:
    #         # 如果找到，取得 href 屬性的值
    #         href_value = a_element.get('href')
    #         # link = href_value
    #         # if "https://" not in href_value:
    #         #     link = "https://tw.news.yahoo.com" + href_value
    #         link = "https://tw.news.yahoo.com" + href_value
    #         # print(link)

    #         link_dict = {"ID": i, "Title": title, "Link": link}
    #         link_list.append(link_dict)

    # print(link_list)
    return link_list

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
        link_list = crawler_scrollDown_ToBottom(link)

        # link = "https://tw.news.yahoo.com/_td-news/api/resource?bkt=news-TW-zh-Hant-TW-def&crumb=m3BeptrhSf3&device=desktop&ecma=modern&feature=oathPlayer%2CenableEvPlayer%2CenableGAMAds%2CenableGAMEdgeToEdge%2CvideoDocking&intl=tw&lang=zh-Hant-TW&partner=none&prid=0qj7ma9iri3j5&region=TW&site=news&tz=Asia%2FTaipei&ver=2.3.2669"
        # # link_list = crawler_scrollDown_NTime(link, 3)
        # link_list = crawler_Yahoo(link)

        print("Crawler Processing ... ")
        for link_dict in tqdm(link_list):
            link = link_dict["Link"]
            output_dict = get_article(link)

            content = [link_dict["ID"], output_dict["Title"], output_dict["Link"], output_dict["Paragraph"]]
            writer.writerow(content)

def crawler_keyword_search(link, keyword):
    """
    輸入特定關鍵字，
    回傳搜尋到的相關文章
    """
    # 連線到 Yahoo! 新聞 / 財金版
    driver.get(link)

    # 等待網頁加載完畢
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "ybar-sbq")))

    # 取得搜尋框
    search_bar = driver.find_element(By.XPATH, "//input[@class='_yb_11ieitq _yb_1tg75ri    ' and @id='ybar-sbq']")
    search_bar.send_keys(Keys.CONTROL + "a")  # 清空搜尋框中的內容
    search_bar.send_keys(keyword)
    search_bar.send_keys(Keys.ENTER)

    # 等待網頁加載完畢
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "Col1-0-SearchTitle-Proxy")))
    

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
            link = "https://tw.news.yahoo.com/" + href_value
            # print(link)

            link_dict = {"ID": i, "Title": title, "Link": link}
            link_list.append(link_dict)

    # print(link_list)
    return link_list


if __name__ == "__main__":
    # # 連線到 Yahoo! 新聞 / 財金版
    # link = "https://tw.news.yahoo.com/finance/"
    # crawler_scrollDown_NTime(link, 3)


    # crawler_scrollDown_ToBottom()


    # link = "https://tw.news.yahoo.com/%E5%87%BA%E5%B8%AD%E8%BC%9D%E9%81%94%E5%8F%B0%E7%81%A3%E5%88%86%E5%85%AC%E5%8F%B8%E5%B0%BE%E7%89%99-%E9%BB%83%E4%BB%81%E5%8B%B3%E5%BC%B7%E8%AA%BF-%E6%BA%96%E5%82%99%E9%9D%9E%E5%B8%B8%E5%A4%9A%E7%B4%85%E5%8C%85-134055932.html"
    # get_article(link)


    
    # # 獲取當前日期、時間
    # current_date = str(datetime.now().date())
    # current_time = str(datetime.now().time()).split(".")[0].replace(":", "-")
    # current_date_time = current_date + "_" + current_time
    # # print(current_date_time)

    # filename_out = f"crawler_file/crawler_{current_date_time}.csv"
    # crawler_output_csv(filename_out)

    link = "https://tw.news.yahoo.com/finance/"
    keyword = "台積電"
    crawler_keyword_search(link, keyword)