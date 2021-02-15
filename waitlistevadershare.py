# username and password here
USERNAME = "PUT YOUR USERNAME HERE"
PASSWORD = "PUT YOUR PASSWORD HERE"

waiting_time = 1000 #amount of max time to wait when loading pages

# Jeffrey Kozik
# waitlistevader2.py
# #https://medium.com/@igorzabukovec/automate-web-crawling-with-selenium-python-part-1-85113660de96
# https://medium.com/@igorzabukovec/crawl-websites-with-selenium-part-2-3e714120e93f
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# make incognito
chrome_options = Options()
chrome_options.add_argument("--incognito")
# path is executable selenium file
driver = webdriver.Chrome(options=chrome_options, executable_path=r'PUT YOUR PATH HERE')
# sis homepage
url = "https://sis.case.edu/psp/P92SCWR/?cmd=login&languageCd=ENG&"

# https://www.selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.by.html
# open website, instead of waiting 3 seconds for it to load, wait up to waiting_time for it to load, but as soon as needed elements are loaded - continue
# https://stackoverflow.com/questions/27112731/selenium-common-exceptions-nosuchelementexception-message-unable-to-locate-ele
# wait for it to load
# https://pythonbasics.org/selenium-wait-for-page-to-load/
driver.get(url)
try:
    element = WebDriverWait(driver, waiting_time).until(
        EC.presence_of_element_located((By.ID, "userid"))
        and EC.presence_of_element_located((By.ID, "pwd"))
        and EC.presence_of_element_located((By.NAME, "Sign in"))
    )
except:
    print("Timed out")

# fill in username
usid = driver.find_element_by_id("userid")
usid.clear()
usid.send_keys(USERNAME)

# fill in password
pwd = driver.find_element_by_id("pwd")
pwd.clear()
pwd.send_keys(PASSWORD)

# click submit
submit = driver.find_element_by_name("Sign in")
submit.click()

try:
    element = WebDriverWait(driver, waiting_time).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".card-body"))
    )
except:
    print("Timed out")

# click "classes and enrollment"
elements = driver.find_elements_by_css_selector(".card-body")
classes_and_enrollment = elements[2]
classes_and_enrollment.click()

try:
    element = WebDriverWait(driver, waiting_time).until(
        EC.presence_of_element_located((By.CLASS_NAME, "psa_tab_SSR_TERM_STA3_FL"))
    )
except:
    print("Timed out")

# click on "shopping cart"
# https://stackoverflow.com/questions/8832858/using-python-bindings-selenium-webdriver-click-is-not-working-sometimes
shopping_cart = driver.find_element_by_class_name("psa_tab_SSR_TERM_STA3_FL")
shopping_cart.click()
shopping_cart.send_keys("\n")
#print("shopping cart clicked on")

while True:

    try:
        #print("trying")
        element = WebDriverWait(driver, waiting_time).until(
            EC.presence_of_element_located((By.ID, "SSR_REGFORM_VW$0_row_0"))
            # and EC.presence_of_all_elements_located((By.CLASS_NAME, "ps_grid-cell"))
            # and EC.presence_of_all_elements_located((By.CLASS_NAME, "ps_box-group"))
            # and EC.presence_of_all_elements_located((By.CLASS_NAME, "ps_box-edit"))
            # and EC.presence_of_all_elements_located((By.CLASS_NAME, "ps_box-value"))
            # and EC.presence_of_all_elements_located((By.CLASS_NAME, "ps_box-checkbox"))
            # and EC.presence_of_all_elements_located((By.CLASS_NAME, "ps_box-control"))
            # and EC.presence_of_all_elements_located((By.CLASS_NAME, "ps_checkbox"))
            # and EC.presence_of_all_elements_located((By.CLASS_NAME, "ps-button"))
        )
    except:
        print("Timed out")

    # check if any of the waitlist classes are open
    # https://www.geeksforgeeks.org/convert-integer-to-string-in-python/
    row = 0
    enrollable_classes = 0

    #time.sleep(10)

    #print(len(driver.find_elements_by_id("SSR_REGFORM_VW$0_row_" + str(row))))

    # https://stackoverflow.com/questions/7991522/test-if-element-is-present-using-selenium-webdriver
    # https://www.edureka.co/blog/python-list-length/#:~:text=There%20is%20a%20built%2Din,length%20of%20the%20given%20list.
    while len(driver.find_elements_by_id("SSR_REGFORM_VW$0_row_" + str(row))) > 0:
        #print("while")
        #https://www.tutorialspoint.com/finding-an-element-in-a-sub-element-in-selenium-webdriver
        parent = driver.find_element_by_id("SSR_REGFORM_VW$0_row_" + str(row))
        child1 = parent.find_elements_by_class_name("ps_grid-cell")[1]
        child2 = child1.find_elements_by_class_name("ps_box-group")[0]
        child3 = child2.find_elements_by_class_name("ps_box-edit")[0]
        specific_class = child3.find_elements_by_class_name("ps_box-value")[0].text
        # https://www.edureka.co/community/33869/how-to-use-not-equal-operator-in-python#:~:text=The%20python%20!%3D,are%20not%20equal%2C%20otherwise%20false%20.&text=So%20if%20the%20two%20variables,equal%20operator%20will%20return%20True.
        if specific_class != "Closed":
            child1 = parent.find_elements_by_class_name("ps_grid-cell")[0]
            child2 = child1.find_elements_by_class_name("ps_box-group")[0]
            child3 = child2.find_elements_by_class_name("ps_box-checkbox")[0]
            child4 = child3.find_elements_by_class_name("ps_box-control")[0]
            child5 = child4.find_elements_by_class_name("ps-checkbox")[0]
            child5.click()
            enrollable_classes = enrollable_classes + 1
        row = row + 1;

    if enrollable_classes > 0:
        enroll = driver.find_elements_by_class_name("ps-button")[12]
        enroll.click()

        try:
            element = WebDriverWait(driver, waiting_time).until(
                EC.presence_of_all_elements_located((By.ID, "#ICYes"))
            )
        except:
            print("Timed out")

        yes_confirmed = driver.find_element_by_id("#ICYes")
        yes_confirmed.click()

        try:
            element = WebDriverWait(driver, waiting_time).until(
                EC.presence_of_element_located((By.ID, "DERIVED_REGFRM1_DESCRLONG$0"))
            )
        except:
            print("Timed out")

        # click on "shopping cart"
        shopping_cart = driver.find_element_by_class_name("psa_tab_SSR_TERM_STA3_FL")
        shopping_cart.click()
        shopping_cart.send_keys("\n")
        #print("shopping cart clicked on")

    else:
        # https://www.guru99.com/selenium-refresh-page.html
        driver.refresh()
        #print("refreshed")




























#     #https://www.w3schools.com/python/python_conditions.asp
#     potential_desired_semester = driver.find_element_by_id("SSR_CSTRMCUR_VW_DESCR$0")
#     # https://stackoverflow.com/questions/28022764/python-and-how-to-get-text-from-selenium-element-webelement-object
#     if potential_desired_semester.text == SEMESTER:
#         desired_semester = driver.find_element_by_id("SSR_CSTRMCUR_GRD$0_row_0")
#     potential_desired_semester = driver.find_element_by_id("SSR_CSTRMCUR_VW_DESCR$1")
#     if potential_desired_semester.text == SEMESTER:
#         desired_semester = driver.find_element_by_id("SSR_CSTRMCUR_GRD$0_row_1")
#     # click desired semester (for the first time coding this it's spring 2021)
#     desired_semester.click()
#     time.sleep(3)
#
#     # search for class I want
#     class_i_want = driver.find_element_by_id("CW_CLSRCH_WRK2_PTUN_KEYWORD")
#     class_i_want.send_keys(my_class)
#
#     # press search
#     search_for_class = driver.find_element_by_id("CW_CLSRCH_WRK_SSR_PB_SEARCH")
#     search_for_class.click()
#     time.sleep(3)
#
#     omg_register = False
#
#     # https://www.geeksforgeeks.org/convert-integer-to-string-in-python/
#     row = 0
#     # https://stackoverflow.com/questions/7991522/test-if-element-is-present-using-selenium-webdriver
#     # https://www.edureka.co/blog/python-list-length/#:~:text=There%20is%20a%20built%2Din,length%20of%20the%20given%20list.
#     while len(driver.find_elements_by_id("DESCR100$0_row_" + str(row))) > 0:
#         #https://www.tutorialspoint.com/finding-an-element-in-a-sub-element-in-selenium-webdriver
#         parent = driver.find_element_by_id("DESCR100$0_row_" + str(row))
#         child1 = parent.find_elements_by_class_name("ps_grid-cell")[0]
#         child2 = child1.find_elements_by_class_name("ps_box-group")[0]
#         child3 = child2.find_elements_by_class_name("ps_box-htmlarea")[1]
#         specific_class = child3.find_elements_by_class_name("ps-htmlarea")[0].text
#         if specific_class == my_specific_class:
#             child1 = parent.find_elements_by_class_name("ps_grid-cell")[1]
#             child2 = child1.find_elements_by_class_name("ps_box-group")[0]
#             child3 = child2.find_elements_by_class_name("ps_box-htmlarea")[1]
#             open_seats_unparsed = child3.find_elements_by_class_name("ps-htmlarea")[0].text
#             # https://www.pythonforbeginners.com/basics/string-manipulation-in-python
#             open_seats = open_seats_unparsed[12:]
#             # https://www.geeksforgeeks.org/convert-string-to-integer-in-python/
#             open_seats_number = int(open_seats)
#             omg_register = True
#             # https://realpython.com/python-while-loop/
#             break
#         row = row + 1;
#         time.sleep(3)
#
#     if omg_register:
#         parent.click()
#
# search_for_class(CLASSES[0][0], CLASSES[0][1])
