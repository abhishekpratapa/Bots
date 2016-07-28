from enum import Enum
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from pymongo import MongoClient
from bs4 import BeautifulSoup
import time
import random
import datetime
#kivy UI/UX

# define exceptions

# User Agent Exception
class UserAgentError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

# Site Selection Exception
class siteError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

# Login Exception
class LoginError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

# Enum type User Agent
class UserAgent(Enum):
    Firefox = 1
    Chrome = 2

# Enum type for Logins
class Sites(Enum):
    LinkedIn = 1
    Google = 2
    Twitter = 3
#
#  createUserInstance() :  create a new Browser window
#  search(): Search Google, Twitter or LinkedIn based off of certain query parameters
#  post(): Post a public message to Google, Twitter or Linkedin
#
#
#
class BrowserInstance:
    def __init__(self, username, password, phone, site=Sites.LinkedIn, UserInterface=UserAgent.Firefox, database_used = True):

        # check if useragent is valid
        if not isinstance(UserInterface, UserAgent):
            raise UserAgentError('Please select the correct UserAgent:  Types: [Firefox] [Chrome]')

        # check if site is valid
        if not isinstance(site, Sites):
            raise siteError('Please select the correct site:  Types: [Google] [LinkedIn] [Twitter]')

        # self defined variables
        self.username = username
        self.password = password
        self.phone = phone
        self.agent = UserInterface

        #for text confirmation
        self.google_login_value = False
        self.site = site

        #set up database connection
        if database_used:
            self.client = MongoClient("mongodb://127.0.0.1:27017");
            self.db = self.client.DataCollection

        #delay for 3 seconds
        time.sleep(3)
    #confirmation message
    def __send_text_confirmation(self):
        self.driver.get("http://voice.google.com")

        if not self.google_login_value:
            login_form_gmail = self.driver.find_element_by_id('Email')
            time.sleep(1)
            login_form_gmail.send_keys(self.username)
            time.sleep(6)
            login_form_gmail.send_keys(Keys.RETURN)
            time.sleep(1)
            password_form_gmail = self.driver.find_element_by_id('Passwd')
            time.sleep(1)
            password_form_gmail.send_keys(self.password)
            time.sleep(5)
            password_form_gmail.send_keys(Keys.RETURN)
            time.sleep(2)

        button_press_gmail = self.driver.find_elements_by_class_name("goog-inline-block")
        time.sleep(1)
        for button in button_press_gmail:
            if "Text" == button.get_attribute('innerHTML'):
                button.click()
                break
        time.sleep(2)
        smsSent_gmail = self.driver.find_element_by_id("gc-quicksms-number")
        smsSent_gmail.send_keys(self.phone)
        time.sleep(2)
        message_gmail = self.driver.find_element_by_id("gc-quicksms-text2")
        message_gmail.send_keys("Done with the Linkedin crawling")
        time.sleep(5)
        send_button_press_gmail = self.driver.find_elements_by_class_name("goog-button-base-content")
        index_gmail = 0;
        for this_button_gmail in send_button_press_gmail:
            if this_button_gmail.get_attribute('innerHTML') == "Send":
                index_gmail = index_gmail + 1
                if index_gmail == 3:
                    this_button_gmail.click()
                    break
        return

    #   Function to login for LinkedIn
    def __Login_Linkedin(self):
        # start instance of browser
        self.driver.get("http://www.linkedin.com")

        # sleep for 6 seconds
        time.sleep(6)

        # login to linkedin
        # send login keystrokes
        login_form = self.driver.find_element_by_id('login-email')
        login_form.send_keys(self.username)

        # sleep for 3 seconds
        time.sleep(3)

        # send password keystrokes
        password_form = self.driver.find_element_by_id('login-password')
        password_form.send_keys(self.password)

        # sleep for 3 seconds
        time.sleep(3)

        # hit enter key in password form
        password_form.send_keys(Keys.RETURN);

        # sleep for 3 seconds
        time.sleep(3)

        # validate login
        try:
            disposable_variable = self.driver.find_elements_by_class_name('name')
        except NoSuchElementException as e:
            raise LoginError("Could not Login to Linkedin")

        # login worked
        return True

    #   Function to login to twitter
    def __Login_Twitter(self):
        # start instance of browser
        self.driver.get("http://twitter.com")

        # sleep for 6 seconds
        time.sleep(6)

        # test if the sign-up button was successfully pressed
        successfully_pressed_login = False
        login_button = None
        # login to Twitter

        try:
            # press the Login Button
            login_button = self.driver.find_element_by_class_name("js-login")
            successfully_pressed_login = True
            print("Success")
        except:
            pass

        #different page layout
        if not successfully_pressed_login:
            login_button = self.driver.find_element_by_id("signin-link")

        #press the login button
        login_button.click()

        # sleep for 3 seconds
        time.sleep(3)

        # send email address
        email_text = self.driver.find_element_by_name("session[username_or_email]")
        email_text.send_keys(self.username)

        # sleep for 3 seconds
        time.sleep(3)

        # send password keystrokes
        password_text = self.driver.find_element_by_name("session[password]")
        password_text.send_keys(self.password)

        # sleep for 3 seconds
        time.sleep(3)

        # hit enter key in password form
        password_text.send_keys(Keys.RETURN)

        # sleep for 3 seconds
        time.sleep(3)

        # validate login
        try:
            disposable_variable = self.driver.find_elements_by_class_name('DashboardProfileCard-avatarImage')
        except NoSuchElementException as e:
            raise LoginError("Could not Login to Twitter")

        # login worked
        return True

    # Function to login to google
    def __Login_Google(self):
        # start instance of browser
        self.driver.get("http://www.google.com")

        # sleep for 3 seconds
        time.sleep(3)

        # Initiate login sequence
        # Click sign in button
        login_button = self.driver.find_element_by_id("gb_70")
        login_button.click()

        # sleep for 6 seconds
        time.sleep(6)

        #send my email address
        login_form_gmail = self.driver.find_element_by_id('Email')
        login_form_gmail.send_keys(self.username)

        # sleep for 5 seconds
        time.sleep(5)

        # Hit the return key to continue
        login_form_gmail.send_keys(Keys.RETURN)

        # sleep for 3 seconds
        time.sleep(3)

        # type in the password
        password_form_gmail = self.driver.find_element_by_id('Passwd')
        password_form_gmail.send_keys(self.password)

        # sleep for 5 seconds
        time.sleep(5)

        # Hit the return key to complete logging in
        password_form_gmail.send_keys(Keys.RETURN)

        # sleep for 5 seconds
        time.sleep(5)

        # validate login
        try:
            disposable_variable = self.driver.find_elements_by_class_name('tsf')
        except NoSuchElementException as e:
            raise LoginError("Could not Login to Google")

        # login worked
        self.google_login_value = True
        return True

    def __Logout_Linkedin(self):
        # go to the homepage
        self.driver.get("https://www.linkedin.com")

        # open the account settings
        element = self.driver.find_element_by_class_name("account-settings-tab")
        hov = ActionChains(self.driver).move_to_element(element)
        hov.perform()

        # press sign out on the menu
        menu_elements = self.driver.find_elements_by_class_name('account-submenu-split-link')
        for element in menu_elements:
            if "Sign Out" in element.text:
                element.click()
                break

        # sleep for 3000 seconds
        time.sleep(3)



    def __Logout_Twitter(self):
        # go to the homepage
        self.driver.get("https://www.twitter.com/")

        # sleep for 3 seconds
        time.sleep(3)

        # Click profile button
        toggle_button = self.driver.find_element_by_id("user-dropdown-toggle")
        toggle_button.click()

        # sleep for 3 seconds
        time.sleep(3)

        # Click logout button
        logout_button = self.driver.find_element_by_id("signout-button")
        logout_button.click()

        # sleep for 3 seconds
        time.sleep(3)

        return


    def __Logout_Google(self):
        #go to the homepage
        self.driver.get("https://accounts.google.com/SignOutOptions?hl=en&continue=https://www.google.com/")

        # sleep for 3 seconds
        time.sleep(3)

        # Click log out button
        logout_button = self.driver.find_element_by_id("signout")
        logout_button.click()

        #set value to Logout
        self.google_login_value = False

    def __Posting_Linkedin(self, textArea):
        # go to the homepage
        self.driver.get("https://www.linkedin.com")

        #press icon for posting
        menu_elements = self.driver.find_elements_by_class_name('share')
        for element in menu_elements:
            if "Share an update" in element.text:
                element.click()
                break

        #making a post
        module_text = self.driver.find_element_by_id("postmodule-text")
        module_text.send_keys(textArea)

        # press share for posting
        menu_elements = self.driver.find_elements_by_class_name('postmodule-submit')
        for element in menu_elements:
            if "Share" in element.text:
                element.click()
                break

        # post to Linkedin
    def __Posting_Twitter(self, textArea):
        # go to the homepage
        self.driver.get("https://www.twitter.com/")

        # sleep for 3 seconds
        time.sleep(3)

        #press the tweet button
        tweet_button = self.driver.find_element_by_id("global-new-tweet-button")
        tweet_button.click()

        # sleep for 3 seconds
        time.sleep(3)

        # find the tweet textbox
        tweet_text = self.driver.find_element_by_id("tweet-box-global")
        tweet_text.send_keys(textArea)

        # find the proper tweet button to press since there are multiple on the page
        different_buttons = self.driver.find_elements_by_class_name("js-tweet-btn")
        for each_element in different_buttons:
            sentAttributes = each_element.get_attribute("class")
            if not "disabled" in sentAttributes:
                each_element.click()
                break

        # sleep for 3 seconds
        time.sleep(3)



    #DOESN'T WORK

    # post to google
    def __Posting_Google(self, textArea):
        # make sure there are no offers or modal windows
        # start instance of browser
        self.driver.get("https://plus.google.com/")

        # sleep for 3 seconds
        time.sleep(3)

        # find the tweet textbox
        google_post = self.driver.find_elements_by_class_name("kqa")

        for post in google_post:
            if ("kqa es" in post.get_attribute("class")) and ("new with" in post.get_attribute("innerHTML")):
                post.click()
                break

        time.sleep(3)

        text_box = self.driver.find_elements_by_class_name("df")

        for button in text_box:
            if ("df b-K b-K-Xb URaP8 editable" in button.get_attribute("class")):
                button.send_keys(textArea)
                break

        # find the tweet textbox
        send_buttons = self.driver.find_elements_by_class_name("d-k-l")

        time.sleep(3)

        for button in send_buttons:
            if ("d-k-l b-c b-c-Ba qy jt" in button.get_attribute("class")) and ("Share" in button.get_attribute("innerHTML")):
                button.click()
                break

        time.sleep(3)

        #post to google


    # Create a new User Instance
    #
    # method createUserInstance: Create a new LinkedIn bot to login to the account
    #
    # @params   self:       defined
    # @params   Display:    Show the Browser, defined [Default = True]
    #
    # return True if login is a success
    #

    def createUserInstance(self, Display=True):
        # check whether the user wants a background or foreground process
        if not Display:
            display = Display(visible=False, size=(800, 600))
            display.start()

        # detect what browser to use and start browser
        if self.agent.name == "Firefox":
            self.driver = webdriver.Firefox()
        elif self.agent.name == "Chrome":
            self.driver = webdriver.Chrome()
        else:
            raise NameError('The specified useragent doesn\'t exist')

        #login
        if self.site.name == "Google":
            return self.__Login_Google()
        elif self.site.name == "LinkedIn":
            return self.__Login_Linkedin()
        elif self.site.name == "Twitter":
            return self.__Login_Twitter()

        raise siteError('Please select the correct site:  Types: [Google] [LinkedIn] [Twitter]')

    def close_last_tab(self):
        if (len(self.driver.window_handles) == 2):
            self.driver.switch_to.window(window_name=self.driver.window_handles[-1])
            self.driver.close()
            self.driver.switch_to.window(window_name=self.driver.window_handles[0])

    def __google_search_query(self, Limit, startDate="0/0/0", endDate="0/0/0"):

        if not (startDate == "0/0/0" and endDate  == "0/0/0"):
            more_button = self.driver.find_element_by_id("hdtb-tls")
            more_button.click()

            time.sleep(3)

            range_selector = self.driver.find_elements_by_class_name("mn-hd-txt")

            for select in range_selector:
                if ("Any time" in select.get_attribute("innerHTML")):
                    select.click()
                    break

            time.sleep(3)

            click_calandar_link = self.driver.find_element_by_id("cdrlnk")
            click_calandar_link.click()

            time.sleep(3)

            cdr_min = self.driver.find_element_by_id("cdr_min")
            cdr_min.send_keys(startDate)

            time.sleep(3)

            cdr_max = self.driver.find_element_by_id("cdr_max")
            cdr_max.send_keys(endDate)

            index_date = 0

            submit_date = self.driver.find_elements_by_class_name("ksb")
            for sub in submit_date:
                index_date = index_date + 1
                if ("ksb mini cdr_go" in sub.get_attribute("class")) and index_date == 2:
                    print(sub.get_attribute("value"))
                    sub.click()
                    break
            time.sleep(3)
        elif not (startDate == "0/0/0"):
            more_button = self.driver.find_element_by_id("hdtb-tls")
            more_button.click()

            time.sleep(3)

            range_selector = self.driver.find_elements_by_class_name("mn-hd-txt")

            for select in range_selector:
                if ("Any time" in select.get_attribute("innerHTML")):
                    select.click()
                    break

            time.sleep(3)

            click_calandar_link = self.driver.find_element_by_id("cdrlnk")
            click_calandar_link.click()

            time.sleep(3)

            cdr_min = self.driver.find_element_by_id("cdr_min")
            cdr_min.send_keys(startDate)

            #add one month to cdr
            dt = datetime.datetime.strptime(startDate, '%m/%d/%Y')
            newTimestamp = time.mktime(dt.timetuple())
            nextMonth = int(newTimestamp)+2721600;
            newDate = datetime.datetime.fromtimestamp(nextMonth).strftime("%m/%d/%Y")

            cdr_max = self.driver.find_element_by_id("cdr_max")
            cdr_max.send_keys(newDate)
            #add one month

            index_date = 0

            submit_date = self.driver.find_elements_by_class_name("ksb")
            for sub in submit_date:
                index_date = index_date + 1
                if ("ksb mini cdr_go" in sub.get_attribute("class")) and index_date == 2:
                    print(sub.get_attribute("value"))
                    sub.click()
                    break
            time.sleep(3)
        # find all class "r" terms
        main_window = self.driver.current_window_handle
        searchArray = []

        time.sleep(10)

        while Limit > len(searchArray):
            time.sleep(5)
            new_elements = self.driver.find_elements_by_xpath("//h3[contains(@class,'r')]/a")
            looper = len(new_elements) - 1
            indexLoop = 0;
            while looper > indexLoop:
                try:
                    elements_with_r = self.driver.find_elements_by_xpath("//h3[contains(@class,'r')]/a")
                    print(elements_with_r[indexLoop].get_attribute("innerHTML"))
                    elements_with_r[indexLoop].send_keys(Keys.COMMAND + Keys.RETURN)
                    time.sleep(1)
                    self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
                    time.sleep(random.randint(4, 7))
                    searchArray.append(self.driver.current_url)
                    self.driver.switch_to.window(main_window)
                    time.sleep(2)
                    self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
                    time.sleep(random.randint(4, 7))
                    # Put focus on current window which will be the window opener
                    self.driver.switch_to.window(main_window)
                except:
                    time.sleep(random.randint(4, 7))
                    pass

                if Limit < len(searchArray):
                    break
                indexLoop = indexLoop + 1
            print(searchArray)
            time.sleep(4)

            backbutton = self.driver.find_elements_by_class_name('pn')
            backbutton[len(backbutton) - 1].click()

            time.sleep(3)
        time.sleep(4)

        return searchArray[:Limit]

    ######################################################################################

    def __get_profile_information(self, url_sent, Term):

        # set parameters
        name_form = None
        discription_form = None
        location_form = None
        current_form = None
        background_experience = None

        education_form = []
        experience_array = []
        # relevant pieces of information

        person_dictionary = dict()

        # name
        try:
            name_form = self.driver.find_element_by_class_name('full-name')
        except:
            # cannot find element
            pass

        # discription
        try:
            discription_form = self.driver.find_element_by_id('headline')
        except:
            # do stuff
            pass

        # locality
        try:
            location_form = self.driver.find_element_by_class_name('locality')
        except:
            # do stuff
            pass

        # current work
        try:
            current_form = self.driver.find_element_by_id('overview-summary-current')
        except:
            # do stuff
            pass

        # current work
        try:
            current_form = self.driver.find_element_by_id('background-education')
            educationSoup = BeautifulSoup(current_form.get_attribute('innerHTML'), 'html.parser')
            for link in educationSoup.find_all('div', class_='education'):
                educationDict = dict()
                try:
                    educationLink = link.find("header")
                    try:
                        educationDict['school'] = educationLink.find("h4").get_text()
                        try:
                            more_processing = educationLink.find("h5")
                            try:
                                educationDict['degree'] = more_processing.find('span', class_="degree").get_text()
                                educationDict['major'] = more_processing.find('span', class_="major").get_text()
                            except:
                                pass
                        except:
                            pass
                    except:
                        pass
                except:
                    pass
                education_form.append(educationDict);
        except:
            # do stuff
            pass

        # current work
        try:
            background_experience = self.driver.find_element_by_id('background-experience')
            experienceSoup = BeautifulSoup(background_experience.get_attribute('innerHTML'), 'html.parser')
            for link in experienceSoup.find_all('div', class_='editable-item'):

                the_dictionary = dict()

                temp_titleJob = None
                temp_companyJob = None
                temp_timeExperienceJob = None
                temp_summaryJob = None

                try:
                    temp_titleJob = link.find('h4').get_text()
                    the_dictionary['job'] = temp_titleJob
                except:
                    pass

                try:
                    temp_companyJob = link.find('h5').get_text()
                    the_dictionary['company'] = temp_companyJob
                except:
                    pass

                try:
                    temp_timeExperienceJob = link.find('span', class_='experience-date-locale').get_text()
                    the_dictionary['experience'] = temp_timeExperienceJob
                except:
                    pass

                try:
                    temp_summaryJob = link.find('p', class_='summary-field-show-more').get_text()
                    the_dictionary['summary'] = temp_summaryJob
                except:
                    pass

                experience_array.append(the_dictionary)

        except:
            # do stuff
            pass

        if name_form != None:
            print(name_form.text)
            person_dictionary['name'] = name_form.text
            person_dictionary['url'] = url_sent
            person_dictionary['searchTerm'] = Term

        if discription_form != None:
            print(discription_form.text)
            person_dictionary['discription'] = discription_form.text

        if location_form != None:
            print(location_form.text)
            person_dictionary['location'] = location_form.text

        if current_form != None:
            print(current_form.text)
            person_dictionary['currentJob'] = current_form.text

        if experience_array:
            print(experience_array)
            person_dictionary['experiences'] = experience_array

        if education_form:
            print(education_form)
            person_dictionary['education'] = education_form

        # push to database
        if person_dictionary:
            result = self.db.LinkedinUsers.insert_one(person_dictionary)
            print(result.inserted_id)

        # figure out a proper wait time for linkedin
        WaitTime = random.randint(4, 10)
        time.sleep(WaitTime)
        return

    ####################################################################

    def __linkedin_search_query(self, Term, Limit, Database_save=True, Recursive=True, Recursion=3):
        time.sleep(3)
        set_urls = []

        total_urls = []

        while Limit > len(set_urls):
            #find more people
            elements = self.driver.find_elements_by_class_name("people")
            for element in elements:
                try:
                    attributeHere = element.find_element_by_class_name("result-image");
                    link = attributeHere.get_attribute("href")
                    if "profile" in link:
                        newPersonUrl = link.split("&auth")[0]
                        set_urls.append(newPersonUrl)
                        print(newPersonUrl)
                except:
                    pass

            #check if we have exceeded our search limit
            if len(set_urls) < 5:
                break

            print(set_urls)

            #go to next page
            pagination = self.driver.find_elements_by_class_name("pagination")
            for pages in pagination:
                click_next = pages.find_element_by_class_name("next")
                click_next.click()
                break

        total_urls += set_urls

        #get more
        main_window = self.driver.current_window_handle

        index_recursion = 0
        while Recursion > index_recursion:
            new_list = set_urls[:]
            print(set_urls)
            set_urls = []
            for each_url in new_list:
                self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
                time.sleep(2)
                self.driver.switch_to.window(main_window)
                self.driver.get(each_url)
                time.sleep(2)
                #do something recursive
                recommended = self.driver.find_elements_by_class_name("browse-map-photo")
                for person in recommended:
                    try:
                        personLink = person.get_attribute("href")
                        if "profile" in personLink:
                            set_urls.append(personLink)
                    except:
                        pass
                time.sleep(3)
                similar = self.driver.find_elements_by_class_name("discovery-photo")
                for person in similar:
                    try:
                        personLink = person.get_attribute("href")
                        if "profile" in personLink:
                            newPersonUrl = personLink.split("&auth")[0]

                            #check for duplicates
                            if not(newPersonUrl in set_urls) and not (newPersonUrl in total_urls):
                                set_urls.append(newPersonUrl)
                    except:
                        pass

                #get info of person
                if Database_save:
                    self.__get_profile_information(each_url, Term)
                #here get the info end

                time.sleep(2)
                self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
                time.sleep(2)
                self.driver.switch_to.window(main_window)
                print(len(set_urls))
            total_urls += set_urls
            index_recursion = index_recursion + 1
        return total_urls

    # Searches
    def search(self, term, Limit=20, Database_save=False, stDate = "0/0/0", edDate = "0/0/0"):
        # Search Terms
        # Google
        if self.site.name == "Google":
            searchBar = self.driver.find_element_by_id("lst-ib")
        # LinkedIn
        elif self.site.name == "LinkedIn":
            searchBar = self.driver.find_element_by_id('main-search-box')
        # Twitter
        elif self.site.name == "Twitter":
            searchBar = self.driver.find_element_by_id("search-query")
        else:
            raise siteError('Please select the correct site:  Types: [Google] [LinkedIn] [Twitter]')

        # All
        searchBar.clear()
        searchBar.send_keys(term)
        searchBar.send_keys(Keys.RETURN)

        # Sleep before sending info
        time.sleep(int(len(term) / 3))

        # Press enter
        searchBar.send_keys(Keys.RETURN)

        searchBar.send_keys(Keys.RETURN)
        # Google
        if self.site.name == "Google":
            return self.__google_search_query(Limit, stDate, edDate)
        # LinkedIn
        elif self.site.name == "LinkedIn":
            return self.__linkedin_search_query(term, Limit, Database_save);
        # Twitter
        elif self.site.name == "Twitter":
            pass
        else:
            raise siteError('Please select the correct site:  Types: [Google] [LinkedIn] [Twitter]')
    # Make a posting
    def posting(self, post):
        #Posting session

        # Google
        if self.site.name == "Google":
            self.__Posting_Google(post)
        # LinkedIn
        elif self.site.name == "LinkedIn":
            self.__Posting_Linkedin(post);
        # Twitter
        elif self.site.name == "Twitter":
            self.__Posting_Twitter(post)
        else:
            raise siteError('Please select the correct site:  Types: [Google] [LinkedIn] [Twitter]')

    # Close out the session
    def CloseSession(self):
        # Logout

        # Google
        if self.site.name == "Google":
            self.__Logout_Google()
        # LinkedIn
        elif self.site.name == "LinkedIn":
            self.__Logout_Linkedin();
        # Twitter
        elif self.site.name == "Twitter":
            self.__Logout_Twitter()
        else:
            raise siteError('Please select the correct site:  Types: [Google] [LinkedIn] [Twitter]')

        # sleep for 3 seconds
        time.sleep(3)

        # close the browser
        self.driver.close()