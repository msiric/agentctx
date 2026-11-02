import contextlib
import json.decoder


@contextlib.contextmanager
def count_json_parses():
    """Count JSON documents decoded through the stdlib json module."""
    calls = [0]
    original = json.decoder.JSONDecoder.decode

    def decode(self, s, *args, **kwargs):
        calls[0] += 1
        return original(self, s, *args, **kwargs)

    json.decoder.JSONDecoder.decode = decode
    try:
        yield calls
    finally:
        json.decoder.JSONDecoder.decode = original
