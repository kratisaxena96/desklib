from django import forms
from haystack.forms import FacetedSearchForm

class CustomFacetedSearchForm(FacetedSearchForm):
    from_page = forms.IntegerField(required=False)
    to_page = forms.IntegerField(required=False)
    from_words = forms.IntegerField(required=False)
    to_words = forms.IntegerField(required=False)


    def __init__(self, *args, **kwargs):
        super(CustomFacetedSearchForm, self).__init__(*args, **kwargs)

    def search(self):

        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q') and not self.selected_facets:
            return self.no_query_found()

        sqs = self.searchqueryset.auto_query(self.cleaned_data.get('q'))

        if self.load_all:
            sqs = sqs.load_all()
        # We need to process each facet to ensure that the field name and the
        # value are quoted correctly and separately:
        # self.searchqueryset.facet('author', size=10, order='term')

        if self.cleaned_data['from_page']:
            sqs = sqs.filter(no_of_pages__gte=self.cleaned_data['from_page'])
        if self.cleaned_data['from_words']:
            sqs = sqs.filter(no_of_words__gte=self.cleaned_data['from_words'])

            # Check to see if an end_date was chosen.
        if self.cleaned_data['to_page']:
            sqs = sqs.filter(no_of_pages__lte=self.cleaned_data['to_page'])
        if self.cleaned_data['to_words']:
            sqs = sqs.filter(no_of_words__lte=self.cleaned_data['to_words'])

        for facet in self.selected_facets:
            if ":" not in facet:
                continue

            field, value = facet.split(":", 1)

            if value:
                sqs = sqs.narrow(u'%s:"%s"' % (field, sqs.query.clean(value)))
            else:
                sqs = self.searchqueryset.facet(field, size=10, order='term')

        return sqs