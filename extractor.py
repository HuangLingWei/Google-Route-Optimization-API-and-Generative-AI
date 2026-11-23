import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from models import LogisticsExtraction
from geocoder import get_coordinates
from optimizer import call_route_optimization
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

load_dotenv(override=True)

# 1. 初始化模型
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro",GEMINI_API_KEY="key", temperature=0)

# 2. 設定 JSON 解析器
parser = JsonOutputParser(pydantic_object=LogisticsExtraction)

def extract_logistics_info(user_input: str):
    """將自然語言配送需求轉換為結構化資料"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一位專業物流調度專家。請從使用者的描述中提取訂單與車輛資訊。\n{format_instructions}"),
        ("user", "{user_input}")
    ])
    
    chain = prompt | llm | parser
    
    return chain.invoke({
        "user_input": user_input, 
        "format_instructions": parser.get_format_instructions()
    })