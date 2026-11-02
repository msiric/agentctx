#!/usr/bin/env python3
"""A stand-in for the Anthropic Messages API, for model-free harness tests.

Every request body is appended to $MOCK_LOG as one JSON line. Each reply is a
short text turn, unless $MOCK_SCRIPT names a JSON file holding a list of
replies; each entry is either a string (text) or {"tool": NAME, "input": {...}}
(a tool call). Entries are used in order; once the list runs out, it replies "ok".

    MOCK_LOG=req.jsonl python3 mock-anthropic.py 8765
"""
import json, os, sys, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

LOG = os.environ.get("MOCK_LOG", "mock-requests.jsonl")
script = json.load(open(os.environ["MOCK_SCRIPT"])) if os.environ.get("MOCK_SCRIPT") else []
lock = threading.Lock()
n = [0]

def next_reply():
    with lock:
        i = n[0]; n[0] += 1
    return script[i] if i < len(script) else "ok"

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def do_HEAD(self):
        self.send_response(200); self.end_headers()

    def do_GET(self):
        self.send_response(200); self.send_header("content-type", "application/json"); self.end_headers()
        self.wfile.write(b"{}")

    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("content-length", 0)) or 0)
        try:
            req = json.loads(body or b"{}")
        except ValueError:
            req = {}
        with lock, open(LOG, "a") as f:
            f.write(json.dumps({"path": self.path, "body": req}) + "\n")
        if "count_tokens" in self.path:
            return self.json({"input_tokens": len(body) // 4})
        reply = next_reply() if req.get("messages") else "ok"
        if isinstance(reply, str):
            block = {"type": "text", "text": reply}; stop = "end_turn"
        else:
            block = {"type": "tool_use", "id": "toolu_%d" % n[0], "name": reply["tool"], "input": reply.get("input", {})}; stop = "tool_use"
        usage = {"input_tokens": len(body) // 4, "output_tokens": 5, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}
        msg = {"id": "msg_mock", "type": "message", "role": "assistant", "model": req.get("model", "mock"),
               "content": [block], "stop_reason": stop, "stop_sequence": None, "usage": usage}
        if not req.get("stream"):
            return self.json(msg)
        self.send_response(200)
        self.send_header("content-type", "text/event-stream"); self.end_headers()
        def ev(name, data):
            self.wfile.write(f"event: {name}\ndata: {json.dumps(data)}\n\n".encode())
        start = dict(msg, content=[], stop_reason=None)
        ev("message_start", {"type": "message_start", "message": start})
        if block["type"] == "text":
            ev("content_block_start", {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}})
            ev("content_block_delta", {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": block["text"]}})
        else:
            ev("content_block_start", {"type": "content_block_start", "index": 0, "content_block": dict(block, input={})})
            ev("content_block_delta", {"type": "content_block_delta", "index": 0, "delta": {"type": "input_json_delta", "partial_json": json.dumps(block["input"])}})
        ev("content_block_stop", {"type": "content_block_stop", "index": 0})
        ev("message_delta", {"type": "message_delta", "delta": {"stop_reason": stop, "stop_sequence": None}, "usage": {"output_tokens": 5}})
        ev("message_stop", {"type": "message_stop"})

    def json(self, obj):
        b = json.dumps(obj).encode()
        self.send_response(200); self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(b))); self.end_headers(); self.wfile.write(b)

if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", int(sys.argv[1]) if len(sys.argv) > 1 else 8765), H).serve_forever()
