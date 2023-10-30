# Dog Search

## Description

In this demo, we will use Weaviate to create an image-search application. We'll develop a dog image-search application that lets users upload a photo of a dog and receive a list of dog breeds that are the most similar.

(TODO: Add demo video)

## Used Technologies

- Weaviate
- Vector DB
- Python Programming Language (v3.10+)
- Weaviate Python Client Library
- Flask (For WebApp interface development)
- Docker Desktop

**Weaviate Modules:**
- [List the Weaviate modules used]

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Docker Desktop should be installed and running.
- Python 3.10 or later should be installed.

### Setup Instructions

Note: We recommend you create a new virtual environment for this.

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the Python packages.

```bash
pip install -r requirements.txt
```

Run the Docker file.

```bash
docker compose up
```

Create the class definition.

```bash
python create-collection.py
```

Convert images to base64 encodings.

```bash
python images-to-base64.py
```

Upload the encoded images.

```bash
python upload-data-objects.py
```

### Usage Instructions

Run the application.

```bash
python flask-app/application.py
```

Access the application by opening your web browser and visiting http://localhost:5001.

**To run a query:**

Run the query to see dogs that are under 60 pounds.

```bash
python query.py
```

## Dataset License

The dataset currently contains ten images of different dog breeds. You can also build on this and add your own images to the dataset!
