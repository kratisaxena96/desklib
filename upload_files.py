import os
from documents.models import Document
from django.core.files import File
from documents.utils import get_text

# command to run the file
# exec(open("./upload_files.py").read())

path = input("Folder Path: ")
ALLOWED_EXTENSIONS = ['pdf','docx','doc', 'pptx', 'ppt', 'odt', 'odf']
IGNORE_FILENAME_KEYWORDS = ['lecture','rubics','assignment_brief','criteria']
IGNORE_FILECONTENT_KEYWORDS = ['similarity report']
filename_valid = False
filecontent_valid = False


for root, dirs, files in os.walk(path, topdown=False):
    for filename in files:
        try:
            ext = filename.split(".")[-1]
            if ext in ALLOWED_EXTENSIONS:
                filename_lower = filename.lower()
                for ignore_filename_keyword in IGNORE_FILENAME_KEYWORDS:
                    if not ignore_filename_keyword in filename_lower:
                        filename_valid = True
                    else:
                        print("Ignoring file : "+ filename + " Invalid filename Keywords" )

                path_for_text = os.path.join(path,filename)
                text = get_text(path_for_text)
                text= text.lower()
                for ignore_filecontent_keyword in IGNORE_FILECONTENT_KEYWORDS:
                    if not ignore_filecontent_keyword in text:
                        filecontent_valid = True
                    else:
                        print("Ignoring file : "+ filename + " Invalid filename Content" )

                if filename_valid == True and filecontent_valid == True:
                    print("Processing file: "+ filename )
                    filepath = os.path.join(root, filename)
                    with open(filepath, 'rb') as f:
                        djangofile = File(f)
                        doc = Document()
                        doc.upload_file.save(filename ,djangofile)
                    print("Closing file: "+ filename)
            else:
                print("Ignoring file: "+ filename )

        except Exception as e:
            print(e)


