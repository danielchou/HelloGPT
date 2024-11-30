from bs4 import BeautifulSoup
import html2text
from urllib.parse import urljoin, urlparse
from selenium.webdriver.chrome.options import Options
import random
from collections import namedtuple


def get_random_user_agent():
    # 這裡列出一些常用的 User-Agent
    user_agents = [
        # Windows Chrome
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        # Windows Firefox
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
        # Windows Edge
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        # Mac Chrome
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        # Mac Firefox
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0",
        # Mac Safari
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15"
    ]
    return random.choice(user_agents)


# 初始化chrome瀏覽器的基本設定
def init_chrome_option():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)  # 防止程序完成後自動關閉
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 關閉提示
    chrome_options.add_argument(f'user-agent={get_random_user_agent()}')  # 設置 User-Agent
    # 其他有用的設置
    chrome_options.add_experimental_option("detach", True)  # 保持瀏覽器開啟
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 關閉提示
    chrome_options.add_experimental_option('useAutomationExtension', False)  # 關閉自動化提示
    # 如果需要隱藏"Chrome正受到自動測試軟件的控制"這個提示
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    return chrome_options


# 使用一個字典來存儲標籤和相應的不想要的 class 列表
def remove_elements_by_class(soup, tag, unwanted_classes):
    for class_name in unwanted_classes:
        for element in soup.find_all(tag, class_=class_name):
            element.decompose()

def remove_elements_by_text(soup, tag, unwanted_texts):
    for text in unwanted_texts:
        for element in soup.find_all(tag):
            if text in element.get_text():
                element.decompose()

def keep_elements_by_class(soup, tag, wanted_classes):
    # 找到並保留想要的元素
    wanted_elements = []
    for class_name in wanted_classes:
        for element in soup.find_all(tag, class_=class_name):
            wanted_elements.append(element.extract())

    # 移除其他不想要的元素
    for element in soup.find_all(tag):
        element.decompose()

    # 將保留的元素重新插入到原始位置
    for element in wanted_elements:
        soup.append(element)

def is_under_specific_url(base_url, href, specific_url):
    specific_path = urlparse(specific_url).path
    href_path = urlparse(href).path
    return href_path.startswith(specific_path)


def find_all_links(soup, base_url, except_urls=[]):
    links = []
    i_token, i_except = 0 , 0
    for link in soup.find_all('a', href=True):
        href = link['href']
        # title = link.get('title', '')  # 獲取 title 屬性，如果沒有則返回空字符串

        if '#' in href:
            i_token += 1
            continue  # 排除包含#符號的鏈接

        full_url = urljoin(base_url, href)
        if except_urls != []:
            if full_url in except_urls:
                i_except += 1
                continue  # 排除特定的網址

        links.append(full_url)
        # links[title] = full_url
    print(f"排除掉#連結有：{i_token}、已爬過的有：{i_except}")
    return links



def extractor(html_content, unwanted_tags = [], unwanted_elements = {}, unwanted_texts={}, wanted_elements = {}):
    soup = BeautifulSoup(html_content, 'html.parser')
    title_tag = soup.find('title')
    title = title_tag.get_text(strip=True) if title_tag else ''
    title = title.replace('?', '？')
    title = title.replace('/','／')

    # 找到 <meta> 標籤中 name 屬性為 "description" 的標籤，並提取內容出來
    meta_description = soup.find('meta', attrs={'name': 'description'})
    meta_description_text = meta_description['content'] if meta_description and 'content' in meta_description.attrs else ''
    
    if unwanted_tags != []:
        # 移除腳本和樣式標籤/
        for script_or_style in soup(unwanted_tags):
            script_or_style.decompose()
    
    if unwanted_elements != {}:
        # 移除不想要的元素
        for tag, classes in unwanted_elements.items():
            remove_elements_by_class(soup, tag, classes)

    if wanted_elements != {}:
        # 保留想要的元素並移除其他不想要的元素
        for tag, classes in wanted_elements.items():
            keep_elements_by_class(soup, tag, classes)

    if unwanted_texts != {}:
        # 保留想要的元素並移除其他不想要的元素
        for tag, text in unwanted_texts.items():
            remove_elements_by_text(soup, tag, text)

    


    # 將 HTML 轉換為 Markdown
    h = html2text.HTML2Text()
    h.ignore_links = True  # 保留鏈接
    h.ignore_images = True
    h.ignore_mailto_links = True
    markdown_text = h.handle(str(soup))

    # 提取文字內容
    text = soup.get_text(separator=' ', strip=True)
    # text = '\n'.join(soup.stripped_strings)
    # elements = soup.find_all(['a', lambda tag: not tag.name])
    # text = ''
    # for element in elements:
    #     if element.name == 'a':
    #         # text += f'<a href="{element.get("href")}" target="_blank">{element.get_text()}</a>'
    #         text += f'{element.get_text()}，網址是:[{ element.get("href") }]\n'
    #     else:
    #         text += element.get_text()
    text = text.replace('。', '。\n')

    # 創建一個具有命名字段的元組
    ExtractResult = namedtuple('ExtractResult', ['soup2', 'title', 'meta_description', 'extract_text', 'markdown_text'])
    # 使用 namedtuple 創建一個包含結果的元組
    result = ExtractResult(soup, title, meta_description_text, text, markdown_text)

    return result