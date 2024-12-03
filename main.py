import uvicorn
from fastapi import FastAPI, UploadFile, File
import numpy as np 
import pickle
import pandas as pd 
from pydantic import BaseModel
from typing import Union 
from inference import ques_ans_url,single_url_translate,single_url_summary,test_completion_stream,single_pdf_summary,single_pdf_translate
import os 
import openai

os.environ['REQUESTS_CA_BUNDLE'] = 'ca-bundle.crt'  
openai.api_key = "EMPTY"
openai.api_base = "https://aml-llm-models.icp.infineon.com/v1"

token ='eyJhbGciOiJSUzI1NiIsImtpZCI6Ik52TWQ1WXNQd0JvOTJEd2xIbm9TTXNISTh4byIsInBpLmF0bSI6Im5idjMifQ.eyJzY29wZSI6Im9wZW5pZCBlbWFpbCBwcm9maWxlIiwiY2xpZW50X2lkIjoiTUlBTUlfREVTQU1MIiwiaXNzIjoiaHR0cHM6Ly9zc28uaW5maW5lb24uY29tIiwibGFzdE5hbWUiOiJHb2VsIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImNvdW50cnlTaG9ydCI6IklOIiwiZGlzcGxheU5hbWUiOiJHb2VsIERha3NoaSAoRENJIERDUCBUUCBDTSkiLCJjcmVhdGVUaW1lU3RhbXAiOiIyMDIzMTIwNzA2MDIxNS4wMDBaIiwibWFpbERvbWFpblR5cGUiOiJPSyIsImF1ZCI6Ik1JQU1JX0RFU0FNTCIsImZpcnN0TmFtZSI6IkRha3NoaSIsIm9iamVjdEdVSUQiOiI2QzVCMUQ0RS01MTgzLTRDMzUtQUU2Qy0zMjQ2OTM1RkExNTkiLCJjb21wYW55IjoiSW5maW5lb24gVGVjaG5vbG9naWVzIFNlbWljb25kdWN0b3IgSW5kaWEgUHJpdmF0ZSBMaW1pdGVkIiwicmVhbG0iOiJJTlQiLCJlbWFpbCI6IkRha3NoaS5Hb2VsQGluZmluZW9uLmNvbSIsImhhc1JlZ2lzdGVyZWQiOmZhbHNlLCJ1c2VybmFtZSI6ImdvZWxkIiwiZXhwIjoxNzE2ODg1Mzc4fQ.qPjixC3cU8Gs6gndSjZvf_D5AAaAFy4umj5M422T3HsYWhYewZ6Ib0w4ya_aCSTvge_CdcS9E508wP8OUD4y5YcQdtMeCPSQFfSs9kgfgdyOjATPR3wZyum9vuFCe6vG8f-9Qtn4Rfa0L_5WR-LRcD08YRoGDPR3TI3GvKHZcJP3stSdPiLIHAh5S4AlMo2r8RUPEyc20unIcjOnHxjAQbzxtCm6Qks3forFgmyDxM6bFcv8XLGAwqfCfgmTck_RCR2W-HsLHU4cMhEq-xgO2uRxdC6xflsL-VlvMv4S5wNrgVB_PYr6XgdIlBLcZX99U7-R0yojr16qRKuYpuouOw'
headers = {
    'Authorization': f"Bearer {token}",
}

app=FastAPI()

class Item(BaseModel):
    summarize: Union[str, None] = None
    translate: Union[str, None] = None
    qa: Union[str, None] = None
    language: Union[str, None] = None
    query: Union[str, None] = None
    url:Union[str, None] = None

@app.post('/')

def upload_url_path(data:Item):
    # Do here your stuff with the file
    output=''
    # output_summarize+=single_pdf_summary(file.filename,headers)
    print("summarize:",data.summarize,"translate:",data.translate,"language:",data.language,"qa:",data.qa,"query:",data.query,"url:",data.url)
    if(data.summarize=="True"):
        print("understood this")
        output+=single_url_summary(data.url,headers)
    if(data.translate=="True"):
        output+=single_url_translate(data.url,data.language,headers)
    if(data.qa=="True"):
        output+=ques_ans_url(data.url,data.query,headers)
    
    return {'message': output}


if __name__ == '__main__':
    uvicorn.run(app,host='127.0.0.1',port=8000)