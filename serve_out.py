#!/usr/bin/env python3
# serve_out.py — minimal HTTP server for DeepLinks /out
# - Serves ONLY the ./out directory
# - Random high port by default (ephemeral); override with --port or PORT env

import argparse, http.server, os, random, socket, socketserver, sys
from pathlib import Path

OUT_DIR = Path(__file__).parent / "out"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(OUT_DIR), **kwargs)
    def log_message(self, fmt, *args):
        sys.stdout.write("[http] " + (fmt % args) + "\n")
    def end_headers(self):
        # Light CORS for convenience
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

def pick_port(preferred: int | None) -> int:
    if preferred and 1 <= preferred <= 65535:
        return preferred
    # random high port
    for _ in range(32):
        p = random.randint(49152, 65535)
        with socket.socket() as s:
            try:
                s.bind(("", p))
                return p
            except OSError:
                continue
    return 6967  # last resort

def host_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def main():
    parser = argparse.ArgumentParser(description="Serve DeepLinks ./out over HTTP")
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "0")),
                        help="Port to bind (0 or omit for random high port)")
    parser.add_argument("--host", default=os.getenv("HOST", "0.0.0.0"),
                        help="Host/IP to bind (default 0.0.0.0)")
    args = parser.parse_args()

    if not OUT_DIR.exists():
        print(f"[serve_out] Missing {OUT_DIR}. Run generate_guide.py first.")
        sys.exit(1)

    port = pick_port(args.port if args.port != 0 else None)
    httpd = socketserver.TCPServer((args.host, port), Handler)
    httpd.allow_reuse_address = True

    lan = host_ip() if args.host in ("0.0.0.0", "") else args.host
    base = f"http://{lan}:{port}"
    print("==================================")
    print("DeepLinks — /out HTTP server")
    print("==================================")
    print(f"Serving: {OUT_DIR.resolve()}")
    print(f"Listen : {args.host}:{port}")
    print("Open   :", base)
    print("Files  :", f"{base}/espn_plus.xml", f"{base}/espn_plus.m3u", sep="\n         ")
    print("==================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[serve_out] shutting down...")
    finally:
        httpd.server_close()

if __name__ == "__main__":
    main()
