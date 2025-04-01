"""
主程式入口
"""
from scraper import CteeScraper

def main():
    # 範例：如果想要在找到特定網址時中斷
    stop_url = "https://www.ctee.com.tw/news/20241205700593-430201"
    scraper = CteeScraper(max_pages=10, stop_url=stop_url)
    news_data = scraper.get_news()

if __name__ == "__main__":
    main()
