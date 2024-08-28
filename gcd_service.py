# from google.cloud import storage
# import os

# if 'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ:
#     raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

# client = storage.Client()
# bucket = client.bucket('project_colab32')

# def upload_image(file, file_name):
#     blob = bucket.blob(file_name)
#     blob.upload_from_file(file)
    
#     return blob.public_url

# def delete_image(file_name):
#     blob = bucket.blob(file_name)
#     blob.delete()

# def get_image_url(file_name):
#     blob = bucket.blob(file_name)
#     return blob.public_url
