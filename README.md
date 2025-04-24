# HelloGPT
## 初衷
  
- 透過實作方式了解OpenAI運作方式。

## 安裝
1. 首先要透過pip安裝openai套件，目前版本是1.6.0
```
pip install openai
```

## 爬蟲腳本

### `crawl.fubon.py`

此腳本用於抓取富邦銀行網站上的常見問題 (FAQ) XML 檔案。

- **功能**: 從指定 URL 範圍下載 XML 檔案。
- **URL 來源**: `https://www.fubon.com/banking/FAQ_Data//faq/index_data/faqData{2~18}.xml`
- **儲存位置**: `result/fubon/faq/`
- **依賴**: `requests` (詳見 `requirements.txt`)

**執行方式**:

```bash
python crawl.fubon.py
