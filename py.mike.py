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

# Google Trends Nischenthemen holen (international)
def lade_trend_themen():
    fallback_themen = ["Fitness", "AI", "Minimalism", "Smartphone", "Camping"]
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        trending_searches_df = pytrends.trending_searches(pn='united_states')
        trends = trending_searches_df[0].tolist()[:10]  # Top 10
        print("✅ Google Trends (international) successfully loaded.")
        return trends
    except Exception as e:
        print("❌ Could not load trends:", e)
        print("⚠️ Using fallback topics instead.")
        return fallback_themen

# Beispielhafte Infotexte als Platzhalter
def generiere_infotext(nische):
    return f"{nische} is currently a trending topic. Here you'll find useful products, tips and recommendations to get familiar with it."

# SEO Meta-Texte
def meta_description():
    return "Daily new niche pages with honest product recommendations and affiliate links. Practical, independent and free."

def meta_keywords():
    return "Affiliate, Product recommendation, Amazon, eBay, Trends, Tips, Reviews"

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

# Kategorie aus Thema ableiten
def ermittle_kategorie(nische):
    kategorien = {
        "Camping": "Camping",
        "Garden": "Garden",
        "Coffee": "Kitchen",
        "Smart": "Tech",
        "Fitness": "Health",
        "Minimalism": "Lifestyle",
    }
    for schluessel, kategorie in kategorien.items():
        if schluessel.lower() in nische.lower():
            return kategorie
    return "Other"

# HTML-Seite generieren
def generiere_html(nische):
    beschreibung = generiere_infotext(nische)
    bild = f"https://source.unsplash.com/800x400/?{nische.replace(' ', '+')}"
    schemaorg = generiere_schemaorg(nische, beschreibung, bild)
    plausible = '<script async defer data-domain="mike181812.github.io/meine-nischenseite" src="https://plausible.io/js/plausible.js"></script>'

    html = f"""
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
        <meta name=\"description\" content=\"{meta_description()}\">
        <meta name=\"keywords\" content=\"{meta_keywords()}\">
        <title>{nische} Recommendations</title>
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
        <h1>{nische} – Our Recommendations</h1>
        <img src=\"{bild}\" alt=\"{nische}\">
        <p>{beschreibung}</p>
        <h2>Benefits of {nische}</h2>
        <p>Discover why {nische} can be useful for you. Many people already use it in their daily lives or hobbies.</p>
        <h2>Our Product Recommendations</h2>
        <p>Here are some recommended products with affiliate links:</p>
        <ul>
    """

    affiliate_links = {
        "Amazon": "https://www.amazon.de/?tag=mike123-21",
        "eBay": "https://www.ebay.de/?_trkparms=mikeaffiliateid"
    }

    for name, link in affiliate_links.items():
        html += f'<li><a href="{link}" target="_blank" rel="nofollow sponsored">{name} Link</a></li>\n'

    html += f"""
        </ul>
        <p><em>By clicking the links you support this site. Thank you!</em></p>
        {plausible}
    </body>
    </html>
    """
    return html

# Index-Seite aktualisieren (englisch)
def aktualisiere_index():
    dateien = [f for f in os.listdir(github_ordner) if f.endswith(".html") and f != "index.html"]
    links = "\n".join([f'<li><a href="{datei}">{datei.replace(".html", "").replace("_", " ")}</a></li>' for datei in sorted(dateien)])
    html = f"""
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <title>Daily Niche Recommendations</title>
        <meta name=\"description\" content=\"Overview of all niche pages generated automatically.\">
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; max-width: 700px; margin: auto; }}
            h1 {{ color: #003366; }}
            ul {{ line-height: 1.8; }}
        </style>
    </head>
    <body>
        <h1>Daily Niche Pages</h1>
        <p>Here you can find all the niche pages created using Google Trends and affiliate tools:</p>
        <ul>
            {links}
        </ul>
        <p><em>New pages are added every day. Stay tuned!</em></p>
    </body>
    </html>
    """
    with open(os.path.join(github_ordner, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

# Sitemap automatisch generieren
def generiere_sitemap():
    dateien = [f for f in os.listdir(github_ordner) if f.endswith(".html")]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for datei in sorted(dateien):
        url = f"https://mike181812.github.io/meine-nischenseite/{datei}"
        sitemap += f"  <url>\n    <loc>{url}</loc>\n  </url>\n"
    sitemap += '</urlset>'
    with open(os.path.join(github_ordner, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
    print("✅ Sitemap erstellt: sitemap.xml")

# Automatisch zu GitHub hochladen
def git_push():
    try:
        subprocess.run(["git", "-C", github_ordner, "add", "."], check=True)
        subprocess.run(["git", "-C", github_ordner, "commit", "-m", "Auto update"], check=True)
        subprocess.run(["git", "-C", github_ordner, "push"], check=True)
        print("✅ Auto-push to GitHub successful.")
    except subprocess.CalledProcessError as e:
        print("❌ GitHub upload failed:", e)

# Hauptablauf
if __name__ == "__main__":
    themen = lade_trend_themen()
    for thema in themen:
        dateiname = f"{thema.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        inhalt = generiere_html(thema)
        with open(os.path.join(github_ordner, dateiname), "w", encoding="utf-8") as f:
            f.write(inhalt)

    aktualisiere_index()
    generiere_sitemap()
    git_push()
