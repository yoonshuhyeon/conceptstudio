import os
from datetime import datetime, timezone

from flask import Flask, jsonify, request, send_from_directory


PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "public")

app = Flask(__name__, static_folder="public", static_url_path="")


@app.get("/api/health")
def health():
    return jsonify(
        {
            "ok": True,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )


@app.post("/api/events")
def events():
    event = request.get_json(silent=True)
    print(
        "[event]",
        {
            "at": datetime.now(timezone.utc).isoformat(),
            "ip": request.remote_addr,
            "event": event,
        },
        flush=True,
    )
    return jsonify({"ok": True}), 202


@app.get("/")
def index():
    return send_from_directory(PUBLIC_DIR, "index.html")


@app.get("/<path:subpath>")
def static_or_index(subpath: str):
    # If the file exists under public/, serve it. Otherwise serve index.html
    # so the app still loads even for unknown paths.
    candidate = os.path.join(PUBLIC_DIR, subpath)
    if os.path.isfile(candidate):
        return send_from_directory(PUBLIC_DIR, subpath)

    # Keep /api/* as JSON 404
    if subpath.startswith("api/"):
        return jsonify({"ok": False, "error": "Not found"}), 404

    return send_from_directory(PUBLIC_DIR, "index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "3000"))
    app.run(host="0.0.0.0", port=port)
