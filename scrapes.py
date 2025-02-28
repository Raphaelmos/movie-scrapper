import requests
from bs4 import BeautifulSoup
import csv

debug = False

def get_url(filename):
    urls = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                urls.append(line)
    return urls

def get_element(game_url, element):
    response = requests.get(game_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.find_all(class_=element)

        results = [elem.get_text().strip() for elem in elements]
        if debug: print(results)
        return results
    else:
        if debug: print("Error fetching page:", response.status_code)
        return []

def get_avis(urls, elements):
    previous_pseudos = set()  # Set of pseudonyms from the previous page

    with open('films_avis_populaire.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Titre', 'URL', 'Note', 'Pseudo', 'Avis']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
        writer.writeheader()

        for i, url_main in enumerate(urls, 1):
            print(f"Scraping URL {i}: {url_main}")
            r = 1
            while True:
                url = f"{url_main}?page={r}"
                print(f"Scraping page {r}: {url}")
                response = requests.get(url)
                if response.status_code == 200:
                    resultats = [get_element(url, elem) for elem in elements]
                    titre, note, pseudo, avis = resultats
                    if len(titre) == 0:
                        print("No titles found. Exiting...")
                        break

                    note = note[2:]
                    pseudo = [p.split('\n')[0] for p in pseudo]
                    pseudo = pseudo[2:]
                    avis = avis[2:]

                    current_pseudos = set(pseudo)
                    if current_pseudos == previous_pseudos:
                        print("The pseudonyms on the current page are the same as those on the previous page. Skipping...")
                        break

                    previous_pseudos = current_pseudos

                    max_length = max(len(titre), len(note), len(pseudo), len(avis))
                    for j in range(max_length):
                        titre_value = titre[j] if j < len(titre) else ""
                        note_value = note[j] if j < len(note) else ""
                        pseudo_value = pseudo[j] if j < len(pseudo) else ""
                        avis_value = avis[j] if j < len(avis) else ""

                        writer.writerow({'Titre': titre_value, 'URL': url, 'Note': note_value, 'Pseudo': pseudo_value, 'Avis': avis_value})
                else:
                    if debug: print("Error fetching page:", response.status_code)
                    break
                r += 1

def main():
    urls = get_url("url.txt")
    elements = [
        "xXx titlebar-link",
        "stareval-note",
        "meta-title",
        "content-txt review-card-content",
    ]
    get_avis(urls, elements)

if __name__ == "__main__":
    main()
