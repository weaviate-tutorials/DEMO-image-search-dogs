# Dog Search 

This project's origin is [here](https://github.com/weaviate/weaviate-examples/tree/main/nearest-neighbor-dog-search).

(TODO: Add Description)

(TODO: Add demo video)

(TODO: Add used technology stack)

## Prerequisites
Docker Desktop should be installed and running.
Python 3.10 or later should be installed.

## Setup instructions
1. Make sure you have Weaviate installed and set up. [Check out the documentation](https://weaviate.io/developers/weaviate/current/installation/index.html) for more information!
2. Run the docker file 
    ```bash
    docker compose up
    ```
3. Run the schema file
    ```bash
    python create-schema.py
    ```
4. Run the images to base64 file 
    ```bash
    python images-to-base64.py
    ```
5. Upload the encoded images 
    ```bash
    python upload-data-objects.py
    ```
## Usage instructions
### Run the application
Run the Python Flask application and go to http://localhost:5000
```bash
python flask-app/application.py 
```

### Run the query 
Run the query to see dogs that are under 60 pounds
```bash
python query.py
```

## Dataset license
The dataset currently contains ten images of different dog breeds. You can also build on this and add your own images to the dataset!
