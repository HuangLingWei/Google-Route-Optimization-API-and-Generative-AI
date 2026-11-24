 🚚 AI 智慧物流路徑優化系統
    ### Vehicle Routing System Integrating Google Route Optimization API and Generative AI

    ![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
    ![LangChain](https://img.shields.io/badge/LLM-LangChain_%2B_Gemini-1C3C3C?logo=langchain)
    ![Google Maps](https://img.shields.io/badge/API-Google_Route_Optimization-4285F4?logo=googlemaps)
    ![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit)

    本專案結合 **大型語言模型 (Google Gemini via LangChain)** 與 **Google Cloud Route Optimization
    API**，使用者只需以自然語言輸入物流調度需求，系統即可自動解析地址、車輛限制與時窗，計算出最短行車距離與最佳停靠順序，並一鍵產出
    Google Maps 導航連結。

    ---

    ## 🔄 系統架構流程

    > **Diagram exceeds terminal width (141 > 133 cols)**
    > Displayed as code block. Widen terminal to view inline.

    ```mermaid
    flowchart LR
        A[使用者自然語言輸入<br>配送需求與車輛資訊] --> B[Gemini LLM<br>LangChain 結構化抽取]
        B --> C[Google Geocoding API<br>地址轉經緯度座標]
        C --> D[Google Route Optimization API<br>限制式最佳化路徑運算]
        D --> E[Streamlit 儀表板呈現<br>& Google Maps 導航 URL]
  ──────
  ✨ 核心功能

  • 自然語言派車：輸入「貨車載重 500kg，早上 09:00 從觀音區光明路出發至...」，AI 自動提取站點、載重與時限。
  • 精準地理編碼：結合 Google Maps Geocoding API 自動補正台灣地址經緯度。
  • 限制式車輛路徑規劃 (VRP)：自動考量時區 (Asia/Taipei)、固定卸貨停留時間 (30 分鐘/站) 與車輛載重，達到總里程最小化。
  • 多介面支援：
      • Web 儀表板 (app.py)：基於 Streamlit 的即時互動規劃介面。
      • CLI / 自動化指令 (main.py)：快速測試並直接開啟 Google Maps 多點導航。

  ──────
  📂 專案檔案清單

    ├── app.py              # Streamlit Web 視覺化系統
    ├── main.py             # 命令列主程式 (自動生成 Maps 多點路徑)
    ├── extractor.py        # LangChain + Gemini 語意提取模組
    ├── geocoder.py         # Google Maps 地址轉經緯度模組
    ├── optimizer.py        # Route Optimization API 呼叫與回傳解析
    ├── models.py           # Pydantic 資料模型與結構驗證
    ├── requirements.txt    # 系統相依套件
    ├── .env.example        # 環境變數設定範本 (請勿直接上傳 .env)
    └── README.md
  ──────
  🚀 快速上手

  1. 安裝套件

    pip install -r requirements.txt

  2. 環境變數配置

  複製 .env.example 為 .env，並填入您的 API 金鑰與 GCP 專案：

    GEMINI_API_KEY=你的_Gemini_API_Key
    GOOGLE_CLOUD_PROJECT=你的_GCP_Project_ID
    GOOGLE_APPLICATION_CREDENTIALS=你的_服務帳戶密鑰_路徑.json
    GOOGLE_MAPS_API_KEY=你的_Google_Maps_API_Key

  3. 啟動系統

  • 啟動 Web 介面 (推薦)：

    streamlit run app.py

  • 執行 CLI 測試：

    python main.py
