from __future__ import annotations

import json
import unittest

from pydocs import extract_associations


class ExtractorTests(unittest.TestCase):
    def test_extracts_function_docstring_tags(self) -> None:
        source = '''
def authenticate(token: str) -> str:
    """
    Authenticate a session token.

    @associated doc:auth-flow.md
    @see symbol:Session
    """
    return token
'''
        nodes = extract_associations(source, filename="auth.py")

        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].kind, "pydoc")
        self.assertEqual(nodes[0].attachedToContext.kind, "function")
        self.assertEqual(nodes[0].attachedToContext.qualifiedName, "authenticate")
        self.assertEqual(nodes[0].tags[0].tag, "associated")
        self.assertEqual(nodes[0].tags[0].normalizedValue, "doc:auth-flow.md")
        self.assertEqual(nodes[1].tags[0].tag, "see")

    def test_extracts_comment_anchored_assignment(self) -> None:
        source = """
# @associated doc:auth-config.md
AUTH_TOKEN_TTL = 3600
"""
        nodes = extract_associations(source, filename="settings.py")

        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].attachedToContext.kind, "assignment")
        self.assertEqual(nodes[0].attachedToContext.qualifiedName, "AUTH_TOKEN_TTL")
        self.assertEqual(nodes[0].line, 2)
        self.assertEqual(nodes[0].tags[0].normalizedValue, "doc:auth-config.md")

    def test_extracts_nested_qualified_names(self) -> None:
        source = '''
class AuthService:
    """
    @see symbol:Session
    """

    @property
    def token(self) -> str:
        """
        @associated doc:token.md
        """
        return "value"
'''
        nodes = extract_associations(source, filename="service.py")

        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].attachedToContext.kind, "class")
        self.assertEqual(nodes[0].attachedToContext.qualifiedName, "AuthService")
        self.assertEqual(nodes[1].attachedToContext.kind, "property")
        self.assertEqual(nodes[1].attachedToContext.qualifiedName, "AuthService.token")

    def test_serializes_to_json_cleanly(self) -> None:
        source = """
# @see doc:example.md
VALUE = 1
"""
        payload = [node.to_dict() for node in extract_associations(source)]
        raw = json.dumps(payload)
        self.assertIn("example.md", raw)


if __name__ == "__main__":
    unittest.main()
