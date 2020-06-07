import re

from bridge.from_choice import to_format


class Searcher:

    def __init__(self):
        self.ctx = None

    def set_context(self, ctx):
        self.ctx = ctx

    def queryset(self, search, storage, fields):
        entry_query = self.get_query(search, [to_format(field) for field in fields])
        found_entries = self.ctx.Cargo().order_by("-date_added").query().filter(entry_query)
        return found_entries

    def get_query(self, query_string, search_fields):
        query = None  # Query to search for every search term
        terms = self.normalize_query(query_string)
        for term in terms:
            or_query = None  # Query to search for a given term in each field
            for field_name in search_fields:
                q = Q(**{"%s__icontains" % field_name: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query & or_query
        return query

    def normalize_query(
            self,
            query_string,
            findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
            normspace=re.compile(r'\s{2,}').sub):
        return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]
