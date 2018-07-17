"""
Unit tests for write leda.
"""
from nose.tools import assert_equal
import writeleda as wl
import io
import networkx as nx


class TestWriteLeda:
    def test_write_leda(self):
        fh = io.BytesIO()
        nx.write_leda(self.graph, fh)
        fh.seek(0)
        assert_equal(
            fh.read(),
            b"LEDA.GRAPH\nstring\nint\n-1\n2\n|{1}|\n|{2}|\n1\n1 2 0 |{0}|\n"
        )