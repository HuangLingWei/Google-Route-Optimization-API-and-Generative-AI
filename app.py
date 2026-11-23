import streamlit as st
import json
import pandas as pd
from extractor import extract_logistics_info
from geocoder import get_coordinates
from optimizer import call_route_optimization

st.set_page_config(page_title="AI 智慧物流路徑優化器", layout="wide")

st.title("📦 AI 智慧物流路徑優化系統 (觀音區驗證版)")
st.markdown("輸入配送需求，系統將自動處理時區 (UTC+8) 與每站 30 分鐘停留時間。")

# --- 側邊欄：系統狀態 ---
with st.sidebar:
    st.header("⚙️ 系統參數")
    st.info("時區：Asia/Taipei\n\n停留時間：30 min/站\n\n⚖️ 優化目標：總距離最小化")
    if st.button("清除快取並重整"):
        st.rerun()

# --- 主介面：輸入區 ---
user_input = st.text_area(
    "請輸入配送需求：", 
    placeholder="例如：我有一台貨車載重 500kg，預計早上 09:00 從桃園市觀音區光明路43號出發...",
    height=150
)

# --- 核心邏輯區 (按鈕保護) ---
submit_button = st.button("🚀 開始規劃路線", type="primary")

if submit_button:
    if not user_input.strip(): # 加上 .strip() 確保使用者沒有只輸入空白鍵
        st.warning("⚠️ 請先輸入配送需求內容！")
    else:
        with st.spinner("🤖 AI 正在解析語意並計算最佳路徑..."):
            try:
                # 1. 解析語意
                raw_data_obj = extract_logistics_info(user_input)

                # 判斷回傳值類型並處理時間
                if isinstance(raw_data_obj, dict):
                    extracted_time = raw_data_obj.get('start_time', "none")
                    raw_data = raw_data_obj  
                else:
                    extracted_time = getattr(raw_data_obj, 'start_time', "none")
                    # 使用 Pydantic 的 model_dump() 替代已棄用的 dict()
                    raw_data = raw_data_obj.model_dump() if hasattr(raw_data_obj, 'model_dump') else raw_data_obj.dict()

                # 顯示時間邏輯
                if not extracted_time or extracted_time == "none":
                    final_start_time = "08:30"
                    st.info("ℹ️ 偵測到未指定時間，已自動套用預設出發時間：08:30")
                else:
                    final_start_time = extracted_time

                # 2. 轉換座標
                with st.status("🗺️ 正在進行地理編碼轉換...", expanded=False) as status:
                    for s in raw_data['shipments']:
                        coords = get_coordinates(s['location_name'])
                        if coords:
                            s['lat'], s['lng'] = coords['lat'], coords['lng']
                            st.write(f"✅ {s['location_name']} -> 已轉換")
                        else:
                            # 👇 防呆機制 1：找不到配送地址時，亮紅燈並停止執行
                            status.update(label="地理編碼失敗！", state="error", expanded=True)
                            st.error(f"🛑 找不到配送點座標：【{s['location_name']}】\n\n👉 請嘗試刪除幾鄰、幾里，或簡化地址後再試一次！")
                            st.stop()
                    
                    for v in raw_data['vehicles']:
                        coords = get_coordinates(v['start_location'])
                        if coords:
                            v['lat'], v['lng'] = coords['lat'], coords['lng']
                            st.write(f"✅ 起點：{v['start_location']} -> 已轉換")
                        else:
                            # 👇 防呆機制 2：找不到出發地址時，亮紅燈並停止執行
                            status.update(label="地理編碼失敗！", state="error", expanded=True)
                            st.error(f"🛑 找不到出發點座標：【{v['start_location']}】\n\n👉 請嘗試簡化地址後再試一次！")
                            st.stop()
                    status.update(label="地理編碼轉換完成！", state="complete", expanded=False)

                # 3. 呼叫 Google Optimization API
                result = call_route_optimization(raw_data, user_start_time=final_start_time)

                # 4. 顯示結果
                if result and "routes" in result:
                    st.balloons()
                    st.success(f"✨ 路徑優化成功！共動用 {len(result['routes'])} 台車輛。")

                    vehicle_tabs = st.tabs([f"車輛: {r.get('vehicle_label', f'車輛 {i+1}')}" for i, r in enumerate(result["routes"])])

                    for idx, route in enumerate(result["routes"]):
                        with vehicle_tabs[idx]:
                            col1, col2 = st.columns([1, 1])
                            
                            visits = route.get("visits", [])
                            if not visits:
                                st.write("此車輛無分配任務。")
                                continue

                            with col1:
                                st.subheader("📋 配送行程清單")
                                
                                metrics = route.get('metrics', {})
                                dist_km = metrics.get('travel_distance_meters', 0) / 1000
                                duration_min = metrics.get('total_duration', "0s").replace('s','')
                                st.write(f"**總里程:** {dist_km:.2f} km | **總耗時:** {int(float(duration_min)/60)} 分鐘")

                                v_id = route.get('vehicle_label', 'Truck')
                                v_start_addr = next((v['start_location'] for v in raw_data['vehicles'] if v['id'] == v_id), "起點")
                                
                                st.write(f"**出發點:** {v_start_addr}")
                                
                                for i, visit in enumerate(visits):
                                    from datetime import datetime, timedelta
                                    utc_time = datetime.strptime(visit['start_time'], "%Y-%m-%dT%H:%M:%SZ")
                                    tw_time = utc_time + timedelta(hours=8)
                                    arrival_str = tw_time.strftime("%H:%M")
                                    
                                    st.write(f"**第 {i+1} 站:** {visit['shipment_label']} (預計 {arrival_str} 抵達)")
                                
                                st.write(f"**回程點:** {v_start_addr}")

                                # --- 生成 Google Maps 連結 ---
                                v_info = next((v for v in raw_data['vehicles'] if v['id'] == v_id), raw_data['vehicles'][0])
                                vehicle_pos = f"{v_info['lat']},{v_info['lng']}"
                                
                                shipment_lookup = {s['id']: f"{s['lat']},{s['lng']}" for s in raw_data['shipments']}
                                waypoint_list = [shipment_lookup[v['shipment_label']] for v in visits]
                                
                                all_stops = [vehicle_pos] + waypoint_list + [vehicle_pos]
                                maps_link = f"https://www.google.com/maps/dir/{'/'.join(all_stops)}"
                                
                                st.divider()
                                st.link_button(f"🗺️ 開啟 {v_id} 導航路線", maps_link)

                            with col2:
                                st.subheader("📍 配送地圖預覽")
                                map_points = [{"lat": v_info['lat'], "lon": v_info['lng'], "name": "起點"}]
                                for v in visits:
                                    s_info = next(s for s in raw_data['shipments'] if s['id'] == v['shipment_label'])
                                    map_points.append({"lat": s_info['lat'], "lon": s_info['lng'], "name": s_info['id']})
                                
                                st.map(pd.DataFrame(map_points))

                            st.divider()
                            with st.expander("🔍 查看詳細 JSON 運算數據"):
                                st.json(result)
                else:
                     st.error("❌ 規劃失敗。可能是地點解析錯誤、超載或 API 額度限制。")
                     with st.expander("查看回傳數據"):
                         st.json(result)

            except Exception as e:
                st.error(f"❌ 發生錯誤，請檢查系統或 API 狀態：\n\n{e}")