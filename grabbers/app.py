#!/usr/bin/env python
import re

from httpx import AsyncClient
from loguru import logger
from orjson import dumps, loads
from sanic import Sanic, raw

app = Sanic("Jumper", dumps=dumps, loads=loads)


class Cache:
    last_domain = ""


@app.route("", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def index(request):
    return raw(b"Welcome. Example>> http :8000/http.127.0.0.1:9000/home")


@app.route("/<full:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def handler(request, full: str):
    host, url = full.lstrip("/"), ""
    if m := re.search(r"(https?)[^0-9a-zA-Z]+(.+)", host):
        scheme, host = m.groups()
    else:
        scheme = "https"
    try:
        domain, url = host.split("/", 1)
    except ValueError:
        domain = host
    else:
        if "." not in domain:
            domain = Cache.last_domain
            url = host
    base_url = scheme + "://" + domain
    target_path = url
    if qs := request.query_string:
        target_path += "?" + qs
    if not target_path:
        target_path = base_url
    if not target_path.startswith("/") and not target_path.startswith("http"):
        target_path = "/" + target_path
    logger.debug(f"{base_url=}; {target_path=}")
    async with AsyncClient(
        base_url=base_url, follow_redirects=True, timeout=20
    ) as client:
        method, body = request.method, request.body
        r = await client.request(method, target_path, content=body)
        if r.status_code == 302 and (next_url := r.headers.get("location")):
            r = await client.request(method, next_url, content=body)
    if r.status_code < 300:
        Cache.last_domain = domain
    for key in r.headers:
        if key.lower() == "content-type":
            headers = {key: r.headers.get(key)}
            return raw(r.content, status=r.status_code, headers=headers)
    return raw(r.content, status=r.status_code)


if __name__ == "__main__":  # pragma: no cover
    app.run(debug=True, host="0.0.0.0")
