from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.common.exceptions import StaleElementReferenceException
import smtplib
import os
from dotenv import load_dotenv
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()



load_dotenv()




def close_ads():
    time.sleep(2)
    try:
        close_button = driver.find_element(By.CSS_SELECTOR, "div.adm-scroll-header div.h-right a.h-href img")
        close_button.click()
    except NoSuchElementException:
        pass


os.environ["PATH"] += os.pathsep + os.getenv("GOOGLE_CHROME_BIN", "/usr/bin/chromium")
os.environ["PATH"] += os.pathsep + os.getenv("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)

chrome_options.add_argument("--headless")  # Headless modda çalıştır
chrome_options.add_argument("--no-sandbox")  # Sandbox modunu kapat
chrome_options.add_argument("--disable-dev-shm-usage")  # Düşük bellek sorunlarını önle
chrome_options.add_argument("--remote-debugging-port=9222")  # Debugging için port ayarla

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://kykyemek.com/#google_vignette")


while True:
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "slider"))
        )
        button.click()
        print("Slider başarıyla tıklandı!")
        break
    except (TimeoutException, NoSuchElementException):
        close_ads()
        time.sleep(2)

time.sleep(3)

while True :
    try :
        dropdown = driver.find_element(By.ID, "navbarDropdown")
        dropdown.click()
        time.sleep(1)
        izmir_option = driver.find_element(By.XPATH, "//select[@id='navbarDropdown']/option[text()='İzmir']")
        izmir_option.click()
        break
    except (TimeoutException, NoSuchElementException) :
        close_ads()
        time.sleep(2)

time.sleep(5)

# İzmir seçildikten sonra sayfanın gerçekten değişmesini bekle
WebDriverWait(driver, 10).until(
    EC.text_to_be_present_in_element(
        (By.TAG_NAME, "body"), "İzmir Kyk Akşam Yemeği Listesi"
    )
)

cards = driver.find_elements(By.CSS_SELECTOR, "div.col[style*='min-height:385px']")

now = datetime.now()

day = int(now.strftime("%d"))

menu = ""
card_header = ""

safety_date = 1

is_found = False

for i, card in enumerate(cards) :
    while True :
        try :
            cards = driver.find_elements(By.CSS_SELECTOR, "div.col[style*='min-height:385px']")
            card = cards[i]

            driver.execute_script("arguments[0].scrollIntoView();", card)
            time.sleep(3)

            header_element = card.find_elements(By.CSS_SELECTOR, ".card-header")
            if not header_element:
                print("Bu kartta `.card-header` bulunamadı, atlanıyor...")
                break

            if header_element[0].value_of_css_property("display") == "none":
                print("Kart header gizli, açılıyor...")
                driver.execute_script("arguments[0].style.display = 'block';", header_element[0])
                time.sleep(1)


            card_header = WebDriverWait(card, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".card-header p"))
            ).text
            print(f"Kart başlığı bulundu: {card_header}")
            break

        except StaleElementReferenceException:
            print("Stale Element hatası alındı! Kartları tekrar buluyoruz...")
            time.sleep(1)
            cards = driver.find_elements(By.CSS_SELECTOR, "div.col[style*='min-height:385px']")

            try:
                card = cards[cards.index(card)]
            except ValueError:
                print("Kart artık DOM'da bulunmuyor, sayfa güncellenmiş olabilir!")
                break

            continue

        except TimeoutException:
            print("Kart başlığı bulunamadı, reklam kontrol ediliyor...")
            close_ads()
            print("Reklam kapatıldı, kart tekrar kontrol ediliyor...")
            time.sleep(3)
            break


    try :
        date = int(card_header.split()[0])
    except (ValueError,IndexError) :
        date=safety_date


    if date == day :
        while True :
            menu = [p.text for p in card.find_elements(By.CSS_SELECTOR, ".card-body p")]
            print(f"Menü kontrol ediliyor: {menu}")
            if menu :
                is_found = True
                print(menu)
                break

            else :
                print("Menü boş, reklam kapatılıyor...")
                close_ads()


    safety_date += 1

    if is_found :
        break



my_email = os.getenv("EMAIL")

password = os.getenv("PASSWORD")

msg = f"Subject: Kyk Dinner\n\nToday's Menu:\n\n" + "\n".join(f"- {item}" for item in menu) + "\n\nFuck you Boran"

mails = ["dumansali74@gmail.com","11brn0604@gmail.com","baranucar002@gmail.com","egeycl@gmail.com","yusufealb@gmail.com"]

for mail in mails :
    with  smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()

        connection.login(user=my_email, password=password)

        connection.sendmail(from_addr=my_email,
                            to_addrs=mail,
                            msg = msg.encode("utf-8") )

