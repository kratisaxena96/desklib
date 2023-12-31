from django.http import Http404
from django_json_ld.views import JsonLdDetailView, JsonLdListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.views.generic import ListView, DetailView
from meta.views import MetadataMixin
from django.core.paginator import Paginator

from blogs.models import BlogModel


class BlogListPageView(MetadataMixin, JsonLdListView, ListView):
    template_name = "blogs/v2/blog_list.html"
    paginate_by = 6
    title = 'Blog - Desklib'
    description = 'Desklib blog list page'
    use_title_tag = True


    def get_structured_data(self):
        sd = super(BlogListPageView, self).get_structured_data()
        return sd

    def get_queryset(self):
        return BlogModel.objects.filter(is_published=True, is_visible=True, published_date__lte=timezone.now()).order_by('published_date')[::-1]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BlogListPageView, self).get_context_data(**kwargs)
        blog_list = BlogModel.objects.filter(is_published=True, is_visible=True, published_date__lte=timezone.now())
        paginator = Paginator(blog_list,self.paginate_by)
        page = self.request.GET.get('page')

        try:
            blog_page = paginator.page(page)
        except PageNotAnInteger:
            blog_page = paginator.page(1)
        except EmptyPage:
            blog_page = paginator.page(paginator.num_pages)

        featured_blog = BlogModel.objects.filter(is_published=True, is_featured=True, is_visible=True, published_date__lte=timezone.now())[:4]
        context['featured_blog'] = featured_blog
        context['object'] = blog_page
        return context


class BlogDetailPageView(JsonLdDetailView, DetailView):
    template_name = "blogs/v2/blog_detail.html"
    model = BlogModel

    def get_structured_data(self):
        sd = super(BlogDetailPageView, self).get_structured_data()
        return sd

    def get_context_data(self, **kwargs):
        context = super(BlogDetailPageView, self).get_context_data(**kwargs)
        data = self.request.path.split('/')
        year = data[1]
        month = data[2]
        day = data[3]
        if year == str(kwargs.get('object').published_date.year) and month == str(kwargs.get('object').published_date.month) and day == str(kwargs.get('object').published_date.day):
            context['meta'] = self.get_object().as_meta(self.request)
            featured_blog = BlogModel.objects.filter(is_published=True, is_featured=True, is_visible=True, published_date__lte=timezone.now())[:4]
            context['featured_blog'] = featured_blog
            return context
        raise Http404()
