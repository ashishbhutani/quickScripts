#!/usr/bin/python

#  My ISP Hathway's connection gets dropeed sometimes forcing to login again through their login page.
#  This script will:
#  1. Check if internet is connected by pinging Google's public server.
#  2. If not, it will launch a selenium webdriver.
#  3. Headless browser PhantomJS will ensure that browser window is not opened explicitly.
#  4. It will then simulate filling username/password and submitting login form.
#  5. Script will run as cron, checking every 10 minutes and logging in if disconnected.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import datetime
global driver
global fo
import urllib2

def internet_on():
    try:
        response=urllib2.urlopen('http://8.8.8.8',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

def main():	
	fo = open("/tmp/hathway_login.log", "a")
	fo.write("["+str(datetime.datetime.now())+"]:"+ "Trying Hathway Login...\n");
	if internet_on:
		fo.write("["+str(datetime.datetime.now())+"]:"+ "Already connected to internet\n");
		fo.close()
		exit()

	driver = webdriver.PhantomJS()
	driver.get("http://login.hathway.com")
	global elem_un
	global elem_pw
	global elem_bt
	try:
		elem_un = driver.find_element_by_name("username")
		elem_pw = driver.find_element_by_name("password")
		elem_bt = driver.find_element_by_name("Submit")
	except NoSuchElementException:
		fo.write("["+str(datetime.datetime.now())+"]:"+ "Something went wrong (Hathway changed page strcuture ??)\n");
		fo.close()
		driver.quit()
		exit()

	elem_un.send_keys("")
	elem_pw.send_keys("")
	elem_bt.click()
	fo.write("["+str(datetime.datetime.now())+"]:"+ "Made a new login.Yay!\n");
	fo.close()
	driver.quit() 
	exit()


if __name__ == '__main__':
	main()
