"""Sincronizza prompt degli agenti, catalogo e documenti di esempio dentro app/index.html.

I prompt si modificano solo in agents/runtime/*.md (blocco ```prompt).
Uso:  python agents/sync_prompts.py
"""
import base64, json, re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RUNTIME = ROOT / "agents" / "runtime"
APP = ROOT / "app" / "index.html"
AGENTI = {
    "lettore": "01-lettore-fattura.md",
    "classificatore": "02-classificatore-prestazione.md",
    "verificatore": "03-verificatore-prescrizione.md",
    "traduttore": "04-traduttore-errori.md",
}
INIZIO, FINE = "/* AGENTI:INIZIO */", "/* AGENTI:FINE */"
E_INIZIO, E_FINE = "/* ESEMPI:INIZIO */", "/* ESEMPI:FINE */"
ESEMPI = ROOT / "app" / "esempi"


def sostituisci(html, inizio, fine, blocco):
    if inizio not in html or fine not in html:
        sys.exit(f"Marcatori {inizio} non trovati in app/index.html")
    return re.sub(re.escape(inizio) + r".*?" + re.escape(fine), lambda _: blocco, html, flags=re.S)


def estrai_prompt(path):
    m = re.search(r"```prompt\n(.*?)\n```", path.read_text(encoding="utf-8"), re.S)
    if not m:
        sys.exit(f"Nessun blocco ```prompt in {path.name}")
    return m.group(1).strip()


def main():
    prompts = {k: estrai_prompt(RUNTIME / f) for k, f in AGENTI.items()}
    catalogo = json.loads((RUNTIME / "catalogo-prestazioni.json").read_text(encoding="utf-8"))["voci"]
    blocco = (
        f"{INIZIO}\n"
        f"const PROMPTS = {json.dumps(prompts, ensure_ascii=False, indent=1)};\n"
        f"const CATALOGO = {json.dumps(catalogo, ensure_ascii=False)};\n"
        f"{FINE}"
    )
    esempi = {k: base64.b64encode((ESEMPI / f"{k}_esempio.jpg").read_bytes()).decode() for k in ("fattura", "prescrizione")}
    blocco_esempi = f"{E_INIZIO}\nconst ESEMPI = {json.dumps(esempi)};\n{E_FINE}"
    html = APP.read_text(encoding="utf-8")
    html = sostituisci(html, INIZIO, FINE, blocco)
    html = sostituisci(html, E_INIZIO, E_FINE, blocco_esempi)
    APP.write_text(html, encoding="utf-8")
    print(f"Sincronizzati {len(prompts)} prompt, {len(catalogo)} voci di catalogo e {len(esempi)} documenti di esempio in {APP.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
