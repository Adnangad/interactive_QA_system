from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import urllib
from selenium.webdriver.chrome.options import Options

def scrape_aljazeera():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome()
    url = "https://www.aljazeera.com"
    wait = WebDriverWait(driver, 7)
    driver.get(url)
    article_links = []
    file_path = os.path.dirname(os.path.abspath(__file__)) + "/documents/aljazeera.txt"
    
    try:
        try:
            cookie_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Allow all')]"))
            )
            cookie_btn.click()
            print("Cookie banner closed")
        except:
            print("No cookie popup detected")
        sports_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//ul[@class='menu header-menu']//a[@href='/sports/']"))
        )
        sports_link.click()
        print("STarted.......")
        wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "ul.themed-featured-posts-list li.themed-featured-posts-list__item")
            )
        )
        driver.set_page_load_timeout(180)
        page = BeautifulSoup(driver.page_source, "html.parser")
        ul = page.find_all("li", class_="themed-featured-posts-list__item")

        for li in ul:
            link_tag = li.find("a", class_="article-card__link")
            if link_tag and link_tag.get("href"):
                full_url = urllib.parse.urljoin(url, link_tag["href"])
                article_links.append(full_url)

        print("LINKS:: ", article_links)
        with open(file_path, "a", encoding="utf-8") as f:
            for link in article_links:
                driver.get(link)
                wait.until(EC.presence_of_element_located((By.ID, "main-content-area")))
                body = BeautifulSoup(driver.page_source, "html.parser")
                content = body.find("main", id="main-content-area")
                title = content.find("header", class_="article-header")
                h1 = title.find("h1") if title else None
                if h1:
                    f.write(h1.get_text(strip=True) + "\n" + "\n")
                root = content.find("div", class_="wysiwyg--all-content")
                ps = root.find_all("p")
                for p in ps:
                    f.write(p.get_text(strip=True) + "\n")
                f.write("\n" * 3)
                print("WRITTEN")
                time.sleep(3)
        print("DONE")
    except Exception as e:
        print(e)
        print("ERROR IS:: ", e)