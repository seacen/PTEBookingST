# PTEBookingST
PTEBookingST is a program that helps people snap up newly available seats for PTE Academic Exam.

## Features
### Scraping
Scrape the seat availability website continuously to report new vacant seats.
### Notification
Alert the user by email when a new seat in preferred date range has become available.
### Booking
Sort new seats by user preference and auto secure seats (book the exam) for the user according to the sorted order.

**_This feature is currently not complete. Please feel free to check out the [sorter.py](../master/sorter.py) and [booker.py](../master/booker.py) files to extend the codes._**

## License
This project is licensed under [Attribution-NonCommercial 4.0 International](https://creativecommons.org/licenses/by-nc/4.0/legalcode).

As part of the initiative for urging Pearson to improve its PTE exam booking impartiality and website robustness (e.g. Adding CAPTCHAs), this project has been made open source and is free for download and use under the constraints specified in the license. Check out this page for a brief summary of the license: https://creativecommons.org/licenses/by-nc/4.0/

## Dependency Installation
PTEBookingST requires several dependencies to be installed in order to be succesfully up and running.

### Python
This program is written in python and thus requires python to be installed on your computer to be able to run.
#### Python3 installation instruction
##### Mac
[Installing Python 3 on Mac OS X](http://python-guide-pt-br.readthedocs.io/en/latest/starting/install3/osx/)
##### Windows
[How to Install Python on Windows](https://www.howtogeek.com/197947/how-to-install-python-on-windows/)

### Selenium
Selenium is a browser automation tool and is at the core of the program. Run the following on Mac Terminal or Windows Command Line to install:
```
pip3 install selenium
```
or
```
pip install selenium
```

### PhantomJS
PhantomJS is a headless browser with JavaScript support. It is used in conjunction with Selenium (as the driver).
#### Download
Download PhantomJS at this address: http://phantomjs.org/download.html
#### Make sure the executable is in PATH
##### Mac
Place it in `/usr/bin` or `/usr/local/bin`  (`command`+`shift`+`.` to show hidden files and folders)
##### Windows
Add the directory where you executable is in to PATH environment variable. Refer to this doc for instructions: [How to set the path and environment variables in Windows](https://www.computerhope.com/issues/ch000549.htm)

### Requests
Requests is a python module for easily sending web requests to API. It is used for sending requests to MailGun email sending API. Run the following on Mac Terminal or Windows Command Line to install:
```
pip3 install requests
```
or
```
pip install requests
```
## Email Notification
PTEBookingST consumes [mailgun API](https://www.mailgun.com/) under the hood to send email notifications. To enable email notification functionality in the program, users need to register with mailgun to obtain a free mailgun domain and an API key for authenticating with mailgun service.

Once registered and logged in, go to Domains > _Your random allocated domain_ > Domain Information for domain name and API key.

## Usage
1. Download this project to local and point Mac Terminal or Windows Command Line to the project folder. E.g:
```
cd /Users/seacen/Development/Projects/PTEBookingST
```
2. Run the program by executing this command:
```
python3 run.py
```
or
```
python run.py
```

## Configuration
PTEBookingST stores and reads your settings in _configs_ folder. Modify values in the following files to manipulate the program behaviour.
### [settings.txt](../master/configs/settings.txt)
This file stores common settings for the program.

| Key | Description | Value Format |
| --- | --- | --- |
| start_date | the earlist date you want to take the exam in | `yyyy-mm-dd` |
| end_date | the latest date you want to subscribe the seats information of | `yyyy-mm-dd` |
| city | city to sit your exam in | city name in **lower** letters |
| scraping_interval | the interval between each new scraping round | number in minutes, can be decimal |
| do_email_alert | whether email alert should be sent when new seat is found | `true` or `false` |
| do_check_time | whether to scrape the individual time of the available date | `true` or `false` |

### [emails.txt](../master/configs/emails.txt)
This file stores the email addresses that you want to be put as recipients of the email notification. Each email address should take up a line in the file.

### [emailer_settings.txt](../master/configs/emailer_settings.txt)
This file stores your mailgun account information. See [Email Notification](#email-notification) for details.

| Key | Description | Value Format |
| --- | --- | --- |
| domain | the free domain that has been allocated to your account | full domain |
| api_key | API key of your mailgun account | API key |
