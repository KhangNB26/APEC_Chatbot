from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def crawl_text(driver, url, selectors):
    driver.get(url)
    time.sleep(3)
    results = []
    for sel in selectors:
        try:
            title = driver.find_element(*sel['title']).text
            content = driver.find_element(*sel['content']).text
            results.append({"section": title, "content": content})
        except Exception as e:
            print(f"Error: {e}")
    return results

def crawl_table(driver, url):
    driver.get(url)
    time.sleep(3)
    rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
    meetings = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) == 4:
            meetings.append({
                "No": cols[0].text.strip(),
                "Event Title": cols[1].text.strip(),
                "Date": cols[2].text.strip(),
                "Venue": cols[3].text.strip()
            })
    return meetings

def main():
    driver = setup_driver()
    data = []

    # Crawl APEC Overview
    overview_selectors = [
        {
            "title": (By.CSS_SELECTOR, "h3.pt0"),
            "content": (By.CSS_SELECTOR, ".about_apec_wrap")
        }
    ]
    data += crawl_text(driver, 'https://apec2025.kr/?menuno=89', overview_selectors)

    # Crawl APEC Member Economies
    driver.get('https://apec2025.kr/?menuno=89')
    time.sleep(3)
    try:
        title = driver.find_element(By.XPATH, "//h3[contains(text(), 'APEC Member Economies')]").text
        members = [li.text for li in driver.find_elements(By.CSS_SELECTOR, ".apec_member li")]
        data.append({"section": title, "content": members})
    except Exception as e:
        print(f"Error: {e}")

    # Crawl APEC in the World & How APEC operates
    more_sections = [
        {
            "title": (By.XPATH, "//h3[contains(text(), 'APEC in the World')]"),
            "content": (By.XPATH, "//h3[contains(text(), 'APEC in the World')]/following-sibling::p")
        },
        {
            "title": (By.XPATH, "//h3[contains(text(), 'How APEC operates')]"),
            "content": (By.CSS_SELECTOR, ".info_wrap p.mt30")
        }
    ]
    data += crawl_text(driver, 'https://apec2025.kr/?menuno=89', more_sections)

    # Crawl Meeting Schedules
    meetings = crawl_table(driver, 'https://apec2025.kr/?menuno=93')
    data.append({"section": "APEC 2025 Meeting Schedule", "content": meetings})

    # Crawl Side Events
    side_events = crawl_table(driver, 'https://apec2025.kr/?menuno=94')
    data.append({"section": "APEC 2025 Side Events", "content": side_events})

    # Crawl Visit Korea information
    visit_korea_selectors = [
        {
            "title": (By.CSS_SELECTOR, "li.on a"),
            "content": (By.CSS_SELECTOR, "div.text_box03.mt50 p")
        }
    ]
    data += crawl_text(driver, 'https://apec2025.kr/?menuno=19', visit_korea_selectors)

    # Practical Information
    driver.get('https://apec2025.kr/?menuno=22')
    time.sleep(3)
    practicals = [
        "Traveler’s Checks", "Credit Cards", "Money Exchange", "Currency Converter"
    ]
    for item in practicals:
        try:
            title = driver.find_element(By.XPATH, f"//h4[contains(text(), '{item}')]").text
            content = driver.find_element(By.XPATH, f"//h4[contains(text(), '{item}')]/following-sibling::p").text
            data.append({"section": title, "content": content})
        except Exception as e:
            print(f"Error: {e}")

    # Electricity and Voltage
    try:
        title = driver.find_element(By.XPATH, "//h3[contains(text(), 'Electricity and Voltage')]").text
        content = driver.find_element(By.XPATH, "//h3[contains(text(), 'Electricity and Voltage')]/following-sibling::p").text
        data.append({"section": title, "content": content})
    except Exception as e:
        print(f"Error: {e}")

    # Gyeongju Information
    driver.get('https://apec2025.kr/?menuno=102')
    time.sleep(3)
    try:
        title = driver.find_element(By.XPATH, "//h2[contains(text(), 'Gyeongju')]").text
        content = driver.find_element(By.CSS_SELECTOR, "div.text_box03.mt50 p").text
        data.append({"section": title, "content": content})
    except Exception as e:
        print(f"Error: {e}")

    # Gyeongju Transportation
    driver.get('https://apec2025.kr/?menuno=137')
    time.sleep(3)
    try:
        section = driver.find_element(By.CSS_SELECTOR, "h3.pt0").text.strip()
        intro = driver.find_element(By.CSS_SELECTOR, "h3.pt0 + p").text.strip()
        ways = [li.text.strip() for li in driver.find_elements(By.CSS_SELECTOR, "h3.pt0 + p + ol li")]
        ktx = " ".join([p.text.strip() for p in driver.find_elements(By.XPATH, "//h4[normalize-space()='1. By KTX']/following-sibling::p")[:3]])
        gimhae = " ".join([p.text.strip() for p in driver.find_elements(By.XPATH, "//h4[contains(text(),'Gimhae International Airport')]/following-sibling::p")[:3]])
        content = f"{intro}\n" + "\n".join(ways) + f"\n{ktx}\n{gimhae}"
        data.append({"section": section, "content": content})
    except Exception as e:
        print(f"Error: {e}")

    # Gyeongju Heritage
    driver.get('https://apec2025.kr/?menuno=108')
    time.sleep(3)
    try:
        title = driver.find_element(By.XPATH, "//h3[contains(text(), 'Seokguram Grotto and Bulguksa Temple')]").text
        content = driver.find_element(By.XPATH, "//h3[contains(text(), 'Seokguram Grotto and Bulguksa Temple')]/following-sibling::p").text
        data.append({"section": title, "content": content})
    except Exception as e:
        print(f"Error: {e}")

    driver.quit()

    # Save to JSON
    with open('APEC_Chatbot/backend/APEC.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    print("Crawled data has been saved to APEC.json")

if __name__ == "__main__":
    main()
