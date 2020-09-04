import csv
from django.contrib.sites.models import Site

from documents.models import Document



outfile_path = "/home/locus/Downloads/Check.csv"
doc = Document.objects.filter(is_visible=True)

def run(doc, outfile_path):
    row = []
    for question in doc:
        if "san" in question.title or "JANUARY" in question.description:
            ip = "https://" + Site.objects.get_current().domain
            csvwriter = csv.writer(open(outfile_path, 'w'))
            heading_row = ['Admin Url']
            data_row = [ip + '/admin/documents/document/' + str(question.id) + '/change']
            print(data_row)
            csvwriter.writerow(heading_row)
            for i in row:
                csvwriter.writerow(i)
            row.append(data_row)

run(doc, outfile_path)

