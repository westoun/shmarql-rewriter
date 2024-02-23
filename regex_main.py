#!/usr/bin/env python3

import re
from typing import Callable, List


def normalize_query(query: str, max_iterations: int = 10) -> str:
    for _ in range(max_iterations):
        match = re.search(r"(\?[a-zA-z]+)\s+(?:\<\S+\>)\s+(?:\S+)\s*(;)", query)

        if match is None:
            break

        subject = match.groups()[0]
        target_i = match.span()[1]

        query = query[: target_i - 1] + f". \n{subject}" + query[target_i + 2 :]

    return query


class QueryRewriter:
    rewrite_functions = {}

    def __init__(self) -> None:
        pass

    def rewrite(self, query: str) -> str:
        query = normalize_query(query)

        for match in reversed(
            list(re.finditer(r"(\?[a-zA-z]+)\s+(\S+)\s+(\S+)\s*\.", query))
        ):
            subject, predicate, object = match.groups()
            start_i, end_i = match.span()

            if not predicate in self.rewrite_functions:
                continue

            target_values = self.rewrite_functions[predicate](object)

            replacement_text = f"VALUES {subject} {{{' '.join(target_values)}}}"

            query = query[: start_i - 1] + replacement_text + query[end_i - 1 :]

        return query

    def register_rewrite_function(
        self, predicate: str, function: Callable[[str], List[str]]
    ) -> None:
        self.rewrite_functions[predicate] = function


def spellcheck(text: str) -> List[str]:
    return ['"bread"']


if __name__ == "__main__":
    query = """
        PREFIX schema: <https://schema.org>
        SELECT ?sub ?o WHERE {
            ?sub dbo:test "blob" .
            ?sub <http://hackalod/fizzy/fts> "Fossenburg" .
            ?sub schema:name ?o .
            ?o <barf> "blarg";
            <http://hackalod/fizzy/spellcheck> "bried";
            <burfl> 2 .
        }
    """

    rewriter = QueryRewriter()
    rewriter.register_rewrite_function("<http://hackalod/fizzy/spellcheck>", spellcheck)

    query = rewriter.rewrite(query)
    print(query)
