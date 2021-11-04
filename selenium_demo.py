from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import csv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy,ProxyType
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName,OperatingSystem



software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value,OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(software_names = software_names, operating_systems= operating_systems,limit=100)

user_agent = user_agent_rotator.get_random_user_agent()

chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1420,1080")
#chrome_options.add_argument(f"user-agent={user_agent}")

PROXY = "https://80.59.199.213:8080"
prox = Proxy()
prox.proxy_type = ProxyType.MANUAL
prox.auto_detect = False
capabilites = webdriver.DesiredCapabilities.CHROME
prox.http_proxy = PROXY
prox.ssl_proxy = PROXY
prox.add_to_capabilities(capabilites)

driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get("https://www.gmc-uk.org/doctors")
time.sleep(3)

__cf_bm = "IjBhdrrIcKSaYZ1gcwlujNqn9W4lkBC3HjZuJZav5ls-1636036674-0-Ab+PEYAc628+iCHl493jl8BWVI8hEPwDMPy/sZ7FjQekXrEEeRIyRX+SS1ieH0bFHzCV6PdnivHQJ2s6qWF9OSk="
cf_clearance = "mgN1pVjs2kAPi7ZdsKYIXcWFYVorrSTaXMal45XAQB8-1636037475-0-250"
cf_clearence_expiry = 1667577075
__cf_bm_expiry = 1636038474


def add_cookie(cf_clearance,cf_clearence_expiry,__cf_bm,__cf_bm_expiry):
    cookie2 = {'domain': '.gmc-uk.org', 'expiry': cf_clearence_expiry, 'httpOnly': True, 'name': 'cf_clearance', 'path': '/',
               'sameSite': 'None', 'secure': True,'value': cf_clearance}
    cookie1 = {'domain': '.gmc-uk.org', 'expiry': __cf_bm_expiry, 'httpOnly': True, 'name': '__cf_bm', 'path': '/',
    'sameSite': 'None', 'secure': True,'value': __cf_bm}
    driver.add_cookie(cookie1)
    driver.add_cookie(cookie2)

    return driver

driver = add_cookie(cf_clearance,cf_clearence_expiry,__cf_bm,__cf_bm_expiry)

time.sleep(1)

name_list = ["george"]

for name in name_list:
    try:
        driver.get("https://www.gmc-uk.org/doctors?page=1&givenNameText="+name+"&pagesize=50")
        time.sleep(2)
        page_input = driver.find_element_by_class_name("paginationInput").text.split(" ")[2]
        all_gmc_numbers = []
        for page in range(1,int(page_input)):
            if len(all_gmc_numbers) > 100:
                break
            print("Toplanan gmc sayısı : {}".format(len(all_gmc_numbers)))
            try:
                next_page = "https://www.gmc-uk.org/doctors?page=" + str(page) + "&givenNameText=george&pagesize=50"
                driver.get(next_page)
                all_gmc_numbers_raw = driver.find_elements_by_class_name("faded")
                for gmc_number in all_gmc_numbers_raw:
                    all_gmc_numbers.append(gmc_number.text)
            except Exception as e:
                print(e)
                print("Finish page")
                break
        count_register = 0
        for gmc_number in all_gmc_numbers:
            driver.get("https://www.gmc-uk.org/doctors/"+gmc_number)
            name = driver.find_element_by_tag_name("h1").text
            register_status = driver.find_element_by_class_name("c-dr-details__status-description").text
            gp_status = driver.find_elements_by_class_name("simpletooltip_container")[2].text
            specialist_status = driver.find_elements_by_class_name("simpletooltip_container")[3].text
            medical_qualification =driver.find_elements_by_class_name("print-doctor-info")[0].text.split("\n")[3]
            final_data = [[gmc_number,name,register_status,gp_status,specialist_status,medical_qualification]]

            header = ["gmc_number", "name", "registered_status","gp_status","specialist_status","medical_qualification"]
            with open('doctors.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerows(final_data)
            print("Kaydedilen doktor sayısı {}".format(count_register))
            count_register +=1
    except Exception as e:
        print(e)
        print("There is no data")
