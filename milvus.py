from pymilvus import MilvusClient, DataType
import os
import json
from dotenv import load_dotenv

load_dotenv()


class MilvusApp:
    def __init__(self, api_key, api_endpoint):
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.client = self.connect()

    def connect(self):
        self.client = MilvusClient(uri=self.api_endpoint, token=self.api_key) 
        if not self.client:
            raise Exception("Client not established.")

    def disconnect(self):
        if self.client:
            self.client.close()


    def create_embedding_schema(self):
        # each entry is one article
        schema = MilvusClient.create_schema(
            auto_id=True,
            enable_dynamic_field=True
        )

        schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
        schema.add_field(field_name="team_name_vector", datatype=DataType.FLOAT_VECTOR, dim=768)
        schema.add_field(field_name="article_json", datatype=DataType.JSON)
        return schema
    

    def format_data(self, team_name, team_name_vector, article_text_list):
        data = {
            "team_name_vector": team_name_vector,
            "article_json": {
                'team_name': team_name,
                'article_content': article_text_list, 
            }  
        }
        return data
    

    def upload_data(self, collection_name, data):
        res = self.client.insert(
            collection_name=collection_name,
            data=data
        )
        print(res)


    def create_collection(self, collection_name, schema=None):
        res = self.client.list_collections()
        # print(res)
        if collection_name in res:
            raise Exception(f"'{collection_name}' already exists in cluster.\n{self.client.describe_collection(collection_name=collection_name)}")
        
        index_params = self.client.prepare_index_params()
        
        index_params.add_index(
            field_name="team_name_vector", 
            index_type="AUTOINDEX", # zilliz
            metric_type="L2",
            params={}
        )
        
        if not schema:
            schema = self.create_embedding_schema()
        print(index_params)
        print(schema)
        collection = self.client.create_collection(
                collection_name=collection_name, 
                schema=schema, 
                index_params=index_params)
        return collection


    def load_collection(self, collection_name):
        # for searching entities purpose only 
        self.client.load_collection(
            collection_name=collection_name
        )
        res = self.client.get_load_state(
            collection_name=collection_name
        )
        print(res)
    

    def drop_collection(self, collection_name):
        self.client.drop_collection(
            collection_name=collection_name
        )


    def upload_data(self, collection_name, data):
        res = self.client.insert(
            collection_name=collection_name,
            data=data
        )
        print(res)
    

    def find_data(self, collection_name, query_vectors: list, top_k=5):
        self.load_collection(collection_name)
        res = self.client.search(
            collection_name=collection_name,
            data=query_vectors,
            limit=top_k, # Max. number of search results to return
            search_params={"metric_type": "L2"}
        )

        result = json.dumps(res, indent=4)
        print(result)
        
        result_ids = [entry["id"] for entry in res[0]]

        res = self.client.get(
            collection_name=collection_name,
            ids=result_ids
        )

        content = [entry["article_json"]["article_content"] for entry in res]

        return content
    
