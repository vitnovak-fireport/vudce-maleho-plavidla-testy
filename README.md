# Trenažér VMP

Webová aplikace na procvičování testových otázek ke zkoušce vůdce malého plavidla (M a C).
Otázky pocházejí ze [spspraha.cz](https://www.spspraha.cz/zkousky/).

Aplikace je vystavená pomocí Cloudflare Pages na https://vudce-maleho-plavidla-testy.drozdak.cz/.

- otázky v náhodném pořadí, odpovědi pokaždé zamíchané
- okamžitá zpětná vazba po odpovědi
- špatně zodpovězené otázky se vracejí častěji (Leitnerovy přihrádky), po 3 správných odpovědích v řadě je otázka zvládnutá
- výběr zkoušky (M, C, M + C), okruhů a režim „Jen chyby“

## Soubory

- `template.html` – zdroj aplikace (HTML, CSS, JS)
- `questions.json`, `img/` – otázky a obrázky
- `index.html` – sestavená stránka (šablona s vloženými otázkami)

## Aktualizace otázek a sestavení

```
py fetch_questions.py   # stáhne otázky a obrázky ze spspraha.cz
py build.py             # vytvoří index.html
```

Lokálně: `py -m http.server 8765` a otevřít http://localhost:8765.
