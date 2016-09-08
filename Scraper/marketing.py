import bot
from bs4 import BeautifulSoup
import requests
import requests.exceptions
import random
from urllib.parse import urlsplit
from pymongo import MongoClient
from collections import deque
from threading import Thread
import re
import time
import calendar

# automated marketing app
class Marketing:
    def __init__(self):
        self.client = MongoClient("mongodb://127.0.0.1:27017");
        self.db = self.client.DataCollection
        pass

    def __email_crawler(self, new_url, web_name):
        epoch_timestamp = int(calendar.timegm(time.gmtime()))
        epoch_timestamp += 420;
        new_urls = deque(new_url)
        processed_urls = set()
        emails = set()

        while len(new_urls):
            url = new_urls.popleft()
            processed_urls.add(url)

            parts = urlsplit(url)
            base_url = "{0.scheme}://{0.netloc}".format(parts)
            path = url[:url.rfind('/') + 1] if '/' in parts.path else url

            print("Processing %s" % url)
            try:
                response = requests.get(url)
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                continue

            new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))

            remove_set = set()

            for set_email in new_emails:
                if ".png" in set_email:
                    remove_set.add(set_email)
                if ".jpg" in set_email:
                    remove_set.add(set_email)
                if ".jpeg" in set_email:
                    remove_set.add(set_email)
                if "email.com" in set_email:
                    remove_set.add(set_email)

            for email in remove_set:
                new_emails.remove(email)

            epoch_timestamp_new = int(calendar.timegm(time.gmtime()))

            if epoch_timestamp_new > epoch_timestamp:
                break

            emails.update(new_emails)
            print(emails)

            soup = BeautifulSoup(response.text)

            for anchor in soup.find_all("a"):
                link = anchor.attrs["href"] if "href" in anchor.attrs else ''
                if link.startswith('/'):
                    link = base_url + link
                elif not link.startswith('http'):
                    link = path + link
                if not link in new_urls and not link in processed_urls:
                    new_urls.append(link)

        database_emails = dict()

        database_emails['names'] = web_name
        database_emails['url'] = url
        database_emails['emails'] = list(emails)

        result = self.db.EmailScraper.insert_one(database_emails)
        print(result.inserted_id)


    def leads_text_file(self, text_file, addendum=[' marajuana in Colorado', ' cannabis dispensary']):
        the_file = open(text_file, "r")
        lines = the_file.read().split("\n");
        names_companies = set()
        for line in lines:
            names_companies.add(line)

        names_companies = sorted(names_companies)
        the_file.close()

        newBot = bot.BrowserInstance("email", "password", "phone", bot.Sites.Google)
        newBot.createUserInstance()

        for names in names_companies:
            add_choice = random.choice(addendum)
            new_urls = newBot.search(names+add_choice, 3, True)

            remove_list = []

            for url in new_urls:
                if "wikipedia" in url:
                    remove_list.append(url)
                if "facbook" in url:
                    remove_list.append(url)
                if "yelp" in url:
                    remove_list.append(url)
                if "twitter" in url:
                    remove_list.append(url)

            for removeit in remove_list:
                new_urls.remove(removeit)

            t = Thread(target=self.__email_crawler, args=(new_urls,names,))
            t.start()

        newBot.CloseSession()

    def linkedin_person_crawler(self, searchTerm, Limit_terms):
        newBot = bot.BrowserInstance("abhishekpratapa@gmail.com", "AlinaSchroeder#123", "5129831767", bot.Sites.LinkedIn)
        newBot.search(searchTerm, Limit_terms, True)
        newBot.CloseSession()
