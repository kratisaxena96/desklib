import os

import selenium
import textract

from documents.models import Document
from django.core.files import File
from documents.utils import get_text
import requests
from termcolor import colored
# command to run the file
# exec(open("./upload_files_via_api.py").read())

path = input("Folder Path: ")
last_file = input("Enter last filename to restart program: ")
# url = input("Enter Url Of website: ")
# url = 'http://127.0.0.1:8000/api/create/document'
url = 'https://desklib.com/api/document/create/document/'

ALLOWED_EXTENSIONS = ['pdf','docx','doc', 'pptx', 'ppt', 'odt', 'odf']
IGNORE_FILENAME_KEYWORDS = ['lecture', 'rubic', 'rubric', 'instructions', 'assignmentbrief', 'criteria', 'requirements', 'programmingassignment', 'individual-assignment', 'individualassignment']
IGNORE_FILECONTENT_KEYWORDS = ['ORIGINALITY REPORT']

i = 0
for root, dirs, files in os.walk(path, topdown=False):
    for filename in files:
        i = i+1
        print("Processing file no: ", i)
        if last_file:
            if filename == last_file:
                last_file = None

            print("Skipping file: ", filename)
            continue

        print('Processing file: ', filename)
        try:
            # import pdb; pdb.set_trace()
            ext = filename.split(".")[-1].lower()
            if ext in ALLOWED_EXTENSIONS:
                filename_lower = filename.lower()
                is_filename_valid = True
                for ignore_filename_keyword in IGNORE_FILENAME_KEYWORDS:
                    if ignore_filename_keyword.lower() in filename_lower:
                        filename_valid = False
                        break
                if is_filename_valid:
                    print('Filename is valid')
                    path_for_text = os.path.join(path, filename)
                    text = get_text(path_for_text)
                    text = text.lower()

                    is_filecontent_valid = True
                    for ignore_filecontent_keyword in IGNORE_FILECONTENT_KEYWORDS:
                        if ignore_filecontent_keyword.lower() in text:
                            is_filecontent_valid = False
                            break

                    if is_filecontent_valid:
                        print('File content is valid')
                        filepath = os.path.join(path, filename)
                        files = {'upload_file': open(filepath, 'rb')}
                        r = requests.post(url, files=files)
                        print(colored(("Status Code is :%s"%r.status_code), 'green'))
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
        except selenium.common.exceptions.TimeoutException as e:
            print(e)


