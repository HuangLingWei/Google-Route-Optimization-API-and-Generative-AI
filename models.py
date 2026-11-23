from pydantic import BaseModel, Field
from typing import List, Optional

class ShipmentRequest(BaseModel):
    id: str = Field(description="訂單唯一識別碼，如：Order_01")
    location_name: str = Field(description="配送目的地的名稱或地址")
    weight: float = Field(description="貨物重量，單位為公斤")
    # 修改為 Optional 並設定預設值，增加強健性
    due_time: str = Field(default="none", description="最晚送達時間，格式為 HH:mm，若無則為 none")
    priority: int = Field(default=2, description="優先等級：1(高), 2(中), 3(低)")    

class VehicleRequest(BaseModel):
    id: str = Field(description="車輛代號，如：Truck_A")
    capacity: float = Field(description="最大載重限制，單位為公斤")
    start_location: str = Field(description="出發點地址或站點名稱")

class LogisticsExtraction(BaseModel):
    shipments: List[ShipmentRequest] = Field(description="提取到的所有訂單資訊")
    vehicles: List[VehicleRequest] = Field(description="提取到的所有車輛資訊")
    start_time: str = Field(
        default="none", 
        description="配送的出發時間，格式為 HH:mm (24小時制)。如果使用者沒提到，請填入 none"
    )