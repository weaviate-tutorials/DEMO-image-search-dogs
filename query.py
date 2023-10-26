# initiating the Weaviate client
import json
import os

import weaviate
from weaviate import Config
import weaviate.classes as wvc

WEAVIATE_URL = os.getenv('WEAVIATE_URL')
if not WEAVIATE_URL:
    WEAVIATE_URL = 'http://localhost:8080'
print(WEAVIATE_URL, flush=True)

client = weaviate.Client(WEAVIATE_URL,
                         additional_config=Config(grpc_port_experimental=50051))
print(f"Client is ready {client.is_ready()}")

# query dogs that are under 60 pounds
dogs = client.collection.get("Dog")
response = dogs.query.fetch_objects(filters=wvc.Filter(path=["weight"]).less_than(60))
print("Dogs found under 60 pounds...")
for o in response.objects:
    print(json.dumps(o.properties))
