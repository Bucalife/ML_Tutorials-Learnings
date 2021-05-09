# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

def valid_phrase(txt):

    punt_c = 0

    for i in string.punctuation + ' ':
        if i in txt:
            punt_c += 1

    if punt_c >= 2:
        return False

    return True

#======================
# Data structure design
#======================

# Problem 1


class NewsStory(object):

    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def constructor(self):
        constructor = {'guid': self.guid, 'title': self.title, 'description': self.description,
                       'link': self.link, 'pubdate': self.pubdate}
        return constructor

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS


class PhraseTrigger(Trigger):

    def __init__(self, phrase):
        self.phrase = phrase

    def is_phrase_in(self, text):
        """
        if phrase in text:
        return True
        else:
        False
        """
        if not valid_phrase(self.phrase):
            return False

        for i in string.punctuation:
            text = text.replace(i, ' ')

        text_pure = ''.join([ch for ch in text.lower() if ch not in string.punctuation])
        text_pure = ' '.join(text_pure.split())
        phrase_pure = ''.join([l for l in self.phrase.lower() if l not in string.punctuation])
        phrase_in_txt = [1 for i in phrase_pure.split() if i in text_pure.split()]

        if len(phrase_in_txt) == len(phrase_pure.split()) and text_pure.find(phrase_pure) != -1:
            return True
        return False


# Problem 3
class TitleTrigger(PhraseTrigger):

    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())


# Problem 4
class DescriptionTrigger(PhraseTrigger):

    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS


# Problem 5
class TimeTrigger(Trigger):

    def __init__(self, date_time):
        self.time = datetime.strptime(date_time, '%d %b %Y %H:%M:%S').replace(tzinfo=pytz.timezone('EST'))


# Problem 6
class BeforeTrigger(TimeTrigger):

    def evaluate(self, story):
        return story.get_pubdate().replace(tzinfo=pytz.timezone('EST')) < self.time


class AfterTrigger(TimeTrigger):

    def evaluate(self, story):
        return story.get_pubdate().replace(tzinfo=pytz.timezone('EST')) > self.time

# COMPOSITE TRIGGERS


# Problem 7
class NotTrigger(Trigger):

    def __init__(self, trigger2):
        self.trigger2 = trigger2

    def evaluate(self, story):
        return not self.trigger2.evaluate(story)


# Problem 8
class AndTrigger(Trigger):

    def __init__(self, trig_1, trig_2):
        self.trig_1 = trig_1
        self.trig_2 = trig_2

    def evaluate(self, story):
        return self.trig_1.evaluate(story) and self.trig_2.evaluate(story)


# Problem 9
class OrTrigger(Trigger):

    def __init__(self, trig_1, trig_2):
        self.trig_1 = trig_1
        self.trig_2 = trig_2

    def evaluate(self, story):
        return self.trig_1.evaluate(story) or self.trig_2.evaluate(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    filtered_stories = [story for story in stories for trigger in triggerlist if trigger.evaluate(story)]
    return filtered_stories


#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    text_to_trig = {'TITLE': TitleTrigger, 'DESCRIPTION': DescriptionTrigger, 'AFTER': AfterTrigger,
                    'AND': AndTrigger, 'OR': OrTrigger}
    print(lines) # for now, print it so you see what it contains!

    result = [text_to_trig[text.split(',')[1]] for text in lines]
    return result


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("Uganda")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("https://news.google.com/rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

