#!/usr/bin/python

####################################
#GLOBAL VARIABLES
####################################

#static - error messages that indicate la cita previa attempts failed
bad_msg1 = "NO HAY SUFICIENTES"
bad_msg2 = "En este momento no hay citas disponibles"

#static - config
base_path = ""
cita_url = "https://sede.administracionespublicas.gob.es/icpplus/index.html"
ff_profile = "/resource/firefox-profile-copy"
pdf_file_location = "/resource/pdf-downloads"
exdriver = "/resource/geckodriver"

#input - personal details
nie = "A1234567B"
nombre = "FIRST AND LAST NAME"
pais = "COUNTRY NAME IN SPANISH"
phone = "123456789"
email = "yourmail@mail.com"

####################################
#READ ME
####################################

#Function
################
#Uses Firefox to quickly autofill all the intial screens for getting an appointment(cita) for the intial issuing of a Spanish TIE

#PURPOSE
################
#This was created because Spain's national police appointment system is notoriously bad. 
#Often appointments are not available because small amounts of appintments are periodcially made available at unknown times and dates.
#This causes many people to repeat the cita reservation procedure hundreds of times over a month or more to randomly get lucky with a sucessful cita reservation.
#Therefore this script can help to save lots of time and energy from being wasted during someone's cita journey.


#PRE-REQ 1
################
#use linux or change the paths above under "static - config"

#PRE-REQ 2
################
#fill out the "input - personal details" section under GLOBAL VARIABLES

#PRE-REQ 3
################
#COMMAND: pip install selenium

#PRE-REQ 4
################
#have firefox installed

#PRE-REQ 5
################
#--> using firefox manually go to the "cita_url"
#--> enter your details and go past the captcha point to generate a Google from cookie
#--> find your firefox profile folder usually in the home directory, then copy the profile folder to the script directory
#################
#COMMAND EXAMPLE: cp -r /home/gavin/.mozilla/firefox/xoawdc95.default/* /workspace/cita-previa-bot/firefox-profile-copy


#NOTE 1:
################
#PROBLEM:    using selenium will fill the /tmp folder of any linux system
################
#SOLUTION:   --> periodically restart the system or clean the /tmp folder

#NOTE 2:
################
#PROBLEM:    the captcha will eventually distinguish this script as a bot after a string of attempts
#            the number of attempts before the captacha knows can vary anywhere from 10 - 40, sometimes more
################
#WORKAROUND: when the script encounters a failed attempt to proceed past a captcha python will go to debug mode
#            --> manually solve the captcha and stay on the current page
#            --> go back to the CLI and you will see a python debug prompt - press c(ontinue)
#            --> repeat the process
################
#SOLUTION:   --> wait some time
#            --> refresh the contents of the "firefox-profile-copy" directory
#            --> run the script again

#NOTE 3:
################
#PROBLEM:    there is no automated method to exit the script
################
#SOLUTION:   on the CLI press "CTRL+C" at anytime, firefox instances will close when the firefox GUI is closed


####################################
#LIBRARIES
####################################

#for script termination actions
import atexit
import signal

#for getting pwd
import os
#for generating time stamps for pdf files
from datetime import datetime

#for adding wait time
import time

#for adding a breakpoint to interact with captchas
import pdb

#for normal selenium operations
from selenium import webdriver
from selenium.webdriver.support.ui import Select

#for recaptcha bypass
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


####################################
#FUNCTIONS
####################################

#NOT USED
####################################
def exit_browser(INSTANCE):

    print('[INFO] performing browser cleanup')
    try:
        INSTANCE.close()
    except:
        pass

####################################
def create_browser(DL_DIR, FF_PROFILE, EXDRIVER):

    profile = webdriver.FirefoxProfile(FF_PROFILE)
    profile.set_preference("dom.webdriver.enabled", False)
    profile.set_preference('useAutomationExtension', False)
    profile.set_preference('devtools.jsonview.enabled', False)
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir", DL_DIR)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
    profile.update_preferences()

    wdriver = webdriver.Firefox(firefox_profile=profile, executable_path=EXDRIVER)
    return wdriver

####################################
def process_page_error(INSTANCE):

    print("[INFO] NO HAY SUFICIENTES CITAS DISPONIBLES o En este momento no hay citas disponibles")

    try:
        #click the aceptar box
        button = INSTANCE.find_element_by_id('btnSubmit')
        button.click()
    except:
        #click the salir box
        button = INSTANCE.find_element_by_id('btnSalir')
        button.click()

####################################
def process_page1(INSTANCE):

    #select provincia
    selection_box = Select(INSTANCE.find_element_by_xpath("//div[@id='divProvincias']/select[@id='form']"))
    selection_box.select_by_visible_text('Madrid')

    #click the aceptar box
    button = INSTANCE.find_element_by_id('btnAceptar')
    button.click()
    
####################################
def process_page2(INSTANCE):

    #select cita type
    selection_box = Select(INSTANCE.find_element_by_xpath("//fieldset[@id='divGrupoTramites']/div[@class='fld']/select"))
    selection_box.select_by_value('4010')

    #click the aceptar box
    button = INSTANCE.find_element_by_id('btnAceptar')
    button.click()

####################################
def process_page3(INSTANCE):

    #click the entrar box
    button = INSTANCE.find_element_by_id('btnEntrar')
    INSTANCE.execute_script("arguments[0].click();", button)

####################################
def process_page4(INSTANCE, NIE, NOMBRE, PAIS):

    #wait
    time.sleep(3)

    #input NIE
    input_box = INSTANCE.find_element_by_id('txtIdCitado')
    input_box.send_keys(NIE)

    #input nombre
    input_box = INSTANCE.find_element_by_id('txtDesCitado')
    input_box.send_keys(NOMBRE)

    #select pais
    selection_box = Select(INSTANCE.find_element_by_id('txtPaisNac'))
    selection_box.select_by_visible_text(PAIS)

    #bypass recaptcha
    WebDriverWait(INSTANCE, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
    WebDriverWait(INSTANCE, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()

    #wait
    time.sleep(2)
    #return to main page
    INSTANCE.switch_to.default_content()

    #click the entrar box
    try:
        button = INSTANCE.find_element_by_id('btnEnviar')
        INSTANCE.execute_script("arguments[0].click();", button)
    except:
        pass

####################################
def process_page5(INSTANCE):

    #click the solicitar box
    button = INSTANCE.find_element_by_id('btnEnviar')
    INSTANCE.execute_script("arguments[0].click();", button)

####################################
def process_page6(INSTANCE, STAT):

    #click the siguente box
    try:
        button = INSTANCE.find_element_by_id('btnSiguiente')
        INSTANCE.execute_script("arguments[0].click();", button)
    
    except NoSuchElementException:
        print("[INFO] run captcha process")
        pdb.set_trace()
        INSTANCE.switch_to.default_content()

        #from process_page4
        button = INSTANCE.find_element_by_id('btnEnviar')
        INSTANCE.execute_script("arguments[0].click();", button)

        time.sleep(1)
        if (INSTANCE.page_source.find(bad_msg1) != -1) or (INSTANCE.page_source.find(bad_msg2) != -1):
            process_page_error(INSTANCE)
            STAT = "bad_msg"
        else:
            process_page5(INSTANCE)

        time.sleep(1)
        if (INSTANCE.page_source.find(bad_msg1) != -1) or (INSTANCE.page_source.find(bad_msg2) != -1):
            process_page_error(INSTANCE)
            STAT = "bad_msg"
        elif (STAT == "bad_msg"):
            print("[INFO] skipping page 6")   
        else:
            button = INSTANCE.find_element_by_id('btnSiguiente')
            INSTANCE.execute_script("arguments[0].click();", button)

    return STAT

####################################
def process_page7(INSTANCE, PHONE, EMAIL):

    #input phone
    input_box = INSTANCE.find_element_by_id('txtTelefonoCitado')
    input_box.send_keys(PHONE)

    #input email
    input_box = INSTANCE.find_element_by_id('emailUNO')
    input_box.send_keys(EMAIL)
    input_box = INSTANCE.find_element_by_id('emailDOS')
    input_box.send_keys(EMAIL)

    #click the siguente box
    button = INSTANCE.find_element_by_id('btnSiguiente')
    INSTANCE.execute_script("arguments[0].click();", button)


####################################
#MAIN
####################################

def main():

	#declare global variables
	global base_path
	global ff_profile
	global pdf_file_location
	global exdriver

	#set global script paths
	base_path = str(os.getcwd())
	ff_profile = base_path + ff_profile
	pdf_file_location = base_path + pdf_file_location
	exdriver = base_path + exdriver

	#initialize tracking
	process_status = "none"
	attempts = int(1)

	#setup broswer
	browser = create_browser(pdf_file_location, ff_profile, exdriver)
	browser.get(cita_url)

	#execute page processing
	while True:
		print("[INFO] Attempts - " + str(attempts))

		process_page1(browser)
		process_page2(browser)
		process_page3(browser)
		process_page4(browser, nie, nombre, pais)
        
		time.sleep(1)
		if (browser.page_source.find(bad_msg1) != -1) or (browser.page_source.find(bad_msg2) != -1):
		    process_page_error(browser)
		    process_status = "bad_msg"
		else:
		    process_page5(browser)

		time.sleep(1)
		if (browser.page_source.find(bad_msg1) != -1) or (browser.page_source.find(bad_msg2) != -1):
		    process_page_error(browser)
		    process_status = "bad_msg"
		else:
		    process_status = process_page6(browser, process_status)

		time.sleep(1)
		if (browser.page_source.find(bad_msg1) != -1) or (browser.page_source.find(bad_msg2) != -1):
		    process_page_error(browser)
		    process_status = "bad_msg"
		elif (process_status == "bad_msg"):
		    print("[INFO] skipping page 7")
		else:
		    process_page7(browser, phone, email)

		time.sleep(1)
		if (browser.page_source.find(bad_msg1) != -1) or (browser.page_source.find(bad_msg2) != -1):
		    process_page_error(browser)
		    process_status = "bad_msg"
		elif (process_status == "bad_msg"):
		    print("[INFO] skipping page 8")
		else:
		    print("[ALERT] new page found")
		    pdb.set_trace()

		attempts += 1
		process_status = "none"


####################################
#EXECUTE AS A SCRIPT
####################################
if __name__ == "__main__":
    main()