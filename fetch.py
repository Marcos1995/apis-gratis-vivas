"""Escribe data/items.json. Es LO UNICO especifico de cada proyecto: reemplaza este fichero entero.

Contrato: lista de objetos
  {"slug": "kebab-case", "title": str, "summary": str,
   "facts": [["etiqueta", "valor"], ...],   # >=3 datos propios por pagina o se marca noindex
   "group": str (opcional), "updated": "YYYY-MM-DD" (opcional), "source": url (opcional)}

Reglas: solo fuentes publicas y estables, stdlib (urllib) salvo necesidad real, una peticion
ligera por recurso, sin claves de pago. Si una fuente falla: sys.exit(1) y NO tocar data/.
Historico (tendencias): lee el data/items.json anterior antes de sobrescribirlo.
Escribe con json.dumps(ensure_ascii=False, indent=1).
"""
import json
import re
import sys
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).parent
DATA = ROOT / "data"
ITEMS = DATA / "items.json"
HISTORY = DATA / "history.json"
README_URL = "https://raw.githubusercontent.com/public-apis/public-apis/master/README.md"
TIMEOUT = 10
WORKERS = 40
UA = {"User-Agent": "apis-gratis-vivas/1.0"}
LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
TRACKED = ("estado", "autenticacion", "https", "cors")


def get_text(url: str, timeout: int) -> str:
    req = Request(url, headers=UA)
    with urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8")


def parse_readme(md: str) -> list[dict]:
    apis, category, in_table = [], None, False
    for line in md.splitlines():
        if line.startswith("### "):
            category, in_table = line[4:].strip(), False
            continue
        if category and line.startswith("API |") and "HTTPS" in line and "CORS" in line:
            in_table = True
            continue
        if not in_table or not line.startswith("|"):
            if in_table and line.strip() and not line.startswith("|"):
                in_table = False
            continue
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if len(parts) < 5:
            continue
        match = LINK.search(parts[0])
        if not match:
            continue
        title = match.group(1).strip()
        apis.append({
            "title": title,
            "url": match.group(2).strip(),
            "summary": parts[1].strip() or title,
            "auth": parts[2].replace("`", "").strip() or "No",
            "https": parts[3].replace("`", "").strip() or "No",
            "cors": parts[4].replace("`", "").strip() or "Unknown",
            "group": category,
        })
    return apis


def slugify(title: str) -> str:
    text = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "api"


def assign_slugs(apis: list[dict]) -> None:
    seen: dict[str, int] = {}
    for api in apis:
        base = slugify(api["title"])
        n = seen.get(base, 0) + 1
        seen[base] = n
        api["slug"] = base if n == 1 else f"{base}-{n}"


def probe(url: str) -> tuple[int | None, int | None]:
    req = Request(url, headers=UA, method="GET")
    started = time.perf_counter()
    try:
        with urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status, int((time.perf_counter() - started) * 1000)
    except HTTPError as exc:
        return exc.code, int((time.perf_counter() - started) * 1000)
    except (URLError, TimeoutError, OSError, ValueError):
        return None, None


def vivo(code: int | None) -> bool:
    return code is not None and (200 <= code < 400 or code in (401, 403, 405))


def load_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def snapshot(entry: dict) -> dict:
    return {key: entry[key] for key in TRACKED}


def uptime_30(entries: list[dict], today) -> str:
    vivo_days = total = 0
    for offset in range(29, -1, -1):
        day = (today - timedelta(days=offset)).isoformat()
        estado = None
        for entry in entries:
            if entry["date"] <= day:
                estado = entry["estado"]
            else:
                break
        if estado is None:
            continue
        total += 1
        if estado == "vivo":
            vivo_days += 1
    if not total:
        return "sin datos"
    return f"{int(vivo_days * 100 / total + 0.5)}%"


def seed_history(history: dict, previous: list | None) -> None:
    if not previous:
        return
    for item in previous:
        slug = item.get("slug")
        if not slug or slug in history:
            continue
        facts = {k: v for k, v in item.get("facts") or []}
        if "Estado" not in facts:
            continue
        history[slug] = [{
            "date": item.get("updated") or datetime.now(timezone.utc).date().isoformat(),
            "estado": facts["Estado"],
            "autenticacion": facts.get("Autenticación", ""),
            "https": facts.get("HTTPS", ""),
            "cors": facts.get("CORS", ""),
        }]


def remember(history: dict, slug: str, today: str, current: dict) -> list[dict]:
    entries = history.setdefault(slug, [])
    if not entries or snapshot(entries[-1]) != current:
        entries.append({"date": today, **current})
    return entries


def dump(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def main() -> int:
    try:
        readme = get_text(README_URL, 30)
    except (URLError, TimeoutError, OSError, ValueError) as exc:
        print(f"fuente: {exc}", file=sys.stderr)
        return 1

    apis = parse_readme(readme)
    if len(apis) < 300:
        print(f"fuente: solo {len(apis)} APIs con Auth/HTTPS/CORS", file=sys.stderr)
        return 1
    assign_slugs(apis)

    try:
        previous = load_json(ITEMS)
        history = load_json(HISTORY)
    except json.JSONDecodeError as exc:
        print(f"data ilegible: {exc}", file=sys.stderr)
        return 1
    if history is None:
        history = {}
    if previous is not None and not isinstance(previous, list):
        print("data/items.json invalido", file=sys.stderr)
        return 1
    if not isinstance(history, dict):
        print("data/history.json invalido", file=sys.stderr)
        return 1
    seed_history(history, previous)

    urls = list(dict.fromkeys(api["url"] for api in apis))
    probed: dict[str, tuple[int | None, int | None]] = {}
    done = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(probe, url): url for url in urls}
        for future in as_completed(futures):
            probed[futures[future]] = future.result()
            done += 1
            if done % 200 == 0 or done == len(urls):
                print(f"comprobadas {done}/{len(urls)}", flush=True)

    today_d = datetime.now(timezone.utc).date()
    today = today_d.isoformat()
    items = []
    vivos = 0
    for api in apis:
        code, ms = probed[api["url"]]
        estado = "vivo" if vivo(code) else "muerto"
        vivos += estado == "vivo"
        current = {
            "estado": estado,
            "autenticacion": api["auth"],
            "https": api["https"],
            "cors": api["cors"],
        }
        entries = remember(history, api["slug"], today, current)
        items.append({
            "slug": api["slug"],
            "title": api["title"],
            "summary": api["summary"],
            "facts": [
                ["Estado", estado],
                ["Latencia", f"{ms} ms" if ms is not None else "sin respuesta"],
                ["Autenticación", api["auth"]],
                ["HTTPS", api["https"]],
                ["CORS", api["cors"]],
                ["Uptime 30 días", uptime_30(entries, today_d)],
            ],
            "group": api["group"],
            "updated": today,
            "source": api["url"],
        })

    DATA.mkdir(exist_ok=True)
    dump(HISTORY, history)
    dump(ITEMS, items)
    print(f"ok: {len(items)} APIs, {vivos} vivas -> {ITEMS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
