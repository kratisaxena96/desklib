from haystack import indexes
from .models import Document
from haystack.query import SearchQuerySet

class BookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name="search/book_text.txt")
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    content = indexes.CharField(model_attr='content')
    summary = indexes.CharField(model_attr='summary')
    content_auto = indexes.EdgeNgramField(model_attr='description')
    slug = indexes.CharField(model_attr='slug')
    # authors = indexes.CharField()
    def get_model(self):
        return Document
    # def prepare_authors(self, obj):
    #     return [ a.name for a in obj.author.all()]
    def index_queryset(self, using=None):
        print(self.get_model().objects.all().count())
        return self.get_model().objects.all()


