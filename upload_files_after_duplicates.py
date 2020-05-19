import os

import selenium
import textract
from documents.utils import get_text
import requests
from termcolor import colored
import sqlite3
from sqlite3 import Error
from classifier import get_text, get_clean_text, predict
print ("hello")
# command to run the file
# exec(open("./upload_files_after_duplicates.py").read())

path = input("Folder Path: ")
last_file = input("Enter last filename to restart program: ")
# url = input("Enter Url Of website: ")
# url = 'http://127.0.0.1:8000/api/document/create/'
url = 'http://127.0.0.1:8000/api/document/create/'
# ACC-201-Accounting-Cycle-Report-Template1docx-7178.docx
ALLOWED_EXTENSIONS = ['pdf','docx','doc', 'pptx', 'ppt', 'odt', 'odf']
IGNORE_FILENAME_KEYWORDS = ['lecture', 'rubic', 'rubric', 'instructions', 'assignmentbrief', 'criteria', 'requirements', 'programmingassignment', 'individual-assignment', 'individualassignment']
IGNORE_FILECONTENT_KEYWORDS = ['ORIGINALITY REPORT']


script_classifier = input("Do you want to check if the file is question or solution[y/n]: ")
publish = False
visible = False

import hashlib
conn = None;
try:
    conn = sqlite3.connect('UploadFiles.db')
except Error as e:
    print(e)
try:
        c = conn.cursor()
        # c.execute("DROP TABLE IF EXISTS tasks")
        c.execute("""CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    path text NOT NULL,
                                    hash blob);""")
except Error as e:
    print(e)

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
                        sqlite_insert_with_param = """INSERT INTO 'tasks'
                                                  ('id', 'path', 'hash')
                                                  VALUES (?, ?, ?);"""

                        corpus = []

                        if script_classifier == 'y' or script_classifier == 'Y':
                            print('script classifier')
                            text = get_text(filepath)
                            clean = get_clean_text(text).lower()
                            corpus.append(clean)
                            guess = predict(corpus)
                            # print(guess)
                            if guess == 0:
                                publish = False
                                visible = False
                            else:
                                publish = True
                                visible = True

                        hash_md5 = hashlib.md5()
                        digest = None
                        with open(filepath, "rb") as f:
                            for chunk in iter(lambda: f.read(4096), b""):
                                hash_md5.update(chunk)
                            digest = hash_md5.hexdigest()
                        c.execute("SELECT * FROM tasks WHERE hash=?", (digest,))
                        rows = c.fetchall()
                        if rows:
                            pass
                        else:
                            data_tuple = (i, path_for_text, digest)
                            c.execute(sqlite_insert_with_param, data_tuple)
                            conn.commit()
                            f = open(filepath, 'rb')
                            files = {'upload_file': f}
                            r = requests.post(url, files=files, data={'is_published': publish, 'is_visible': visible})
                            print(colored(("Status Code is :%s" % r.status_code), 'green'))
                            f.close()
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
    conn.close()

