from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Avg
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django_json_ld.views import JsonLdContextMixin
from meta.views import MetadataMixin
from django_json_ld.views import JsonLdListView, DEFAULT_STRUCTURED_DATA
from django_json_ld import settings
from django.utils.translation import gettext as _

from review.models import Review
from .forms import ReviewForm


class ReviewPageView(MetadataMixin, JsonLdListView):
    template_name = "review/review.html"
    model = Review

    structured_data = {
        "@type": "LocalBusiness",
        "name": "Desklib- Homework help, online learning library",
        "logo": "https://desklib.com/static/dist/assets/images/desklib-logo-theme.png",
        "image": "https://desklib.com/static/dist/assets/images/desklib-logo-theme.png",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "68 Circular Rd",
            "addressLocality": "Singapore",
            "addressRegion": "Downtown",
            "postalCode": "049422",
            "addressCountry": "Singapore"
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "{{review_avg.stars__avg}}",
            "reviewCount": "{{review_count}}"
        },
        "priceRange": "$25 - $250",
        "url": "https://desklib.com/",
        "telephone": "+44-7482880720"
    }

    def get_queryset(self):
        return Review.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super(ReviewPageView, self).get_context_data(**kwargs)
        #         context = super(OzAssignmentsReviewPageView, self).get_context_data(**kwargs)
        all_reviews = Review.objects.filter(is_published=True).order_by('-created_at')  # For pagination
        #         review_count = Review.objects.aggregate(Count('stars'))
        review_count = Review.objects.filter(is_published=True).count()  # For removing "stars__count" text from template
        review_avg = Review.objects.filter(is_published=True).aggregate(Avg('stars'))  # For removing "stars__avg" text from template
        top_reviews = Review.objects.filter(is_published=True).order_by('-stars')[:5]
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
        context['top_review'] = top_reviews
        context['review_5_stars_count'] = review_5_stars_count
        context['review_4_stars_count'] = review_4_stars_count
        context['review_3_stars_count'] = review_3_stars_count
        context['review_2_stars_count'] = review_2_stars_count
        context['review_1_stars_count'] = review_1_stars_count
        # context['reviews'] = Review.objects.filter(is_published=True)[:5]
        return context

    def get_structured_data(self):
        structured_data = super(ReviewPageView, self).get_structured_data()
        # structured_data["review"] = get_next_event()

        structured_data['review'] = structured_data['@graph']
        del structured_data['@graph']

        review_count = Review.objects.filter(is_published=True).count()  # For removing "stars__count" text from template
        review_avg = Review.objects.filter(is_published=True).aggregate(Avg('stars'))['stars__avg']

        rating = {
            "@type": "AggregateRating",
            "ratingValue": review_avg,
            "reviewCount": review_count
        },
        structured_data['aggregateRating'] = rating

        return structured_data



class AddReviewPageView(MetadataMixin, JsonLdContextMixin, CreateView):
    template_name = "review/add_review.html"
    model = Review
    form_class = ReviewForm
    success_url = reverse_lazy('review:review')
