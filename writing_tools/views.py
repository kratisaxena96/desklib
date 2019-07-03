from django.shortcuts import render, render_to_response

from meta.views import MetadataMixin
from django_json_ld.views import JsonLdContextMixin
from django.utils.translation import gettext as _

from django.views.generic.edit import CreateView, FormView

from .models import Compare, Spell
from .forms import CompareForm, SpellCheckForm

from nltk.tokenize import word_tokenize
import nltk
import re
import difflib
from nltk.util import ngrams
from difflib import SequenceMatcher
from string import punctuation
from termcolor import colored


# Create your views here.

class ComparePageView(MetadataMixin,JsonLdContextMixin, FormView):
    form_class = CompareForm
    use_title_tag = True
    title = 'compare page'
    description = 'This is a compare page'

    template_name = "writing_tools/compare.html"

    context = {}

    structured_data = {
        "@type": "Organization",
        "name": "This is writing Company home",
        "description": _("A writing company."),
    }

    def get_structured_data(self):
        sd = super(ComparePageView, self).get_structured_data()
        return sd

    def get_context_data(self, **kwargs):
        context = super(ComparePageView, self).get_context_data(**kwargs)

        return context

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form = CompareForm(self.request.POST)

        if form.is_valid():
            compare_obj = form.save(commit=False)
            threshold_count = 4
            s1 = compare_obj.textarea1
            s2 = compare_obj.textarea2

            n1 = list(ngrams(word_tokenize(s1), 1))
            n2 = list(ngrams(word_tokenize(s2), 1))
            sequence = SequenceMatcher(None, n1, n2)
            matches = sequence.get_matching_blocks()

            data = {}
            matches_data_list = []
            total_match = 0
            for m in matches:
                if m.size >= threshold_count:
                    match_data = {}
                    match_data['left_string'] = " ".join([" ".join(ngram) for ngram in n1[m.a: m.a + m.size]])
                    match_data['no_of_matches'] = '<< ' + str(m.size) + ' words' + ' >>'
                    match_data['right_string'] = " ".join([" ".join(ngram) for ngram in n2[m.b: m.b + m.size]])
                    matches_data_list.append(match_data)
                    total_match = total_match + m.size

            data['matches'] = matches_data_list
            data['total_word_s1'] = len(n1)
            data['total_word_s2'] = len(n2)
            data['similarity_s1'] = total_match*100/len(n1)
            data['similarity_s2'] = total_match*100/len(n2)

            return render(request, template_name='writing_tools/result.html',context=data)

        else:
            return render(request, self.template_name, {
                'form': form,
            })




class SpellCheckPageView(MetadataMixin,JsonLdContextMixin, FormView):
    form_class = SpellCheckForm
    title = 'spell check page'
    use_title_tag = True
    description = 'This is a spell check page'

    template_name = "writing_tools/spell_check.html"

    structured_data = {
        "@type": "Organization",
        "name": "This is writing Company home",
        "description": _("A writing company."),
    }

    def get_structured_data(self):
        sd = super(SpellCheckPageView, self).get_structured_data()
        return sd
