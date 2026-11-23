import os
from datetime import datetime, timedelta
import pytz
from google.maps import routeoptimization_v1 as routeopt
from dotenv import load_dotenv

load_dotenv()

# 確保抓得到專案 ID
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

def call_route_optimization(data, user_start_time=None):
    if not PROJECT_ID:
        return {"ERROR": {"message": "找不到專案ID，請確認 .env 檔案有設定 GOOGLE_CLOUD_PROJECT"}}

    client = routeopt.RouteOptimizationClient()
    
    # --- 1. 處理時區與開始時間 ---
    tw_tz = pytz.timezone('Asia/Taipei')
    now_tw = datetime.now(tw_tz)
    
    if not user_start_time or user_start_time == "none":
        start_time_str = "08:30"
    else:
        start_time_str = user_start_time

    today_str = now_tw.strftime('%Y-%m-%d')
    
    # 💡 修正1：直接保留 datetime 物件，不要使用 .isoformat()，讓套件自動處理
    global_start_dt = tw_tz.localize(datetime.strptime(f"{today_str} {start_time_str}", "%Y-%m-%d %H:%M"))
    global_end_dt = global_start_dt + timedelta(hours=14)

    model = {
        "shipments": [],
        "vehicles": [],
        "global_start_time": global_start_dt, # 直接傳遞 datetime
        "global_end_time": global_end_dt      # 直接傳遞 datetime
    }

    # --- 2. 轉換訂單 (含停留時間 30 分鐘) ---
    for s in data['shipments']:
        if s.get('due_time') and s['due_time'] != "none":
            arrival_end_dt = tw_tz.localize(
                datetime.strptime(f"{today_str} {s['due_time']}", "%Y-%m-%d %H:%M")
            )
        else:
            arrival_end_dt = global_end_dt
            
        arrival_start_dt = global_start_dt

        model["shipments"].append({
            "label": str(s['id']), # 強制轉字串
            "deliveries": [{
                "arrival_location": {"latitude": float(s['lat']), "longitude": float(s['lng'])}, # 強制轉浮點數
                "duration": "1800s", # 💡 修正2：Google API 規定必須是帶有 's' 的字串
                "time_windows": [{
                    "start_time": arrival_start_dt, # 直接傳遞 datetime
                    "end_time": arrival_end_dt      # 直接傳遞 datetime
                }]
            }],
            "load_demands": {
                "weight": {"amount": int(s['weight'])}
            }
        })

    # --- 3. 轉換車輛 ---
    for v in data['vehicles']:
        model["vehicles"].append({
            "label": str(v['id']), # 強制轉字串
            "start_location": {"latitude": float(v['lat']), "longitude": float(v['lng'])},
            "end_location": {"latitude": float(v['lat']), "longitude": float(v['lng'])},
            "cost_per_kilometer": 1.0,
            "load_limits": {"weight": {"max_load": int(v['capacity'])}}
        })

    parent = f"projects/{PROJECT_ID}"
    request = routeopt.OptimizeToursRequest(parent=parent, model=model)

    try:
        response = client.optimize_tours(request=request)
        # 💡 修正3：使用更安全的 dict 轉換方法
        return type(response).to_dict(response)
    except Exception as e:
        print(f"Optimization API 執行錯誤：{e}")
        return {"ERROR": {"message": str(e)}}