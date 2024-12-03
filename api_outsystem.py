import uvicorn
from fastapi import FastAPI, UploadFile, File
import numpy as np 
import pickle
import pandas as pd 
from pydantic import BaseModel
from typing import Union 
from inference import single_url_translate,test_completion_stream,single_url_summary
import os 
import openai

os.environ['REQUESTS_CA_BUNDLE'] = 'ca-bundle.crt'  
openai.api_key = "EMPTY"
openai.api_base = "https://aml-llm-models.icp.infineon.com/v1"

token ='eyJhbGciOiJSUzI1NiIsImtpZCI6Ik52TWQ1WXNQd0JvOTJEd2xIbm9TTXNISTh4byIsInBpLmF0bSI6Im5idjMifQ.eyJzY29wZSI6Im9wZW5pZCBlbWFpbCBwcm9maWxlIiwiY2xpZW50X2lkIjoiTUlBTUlfREVTQU1MIiwiaXNzIjoiaHR0cHM6Ly9zc28uaW5maW5lb24uY29tIiwibGFzdE5hbWUiOiJHb2VsIiwiZW1haWxfdmVyaWZpZWQiOiJ0cnVlIiwiY291bnRyeVNob3J0IjoiSU4iLCJkaXNwbGF5TmFtZSI6IkdvZWwgRGFrc2hpIChEQ0kgRENQIFRQIENNKSIsImNyZWF0ZVRpbWVTdGFtcCI6IjIwMjMxMjA3MDYwMjE1LjAwMFoiLCJtYWlsRG9tYWluVHlwZSI6Ik9LIiwiYXVkIjoiTUlBTUlfREVTQU1MIiwiZmlyc3ROYW1lIjoiRGFrc2hpIiwib2JqZWN0R1VJRCI6IjZDNUIxRDRFLTUxODMtNEMzNS1BRTZDLTMyNDY5MzVGQTE1OSIsImNvbXBhbnkiOiJJbmZpbmVvbiBUZWNobm9sb2dpZXMgU2VtaWNvbmR1Y3RvciBJbmRpYSBQcml2YXRlIExpbWl0ZWQiLCJyZWFsbSI6IklOVCIsImVtYWlsIjoiRGFrc2hpLkdvZWxAaW5maW5lb24uY29tIiwiaGFzUmVnaXN0ZXJlZCI6ImZhbHNlIiwidXNlcm5hbWUiOiJnb2VsZCIsImV4cCI6MTcwODUxMjQxNn0.Q97mLEk-cZrm3yyOS8HljTGQpIOc-zvN5tYGb2vkQrdU0-4SOd3wj7IxK6wf_hC-lGTrDTZOfgXIAXbbZbDrkZVgUuWFPRx1aFEuYRxOhnNiaEegVY35NJEJxdMwytauoqVcku1NNktnu6FV5rvqvMetAIuH9J9IhP4KsESXUzI-lsYoLZU3GPn5Pw5mArWikmP50Hm7wXy0n8r8GRoJHsLtkfS6NfsHVxLjkmtFOiN5RMTYBCLaYs4rrAD7cSwy4hVqRRHH6kqSji4eYLF9v7KvqRFGdvBwGPjfDgkKJgzjTxQvmvLuw7AHVEugZm_S8cm9L4wdDQiHqDcq4A_CsA'
headers = {
    'Authorization': f"Bearer {token}",
}

app=FastAPI()

@app.post('/url_path/')

async def upload_url_path(summarize:str,translate:str,url:str):
    # Do here your stuff with the file
    output_summarize=''
    output_translate=''
    # output_summarize+=single_pdf_summary(file.filename,headers)
    if(summarize=="True"):
        print("understood this")
        output_summarize+=single_url_summary(url,headers)
    if(translate=="True"):
        output_translate+=single_url_translate(url,'french',headers)
    
    return {'Generated_summary': output_summarize,
            'Generated_translate': output_translate}

if __name__ == '__api_outsystem__':
    uvicorn.run(app,host='127.0.0.1',port=8000)