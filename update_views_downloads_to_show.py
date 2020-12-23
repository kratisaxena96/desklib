import random
from django.utils import timezone

from tqdm import tqdm

from documents.models import Document

# exec(open("./update_views_downloads_to_show.py").read())


def randomNumberViews():
    return random.randint(1000, 5000)


def randomNumberDownloads():
    return random.randint(1, 100)


def randomNumberRating():
    return random.randint(1, 10)


for doc in tqdm(Document.objects.filter(published_date__gte=timezone.now(), is_published=False, is_visible=False), colour='#44f172'):
    doc.total_downloads_to_show = randomNumberDownloads()
    doc.views_to_show = randomNumberViews()
    doc.fake_reviews = randomNumberRating()
    print(doc.title)
    doc.save(update_fields=["total_downloads_to_show","views_to_show","fake_reviews"])

for doc in tqdm(Document.objects.filter(is_published=True, is_visible=True), colour='#44f172'):
    doc.total_downloads_to_show = randomNumberDownloads()
    doc.views_to_show = randomNumberViews()
    doc.fake_reviews = randomNumberRating()
    doc.save(update_fields=["total_downloads_to_show","views_to_show","fake_reviews"])


