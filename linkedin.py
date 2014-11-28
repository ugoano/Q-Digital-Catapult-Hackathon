from urllib import FancyURLopener, urlopen
from BeautifulSoup import BeautifulSoup
import logging
import traceback


class MyURLopener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13'


def find_profile(name):
    # search yahoo first
    search_term = "linkedin+" + name.replace(" ", "+")
    url = "http://search.yahoo.com/search?p=" + search_term
    print "Searching url " + url
    # yraw = MyURLopener().open(url)
    try:
        yraw = urlopen(url)
        ysoup = BeautifulSoup(yraw.read())
        yres = ysoup.find('div', attrs={'id': 'web'}).findAll('h3')
        profile_link = yres[0].find('a')['href']
        logging.info("Profile link: " + profile_link)

        skills = []
        lraw = MyURLopener().open(profile_link)
        lsoup = BeautifulSoup(lraw.read())
        logging.info("Gathering skills:")
        for res in lsoup.findAll('span', attrs={'class': 'endorse-item-name-text'}):
            logging.info(res.text)
            skills.append(res.text)
        return skills
    except:
        logging.error(traceback.format_exc())
        return None


# find_profile("Ugo Anomelechi")
# find_profile("Luke Dacey Digital Catapult")
# find_profile("Jonathan Chevallier Oxehealth")
