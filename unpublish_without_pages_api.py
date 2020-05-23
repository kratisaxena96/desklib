from documents.models import Document

# exec(open("./unpublish_without_pages_api.py").read())

for doc in Document.objects.filter(pages__isnull = True, is_published=True, is_visible=True):
    doc.is_published = False
    doc.is_visible = False
    doc.save(update_fields=["is_published","is_visible"])
