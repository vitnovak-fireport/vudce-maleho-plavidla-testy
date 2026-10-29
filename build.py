"""Vloží questions.json do template.html a vytvoří index.html."""
import json

data = json.load(open("questions.json", encoding="utf-8"))
template = open("template.html", encoding="utf-8").read()
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", r"<\/")
open("index.html", "w", encoding="utf-8").write(template.replace("__DATA__", payload))
