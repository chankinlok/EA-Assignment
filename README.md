# 連登論壇

以 Flask 製作的繁體中文論壇首頁，提供分類瀏覽、最新／熱門排序、主題搜尋與發文表單。

## 啟動

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

開啟 http://127.0.0.1:5000。

主題資料目前存放在記憶體中，重新啟動應用程式後會還原為示範資料。