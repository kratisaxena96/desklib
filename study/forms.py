from django import forms
from haystack.forms import FacetedSearchForm

class CustomFacetedSearchForm(FacetedSearchForm):
    def __init__(self, *args, **kwargs):
        super(CustomFacetedSearchForm, self).__init__(*args, **kwargs)

    def search(self):

        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q') and not self.selected_facets:
            return self.no_query_found()

        # sqs = self.searchqueryset.auto_query(self.cleaned_data.get('q'))
        sqs = self.searchqueryset.all()

        if self.load_all:
            sqs = sqs.load_all()
        # We need to process each facet to ensure that the field name and the
        # value are quoted correctly and separately:
        self.searchqueryset.facet('author', size=10, order='term')

        for facet in self.selected_facets:
            if ":" not in facet:
                continue

            field, value = facet.split(":", 1)

            if value:
                sqs = sqs.narrow(u'%s:"%s"' % (field, sqs.query.clean(value)))
            else:
                sqs = self.searchqueryset.facet(field, size=10, order='term')

        return sqs