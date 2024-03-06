import streamlit as st
import time

st.set_page_config(
    page_title= "新聞爬取工具"
)

st.title("新聞爬取工具")

search_content = st.text_input(label = "輸入想搜尋的主題", placeholder="e.g. 台積電、特斯拉...")
if st.button("搜尋"):
    bar = st.progress(0)
    for i in range(100):
        bar.progress(i + 1, f"目前進度 {i + 1} %")
        time.sleep(0.05)
    bar.progress(100, "搜尋完成")

    st.write("搜尋到的新聞網址")
    url = "https://tw.news.yahoo.com/%E4%BF%84%E7%83%8F%E4%BA%A4%E6%8F%9B%E6%95%B8%E7%99%BE%E5%90%8D%E6%88%B0%E4%BF%98-%E9%96%8B%E6%88%B0%E4%BE%86%E7%AC%AC50%E6%AC%A1%E6%8F%9B%E5%9B%9A-134746621.html"


