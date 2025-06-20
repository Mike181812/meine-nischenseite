# Automatisiertes Python-Skript zum Erstellen von HTML-Webseiten mit Affiliate-Inhalten + SEO-Sitemap + strukturierte Daten + Google Trends + Auto-Git
# Diese HTML-Dateien kannst du auf GitHub Pages hochladen, um eine Nischenseite zu betreiben

import os
import random
from datetime import datetime
from pytrends.request import TrendReq

# Pfad zu deinem GitHub-Ordner (bitte ggf. anpassen)
github_ordner = r"C:\Users\Mike\Desktop\meine-nischenseite"

# Google Trends Nischenthemen holen
def lade_trend_themen():
    pytrends = TrendReq(hl='de-DE', tz=360)
    try:
        trending_searches_df = pytrends.trending_searches(pn='germany')
        trends = trending_searches_df[0].tolist()[:10]  # Top 10
        return trends
    except Exception as e:
        print("❌ Konnte keine Trends laden:", e)
        return ["Garten", "Fitness", "Smart Home", "Camping", "Kaffeeautomat"]

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
    eintrag = f'<li><a href="{dateiname}">{dateiname}</a></li>\n'

    if not os.path.exists(index_datei):
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
    <ul>
""")
            f.write(eintrag)
            f.write("""
    </ul>
</body>
</html>
""")
    else:
        with open(index_datei, "r", encoding="utf-8") as f:
            lines = f.readlines()

        with open(index_datei, "w", encoding="utf-8") as f:
            for line in lines:
                if line.strip() == "</ul>":
                    f.write(eintrag)
                f.write(line)

# Sitemap aktualisieren
def aktualisiere_sitemap(dateiname):
    sitemap_datei = os.path.join(github_ordner, "sitemap.xml")
    url = f"https://mike181812.github.io/meine-nischenseite/{dateiname}"
    eintrag = f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{datetime.now().date()}</lastmod>\n  </url>\n"

    if not os.path.exists(sitemap_datei):
        with open(sitemap_datei, "w", encoding="utf-8") as f:
            f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            f.write("<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n")
            f.write(eintrag)
            f.write("</urlset>")
    else:
        with open(sitemap_datei, "r", encoding="utf-8") as f:
            lines = f.readlines()

        with open(sitemap_datei, "w", encoding="utf-8") as f:
            for line in lines:
                if line.strip() == "</urlset>":
                    f.write(eintrag)
                f.write(line)

# Robots.txt erzeugen
def erstelle_robots_txt():
    robots_path = os.path.join(github_ordner, "robots.txt")
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write("User-agent: *\n")
        f.write("Allow: /\n")
        f.write("Sitemap: https://mike181812.github.io/meine-nischenseite/sitemap.xml\n")

# Automatisch git commit & push ausführen
def git_push(commit_message):
    os.chdir(github_ordner)
    os.system("git add .")
    os.system(f'git commit -m "{commit_message}"')
    os.system("git push")

# Hauptfunktion
def erstelle_webseite():
    trend_themen = lade_trend_themen()
    nische = random.choice(trend_themen)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dateiname = f"{nische.replace(' ', '_')}_{timestamp}.html"
    html_inhalt = generiere_html(nische)
    speichere_html(dateiname, html_inhalt)
    aktualisiere_index(dateiname)
    aktualisiere_sitemap(dateiname)
    erstelle_robots_txt()
    print(f"HTML-Seite '{dateiname}' erstellt mit Google-Trend-Thema.")
    git_push(f"Neue Seite: {dateiname}")

if __name__ == "__main__":
    erstelle_webseite()
