from django.shortcuts import render, render_to_response

from meta.views import MetadataMixin
from django_json_ld.views import JsonLdContextMixin
from django.utils.translation import gettext as _

from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView

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



class WritingPageView(MetadataMixin,JsonLdContextMixin, TemplateView):
    title = 'Writing and content editing services | desklib.com'
    description = 'Desklib provides free writing tools for everyone to improve their writing skills. Hire top content writers and proofreaders for your content requirements.'

    template_name = "writing/writing.html"

    structured_data = {
        "@type": "Organization",
        "name": "Writing and content editing services",
        "description": _("Desklib provides free writing tools for everyone to improve their writing skills. Hire top content writers and proofreaders for your content requirements."),
        "url": "https://desklib.com/writing/",
        "logo": "https://desklib.com/static/dist/assets/images/desklib-logo-theme.png",
        "potentialAction": {
            "@type": "SearchAction",
            "target": "https://www.desklib.com/study/search/?q={search_term}",
            "query-input": "required name=search_term"
        },
        "sameAs": [
            "https://www.facebook.com/desklib",
            "https://twitter.com/desklib",
            "https://www.linkedin.com/company/desklib",
            "https://www.instagram.com/desklib/"
        ]
    }

    def get_structured_data(self):
        sd = super(WritingPageView, self).get_structured_data()
        return sd


class ComparePageView(MetadataMixin,JsonLdContextMixin, FormView):
    form_class = CompareForm
    use_title_tag = True
    title = 'Compare two texts for similarity for free | Desklib'
    description = 'Plagiarism comparison tool for comparing two texts or documents. This free tool compares two texts for similarity and displays copied content.'

    template_name = "writing/compare.html"

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
            threshold_count = 4
            s1 = form.cleaned_data['textarea1']
            s2 = form.cleaned_data['textarea2']

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
            data['matching_length'] = len(matches_data_list)
            data['total_word_s1'] = len(n1)
            data['total_word_s2'] = len(n2)
            data['similarity_s1'] = total_match*100/len(n1)
            data['similarity_s2'] = total_match*100/len(n2)

            return render(request, template_name='writing/result.html',context=data)

        else:
            return render(request, self.template_name, {
                'form': form,
            })




class SpellCheckPageView(MetadataMixin,JsonLdContextMixin, FormView):
    form_class = SpellCheckForm
    title = 'Free grammar check and spell corrector | Desklib'
    use_title_tag = True
    description = 'Check your text for grammar corrections and spelling mistakes using our free tool. Get free writing tips and suggestions to improve your writing skills.'

    template_name = "writing/spell_check.html"

    structured_data = {
        "@type": "Organization",
        "name": "This is writing Company home",
        "description": _("A writing company."),
    }

    def get_structured_data(self):
        sd = super(SpellCheckPageView, self).get_structured_data()
        return sd


class GrammarCorrectPageView(MetadataMixin,JsonLdContextMixin, FormView):
    form_class = SpellCheckForm
    title = 'spell check page'
    use_title_tag = True
    description = 'This is a spell check page'

    template_name = "writing/grammar_correct.html"

    structured_data = {
        "@type": "Organization",
        "name": "This is writing Company home",
        "description": _("A writing company."),
    }

    def get_structured_data(self):
        sd = super(GrammarCorrectPageView, self).get_structured_data()
        return sd
