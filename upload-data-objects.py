import os, re
import weaviate
from weaviate import Config
import weaviate.classes as wvc

weight_dict = {
    "Australian Shepherd": 52,
    "Bernese Mountain Dog": 94,
    "Corgi": 26,
    "French Bulldog": 22,
    "German Shepherd": 68,
    "Golden Retriever": 70,
    "Goldendoodle": 40,
    "Labrador Retriever": 67,
    "Rottweiler": 103,
    "Siberian Husky": 47
}


def get_weight(breed_name):
    if breed_name in weight_dict:
        return weight_dict[breed_name]
    return 50


def clear_up_dogs():
    """
    Remove all objects from the Dogs collection.
    This is useful, if we want to rerun the import with different pictures.
    """
    dogs = client.collection.get("Dog")
    dogs.data.delete_many(where=wvc.Filter(path=["breed"]).not_equal("x"), verbose=True)


def import_data():
    """
    Process all images in [base64_images] folder and add import them into Dogs collection
    """
    dogs_to_add = []
    for encoded_file_path in os.listdir("./base64_images"):
        with open("./base64_images/" + encoded_file_path) as file:
            file_lines = file.readlines()

        base64_encoding = " ".join(file_lines)
        base64_encoding = base64_encoding.replace("\n", "").replace(" ", "")

        # remove .b64 to get the original file name
        image_file = encoded_file_path.replace(".b64", "")

        # remove image file extension and swap - for " " to get the breed name
        breed = re.sub(".(jpg|jpeg|png)", "", image_file).replace("-", " ")

        # The properties from our schema
        dog = wvc.DataObject(
            properties={
                "breed": breed,
                "image": base64_encoding,
                "filepath": image_file,
                "weight": get_weight(breed)
            })
        dogs_to_add.append(dog)

    dogs = client.collection.get("Dog")
    dogs.data.insert_many(dogs_to_add)


# initiating the Weaviate client
WEAVIATE_URL = os.getenv('WEAVIATE_URL')
if not WEAVIATE_URL:
    WEAVIATE_URL = 'http://localhost:8080'
print(WEAVIATE_URL, flush=True)

client = weaviate.Client(WEAVIATE_URL,
                         additional_config=Config(grpc_port_experimental=50051))
print(f"Client is ready {client.is_ready()}")

# clear existing data and upload fresh [base64_images] images data
clear_up_dogs()
import_data()

print("The objects have been uploaded to Weaviate.")
