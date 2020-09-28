import requests
from bs4 import BeautifulSoup
from selenium import webdriver

def download_picture(url, filename):
    with open("../Character_icon/ "+ filename + ".png", 'wb') as handle:
            response = requests.get(url, stream=True)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
                
if __name__ == "__main__":    
    url = 'https://pcredivewiki.tw/Character'
    driver = webdriver.PhantomJS()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    name = [div.text for div in soup.find_all(["small"])]
    url = [x['src'] for x in soup.find_all(["img"]) if x["alt"] == ""]
    for n, u in zip(name, url):
        download_picture("https://pcredivewiki.tw" + u, n)

