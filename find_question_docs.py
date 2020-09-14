import csv
from django.contrib.sites.models import Site

from documents.models import Document


doc = Document.objects.filter(is_visible=True)

def check(doc):
    row = []
    for question in doc:
        if "Question" or "question" in question.description:
            ip = "https://" + Site.objects.get_current().domain
            csvwriter = csv.writer(open('Question_docs_admin_url.csv', 'w'))
            heading_row = ['Admin Url']
            data_row = [ip + '/admin/documents/document/' + str(question.id) + '/change']
            csvwriter.writerow(heading_row)
            for i in row:
                csvwriter.writerow(i)
                print(i)

            row.append(data_row)

check(doc)


