from bs4 import BeautifulSoup
import requests
import sqlite3 as sq



def get_films():
    url = "https://megogo.net/ru/films"
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, "lxml")
    div_elements = soup.select("div.card.videoItem.orientation-portrait.size-normal")
    
    
    with sq.connect("db.sqlite3") as con:
        cur = con.cursor()
        
        for i in div_elements:
            title = i.select_one("h3.video-title.card-content-title").get_text(strip=True)
            img = i.select_one("img[data-original]")["data-original"]
            info_element = i.select_one("div.video-info.card-content-info")
            genre = info_element.select_one("span.video-country").get_text(strip=True)
            year = info_element.select_one("span.video-year").get_text(strip=True)
            href = i.select_one('a.overlay')['href']
            cur.execute("INSERT OR IGNORE INTO sponsor_film (title, img, year, genre, href) VALUES (?, ?, ?, ?, ?)",
                        (title, img, year, genre, href))
    
        con.commit()
        
        # cur.execute("DELETE FROM sponsor_film")