from haystack import indexes
from .models import Document
from django.utils import timezone
from homework_help.models import Question, Answers


class DocumentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name="search/book_text.txt")
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    # content = indexes.CharField(model_attr='content')
    summary = indexes.CharField(model_attr='summary')
    content_auto = indexes.EdgeNgramField(model_attr='title')
    slug = indexes.CharField(model_attr='slug')
    pub_date = indexes.DateTimeField(model_attr='published_date')
    cover_image = indexes.CharField()
    cover_image_name = indexes.CharField()
    no_of_pages = indexes.IntegerField(model_attr='page')
    no_of_words = indexes.IntegerField(model_attr='words')
    subjects = indexes.MultiValueField(faceted=True)
    views = indexes.CharField(model_attr='views')
    p_subject = indexes.MultiValueField(faceted=True)

    def get_model(self):
        return Document

    # def prepare_content(self, obj):
    #     content = ' '.join(map(str, obj.content.split()[:500]))
    #     return content

    def prepare_subjects(self, obj):
        return [(t.slug) for t in obj.subjects.all()]

    def prepare_p_subject(self, obj):
        try:
            parent_sub = {(t.parent_subject.slug) for t in obj.subjects.all()}
        except:
            import pdb; pdb.set_trace()
        return list(parent_sub)
    
    

    def prepare_cover_image(self, obj):
        try:
            if obj.cover_page_number:
                url = obj.pages.get(no=obj.cover_page_number).image_file.url
                return url
            else:
                if obj.pages.count() >= 2:
                    # full_url = ''.join(['http://', get_current_site(obj).domain, obj.pages.first().image_file.url])
                    url = obj.pages.all()[1].image_file.url
                    # print(url)
                    return url
                elif obj.pages.count() == 1:
                    url = obj.pages.first().image_file.url
                    return url
        except:
            pass



    def prepare_cover_image_name(self, obj):
        try:
            if obj.cover_page_number:
                name = obj.pages.get(no=obj.cover_page_number).image_file.name
                return name

            else:
                if obj.pages.count() >= 2:
                    # full_url = ''.join(['http://', get_current_site(obj).domain, obj.pages.first().image_file.url])
                    name = obj.pages.all()[1].image_file.name
                    # print(url)
                    return name
                elif obj.pages.first():
                    # full_url = ''.join(['http://', get_current_site(obj).domain, obj.pages.first().image_file.url])
                    name = obj.pages.first().image_file.name
                    # print(url)
                    return name
        except:
            pass

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(pages__isnull=False, is_visible=True, is_published=True, published_date__lte=timezone.now()).distinct()


class QuestionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name="search/question.txt")
    slug = indexes.CharField(model_attr='slug')
    created_date = indexes.DateTimeField(model_attr='created')
    subjects = indexes.MultiValueField(faceted=True)
    no_of_answers = indexes.IntegerField()
    content_auto = indexes.EdgeNgramField(model_attr='question')
    uid = indexes.CharField()

    def get_model(self):
        return Question

    def prepare_no_of_answers(self, obj):
        answers_count = Answers.objects.filter(question=obj).count()
        return answers_count

    def prepare_subjects(self, obj):
        subject = obj.subjects.slug
        return subject

    def prepare_p_subject(self, obj):
        parent_sub = obj.subjects.parent_subject.slug
        return list(parent_sub)

    def prepare_uid(self, obj):
        uid = obj.uid
        return uid
