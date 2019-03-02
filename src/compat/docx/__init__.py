# encoding: utf-8

import os
import sys


def uppath(n=1):
    if n == 0:
        return os.path.abspath(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(os.path.dirname(__file__), (os.pardir + os.sep) * (n - 1) + os.pardir))


print('compat docx')
sys.path.append(uppath(1))

from docx.api import Document  # noqa

__version__ = '0.8.7'

# register custom Part classes with opc package reader

from docx.opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT
from docx.opc.part import PartFactory
from docx.opc.parts.coreprops import CorePropertiesPart

from docx.parts.document import DocumentPart
from docx.parts.image import ImagePart
from docx.parts.numbering import NumberingPart
from docx.parts.settings import SettingsPart
from docx.parts.styles import StylesPart


def part_class_selector(content_type, reltype):
    if reltype == RT.IMAGE:
        return ImagePart
    return None


PartFactory.part_class_selector = part_class_selector
PartFactory.part_type_for[CT.OPC_CORE_PROPERTIES] = CorePropertiesPart
PartFactory.part_type_for[CT.WML_DOCUMENT_MAIN] = DocumentPart
PartFactory.part_type_for[CT.WML_NUMBERING] = NumberingPart
PartFactory.part_type_for[CT.WML_SETTINGS] = SettingsPart
PartFactory.part_type_for[CT.WML_STYLES] = StylesPart

del (
    CT, CorePropertiesPart, DocumentPart, NumberingPart, PartFactory,
    StylesPart, part_class_selector
)
