from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Avg
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from django_json_ld.views import JsonLdContextMixin
from meta.views import MetadataMixin
from review.models import Review


class ReviewPageView(MetadataMixin, JsonLdContextMixin, ListView):
    template_name = "review/review.html"
    model = Review

    def get_context_data(self, **kwargs):
        context = super(ReviewPageView, self).get_context_data(**kwargs)
        #         context = super(OzAssignmentsReviewPageView, self).get_context_data(**kwargs)
        all_reviews = Review.objects.filter(is_published=True).order_by('-created_at')  # For pagination
        #         review_count = Review.objects.aggregate(Count('stars'))
        review_count = Review.objects.filter(is_published=True).annotate(Count('stars')).values()  # For removing "stars__count" text from template
        review_avg = Review.objects.filter(is_published=True).aggregate(Avg('stars'))  # For removing "stars__avg" text from template
        review_5_stars_count = Review.objects.filter(is_published=True, stars=5).count()
        review_4_stars_count = Review.objects.filter(is_published=True, stars=4).count()
        review_3_stars_count = Review.objects.filter(is_published=True, stars=3).count()
        review_2_stars_count = Review.objects.filter(is_published=True, stars=2).count()
        review_1_stars_count = Review.objects.filter(is_published=True, stars=1).count()

        paginator = Paginator(all_reviews, 6)  # Show 6 reviews per page
        page = self.request.GET.get('page')
        try:
            reviews = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            reviews = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            reviews = paginator.page(paginator.num_pages)

        #         context['latest_assignment'] = Assignment.objects.filter(is_published=True).order_by('-created_at')[:5]
        #         context['latest_solution'] = Solution.objects.filter(is_published=True).order_by('-created_at')[:5]
        context['latest_reviews'] = Review.objects.filter(is_published=True).order_by('-created_at')[:5]
        context['all_reviews'] = reviews
        context['review_count'] = review_count
        context['review_avg'] = review_avg
        context['review_5_stars_count'] = review_5_stars_count
        context['review_4_stars_count'] = review_4_stars_count
        context['review_3_stars_count'] = review_3_stars_count
        context['review_2_stars_count'] = review_2_stars_count
        context['review_1_stars_count'] = review_1_stars_count
        # context['reviews'] = Review.objects.filter(is_published=True)[:5]
        return context