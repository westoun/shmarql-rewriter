#!/usr/bin/env python3

from rdflib.plugins.sparql.parser import (
    expandUnicodeEscapes,
    Query,
    IRIREF,
)


from rdflib import URIRef
from rdflib.term import Variable

from pyparsing import ParseResults, originalTextFor, locatedExpr


def uri_action(string, location, tokens) -> URIRef:
    res = URIRef(tokens[0])
    setattr(res, "loc", location)
    return res


# Overwrite/extend rdflib parse action
IRIREF.setParseAction(uri_action)


def parseQuery(q: str) -> ParseResults:
    if hasattr(q, "read"):
        q = q.read()
    if isinstance(q, bytes):
        q = q.decode("utf-8")

    q = expandUnicodeEscapes(q)
    return Query.parseString(q, parseAll=True)


query = """
PREFIX schema: <https://schema.org>
SELECT ?sub ?o WHERE {
    ?sub dbo:test "blob" .
    ?sub <http://hackalod/fizzy/fts> "Fossenburg" .
    ?sub schema:name ?o .
    ?o <barf> "blarg";
       <burfl> 2 .
}
"""



raise 

result: ParseResults = parseQuery(query)

where_clause = result[1].where
triples = where_clause["part"][0]["triples"]

for triple in triples:
    # interestingly, triple can contain more than 3 entries.
    # especially if line ends beyond "." are used.

    for i, item in enumerate(triple):

        try:
            uri_ref = item["part"][0]["part"][0]["part"]
            uri = str(uri_ref)

            source_ref = triple[i - 1]
            source = str(source_ref)

            target_ref = triple[i + 1]
            target = str(target_ref)

            print(uri, uri_ref.loc)
            print(source)
            print(target)
            print()


        except:
            pass

    #     print(item)
    #     print()
