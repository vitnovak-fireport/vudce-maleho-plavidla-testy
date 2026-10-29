"""Stáhne otázky M, C a S ze spspraha.cz do questions.json a obrázky do img/."""
import html, json, os, re, sys, urllib.request

SOURCES = {
    "M": "https://www.spspraha.cz/zkousky/otazky.asp?zp=M%202015",
    "C": "https://www.spspraha.cz/zkousky/otazky.asp?zp=C",
    "S": "https://www.spspraha.cz/zkousky/otazky.asp?zp=S%202015",
}
IMG_URL = "http://www.spspraha.cz/zkousky/images/"


def get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read()


def clean(s):
    imgs = re.findall(r'<img[^>]*src="([^"]+)"', s, flags=re.I)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = html.unescape(re.sub(r"<[^>]+>", "", s)).replace("\xa0", " ")
    return re.sub(r"[ \t]+", " ", s).strip(), [i.rsplit("/", 1)[1] for i in imgs]


def parse(key, page):
    page = re.sub(r"<!--.*?-->", "", page, flags=re.S)
    qs = []
    for b in re.split(r'<tr class="bg">', page)[1:]:
        num = re.search(r"č\. <span[^>]*>(\d+)</span>", b).group(1)
        setc = re.search(r"Zkratka souboru otázek:</i></span>\s*([^<]*)", b).group(1).strip()
        q, qimg, ans, correct = None, [], [], None
        for th, rest in re.findall(r"<th[^>]*>(.*?)</th>(.*?)</tr>", b, flags=re.S):
            th = html.unescape(th)
            txt, imgs = clean(rest)
            if th.startswith("Otázka"):
                q, qimg = txt, imgs
            else:
                if "Správná" in th:
                    correct = len(ans)
                ans.append({"t": txt, "img": imgs})
        assert q is not None and correct is not None and len(ans) >= 2, (key, num)
        qs.append({"id": f"{key}{num}", "n": int(num), "set": setc, "q": q, "img": qimg, "a": ans, "c": correct})
    return qs


def main():
    out = {k: parse(k, get(u).decode("utf-8")) for k, u in SOURCES.items()}
    for k, qs in out.items():
        print(k, len(qs), "otázek", file=sys.stderr)
    with open("questions.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)
    os.makedirs("img", exist_ok=True)
    names = {i for qs in out.values() for q in qs for i in q["img"] + [x for a in q["a"] for x in a["img"]]}
    for n in sorted(names):
        path = os.path.join("img", n)
        if not os.path.exists(path):
            with open(path, "wb") as f:
                f.write(get(IMG_URL + n))
    print(len(names), "obrázků", file=sys.stderr)


if __name__ == "__main__":
    main()
