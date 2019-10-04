from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, FormView, ListView
from django_json_ld.views import JsonLdContextMixin

from uploads.models import Upload
from uploads.forms import UploadForm
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from uploads.models import Upload

class UploadDocumentView(LoginRequiredMixin, JsonLdContextMixin, CreateView):
    form_class = UploadForm
    model = Upload
    template_name = 'uploads/upload_document.html'
    success_url = "/"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

class MyUploads(LoginRequiredMixin, ListView):
    model = Upload
    template_name = "uploads/my_uploads.html"
    paginate_by = 10
    title = "My-uploads"

    def get_queryset(self):
        queryset = super(MyUploads, self).get_queryset()
        queryset = queryset.filter(author=self.request.user).order_by('created')
        return queryset
#     def get(self, request, *args, **kwargs):


#         my_uploads = Upload.objects.filter(user=self.request.user).order_by('created_at')
#         paginator = Paginator(user_downloads, 6)
#         page = request.GET.get('page1')
#         try:
#             user_downloads = paginator.page(page)
#         except PageNotAnInteger:
#             user_downloads = paginator.page(1)
#         except EmptyPage:
#             user_downloads = paginator.page(paginator.num_pages)
#
#         page_view = PageView.objects.filter(user=self.request.user).order_by('created_at')
#         paginator = Paginator(page_view, 6)
#         page = request.GET.get('page2')
#         try:
#             page_view = paginator.page(page)
#         except PageNotAnInteger:
#             page_view = paginator.page(1)
#         except EmptyPage:
#             page_view = paginator.page(paginator.num_pages)
#
#         context = {'user_downloads': user_downloads, 'page_view': page_view}
#
#         return self.render_to_response(context)