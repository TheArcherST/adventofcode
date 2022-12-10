import dataclasses
import re
from enum import Enum
from typing import Optional, Dict

import docutils.frontend
import docutils.nodes
import docutils.parsers.rst
import docutils.utils

from fastaoc.models import TestCase


def parse_rst(text: str) -> docutils.nodes.document:
    parser = docutils.parsers.rst.Parser()
    components = (docutils.parsers.rst.Parser,)
    settings = docutils.frontend.OptionParser(components=components).get_default_values()
    document = docutils.utils.new_document('<rst-doc>', settings=settings)
    parser.parse(text, document)
    return document


class FieldRegexps:
    INPUT = 'input( [0-9]+)?'
    OUTPUT = 'output( [0-9]+)?'


class FieldType(Enum):
    UNDEFINED = 'UNDEFINED'
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'


@dataclasses.dataclass
class Field:
    type: FieldType
    number: Optional[int] = None


class _DocstringVisitor(docutils.nodes.SparseNodeVisitor):
    inputs: Dict[int, str] = dict()
    outputs: Dict[int, str] = dict()

    @staticmethod
    def _parse_field(field_name: str) -> Field:
        if match := re.fullmatch(FieldRegexps.INPUT, field_name):

            if sel := match.group(1):
                sel = int(sel)
            else:
                sel = None

            return Field(FieldType.INPUT, sel)
        elif match := re.fullmatch(FieldRegexps.OUTPUT, field_name):

            if sel := match.group(1):
                sel = int(sel)
            else:
                sel = None

            return Field(FieldType.OUTPUT, sel)
        else:
            return Field(FieldType.UNDEFINED, None)

    def visit_field(self, node: docutils.nodes.field) -> None:
        """Called for "reference" nodes."""
        field_name, field_body = node.children
        field = self._parse_field(field_name.astext())

        if field.type is FieldType.INPUT:
            number = field.number or (max([-1, *self.inputs.keys()]) + 1)
            self.inputs.update({number: field_body.astext()})
        elif field.type is FieldType.OUTPUT:
            number = field.number or (max([-1, *self.outputs.keys()]) + 1)
            self.outputs.update({number: field_body.astext()})
        elif field.type is FieldType.UNDEFINED:
            pass
        else:
            raise KeyError

    def unknown_visit(self, node: docutils.nodes.Node) -> None:
        """Called for all other node types."""
        pass


def docstring_to_tests(docstring: str) -> list['TestCase']:
    document = parse_rst(docstring)
    visitor = _DocstringVisitor(document)
    document.walk(visitor)
    result = []

    for k in sorted(visitor.inputs.keys()):
        result.append(
            TestCase(
                visitor.inputs[k], visitor.outputs[k]
            )
        )

    return result
