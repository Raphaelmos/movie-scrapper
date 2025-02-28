import requests
from bs4 import BeautifulSoup
"""
url = "https://www.allocine.fr/film/fichefilm-286292/critiques/presse/"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

# Récupérer le titre du film
titre = soup.find('h1', class_="titlebar titlebar-page").text.strip()

# Récupérer les blocs critiques
blocs_critiques = soup.find_all('div', class_="reviews-press-comment")

for bloc in blocs_critiques:

    # Récupérer la note    
    note = bloc.find('div', class_="stareval-note").text

    # Récupérer le nom du critique
    nom = bloc.find('div', class_="meta-title").text

    # Récupérer la critique
    critique = bloc.find('div', class_="content-txt review-card-content").text

    print(f"Titre: {titre}")
    print(f"Note: {note}") 
    print(f"Critique: {nom}")
    print(f"Avis: {critique}")
    print()

import requests
from bs4 import BeautifulSoup
import csv

def read_urls(filename):
    urls = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                urls.append(line)
    return urls

def scrape_reviews(urls, element_classes):
    previous_pseudos = set()

    with open('films_avis_populaire.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Titre', 'URL', 'Note', 'Pseudo', 'Avis']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
        writer.writeheader()

        for i, url_main in enumerate(urls):
            print(f"Scraping URL {i+1}: {url_main}")
            page_number = 1
            while True:
                url = f"{url_main}?page={page_number}"
                print(f"Scraping page {page_number}: {url}")
                try:
                    response = requests.get(url)
                    response.raise_for_status()

                    soup = BeautifulSoup(response.text, 'html.parser')
                    titles = soup.find_all(class_=element_classes[0])
                    if not titles:
                        print("No titles found. Exiting...")
                        break

                    notes = soup.find_all(class_=element_classes[1])
                    pseudos = soup.find_all(class_=element_classes[2])
                    reviews = soup.find_all(class_=element_classes[3])

                    current_pseudos = set()
                    for title, note, pseudo, review in zip(titles, notes, pseudos, reviews):
                        title_text = title.get_text().strip()
                        note_text = note.get_text().strip()
                        pseudo_text = pseudo.get_text().split('\n')[0].strip()
                        review_text = review.get_text().strip()

                        if pseudo_text in previous_pseudos:
                            print("Skipping duplicate pseudonym:", pseudo_text)
                            continue

                        writer.writerow({'Titre': title_text, 'Note': note_text, 'URL': url, 'Pseudo': pseudo_text, 'Avis': review_text})
                        current_pseudos.add(pseudo_text)

                    previous_pseudos = current_pseudos

                    page_number += 1
                except requests.RequestException as e:
                    print(f"Error fetching URL: {url}")
                    print(e)
                    break
                except Exception as e:
                    print(f"Error processing page: {url}")
                    print(e)
                    break

def main():
    urls = read_urls("url.txt")
    element_classes = [
        "xXx titlebar-link",
        "stareval-note",
        "meta-title",
        "content-txt review-card-content",
    ]
    scrape_reviews(urls, element_classes)

if __name__ == "__main__":
    main()
"""
import requests
from bs4 import BeautifulSoup
import csv

def read_urls(filename):
    urls = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                urls.append(line)
    return urls

def scrape_reviews(urls):
    with open('filmstitré', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Titre', 'URL', 'Note', 'Pseudo', 'Avis']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
        writer.writeheader()

        for i, url in enumerate(urls, 1):
            print(f"Scraping URL {i}: {url}")
            try:
                response = requests.get(url)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')
                titles = soup.find_all(class_='titlebar-title titlebar-title-xl')
                if not titles:
                    print("No titles found on the page:", url)
                    continue

                for title in titles:
                    title_text = title.get_text().strip()
                    note_elements = title.find_next(class_='stareval-note')
                    pseudo_elements = title.find_next(class_='meta-title')
                    avis_elements = title.find_next(class_='content-txt review-card-content')

                    note = note_elements.get_text().strip() if note_elements else ''
                    pseudo = pseudo_elements.get_text().strip() if pseudo_elements else ''
                    avis = avis_elements.get_text().strip() if avis_elements else ''

                    print("Title:", title_text)
                    print("Note:", note)
                    print("Pseudo:", pseudo)
                    print("Avis:", avis)

                    writer.writerow({
                        'Titre': title_text,
                        'URL': url,
                        'Note': note,
                        'Pseudo': pseudo,
                        'Avis': avis
                    })
            except requests.RequestException as e:
                print(f"Error fetching URL: {url}")
                print(e)
                continue
            except Exception as e:
                print(f"Error processing page: {url}")
                print(e)
                continue

def main():
    urls = read_urls("url.txt")
    scrape_reviews(urls)

if __name__ == "__main__":
    main()
