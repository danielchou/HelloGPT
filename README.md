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
```

### `fubon.2.py`

此腳本用於處理富邦保險的 FAQ 資料，將 XML 檔案轉換為 TXT 和 Markdown 格式。

- **功能**: 
  - 從 XML 檔案中提取 `<item>` 元素下的 `<title>` 和 `<description>` 內容
  - 將內容轉換為純文字 (TXT) 格式
  - 使用 `html2text` 套件將內容轉換為完整的 Markdown 格式
  - 保留原始 HTML 結構，包括連結、圖片、表格等

- **檔案路徑**:
  - XML 來源目錄：`Result/fubon/faq`
  - TXT 輸出目錄：`Result/fubon/faq/txt`
  - Markdown 輸出目錄：`Result/fubon/faq/md`

- **依賴**: `html2text`

**安裝依賴**:

```bash
pip install html2text
```

**執行方式**:

```bash
python fubon.2.py
```

**輸出格式**:
- TXT 檔案：純文字格式，移除所有 HTML 標籤
- Markdown 檔案：保留原始 HTML 結構，包括標題、連結、圖片、表格等

**檔案名稱處理**:
- 移除所有標點符號（包括半形和全形標點符號）
- 檔案名稱長度限制為最多 30 個字元
- 空格會被替換為底線
- 如果清理後的檔名為空，則使用 "untitled" 作為預設值
