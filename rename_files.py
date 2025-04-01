import os
import re

def clean_filename(filename):
    # 分離檔名和副檔名
    name, ext = os.path.splitext(filename)
    # 移除檔案開頭的數字和點
    cleaned = re.sub(r'^\d+\.', '', name)
    # 移除結尾的 " - 常見問題 - 玉山銀行.md"
    cleaned = re.sub(r' - 常見問題 - 玉山銀行\.md$', '.md', cleaned)
    # 移除結尾的 " - 玉山銀行.md"
    cleaned = re.sub(r' - 玉山銀行\.md$', '.md', cleaned)
    cleaned = re.sub(r'[\uff08\uff09\u3001\u3010\u3011\uff5c\uff0f\u003f\uff1f\u0028\u0029\u300c\u300d\uff0c\uff1b\uff0e\u002d\uff05+＋～\uff5e&＆》《\uff1a:\s\.~。]', '', cleaned)
    # 移除驚嘆號
    cleaned = re.sub(r'[!！]', '', cleaned)
    # 移除多餘的空格
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned + ext

def rename_files():
    directory = "d:/project/HelloGPT/Result/玉山信用卡文件"
    files = sorted(os.listdir(directory))
    
    for filename in files:
        if filename.endswith('.md'):
            new_filename = clean_filename(filename)
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            
            try:
                os.rename(old_path, new_path)
                print(f"已重命名: {filename} -> {new_filename}")
            except Exception as e:
                print(f"重命名失敗 {filename}: {str(e)}")

if __name__ == "__main__":
    rename_files()
