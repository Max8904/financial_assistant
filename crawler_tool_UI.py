import time
import streamlit as st
from crawler import crawler_keyword_search

# 設定頁面配置，設定頁面標題
st.set_page_config(
    page_title= "新聞爬取工具"
)

st.title("新聞爬取工具")
search_content = st.text_input(label = "輸入想搜尋的主題", placeholder="e.g. 台積電、特斯拉...")
if (st.button("搜尋") and search_content != "") or search_content != "":
    # 根據搜尋的 keyword，返回相關的文章列表
    url = "https://tw.news.yahoo.com/finance/"
    link_list = crawler_keyword_search(url, search_content)

    st.subheader("搜尋到的相關新聞", divider='rainbow')
    # 印出各文章的相關資訊
    for link_dict in link_list:
        ID = link_dict["ID"]
        title = link_dict["Title"]
        link = link_dict["Link"]
        st.write(f"{ID + 1}. [{title}]({link})")

