Election Scraper:
Tento projekt slouží ke stažení výsledků voleb do Poslanecké sněmovny 2017 pro všechny obce vybraného územního celku z webu volby.cz. Výsledky jsou ukládány do CSV souboru vhodného pro další zpracování.

Funkce:
 • Stahuje výsledky hlasování pro všechny obce v zadaném okrese nebo kraji.
 • Výstupní CSV obsahuje:
    • kód obce
    • název obce
    • počet voličů v seznamu
    • vydané obálky
    • platné hlasy
    • počet hlasů pro každou kandidující stranu

Instalace
 1.Vytvořte a aktivujte virtuální prostředí
   python -m venv venv
   • Aktivace ve Windows:
     venv\Scripts\activate
   • Aktivace v Linux\Mac:
     source venv/bin/activate

 2. Nainstalovat nutnou knihovnu:
    pip install -r requirements.txt

Tento soubor requirements.txt obsahuje například:
  • requests
  • beautifulsoup4

Použití
Skript se spouští ze složky, kde je uložen, a přijímá dva argumenty:

Odkaz na detail územního celku (okres/kraj) – zkopírujte ze sloupce „Výběr obce“ (symbol X) z webu volby.cz.
Název výstupního CSV souboru (např. vysledky_okres.csv).

Příklad spuštění:
 python election_scraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=9&xnumnuts=5302" "vysledky_pardubice.csv"

Ukázka výstupu (CSV):
code;location;registered;envelopes;valid;ANO 2011;ODS;ČSSD;KSČM;...
530201;Chrudim;18901;11747;11644;3792;1670;1043;530;...
530202;Heřmanův Městec;5075;3113;3095;1020;432;260;143;...
...

 • Každý řádek odpovídá jedné obci.
 • Sloupce s názvy stran se automaticky přizpůsobí danému územnímu celku.

Poznámky
 • Pokud zadáte špatný počet argumentů nebo chybný odkaz, skript vypíše chybovou hlášku a skončí.
 • CSV je generováno s oddělovačem ; a v kódování UTF-8 s BOM, takže je vhodné pro český Excel.
 • Název výstupního souboru musí končit .csv.

   
 




