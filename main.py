from elasticsearch import Elasticsearch
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

class SearchQuery(BaseModel):
    text: str

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# es = Elasticsearch("http://elastic:9200")

@app.get("/health")
def health():
    return {'success': True, 'message': 'healthy :)'}


# endpoint that allows users to search on the frontend :)
@app.post("/search")
def search(search_query: SearchQuery):
    es = Elasticsearch("http://localhost:9200")
    query = {
        "query_string": {
            "query": search_query.text,
            "default_field": "*",
            "fuzziness": 2,
            "lenient": True,
        }
    }
    res = es.search(index='articles', query=query)
    # get results
    data = [x['_source'] for x in res['hits']['hits']]
    return {"query": search_query.text, 'success': True, 'results': data}


@app.get("/")
def root():
    return {"Hello": "World :)"}

