import uvicorn
from fastapi import FastAPI, UploadFile, File
import numpy as np 
import pickle
import pandas as pd 
from pydantic import BaseModel
from typing import Union 
from inference import single_url_translate,single_url_summary,test_completion_stream,single_pdf_summary,single_pdf_translate
import os 
import openai

os.environ['REQUESTS_CA_BUNDLE'] = 'ca-bundle.crt'  
openai.api_key = "EMPTY"
openai.api_base = "https://aml-llm-models.icp.infineon.com/v1"

token ='eyJhbGciOiJSUzI1NiIsImtpZCI6Ik52TWQ1WXNQd0JvOTJEd2xIbm9TTXNISTh4byIsInBpLmF0bSI6Im5idjMifQ.eyJzY29wZSI6Im9wZW5pZCBlbWFpbCBwcm9maWxlIiwiY2xpZW50X2lkIjoiTUlBTUlfREVTQU1MIiwiaXNzIjoiaHR0cHM6Ly9zc28uaW5maW5lb24uY29tIiwibGFzdE5hbWUiOiJHb2VsIiwiZW1haWxfdmVyaWZpZWQiOiJ0cnVlIiwiY291bnRyeVNob3J0IjoiSU4iLCJkaXNwbGF5TmFtZSI6IkdvZWwgRGFrc2hpIChEQ0kgRENQIFRQIENNKSIsImNyZWF0ZVRpbWVTdGFtcCI6IjIwMjMxMjA3MDYwMjE1LjAwMFoiLCJtYWlsRG9tYWluVHlwZSI6Ik9LIiwiYXVkIjoiTUlBTUlfREVTQU1MIiwiZmlyc3ROYW1lIjoiRGFrc2hpIiwib2JqZWN0R1VJRCI6IjZDNUIxRDRFLTUxODMtNEMzNS1BRTZDLTMyNDY5MzVGQTE1OSIsImNvbXBhbnkiOiJJbmZpbmVvbiBUZWNobm9sb2dpZXMgU2VtaWNvbmR1Y3RvciBJbmRpYSBQcml2YXRlIExpbWl0ZWQiLCJyZWFsbSI6IklOVCIsImVtYWlsIjoiRGFrc2hpLkdvZWxAaW5maW5lb24uY29tIiwiaGFzUmVnaXN0ZXJlZCI6ImZhbHNlIiwidXNlcm5hbWUiOiJnb2VsZCIsImV4cCI6MTcwOTYzNDk1NH0.OBXsOgcI0OVhoWInaJIiSx1cJedEA_ZDcu3JGaiCDtXb_SNxidnjtGpj1h0m_tOwubgc_JBhRfeaRsTYWMgf8vYeAWM38bAbD1xgYsWcdBHPqzqXUeIt1YwzdcbVWW6gguCpzHvp12aGK1-TJIN3FuFsr9XLpChi6KTVKwRcW--GddAfG8DBCXNB8go87Ag0TLfrfnVifwHOYm7FBudGXWjJ1D7_sWsW15JmiuTolK0OsFAZIhifkcoXT8Tz66xEICgf8Z0P1Xz1nR3etwjpa6WUu2heD-kNYF0n8unkp3F0dVkyHaCoJdcQFvWWmfCWZ1A0GkS196Miri7aQNCQcQ'
headers = {
    'Authorization': f"Bearer {token}",
}

app=FastAPI()

class Item(BaseModel):
    # summarize: Union[str, None] = None
    # translate: Union[str, None] = None
    language: Union[str, None] = None
    url:Union[str, None] = None

@app.post('/')
def index(data:Item):
    output_translate=''
    output_translate+=single_url_translate(data.url,data.language,headers)
    return {'message':output_translate}

if __name__ == '__translate_api__':
    uvicorn.run(app,host='127.0.0.1',port=8001)