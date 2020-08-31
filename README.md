# Function
Uses Firefox to quickly autofill all the intial screens for getting an appointment(cita) for the intial issuing of a Spanish TIE

# Purpose
This was created because Spain's national police appointment system is notoriously bad. Often appointments are not available because small amounts of appintments are periodcially made available at unknown times and dates. This causes many people to repeat the cita reservation procedure hundreds of times over a month or more to randomly get lucky with a sucessful cita reservation. Therefore this script can help to save lots of time and energy from being wasted during someone's cita journey.

# How to use
After following the prerequisites below run the script without arguments.
```sh
./run.py
```

# Prerequisites

**Basics**
Ensure the following is complete:
- Fill out the "input - personal details" section under GLOBAL VARIABLES
- Use Linux or change the paths above under "static - config"
- Have the selenium package installed for your Python version
- Have firefox installed
- Run the command below
```sh
#COMMAND EXAMPLE
pip install selenium
```

**Prepare the Firefox profile**
Follow this procedure:
- Using firefox manually go to the "cita_url"
- Enter your details and go past the captcha point to generate a Google from cookie
- Find your Firefox profile folder usually in the home directory, then copy the profile folder to the script directory
```sh
#COMMAND EXAMPLE
cp -r /home/gavin/.mozilla/firefox/xoawdc95.default/* /workspace/cita-previa-bot/firefox-profile-copy
```

# Notes

### Issue 1    
Using selenium will fill the /tmp folder of any linux system.

**Solution**
Periodically restart the system or clean the /tmp folder.

### Issue 2
The captcha will eventually distinguish this script as a bot after a string of attempts. The number of attempts before the captacha knows can vary anywhere from 10 - 40, sometimes more.

**Workaround** 
When the script encounters a failed attempt to proceed past a captcha python will go to debug mode.
- Manually solve the captcha and stay on the current page
- Go back to the CLI and you will see a python debug prompt - press c(ontinue)
- Repeat the process

**Solution**
Follow this procedure:
- Wait some time
- Refresh the contents of the "firefox-profile-copy" directory
- Run the script again

### Issue 3
There is no proper automated method to exit the script.

**Solution**
On the CLI press "CTRL+C" at anytime, firefox instances will close when the firefox GUI is closed.