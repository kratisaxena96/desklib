import os
from documents.models import Document
from django.core.files import File

# command to run the file
# exec(open("./upload_files.py").read())

path = input("Folder Path: ")

for root, dirs, files in os.walk(path, topdown=False):
    for filename in files:
        try:
            ext = filename.split(".")[-1]
            if not (ext=="zip" or ext=="jpg" or ext=="ppt" or ext=="xlsx"):
                print("Processing file: "+ filename )
                filepath = os.path.join(root, filename)
                with open(filepath, 'rb') as f:
                    djangofile = File(f)
                    doc = Document()
                    doc.upload_file.save(filename ,djangofile)
                print("Closing file: "+ filename)
        except Exception as e:
            print(e)


