# Public API

## `extract_text`

```python
extract_text(source: str, *, filename: str = "<string>")
```

Parse a Python source string and return a list of `AssociationNode` objects.

## `extract_file`

```python
extract_file(path: str | Path)
```

Read a file from disk and return a list of `AssociationNode` objects.

## `extract_json`

```python
extract_json(source: str, *, filename: str = "<string>") -> str
```

Return a JSON serialization of extracted associations.
