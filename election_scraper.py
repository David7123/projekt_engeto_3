"""
election_scraper.py: třetí projekt do Engeto Online Python Akademie

author: David Štefaník
email: stefanik.david@seznam.cz
"""

import sys
import requests
from bs4 import BeautifulSoup
import csv

def check_args():
    """
    Kontroluje, že první argument je platná URL na detail územního celku
    a druhý argument je název CSV souboru.
    """
    if len(sys.argv) != 3:
        print("Chyba: Zadejte 2 argumenty – odkaz na územní celek a jméno výstupního souboru.")
        print("Příklad: python election_scraper.py \"<URL_na_okres_nebo_kraj>\" \"vysledky_okres.csv\"")
        sys.exit(1)
    url = sys.argv[1]
    output_file = sys.argv[2]
    # Ověření, že první argument je platná URL na detail územního celku (okres/kraj)
    if not (url.startswith("https://www.volby.cz/pls/ps2017nss/ps32") or url.startswith("https://volby.cz/pls/ps2017nss/ps32")):
        print("Chyba: První argument musí být platný odkaz na detail územního celku (začínající https://www.volby.cz/pls/ps2017nss/ps32)")
        sys.exit(1)
    # Ověření, že druhý argument má příponu .csv
    if not output_file.endswith(".csv"):
        print("Chyba: Druhý argument musí být název souboru s příponou .csv")
        sys.exit(1)
    return url, output_file

def get_obec_links(url):
    """
    Stáhne stránku územního celku a najde všechny obce v tabulce.
    Vrací seznam trojic (kód obce, název obce, odkaz na detail obce).
    """
    r = requests.get(url)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", {"class": "table"})
    links = []
    # Prochází všechny řádky tabulky obcí kromě hlavičky
    for row in table.find_all("tr")[2:]:
        cells = row.find_all("td")
        if len(cells) < 2:
            continue
        code = cells[0].text.strip()
        name = cells[1].text.strip()
        link = cells[0].find("a")
        # Pokud je v buňce odkaz, vytvoří absolutní URL a uloží
        if link and "href" in link.attrs:
            href = "https://www.volby.cz/pls/ps2017nss/" + link["href"]
            links.append((code, name, href))
    return links

def get_party_names(url):
    """
    Stáhne detail první obce a najde názvy všech stran (pro sestavení hlavičky CSV).
    """
    r = requests.get(url)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    # Tabulka s výsledky pro strany je druhá v pořadí
    party_table = soup.find_all("table")[1]
    party_names = []
    # Prochází všechny řádky tabulky stran kromě hlavičky
    for row in party_table.find_all("tr")[2:]:
        cells = row.find_all("td")
        if len(cells) > 1:
            party_names.append(cells[1].text.strip())
    return party_names

def get_obec_data(code, name, url, num_parties):
    """
    Načte detailní výsledky pro obec:
    - počet voličů v seznamu
    - vydané obálky
    - platné hlasy
    - počty hlasů pro jednotlivé strany
    Vrací seznam hodnot pro jeden řádek CSV.
    """
    r = requests.get(url)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    tds = soup.find_all("td")
    # Získání základních údajů o obci
    registered = tds[3].text.replace('\xa0','').strip()
    envelopes = tds[4].text.replace('\xa0','').strip()
    valid = tds[7].text.replace('\xa0','').strip()
    parties = []
    party_table = soup.find_all("table")[1]
    # Získání hlasů pro jednotlivé strany
    for row in party_table.find_all("tr")[2:]:
        cells = row.find_all("td")
        if len(cells) > 2:
            parties.append(cells[2].text.replace('\xa0','').strip())
    # Pokud je méně hlasů než stran, doplní nuly
    while len(parties) < num_parties:
        parties.append('0')
    # Pokud by bylo hlasů více (chyba v datech), ořízne na správný počet
    parties = parties[:num_parties]
    return [code, name, registered, envelopes, valid] + parties

def main():
    """
    Hlavní funkce programu.
    Zpracuje argumenty, stáhne a uloží výsledky voleb do CSV.
    """
    url, output_file = check_args()
    print(f"Stahuji data z: {url}")
    obce = get_obec_links(url)
    if not obce:
        print("Nebyla nalezena žádná obec.")
        sys.exit(1)
    # Získání názvů stran pro hlavičku CSV
    party_names = get_party_names(obce[0][2])
    header = ["code", "location", "registered", "envelopes", "valid"] + party_names
    # Export do CSV s BOM pro správnou diakritiku v Excelu
    with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(header)
        # Zpracování všech obcí a zápis do CSV
        for code, name, link in obce:
            row = get_obec_data(code, name, link, len(party_names))
            writer.writerow(row)
    print(f"Ukládám do souboru: {output_file}\nHotovo.")

if __name__ == "__main__":
    main()