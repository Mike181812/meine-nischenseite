# Automatisiertes Python-Skript zum Erstellen von HTML-Webseiten mit Affiliate-Inhalten + SEO-Sitemap + strukturierte Daten + Google Trends + Auto-Git
# Diese HTML-Dateien kannst du auf GitHub Pages hochladen, um eine Nischenseite zu betreiben

import os
import random
import subprocess
from datetime import datetime
from pytrends.request import TrendReq
from collections import defaultdict

# Pfad zu deinem GitHub-Ordner (bitte ggf. anpassen)
github_ordner = r"C:\Users\Mike\Desktop\meine-nischenseite"

# Google Trends Nischenthemen holen
def lade_trend_themen():
    fallback_themen = ["Garten", "Fitness", "Smart Home", "Camping", "Kaffeeautomat"]
    try:
        pytrends = TrendReq(hl='de-DE', tz=360)
        trending_searches_df = pytrends.trending_searches(pn='germany')
        trends = trending_searches_df[0].tolist()[:10]  # Top 10
        print("✅ Google Trends erfolgreich geladen.")
        return trends
    except Exception as e:
        print("❌ Konnte keine Trends laden:", e)
        print("⚠️ Verwende statische Themen als Ersatz.")
        return fallback_themen

# Beispielhafte Infotexte als Platzhalter
def generiere_infotext(nische):
    return f"{nische} ist aktuell ein stark gefragtes Thema. Hier findest du hilfreiche Produkte, Tipps und Empfehlungen, um dich mit diesem Bereich vertraut zu machen."

# SEO Meta-Texte
def meta_description():
    return "Täglich neue Nischenseiten mit ehrlichen Produktempfehlungen und Partnerlinks. Praktisch, unabhängig und kostenlos."

def meta_keywords():
    return "Affiliate, Produktempfehlung, Amazon, eBay, Trends, Tipps, Empfehlungen"

# Strukturierte Daten (schema.org)
def generiere_schemaorg(nische, beschreibung, bild):
    return f'''
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {{
          "@type": "Question",
          "name": "Was ist {nische}?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "{beschreibung}"
          }}
        }}
      ]
    }}
    </script>
    '''

# Kategorie aus Thema ableiten
def ermittle_kategorie(nische):
    kategorien = {
        "Camping": "Camping",
        "Garten": "Garten",
        "Kaffee": "Küche",
        "Smart": "Technik",
        "Fitness": "Gesundheit",
        "Minimalismus": "Lifestyle",
    }
    for schluessel, kategorie in kategorien.items():
        if schluessel.lower() in nische.lower():
            return kategorie
    return "Sonstiges"

# HTML-Seite generieren
def generiere_html(nische):
    beschreibung = generiere_infotext(nische)
    bild = f"https://source.unsplash.com/800x400/?{nische.replace(' ', '+')}"
    schemaorg = generiere_schemaorg(nische, beschreibung, bild)
    html = f"""
    <!DOCTYPE html>
    <html lang=\"de\">
    <head>
        <meta charset=\"UTF-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
        <meta name=\"description\" content=\"{meta_description()}\">
        <meta name=\"keywords\" content=\"{meta_keywords()}\">
        <title>{nische} Empfehlungen</title>
        {schemaorg}
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 30px auto; background: #fff; color: #222; }}
            h1 {{ color: #006699; }}
            h2 {{ color: #003366; margin-top: 30px; }}
            ul {{ padding-left: 20px; }}
            a {{ color: #0066cc; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
            em {{ font-size: 0.9em; color: #555; }}
            img {{ width: 100%; margin: 20px 0; border-radius: 8px; }}
        </style>
    </head>
    <body>
        <h1>{nische} – Unsere Empfehlungen</h1>
        <img src=\"{bild}\" alt=\"{nische}\">
        <p>{beschreibung}</p>
        <h2>Vorteile von {nische}</h2>
        <p>Erfahre, warum {nische} für dich sinnvoll sein kann. Viele Menschen nutzen es bereits für ihren Alltag oder Hobby.</p>
        <h2>Unsere Produktempfehlungen</h2>
        <p>Hier findest du empfohlene Produkte mit Partnerlinks:</p>
        <ul>
    """

    affiliate_links = {
        "Amazon": "https://www.amazon.de/?tag=mike123-21",
        "eBay": "https://www.ebay.de/?_trkparms=mikeaffiliateid"
    }

    for name, link in affiliate_links.items():
        html += f'<li><a href="{link}" target="_blank" rel="nofollow sponsored">{name} Link</a></li>\n'

    html += """
        </ul>
        <p><em>Mit Klick auf die Links unterstützt du diese Seite. Vielen Dank!</em></p>
    </body>
    </html>
    """
    return html

# HTML-Datei speichern
def speichere_html(dateiname, html_inhalt):
    pfad = os.path.join(github_ordner, dateiname)
    with open(pfad, "w", encoding="utf-8") as file:
        file.write(html_inhalt)

# Index-Datei aktualisieren oder erstellen
def aktualisiere_index(dateiname):
    index_datei = os.path.join(github_ordner, "index.html")
    kategorie = ermittle_kategorie(dateiname)
    kategorien_eintraege = defaultdict(list)

    if os.path.exists(index_datei):
        with open(index_datei, "r", encoding="utf-8") as f:
            zeilen = f.readlines()
            aktuelle_kategorie = None
            for zeile in zeilen:
                if zeile.startswith("<h2>"):
                    aktuelle_kategorie = zeile.strip().replace("<h2>", "").replace("</h2>", "")
                elif zeile.startswith("<li><a ") and aktuelle_kategorie:
                    kategorien_eintraege[aktuelle_kategorie].append(zeile)

    kategorien_eintraege[kategorie].append(f'<li><a href="{dateiname}">{dateiname}</a></li>\n')

    with open(index_datei, "w", encoding="utf-8") as f:
        f.write("""
<!DOCTYPE html>
<html lang=\"de\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Startseite – Nischenseite</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 30px auto; background: #fff; color: #222; }}
        h1 {{ color: #006699; }}
        ul {{ padding-left: 20px; }}
        a {{ color: #0066cc; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>Willkommen auf meiner Nischenseite</h1>
""")
        for kat, links in sorted(kategorien_eintraege.items()):
            f.write(f'<h2>{kat}</h2>\n<ul>\n')
            for link in links:
                f.write(link)
            f.write('</ul>\n')
        f.write("""
</body>
</html>
""")

# Automatisches Git Commit + Push
def git_push():
    try:
        subprocess.run(["git", "add", "."], cwd=github_ordner, check=True)
        subprocess.run(["git", "commit", "-m", "Auto-Update Nischenseite"], cwd=github_ordner, check=True)
        subprocess.run(["git", "push"], cwd=github_ordner, check=True)
        print("🚀 Änderungen wurden automatisch zu GitHub hochgeladen.")
    except Exception as e:
        print("❌ Git Push fehlgeschlagen:", e)

# Hauptfunktion
def erstelle_webseite():
    trends = lade_trend_themen()
    jetzt = datetime.now().strftime("%Y%m%d_%H%M%S")
    thema = random.choice(trends)
    dateiname = f"{thema.replace(' ', '_')}_{jetzt}.html"
    html = generiere_html(thema)
    speichere_html(dateiname, html)
    aktualisiere_index(dateiname)
    print(f"✅ HTML-Seite '{dateiname}' erstellt mit Google-Trend-Thema.")
    git_push()

# Starte das Skript
if __name__ == "__main__":
    erstelle_webseite()
    input("Drücke eine beliebige Taste . . .")
