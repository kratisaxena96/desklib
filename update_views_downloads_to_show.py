import random

from tqdm import tqdm

from documents.models import Document

# exec(open("./update_views_downloads_to_show.py").read())

def randomNumberViews():
    return random.randint(1000,5000)

def randomNumberDownloads():
    return random.randint(1,100)

def randomNumberRating():
    return random.randint(1,10)

for doc in tqdm(Document.objects.all(), colour='#44f172'):
    doc.total_downloads_to_show = randomNumberDownloads()
    doc.views_to_show = randomNumberViews()
    doc.fake_reviews = randomNumberRating()
    doc.save(update_fields=["total_downloads_to_show","views_to_show","fake_reviews"])
