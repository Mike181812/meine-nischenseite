# Automatisiertes Python-Skript zum Erstellen von HTML-Webseiten mit Affiliate-Inhalten + SEO-Sitemap + strukturierte Daten + Google Trends + Auto-Git + Backlinks

import os
import random
import subprocess
import requests
from datetime import datetime
from pytrends.request import TrendReq

# Pfad zu deinem GitHub-Ordner (bitte ggf. anpassen)
github_ordner = r"C:\Users\Mike\Desktop\meine-nischenseite"

# Google Trends Nischenthemen holen (international)
def lade_trend_themen():
    fallback_themen = ["Fitness", "AI", "Minimalism", "Smartphone", "Camping"]
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        trending_searches_df = pytrends.trending_searches(pn='united_states')
        trends = trending_searches_df[0].tolist()[:10]
        print("✅ Google Trends geladen.")
        return trends
    except Exception as e:
        print("❌ Fehler bei Trends:", e)
        return fallback_themen

# Infotexte erzeugen
def generiere_infotext(nische):
    return f"{nische} is trending. Here you'll find helpful products and tips."

def meta_description():
    return "Daily new niche pages with product recommendations and affiliate links."

def meta_keywords():
    return "Affiliate, Amazon, eBay, Trends, Recommendations, Reviews"

def generiere_schemaorg(nische, beschreibung):
    return f'''
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {{
          "@type": "Question",
          "name": "What is {nische}?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "{beschreibung}"
          }}
        }}
      ]
    }}
    </script>
    '''

def generiere_html(nische):
    beschreibung = generiere_infotext(nische)
    bild = f"https://source.unsplash.com/800x400/?{nische.replace(' ', '+')}"
    schemaorg = generiere_schemaorg(nische, beschreibung)
    plausible = '<script async defer data-domain="mike181812.github.io/meine-nischenseite" src="https://plausible.io/js/plausible.js"></script>'

    affiliate_links = [
        ("Amazon", "https://www.amazon.de/?tag=mike123-21"),
        ("eBay", "https://www.ebay.de/?_trkparms=mikeaffiliateid"),
        ("Digistore", "https://www.digistore24.com/redir/123456/mikeaffiliate/")
    ]
    random.shuffle(affiliate_links)

    html = f"""
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
        <meta name=\"description\" content=\"{meta_description()}\">
        <meta name=\"keywords\" content=\"{meta_keywords()}\">
        <title>{nische} Recommendations</title>
        {plausible}
        {schemaorg}
        <style>
            body {{ font-family: Arial; max-width: 800px; margin: auto; background: #fff; color: #222; }}
            h1 {{ color: #006699; }}
            img {{ width: 100%; margin: 20px 0; border-radius: 8px; }}
        </style>
    </head>
    <body>
        <h1>{nische} – Our Recommendations</h1>
        <img src=\"{bild}\" alt=\"{nische}\">
        <p>{beschreibung}</p>
        <h2>Product Links</h2>
        <ul>
    """
    for name, url in affiliate_links:
        html += f'<li><a href="{url}" target="_blank" rel="nofollow sponsored">{name}</a></li>'
    html += """
        </ul>
        <p><em>Support us by clicking. Thanks!</em></p>
    </body>
    </html>
    """
    return html

def aktualisiere_index():
    dateien = [f for f in os.listdir(github_ordner) if f.endswith(".html") and f != "index.html"]
    links = "\n".join([f'<li><a href="{d}">{d.replace(".html", "").replace("_", " ")}</a></li>' for d in sorted(dateien)])
    html = f"""
    <!DOCTYPE html>
    <html><head><title>All Pages</title></head>
    <body><h1>Niche Pages</h1><ul>{links}</ul></body></html>
    """
    with open(os.path.join(github_ordner, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

def generiere_sitemap():
    dateien = [f for f in os.listdir(github_ordner) if f.endswith(".html")]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for d in dateien:
        url = f"https://mike181812.github.io/meine-nischenseite/{d}"
        sitemap += f"  <url><loc>{url}</loc></url>\n"
    sitemap += '</urlset>'
    with open(os.path.join(github_ordner, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)

def git_push():
    try:
        subprocess.run(["git", "-C", github_ordner, "add", "."], check=True)
        subprocess.run(["git", "-C", github_ordner, "commit", "-m", "Auto update"], check=True)
        subprocess.run(["git", "-C", github_ordner, "push"], check=True)
        print("✅ GitHub Push erfolgreich.")
    except subprocess.CalledProcessError as e:
        print("❌ GitHub Fehler:", e)

# Neue Backlink-Funktion mit Service-Rotation
def erstelle_backlinks():
    dienste = [
        ("https://pastebin.com/api/api_post.php", "api_dev_key=SLDeut68nHHRo6oTqYz1Jlh0GdZB1wot"),
        ("https://rentry.co/api/new", None),
        ("https://justpaste.it/", None)
    ]
    dateien = [f for f in os.listdir(github_ordner) if f.endswith(".html") and f != "index.html"]
    for i, datei in enumerate(dateien):
        link = f"https://mike181812.github.io/meine-nischenseite/{datei}"
        beschreibung = f"Check this out: {datei.replace('_', ' ').replace('.html', '')}\n{link}"
        dienst = dienste[i % len(dienste)]
        try:
            if "pastebin" in dienst[0]:
                response = requests.post(dienst[0], data={
                    "api_dev_key": dienst[1].split("=")[1],
                    "api_option": "paste",
                    "api_paste_code": beschreibung,
                    "api_paste_private": "1"
                })
            else:
                response = requests.post(dienst[0], data={"text": beschreibung})

            if response.ok:
                print(f"🔗 Backlink erfolgreich auf {dienst[0]}")
            else:
                print(f"⚠️ Fehler bei Backlink: {response.status_code}, {response.text}")
        except Exception as e:
            print("❌ Fehler beim Backlink-Versuch:", e)

if __name__ == "__main__":
    themen = lade_trend_themen()
    for thema in themen[:10]:  # statt 5 jetzt 10
        dateiname = f"{thema.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        inhalt = generiere_html(thema)
        with open(os.path.join(github_ordner, dateiname), "w", encoding="utf-8") as f:
            f.write(inhalt)

    aktualisiere_index()
    generiere_sitemap()
    erstelle_backlinks()
    git_push()
