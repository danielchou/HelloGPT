# fubon.2.py
import os
import xml.etree.ElementTree as ET
import re
import html

# XML 檔案來源目錄
SOURCE_DIR = "result/fubon/faq"
# 輸出根目錄 (與來源相同)
OUTPUT_DIR = SOURCE_DIR

def sanitize_filename(filename):
    """移除或替換檔名中的無效字元"""
    # 移除基本無效字元: \ / : * ? " < > |
    sanitized = re.sub(r'[\\/*?:"<>|]', "", filename)
    # 將多個空格替換為單個底線
    sanitized = re.sub(r'\s+', '_', sanitized)
    # 移除檔名開頭和結尾的點和底線
    sanitized = sanitized.strip('._')
    # 限制檔名長度 (可選，以防萬一)
    max_len = 100 
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

def process_xml_file(xml_filepath):
    """處理單個 XML 檔案"""
    try:
        # 解析 XML
        tree = ET.parse(xml_filepath)
        root = tree.getroot()

        # 建立輸出目錄 (以 XML 檔名命名，不含副檔名)
        base_filename = os.path.splitext(os.path.basename(xml_filepath))[0]
        output_subdir = os.path.join(OUTPUT_DIR, base_filename)
        os.makedirs(output_subdir, exist_ok=True)
        print(f"處理中: {xml_filepath} -> 輸出至目錄: {output_subdir}")

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
                
                output_txt_path = os.path.join(output_subdir, f"{safe_filename}.txt")

                # 寫入 TXT 檔案
                try:
                    with open(output_txt_path, 'w', encoding='utf-8') as f:
                        f.write(cleaned_description)
                    items_processed += 1
                except OSError as e:
                    print(f"錯誤: 無法寫入檔案 {output_txt_path}: {e}")
                except Exception as e:
                     print(f"寫入檔案時發生未知錯誤 {output_txt_path}: {e}")


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