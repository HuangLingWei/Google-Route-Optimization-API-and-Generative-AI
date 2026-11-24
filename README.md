# 🌍 大數據驅動之跨國就業決策支援與 AI 職涯導師系統
    ### Global Placement & Salary Prediction System with Gemini AI Mentor

    ![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
    ![Flask](https://img.shields.io/badge/Backend-Flask-black?logo=flask)
    ![AI](https://img.shields.io/badge/LLM-Gemini_2.5_Flash-4285F4?logo=google)
    ![Frontend](https://img.shields.io/badge/Frontend-HTML5_/_Chart.js-E34F26)

    本專案結合**大數據分析、機器學習薪資預測模型、購買力平價 (PPP) 換算**與 **Google Gemini 2.5 Flash 生成式
    AI**，打造一套協助青年跨國求職的決策支援系統。

    > ⚠️ **注意**：本專案先前暫存於 `digital_wallet_ltv_dataset` 倉庫，核心內容為教育與就業大數據之跨國薪資決策系統。

    ---

    ## ✨ 核心特色與功能

    1. **大數據薪資預測**：
       * 整合歷年跨國就業資料（CGPA、實習次數與品質、專業領域、外語與溝通能力、目標國家）。
       * 即時預估海外年薪（USD），並產出個人市場薪資分位數（PR 值）及常態分佈曲線。
    2. **多維度敏感度分析**：
       * 動態模擬「增加 1 次實習」或「提升 GPA 1.0」對預期年薪的邊際增益。
    3. **實質購買力 (PPP) 平價換算**：
       * 結合各國生活成本物價指數，將海外美金年薪換算為等同於台灣的實質購買力台幣（TWD），避免「名目高薪、實質貧窮」的求職盲點。
    4. **Gemini 2.5 Flash AI 職涯導師**：
       * 自動診斷履歷亮點，生成客製化的【優勢評估】、【弱點診斷】與【具體行動方針】。
    5. **反向目標探索機制**：
       * 輸入期望年薪（例如 8 萬美金），系統反向搜尋大數據中達到該薪資的求職者平均特質（CGPA、熱門國家、實習履歷分佈）。

    ---

    ## 📂 專案結構


  ├── 1-模型分析.ipynb              # 跨國薪資分佈圖表、特徵相關性與統計檢定
  ├── 2-互動工具.ipynb              # Jupyter Widgets 互動原型
  ├── server.py                   # Flask 後端伺服器 (包含預測邏輯與 Gemini API 調用)
  ├── index.html                  # 視覺化互動系統前端 (包含動態圖表與履歷填寫)
  ├── global_placement.csv        # 跨國求職原始數據集
  ├── placed_students_salary.csv  # 成功就業薪資資料集
  ├── requirements.txt            # 相依套件清單
  └── README.md


    ---

    ## 🛠️ 安裝與啟動教學

    ### 1. 下載並安裝相依套件
    ```bash
    git clone https://github.com/HuangLingWei/digital_wallet_ltv_dataset.git
    cd digital_wallet_ltv_dataset
    pip install -r requirements.txt

  2. 設定 Gemini API Key

  在專案根目錄建立 .env 檔案（或直接於環境變數配置）：

    GEMINI_API_KEY="你的_Google_Gemini_API_Key"

  3. 啟動 Flask 伺服器

    python server.py

  伺服器將在 http://127.0.0.1:5000 運行。

  4. 開啟前端介面

  使用瀏覽器打開 index.html 即可開始進行薪資預測與職涯模擬！
