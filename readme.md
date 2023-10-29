# Image Search Application with Weaviate

This project's origin is [here](https://github.com/weaviate/weaviate-examples/tree/main/nearest-neighbor-dog-search).

## Description
This guide demonstrates how to build an Image Search Application with Weaviate. The application allows users to upload images of dogs and find the most similar dog breed. While we focus on dogs, you can adapt this approach for various image recognition and product search applications.

### Used Technologies
- Weaviate
- Flask
- Python
- Docker

**Weaviate Modules:**
- img2vec-neural

## Prerequisites
Before starting, ensure you have the following:

1. Basic knowledge of vector search.
2. A Weaviate instance set up using Docker. For installation, refer to [Weaviate Installation](https://github.com/semi-technologies/weaviate).
3. Docker installed on your system. Get it from [Docker Installation](https://www.docker.com/).

## Setup Instructions
1. Clone this repository to your local machine.
2. Navigate to the `nearest-neighbor-dog-search` directory.
3. Start the Weaviate instance using Docker:
   ```bash
   docker compose up -d
   ```
4. Verify Weaviate's status:
   ```bash
   python weaviate-test.py
   ```
   You should see an output similar to: `{"classes": []}`.

## Usage Instructions
### Image Vectorization
1. Add your images to the `flask-app/static/img` folder.
2. Execute `images-to-base64.py` to convert the images to base64 encoding:
   ```bash
   python images-to-base64.py
   ```
   The base64-encoded images will be stored in the `base64_images` folder.

### Weaviate Database
1. Define the schema in `create-schema.py` to structure the data.
2. Add the schema to Weaviate:
   ```bash
   python create-schema.py
   ```
3. Upload data objects in batches using `upload-data-objects.py`:
   ```bash
   python upload-data-objects.py
   ```

### Flask Application
1. Start the Flask application:
   ```bash
   python flask-app/application.py
   ```
2. Access the application in your web browser at `http://127.0.0.1`.

**To search for similar dog breeds:**
1. Upload an image of a dog.
2. The application will display the uploaded image and the most similar dog breeds from the dataset.

## Dataset License
The dataset currently contains ten images of different dog breeds. You can also build on this and add your own images to the dataset!

