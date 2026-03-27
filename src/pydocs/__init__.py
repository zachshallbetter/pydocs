"""PYDocs package."""

from .api import extract_file, extract_json, extract_text
from .models import AssociationContext, AssociationNode, AssociationTag

__all__ = [
    "__version__",
    "AssociationContext",
    "AssociationNode",
    "AssociationTag",
    "extract_file",
    "extract_json",
    "extract_text",
]

__version__ = "0.1.0"
