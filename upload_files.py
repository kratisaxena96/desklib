import os

import textract

from documents.models import Document
from django.core.files import File
from documents.utils import get_text

# command to run the file
# exec(open("./upload_files.py").read())

path = input("Folder Path: ")
ALLOWED_EXTENSIONS = ['pdf','docx','doc', 'pptx', 'ppt', 'odt', 'odf']
IGNORE_FILENAME_KEYWORDS = ['lecture','rubics','assignment_brief','criteria']
IGNORE_FILECONTENT_KEYWORDS = []

for root, dirs, files in os.walk(path, topdown=False):
    for filename in files:
        print('Processing file: ', filename)
        try:
            ext = filename.split(".")[-1].lower()
            if ext in ALLOWED_EXTENSIONS:
                filename_lower = filename.lower()
                is_filename_valid = True
                for ignore_filename_keyword in IGNORE_FILENAME_KEYWORDS:
                    if ignore_filename_keyword in filename_lower:
                        filename_valid = False
                        break
                if is_filename_valid:
                    print('Filename is valid')
                    path_for_text = os.path.join(path, filename)
                    text = get_text(path_for_text)
                    text = text.lower()

                    is_filecontent_valid = True
                    for ignore_filecontent_keyword in IGNORE_FILECONTENT_KEYWORDS:
                        if ignore_filecontent_keyword in text:
                            is_filecontent_valid = False
                            break

                    if is_filecontent_valid:
                        print('File content is valid')
                        filepath = os.path.join(root, filename)
                        with open(filepath, 'rb') as f:
                            djangofile = File(f)
                            doc = Document()
                            doc.upload_file.save(filename ,djangofile)

                        print("Closing file: "+ filename)
                    else:
                        print("Ignoring file : " + filename + " Invalid filename Content")

                else:
                    print("Ignoring file : "+ filename + " Invalid filename Keywords" )

            else:
                print("Ignoring file: "+ filename )

        except textract.exceptions.ExtensionNotSupported as e:
            print(e)
        except textract.exceptions.ShellError as e:
            print(e)


