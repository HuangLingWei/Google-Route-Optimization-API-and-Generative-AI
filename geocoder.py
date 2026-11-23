import googlemaps
import os
import streamlit as st  # 加入 st 來顯示前端警告
from dotenv import load_dotenv

load_dotenv()

# 初始化 Google Maps 客戶端
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

def get_coordinates(address: str):
    """將地址字串轉換為經緯度"""
    try:
        # 調用 Geocoding API
        geocode_result = gmaps.geocode(address, language='zh-TW')
        
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            return {
                "lat": location['lat'],
                "lng": location['lng'],
                "formatted_address": geocode_result[0]['formatted_address']
            }
        else:
            # 找不到地址時，直接在前端亮起黃燈警告！
            st.warning(f"⚠️ Google Maps 找不到這個地址的座標：{address}")
            return None
            
    except Exception as e:
        # API 發生其他錯誤時亮紅燈
        st.error(f"❌ 地理編碼 API 發生錯誤: {e}")
        return None