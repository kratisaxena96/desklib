from haystack.forms import SearchForm


class HomeSearchForm(SearchForm):
    def __init__(self, *args, **kwargs):
        super(HomeSearchForm, self).__init__(*args, **kwargs)

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()

        sqs = self.searchqueryset.auto_query(self.cleaned_data['q'])

        if self.load_all:
            sqs = sqs.load_all()

        return sqs


