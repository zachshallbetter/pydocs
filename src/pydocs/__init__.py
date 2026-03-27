"""PYDocs package."""

from .extractor import extract_associations
from .models import AssociationContext, AssociationNode, AssociationTag

__all__ = [
    "__version__",
    "AssociationContext",
    "AssociationNode",
    "AssociationTag",
    "extract_associations",
]

__version__ = "0.1.0"
