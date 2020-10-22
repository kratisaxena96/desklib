# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.utils import timezone

from haystack.backends import BaseEngine
from haystack.backends.elasticsearch2_backend import Elasticsearch2SearchBackend
from haystack.backends.elasticsearch2_backend import Elasticsearch2SearchQuery
from haystack.constants import ID
from haystack.utils import get_identifier
from haystack.exceptions import MissingDependency, SkipDocument
from tqdm import tqdm

try:
    import elasticsearch
    if not ((2, 0, 0) <= elasticsearch.__version__ < (3, 0, 0)):
        raise ImportError
    from elasticsearch.helpers import bulk, scan
except ImportError:
    raise MissingDependency("The 'elasticsearch2' backend requires the \
                            installation of 'elasticsearch>=2.0.0,<3.0.0'. \
                            Please refer to the documentation.")


class Elasticsearch2SearchBackendUpdated(Elasticsearch2SearchBackend):
    def __init__(self, connection_alias, **connection_options):
        super(Elasticsearch2SearchBackendUpdated, self).__init__(connection_alias, **connection_options)
        self.content_field_name = None


    def update(self, index, iterable, commit=True):
        if not self.setup_complete:
            try:
                self.setup()
            except elasticsearch.TransportError as e:
                if not self.silently_fail:
                    raise

                self.log.error("Failed to add documents to Elasticsearch: %s", e, exc_info=True)
                return

        prepped_docs = []
        for obj in tqdm(iterable, colour='#44f172'):
        # for obj in iterable:
            if obj.is_visible and obj.is_published and obj.published_date < timezone.now():
                try:
                    prepped_data = index.full_prepare(obj)
                    final_data = {}

                    # Convert the data to make sure it's happy.
                    for key, value in prepped_data.items():
                        final_data[key] = self._from_python(value)
                    final_data['_id'] = final_data[ID]

                    prepped_docs.append(final_data)
                    # print(obj.slug)
                except SkipDocument:
                    self.log.debug(u"Indexing for object `%s` skipped", obj)
                except elasticsearch.TransportError as e:
                    if not self.silently_fail:
                        raise

                    # We'll log the object identifier but won't include the actual object
                    # to avoid the possibility of that generating encoding errors while
                    # processing the log message:
                    self.log.error(u"%s while preparing object for update" % e.__class__.__name__, exc_info=True,
                                   extra={"data": {"index": index,
                                                   "object": get_identifier(obj)}})

        bulk(self.conn, prepped_docs, index=self.index_name, doc_type='modelresult')

        if commit:
            self.conn.indices.refresh(index=self.index_name)


class Elasticsearch2SearchQueryUpdated(Elasticsearch2SearchQuery):
    pass


class Elasticsearch2SearchUpdatedEngine(BaseEngine):
    backend = Elasticsearch2SearchBackendUpdated
    query = Elasticsearch2SearchQueryUpdated