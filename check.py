import google.generativeai as genai

# 請貼上你 66324 專案的無敵金鑰
MY_API_KEY = "GEMINI_API_KEY"
genai.configure(api_key=MY_API_KEY)

print("🔍 正在連線至 Google 伺服器，查詢此金鑰可用的模型清單...\n")

try:
    # 直接跟 Google 索取清單
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            # 把前面的 'models/' 濾掉，只印出我們需要的名字
            print(f"✅ 可用名稱：{m.name.replace('models/', '')}")
            
    print("\n🎉 查詢成功！請從上面挑選一個名稱貼到你的程式碼裡。")
except Exception as e:
    print("❌ 查詢失敗：", e)