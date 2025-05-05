# fubon.2.py
import os
import xml.etree.ElementTree as ET
import re
import html
import html2text

# XML 檔案來源目錄 (大寫 Result)
SOURCE_DIR = "Result/fubon/faq"
# TXT 輸出目錄 (使用 faq/txt 子目錄)
TXT_OUTPUT_DIR = os.path.join(SOURCE_DIR, "txt")
# Markdown 輸出目錄 (使用 faq/md 子目錄)
MD_OUTPUT_DIR = os.path.join(SOURCE_DIR, "md")

def sanitize_filename(filename):
    """移除或替換檔名中的無效字元，包括所有標點符號（半形和全形）"""
    # 定義全形標點符號列表
    full_width_punctuation = '_，。、；：「」『』【】（）？！～＠＃＄％＾＆＊－＋＝｛｝［］｜＼／＜＞'
    
    # 先移除全形標點符號
    for char in full_width_punctuation:
        filename = filename.replace(char, '')
    
    # 再移除所有半形標點符號和特殊字元
    sanitized = re.sub(r'[^\w\s]', "", filename)
    
    # 將多個空格替換為單個底線
    sanitized = re.sub(r'\s+', '', sanitized)
    
    # 移除檔名開頭和結尾的底線
    sanitized = sanitized.strip('_')
    
    # 確保檔名不為空
    if not sanitized:
        return "untitled"
    
    # 限制檔名長度為 30 個字元
    max_len = 500
    return sanitized[:max_len] if len(sanitized) > max_len else sanitized

def clean_html(raw_html):
    """移除 HTML 標籤並解碼 HTML 實體"""
    # 解碼 HTML 實體 (例如 &lt; -> <)
    text = html.unescape(raw_html)
    # 移除所有 HTML 標籤
    clean_text = re.sub(r'<.*?>', '', text)
    # 移除多餘的空白符
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    return clean_text

def html_to_markdown(html_content, title):
    """將 HTML 內容轉換為完整的 Markdown 格式"""
    # 使用 html2text 套件將 HTML 轉換為 Markdown
    h = html2text.HTML2Text()
    h.ignore_links = False  # 保留連結
    h.ignore_images = False  # 保留圖片
    h.ignore_tables = False  # 保留表格
    h.body_width = 0  # 不自動換行
    h.unicode_snob = True  # 使用 Unicode 字元
    h.skip_internal_links = False  # 不跳過內部連結
    
    # 轉換 HTML 內容
    markdown_body = h.handle(html_content)
    
    # 建立 Markdown 內容，加上標題
    markdown_content = f"# {title}\n\n{markdown_body}"
    
    return markdown_content

def process_xml_file(xml_filepath):
    """處理單個 XML 檔案"""
    try:
        # 解析 XML
        tree = ET.parse(xml_filepath)
        root = tree.getroot()

        # 建立輸出目錄 (以 XML 檔名命名，不含副檔名)
        base_filename = os.path.splitext(os.path.basename(xml_filepath))[0]
        
        # TXT 輸出目錄
        txt_output_subdir = os.path.join(TXT_OUTPUT_DIR, base_filename)
        os.makedirs(txt_output_subdir, exist_ok=True)
        
        # Markdown 輸出目錄
        md_output_subdir = os.path.join(MD_OUTPUT_DIR, base_filename)
        os.makedirs(md_output_subdir, exist_ok=True)
        
        print(f"處理中: {xml_filepath}")
        print(f"-> TXT 輸出至目錄: {txt_output_subdir}")
        print(f"-> MD 輸出至目錄: {md_output_subdir}")

        items_processed = 0
        # 遍歷所有 <item> 元素 (假設 item 在根目錄下或常見的 channel/item 結構)
        # 根據實際 XML 結構可能需要調整 findall 路徑
        items = root.findall('.//item') # 查找所有後代的 item 元素
        if not items:
             items = root.findall('item') # 如果 XML 結構是 <root><item>...</item></root>

        if not items:
            print(f"警告: 在 {xml_filepath} 中找不到 <item> 元素。請檢查 XML 結構。")
            # 嘗試查找其他可能的父元素，例如 <channel>
            channel = root.find('channel')
            if channel is not None:
                items = channel.findall('item')
            
        if not items:
             print(f"警告: 在 {xml_filepath} 中仍然找不到 <item> 元素。跳過此檔案。")
             return


        for item in items:
            title_element = item.find('title')
            description_element = item.find('description')

            if title_element is not None and description_element is not None:
                title = title_element.text.strip() if title_element.text else "untitled"
                description = description_element.text.strip() if description_element.text else ""

                # 清理 description
                cleaned_description = clean_html(description)

                # 清理 title 作為檔名
                safe_filename = sanitize_filename(title)
                if not safe_filename: # 如果清理後檔名為空，給一個預設值
                    safe_filename = f"item_{items_processed + 1}"
                
                # TXT 檔案路徑
                output_txt_path = os.path.join(txt_output_subdir, f"{safe_filename}.txt")
                
                # Markdown 檔案路徑
                output_md_path = os.path.join(md_output_subdir, f"{safe_filename}.md")
                
                # 建立 Markdown 內容
                markdown_content = html_to_markdown(description, title)

                try:
                    # 寫入 TXT 檔案 (原有功能)
                    with open(output_txt_path, 'w', encoding='utf-8') as f:
                        f.write(cleaned_description)
                        
                    # 寫入 Markdown 檔案 (新增功能)
                    with open(output_md_path, 'w', encoding='utf-8') as f:
                        f.write(markdown_content)
                        
                    items_processed += 1
                except OSError as e:
                    print(f"錯誤: 無法寫入檔案: {e}")
                except Exception as e:
                     print(f"寫入檔案時發生未知錯誤: {e}")


            else:
                print(f"警告: 在 {xml_filepath} 中的某個 item 缺少 title 或 description。")
        
        print(f"完成: {xml_filepath}, 共處理 {items_processed} 個項目。")

    except ET.ParseError as e:
        print(f"錯誤: 無法解析 XML 檔案 {xml_filepath}: {e}")
    except FileNotFoundError:
        print(f"錯誤: 找不到檔案 {xml_filepath}")
    except Exception as e:
        print(f"處理檔案 {xml_filepath} 時發生未知錯誤: {e}")

def main():
    """主函數，查找並處理所有 XML 檔案"""
    print(f"開始處理 {SOURCE_DIR} 中的 XML 檔案...")
    
    # 確保 TXT 和 Markdown 輸出目錄存在
    os.makedirs(TXT_OUTPUT_DIR, exist_ok=True)
    os.makedirs(MD_OUTPUT_DIR, exist_ok=True)
    print(f"XML 來源目錄: {SOURCE_DIR}")
    print(f"TXT 輸出目錄: {TXT_OUTPUT_DIR}")
    print(f"Markdown 輸出目錄: {MD_OUTPUT_DIR}")
    
    xml_files_found = 0
    for filename in os.listdir(SOURCE_DIR):
        if filename.startswith("faqData") and filename.endswith(".xml"):
            xml_filepath = os.path.join(SOURCE_DIR, filename)
            if os.path.isfile(xml_filepath): # 確保是檔案而不是目錄
                 xml_files_found += 1
                 process_xml_file(xml_filepath)

    if xml_files_found == 0:
         print(f"在 {SOURCE_DIR} 中找不到任何 'faqData*.xml' 檔案。")
    else:
        print(f"\n所有 XML 檔案處理完成。共找到 {xml_files_found} 個 XML 檔案。")


if __name__ == "__main__":
    main()