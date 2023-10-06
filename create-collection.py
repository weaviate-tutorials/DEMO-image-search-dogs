import os
import weaviate
from weaviate import Config
import weaviate.classes as wvc
from weaviate.collection.classes.config import VectorIndexType

# initiating the Weaviate client
WEAVIATE_URL = os.getenv('WEAVIATE_URL')
if not WEAVIATE_URL:
    WEAVIATE_URL = 'http://localhost:8080'
print(WEAVIATE_URL, flush=True)

client = weaviate.Client(WEAVIATE_URL,
                         additional_config=Config(grpc_port_experimental=50051))
print(f"Client is ready {client.is_ready()}")

# delete the Dog collection if already exists
client.collection.delete(["Dog"])

# creating the Dog collection with the following properties: breed, image, and filepath
dogs = client.collection.create(
    name="Dog",
    properties=[
        wvc.Property(
            name="breed",
            data_type=wvc.DataType.TEXT,
            description="name of dog breed",
        ),
        wvc.Property(
            name="image",
            data_type=wvc.DataType.BLOB,
            description="image",
        ),
        wvc.Property(
            name="filepath",
            data_type=wvc.DataType.TEXT,
            description="filepath of the images",
        )
    ],
    # the img2vec-neural Weaviate module
    vectorizer_config=wvc.ConfigFactory.Vectorizer.img2vec_neural(image_fields=["image"]),
    vector_index_type=VectorIndexType.HNSW
)

print("The 'Dog' class has been defined.")
