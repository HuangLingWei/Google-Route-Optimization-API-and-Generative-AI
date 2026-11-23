import json
import webbrowser # 用於自動開啟瀏覽器
from extractor import extract_logistics_info
from geocoder import get_coordinates
from optimizer import call_route_optimization

def generate_maps_link(optimized_result, raw_data):
    """
    從優化結果中提取座標並生成 Google Maps 路線連結
    格式：https://www.google.com/maps/dir/起點/經由點1/經由點2/.../終點
    """
    if not optimized_result or "routes" not in optimized_result:
        return None

    # 取得第一條路線（目前測試只有一台車）
    route = optimized_result["routes"][0]
    
    # 建立地點對照表 (透過 shipment_label 找座標)
    shipment_coords = {s['id']: (s['lat'], s['lng']) for s in raw_data['shipments']}
    vehicle_coords = {v['id']: (v['lat'], v['lng']) for v in raw_data['vehicles']}
    
    # 1. 收集路點：起點 -> 配送點1 -> 配送點2 ... -> 終點
    # 找出這台車的初始位置
    v_label = route.get("vehicle_label", "Truck_A")
    start_pos = f"{vehicle_coords[v_label][0]},{vehicle_coords[v_label][1]}"
    
    waypoints = []
    for visit in route.get("visits", []):
        label = visit.get("shipment_label")
        if label in shipment_coords:
            lat, lng = shipment_coords[label]
            waypoints.append(f"{lat},{lng}")
    
    # 2. 組合 URL
    base_url = "https://www.google.com/maps/dir/"
    all_stops = [start_pos] + waypoints + [start_pos] # 假設最後回原點
    final_url = base_url + "/".join(all_stops)
    
    return final_url

def run_logistics_pipeline():
    print("="*30)
    print("AI 物流路徑優化系統")
    print("="*30)
    
    user_text = input("\n請輸入您的配送需求：\n")
    
    if not user_text.strip():
        # 測試用預設文字
        user_text = "我有一台貨車從觀音工業區出發，要送三件貨到..."

    print("\n[Step 1] 正在解析語意...")
    raw_data = extract_logistics_info(user_text)
    
    # --- 提取開始時間 ---
    # 假設 LogisticsExtraction 模型中有 start_time 欄位
    # 如果 LLM 沒抓到，raw_data.get('start_time') 會是 None
    user_specified_time = raw_data.get('start_time') 
    if not user_specified_time or user_specified_time == "none":
        print("💡 偵測到未指定開始時間，將預設為 08:30 出發")
        user_specified_time = "08:30"
    else:
        print(f"⏰ 偵測到出發時間：{user_specified_time}")
        final_start_time = user_specified_time

    print("[Step 2] 正在轉換經緯度...")
    for shipment in raw_data['shipments']:
        coords = get_coordinates(shipment['location_name'])
        if coords:
            shipment['lat'], shipment['lng'] = coords['lat'], coords['lng']

    for vehicle in raw_data['vehicles']:
        coords = get_coordinates(vehicle['start_location'])
        if coords:
            vehicle['lat'], vehicle['lng'] = coords['lat'], coords['lng']


    print("[Step 3] 正在計算最佳化路線...")
    # --- 將時間參數傳入 optimizer ---
    optimized_result = call_route_optimization(raw_data, user_start_time=user_specified_time)

    if optimized_result and "routes" in optimized_result:
        print(f"\n✅ 優化完成！共動用 {len(optimized_result['routes'])} 台車輛。")
        
        for idx, route in enumerate(optimized_result["routes"]):
            v_id = route.get('vehicle_label', f'Vehicle_{idx+1}')
            print(f"\n--- 🚚 {v_id} 的配送計畫 ---")
            
            # 調用原本的 generate_maps_link（要先確保該函式能處理特定 route）
            maps_url = generate_maps_link(route, raw_data) 
            
            if maps_url:
                print(f"📍 Google Maps 路線連結：\n{maps_url}")
                
                # 只有一台車，直接問是否開啟；多台車則顯示編號
                choice = input(f"是否開啟 {v_id} 的瀏覽器路線？(y/n): ")
                if choice.lower() == 'y':
                    webbrowser.open(maps_url)
    else:
        print("❌ 計算失敗或無有效路徑。")

if __name__ == "__main__":
    run_logistics_pipeline()