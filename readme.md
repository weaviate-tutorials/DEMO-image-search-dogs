# Image Search Application with Weaviate

## Introduction

Welcome to this comprehensive guide on building an Image Search Application with Weaviate. In this tutorial, we will walk you through the process of creating a full-stack web application in Python using Weaviate and Flask. The final application will allow users to upload images of dogs and find the most similar dog breed in an instant. While this guide uses dogs as an example, you can easily adapt it for other image recognition or product search applications.

Before we dive into the details, it's essential to have some basic knowledge of vector search and the ability to set up a Weaviate instance using Docker. If you are not familiar with these topics, you can refer to the following resources:

- [Learn about Weaviate](https://www.weaviate.com/)
- [Weaviate Installation](https://github.com/semi-technologies/weaviate)
- [Docker Installation](https://www.docker.com/)

This guide will cover the following topics:

1. **Image Vectorization**
2. **Weaviate Database Setup**
3. **Flask Application Development**

Throughout the tutorial, we will provide code snippets, but you can also access the full code base in the Weaviate Examples GitHub repository under the `nearest-neighbor-dog-search` directory.

Let's get started!

## Image Vectorization

In this demonstration, we will work with a dataset of dog images. The current dataset includes ten images of different dog breeds. However, you can easily replace these images with any other dataset to suit your specific use case. To do this, add your images to the `flask-app/static/img` folder and execute the `images-to-base64.py` and `upload-data-objects.py` files.

For this use case, it's essential that image vectorization captures information about the dogs, such as breed, size, and color. Weaviate's `img2vec-neural` module is designed to solve this problem. It vectorizes each image, enabling semantic similarity-based searches.

### Img2vec-neural Module

Weaviate's `img2vec-neural` module is a flexible vectorizer that converts images into meaningful vectors. It supports the ResNet-50 model, a Convolutional Neural Network (CNN) trained on the ImageNet database, which contains over 10 million images and 20,000 classes.

## Weaviate Database

### Setup

The demonstration includes a `docker-compose.yml` file that defines all the Weaviate modules required for this project. In this file, you will find the `img2vec-neural` module trained on the ResNet-50 model. To start your Weaviate instance, navigate to the `nearest-neighbor-dog-search` directory in the cloned repository and run the following command:

```bash
docker compose up -d
```

Once Weaviate is up and running, verify its status using:

```bash
python weaviate-test.py
```

You should see an output similar to:

```json
{"classes": []}
```

### Schema Configuration

The dataset used in this project contains ten dogs, each with properties like breed, image, weight, and filepath. To define the structure in which we store data in the Weaviate database, we use a schema. Each object type in the schema is referred to as a class. In our case, the class name is "Dog," and the properties include breed, image, and filepath.

We also specify the vectorizer, which is the `img2vec-neural` module. The schema definition should look like this:

```python
schema = {
   "classes": [
       {
           "class": "Dog",
           "description": "Images of different dogs",
           "moduleConfig": {
               "img2vec-neural": {
                   "imageFields": [
                       "image"
                   ]
               }
           },
           "vectorIndexType": "hnsw",
           "vectorizer": "img2vec-neural",
           "properties": [
               {
                   "name": "breed",
                   "dataType": ["string"],
                   "description": "name of dog breed",
               },
               {
                   "name": "image",
                   "dataType": ["blob"],
                   "description": "image",
               },
               {
                   "name": "filepath",
                   "dataType": ["string"],
                   "description": "filepath of the images",
               }
           ]
       }
   ]
}
```

After defining the schema, you can add it to Weaviate using the following command:

```bash
python create-schema.py
```

### Images to Base64

Before populating the Weaviate database, you need to encode the images to base64 values. This encoding is necessary because we defined the image property as a blob dataType in the schema. The images in the dataset are stored in the `flask-app/static/img` folder. To convert the images to base64, execute the following command:

```bash
python images-to-base64.py
```

The base64-encoded images will be stored in the `base64_images` folder.

### Upload the Data Objects

With the schema and base64-encoded images in place, you can upload the data objects to Weaviate. It's advisable to import data in batches for faster performance. The batch process is configured to upload in batches of 100 objects, ensuring efficiency.

Here's the function to set up the batch process:

```python
def set_up_batch():
   client.batch.configure(
       batch_size=100,
       dynamic=True,
       timeout_retries=3,
       callback=None,
   )
```

The following function defines how to import data:

```python
def import_data():

    client.batch.configure(batch_size=100)  # Configure batch
    with client.batch as batch:
        # Iterate over all .b64 files in the base64_images folder
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
                data_properties = {
                    "breed": breed,
                    "image": base64_encoding,
                    "filepath": image_file,
                }

                batch.add_data_object(data_properties, "Dog")
```

Now, connect to the local host and upload the data objects:

```bash
python upload-data-objects.py
```

Congratulations! Your Weaviate database is now populated with images of cute dogs and their vector representations.

To summarize, here's what we've accomplished so far:

1. Defined the Weaviate schema.
2. Converted the images to base64 values.
3. Uploaded the data objects to Weaviate.

## Flask Application

Flask is a web application framework written in Python. It's an excellent choice for rapidly building web applications. In this section,

 we'll create a Flask application and connect it to your Weaviate client.

### Application File

Start by defining your Flask application and connecting it to the Weaviate client:

```python
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "/temp_images"
client = weaviate.Client("http://localhost:8080")
```

We will use the `nearImage` operator in Weaviate to search for images closest to the uploaded image. To do this, we'll create a function, `weaviate_img_search`, to get relevant results from Weaviate. The function will return the dog image with the breed name and filepath. It's important to note that the query is designed to return a limited set of results.

```python
def weaviate_img_search(img_str):
   sourceImage = { "image": img_str}

   weaviate_results = client.query.get(
       "Dog", ["filepath","breed"]
       ).with_near_image(
           sourceImage, encode=False
       ).with_limit(2).do()

   return weaviate_results["data"]["Get"]["Dog"]
```

With this function, you can quickly find visually similar dogs with a simple query to Weaviate. This capability can be scaled to handle millions of images, running in milliseconds with Weaviate's Approximate Nearest Neighbors (ANN) index.

### Defining Application Pages

Next, define the pages that will be part of your web application. The homepage will display the ten images of dogs from your dataset. If you add more images to the dataset, they will automatically appear on the homepage.

The `/process_image` page will display the uploaded image along with the results from Weaviate. After storing and converting the image to base64, you'll send it to the `weaviate_img_search` function to retrieve the results and update the page.

The following code block accomplishes the following:

1. Populates the homepage with images from the dataset.
2. Saves the uploaded image and converts it to base64.
3. Retrieves results from Weaviate and updates the page with the filepaths and breed names.

```python
@app.route("/") # defining the pages that will be on the website
def home(): # home page
    return render_template("index.html", content=list_images())

@app.route("/process_image", methods=["POST"]) # save the uploaded image and convert it to base64
# process the image upload request by converting it to base64 and querying Weaviate
def process_image():
        uploaded_file = Image.open(request.files['filepath'].stream)
        buffer = BytesIO()
        uploaded_file.save(buffer, format="JPEG")
        img_str = base64.b64encode(buffer.getvalue()).decode()

        weaviate_results = weaviate_img_search(img_str)

        results = []
        for result in weaviate_results:
            results.append({
                "path": result["filepath"],
                "breed": result["breed"]
            })

        return render_template("index.html", content=results, dog_image=img_str)
```

The `index.html` template has been set up to display images of the returned dog breeds.

```html
{% for x in content %}
<div class="imgCard">
    <img src="./static/img/{{ x['path'] }}" />
    <h4>{{ x['breed'] }}</h4>
</div>
{% endfor %}
```

### Running the Application

To run your Flask application, use the following command:

```bash
python flask-app/application.py
```

Navigate to `http://127.0.0.1` to see your running web app in action.

Now, you can test a query to find the dog breed that looks most similar to a Goldendoodle puppy. You'll notice that the puppy resembles the Goldendoodle and Golden Retriever in your database.
