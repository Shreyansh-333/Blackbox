import openai
import os
from langchain_community.document_loaders import SeleniumURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.document_loaders import WebBaseLoader
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS


os.environ['REQUESTS_CA_BUNDLE'] = 'ca-bundle.crt'  
openai.api_key = "EMPTY"
openai.api_base = "https://aml-llm-models.icp.infineon.com/v1"

token ='eyJhbGciOiJSUzI1NiIsImtpZCI6Ik52TWQ1WXNQd0JvOTJEd2xIbm9TTXNISTh4byIsInBpLmF0bSI6Im5idjMifQ.eyJzY29wZSI6Im9wZW5pZCBlbWFpbCBwcm9maWxlIiwiY2xpZW50X2lkIjoiTUlBTUlfREVTQU1MIiwiaXNzIjoiaHR0cHM6Ly9zc28uaW5maW5lb24uY29tIiwibGFzdE5hbWUiOiJHb2VsIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImNvdW50cnlTaG9ydCI6IklOIiwiZGlzcGxheU5hbWUiOiJHb2VsIERha3NoaSAoRENJIERDUCBUUCBDTSkiLCJjcmVhdGVUaW1lU3RhbXAiOiIyMDIzMTIwNzA2MDIxNS4wMDBaIiwibWFpbERvbWFpblR5cGUiOiJPSyIsImF1ZCI6Ik1JQU1JX0RFU0FNTCIsImZpcnN0TmFtZSI6IkRha3NoaSIsIm9iamVjdEdVSUQiOiI2QzVCMUQ0RS01MTgzLTRDMzUtQUU2Qy0zMjQ2OTM1RkExNTkiLCJjb21wYW55IjoiSW5maW5lb24gVGVjaG5vbG9naWVzIFNlbWljb25kdWN0b3IgSW5kaWEgUHJpdmF0ZSBMaW1pdGVkIiwicmVhbG0iOiJJTlQiLCJlbWFpbCI6IkRha3NoaS5Hb2VsQGluZmluZW9uLmNvbSIsImhhc1JlZ2lzdGVyZWQiOmZhbHNlLCJ1c2VybmFtZSI6ImdvZWxkIiwiZXhwIjoxNzE2ODg1Mzc4fQ.qPjixC3cU8Gs6gndSjZvf_D5AAaAFy4umj5M422T3HsYWhYewZ6Ib0w4ya_aCSTvge_CdcS9E508wP8OUD4y5YcQdtMeCPSQFfSs9kgfgdyOjATPR3wZyum9vuFCe6vG8f-9Qtn4Rfa0L_5WR-LRcD08YRoGDPR3TI3GvKHZcJP3stSdPiLIHAh5S4AlMo2r8RUPEyc20unIcjOnHxjAQbzxtCm6Qks3forFgmyDxM6bFcv8XLGAwqfCfgmTck_RCR2W-HsLHU4cMhEq-xgO2uRxdC6xflsL-VlvMv4S5wNrgVB_PYr6XgdIlBLcZX99U7-R0yojr16qRKuYpuouOw'
headers = {
    'Authorization': f"Bearer {token}",
}

def test_completion_stream(prompt,message):  
    model='llm70b'  
    res = openai.Completion.create(  
        model=model,  
        prompt=prompt,  
        messages=message,
        max_tokens=4096,  
        stream=False,  
        temperature=0.7,  
        headers=headers 
    )
    # for chunk in res:  
    #     print(chunk["choices"][0]["text"], end="", flush=True)  
    return res.choices[0]["text"]

def ques_ans_url(url,prompt,headers):
    # Load document using WebBaseLoader document loader
    print("Working to answer the question")
    
    # if os.path.exists("faiss_index_constitution"):
    #     print('The file exists!')
    #     embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',model_kwargs={'device': 'cpu'})
    #     persisted_vectorstore = FAISS.load_local("faiss_index_constitution", embeddings)
    
    # else:
    loader = WebBaseLoader([url])
    documents = loader.load()
    # Split document in chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    documents_splits = text_splitter.split_documents(documents)
    print(documents_splits[0])
    print("It the except block-- creating embeddings")

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',model_kwargs={'device': 'cpu'})
    # Create vectors
    vectorstore = FAISS.from_documents(documents_splits, embeddings)
    # Persist the vectors locally on disk
    vectorstore.save_local("faiss_index_constitution")
    persisted_vectorstore = FAISS.load_local("faiss_index_constitution", embeddings)


    # Find the most similar parts from the docs for the query using FAISS - get_relevant_documents
    retriever = persisted_vectorstore.as_retriever()
    similar_doc_list= retriever.get_relevant_documents(query=prompt)
    combined_similar_docs=""
    for i in range(0,len(similar_doc_list)):
        combined_similar_docs+=similar_doc_list[i].page_content
    
    prompt=f"Given the prompt and the relevant part from the docs, generate a response. Prompt:{prompt}, Relevant_docs:{combined_similar_docs} "
    model='llm70b'  
    res = openai.Completion.create(  
        message=[{
                "role":"system","content":"You are a helpful assistant for Infineon",
                "role":"user","content":prompt
                }],
        model=model,  
        prompt=prompt,  
        max_tokens=256,  
        stream=False,  
        temperature=0.7,  
        headers=headers 
    )
    # for chunk in res:  
    #     print(chunk["choices"][0]["text"], end="", flush=True)   
    output =  res.choices[0]["text"]
    return output


def single_url_translate(url,language,headers):
    #for a single url
    print("working to translate")
    loader = SeleniumURLLoader(urls=[url])
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    documents_splits = text_splitter.split_text(data[0].page_content)
    combined_translated='' #creating an empty string to store the combined translated text\

    for i in range(0,len(documents_splits)):
        prompt=f"Translate the following text in {language} :"+documents_splits[i]
        message=[
        {"role":"assistant", "content": "You are an assistant who can translate the given text into specified language"},
        {"role": "user", "content":prompt} 
        ]
        model='llm70b'  
        res = openai.Completion.create(  
            model=model,  
            prompt=prompt,  
            messages=message,
            max_tokens=4096,  
            stream=False,  
            temperature=0.7,  
            headers=headers 
        )

        combined_translated+=res.choices[0]["text"]
        # combined_translated+=test_completion_stream(prompt,message)
    return combined_translated

def single_pdf_translate(pdf,language,headers):
    loader = PyPDFLoader(pdf)
    pages = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    combined_translated=''
    print("entered here")
    for i in range(0,len(pages)):
        documents_splits = text_splitter.split_text(pages[i].page_content)
        for j in range(0,len(documents_splits)):
            prompt=f"Translate the following text in {language} :"+documents_splits[j]
            message=[
                {"role":"assistant", "content": "You are an assistant who can translate the given text into specified language"},
                {"role": "user", "content":prompt} 
                ] 
            model='llm70b'  
            res = openai.Completion.create(  
                model=model,  
                prompt=prompt,  
                messages=message,
                max_tokens=4096,  
                stream=False,  
                temperature=0.7,  
                headers=headers 
            )
    # for chunk in res:  
    #     print(chunk["choices"][0]["text"], end="", flush=True)  
            combined_translated+=res.choices[0]["text"]
        print("done with page:",i)
    
    return combined_translated

def single_pdf_summary(pdf,headers):
    loader = PyPDFLoader(pdf)
    pages = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    page_summary=''
    for i in range(0,len(pages)):
        documents_splits = text_splitter.split_text(pages[i].page_content)
        for chunks in documents_splits:
            prompt=f"Summarize the text:{chunks}"
            # text=test_completion_stream(f"Summarize the text:{chunks}")
            # page_summary+=text
            message=[
                {"role":"assistant", "content": "You are an assistant who can summarize the pdf file"},
                {"role": "user", "content":prompt} 
                ] 
            model='llm70b'  
            res = openai.Completion.create(  
                model=model,  
                prompt=prompt,  
                messages=message,
                max_tokens=4096,  
                stream=False,  
                temperature=0.7,  
                headers=headers 
            )
            page_summary+= res.choices[0]["text"]
        print("done with page:",i)
    documents_splits = text_splitter.split_text(page_summary)
    final_summary=''
    for chunks in documents_splits:
        prompt=f"Summarize the text:{chunks}"
            # text=test_completion_stream(f"Summarize the text:{chunks}")
            # page_summary+=text
        message=[
            {"role":"assistant", "content": "You are an assistant who can summarize the pdf file"},
            {"role": "user", "content":prompt} 
            ] 
        model='llm70b'  
        res = openai.Completion.create(  
            model=model,  
            prompt=prompt,  
            messages=message,
            max_tokens=4096,  
            stream=False,  
            temperature=0.7,  
            headers=headers 
        )
        final_summary+= res.choices[0]["text"]
        # text=test_completion_stream(f"These are the summaries of the pages of a pdf.Now Summarize all these summary 100 words:{chunks}")
        # final_summary+=text
    
    return final_summary


def single_url_summary(url,headers):
    #for a single url
    print("working here ")
    loader = SeleniumURLLoader(urls=[url])
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    documents_splits = text_splitter.split_text(data[0].page_content)
    page_summary=''
    for chunks in documents_splits:
        # text=test_completion_stream(f"Summarize the text:{chunks}")
        prompt=f"Summarize the text:{chunks}"
            # text=test_completion_stream(f"Summarize the text:{chunks}")
            # page_summary+=text
        message=[
            {"role":"assistant", "content": "You are an assistant who can summarize the pdf file"},
            {"role": "user", "content":prompt} 
            ] 
        model='llm70b'  
        res = openai.Completion.create(  
            model=model,  
            prompt=prompt,  
            messages=message,
            max_tokens=4096,  
            stream=False,  
            temperature=0.7,  
            headers=headers 
        )
        page_summary+= res.choices[0]["text"]# page_summary+=text

    return page_summary


# out=single_url_summary('https://en.wikipedia.org/wiki/List_of_songs_by_Taylor_Swift',headers)
# print(out)