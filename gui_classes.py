# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 13:08:31 2019

@author: Omar
"""

try:
    import Tkinter as tk
    import ttk
except ImportError:  # Python 3
    import tkinter as tk
    from tkinter import ttk

import twitter
import server_code as sc

import numbers

try:
    import os
    os.chdir("D:\(PC)\Desktop\Coding\Python\Twitter prototype\github\Twitter-prototype")
except:
    pass

import webbrowser as browser

import io

from PIL import Image, ImageTk
import urllib.request

class CustomNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""
    notebook_id = 0
    __initialized = False

    def __init__(self, master, close_button = True, *args, **kwargs):
        CustomNotebook.notebook_id += 1
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        self.abbreviate = kwargs.get('abbreviate', False)

        try:
            kwargs.pop('abbreviate')
        except KeyError:
            pass

        if close_button == True:
            kwargs["style"] = "CustomNotebook"

        super().__init__(master, *args, **kwargs)

        self._active = None
        self.tabs = []
        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""
        element = self.identify(event.x, event.y)
        index = self.index("@%d,%d" % (event.x, event.y))

        if(self.abbreviate == True):
            self.abbreviateTabNames(index)

        if "close%d"%CustomNotebook.notebook_id in element:


            self.state(['pressed'])
            self._active = index

    def on_close_release(self, event):
        """Called when the button is released over the close button"""

        try:
            if not self.instate(['pressed']):
                return

            element =  self.identify(event.x, event.y)
            index = self.index("@%d,%d" % (event.x, event.y))

        except tk.TclError:
            pass

        if "close%d"%CustomNotebook.notebook_id in element and self._active == index:
            self.forget(index)
            self.tabs.pop(index)
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None


    def abbreviateTabNames(self, index):

        for i in range(0, len(self.tabs)):
            if(i == index):
                self.tab(i, text = self.tabs[i].tabName)
            else:
                self.tab(i, text = self.tabs[i].tabName[0:3] + '...')






    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            tk.PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            tk.PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            tk.PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )

        style.element_create("close%d" % CustomNotebook.notebook_id, "image", "img_close",
                            ("active", "pressed", "!disabled", "img_closepressed"),
                            ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("CustomNotebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("CustomNotebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                                    ("CustomNotebook.close%d"%CustomNotebook.notebook_id, {"side": "left", "sticky": ''}),
                                ]
                        })
                    ]
                })
            ]
        })
    ])

    def close(self, **kwargs):
        tabName = kwargs.get('tabName')
        index = kwargs.get('index')

        if tabName == None and index == None:
            pass

        elif tabName == None:
            try:
                self.forget(index)
                self.event_generate("<<NotebookTabClosed>>")
                del self.tabs[index]
            except:
                tk.messagebox.showinfo('Error', 'The tab is already closed!')
        elif index == None:
            try:
                for tab in self.tabs:

                    if tabName == tab.tabName:
                        index = self.tabs.index(tab)

                self.forget(index)
                self.event_generate("<<NotebookTabClosed>>")
                del self.tabs[index]
            except:
                tk.messagebox.showinfo('Error', 'The tab is already closed!')


class TweetsDisplay():

    def __init__(self, master, text = "", close_button = False, width = 200, height = 200, x = 0, y = 0, *args, **kwargs):
        self.labelFrame = tk.LabelFrame(master, text = text, width = width, height = height)
        self.labelFrame.place(x = x, y = y)
        self.width, self.height = width, height
        self.name = text
        self.update("")

    def update(self, data, **kwargs):
        self.show_tweet(data, 0)

    def show_tweet(self, data, index, bg = "white"):
        # This should point towards some random example tweet for now.
        tweet = sc.tweet1_data

        # Getting the profile pic.
        with urllib.request.urlopen(tweet.get("user").get("profile_image_url_https")) as url:
            profile_image_file = io.BytesIO(url.read())
        profile_image_open = Image.open(profile_image_file)
        profile_image = ImageTk.PhotoImage(profile_image_open)

        # This label holds everything in the tweet.
        tweet_label = tk.Label(self.labelFrame, bg = bg)

        # The pofile pic to the left - and nothing under it.
        left_label = tk.Label(tweet_label, bg = bg)
        img_label = tk.Label(left_label, image=profile_image)
        img_label.image = profile_image
        img_label.bind('<Double-Button-1>', lambda event : browser.open("https://twitter.com/{}".format(tweet.get("user").get("screen_name"))))
        img_label.pack(side = "top")
        left_label.pack(side = "left", fill = 'y')

        # Display name, along with verified etc.
        name_label = tk.Label(tweet_label, bg = bg)
        tk.Label(name_label, text = tweet.get("user").get("name"), font = 'bold', bg = bg).pack(side = "left")
        if tweet.get("user").get("verified"):
            verified_image_open = Image.open("images/verified.png").resize((15, 15), Image.ANTIALIAS)
            verified_image = ImageTk.PhotoImage(verified_image_open)
            verified_image_label = tk.Label(name_label, image = verified_image, bg = bg)
            verified_image_label.image = verified_image
            verified_image_label.pack(side = "left")
        tk.Label(name_label, text = "@" + tweet.get("user").get("screen_name"), fg = 'grey35', bg = bg).pack(side = "left")
        name_label.pack(side = "top", fill = 'x')

        # The tweet text label.
        tk.Label(tweet_label, text = tweet.get("text"), wraplength = self.labelFrame["width"] - left_label["width"], justify = "left", bg = bg).pack(side = "top", fill = 'x')

        # The retweet and favorite count.
        stats_bar = tk.Label(tweet_label, bg = bg)
        retweet_image_open = Image.open("images/retweet.jpg").resize((30, 30), Image.ANTIALIAS)
        retweet_image = ImageTk.PhotoImage(retweet_image_open)
        retweet_image_label = tk.Label(stats_bar, image = retweet_image, bg = bg)
        retweet_image_label.image = retweet_image
        retweet_image_label.pack(side = "left")
        tk.Label(stats_bar, text = "{}     ".format(tweet.get("retweet_count")), bg = bg).pack(side = "left")
        like_image_open = Image.open("images/like.png").resize((30, 30), Image.ANTIALIAS)
        like_image = ImageTk.PhotoImage(like_image_open)
        like_image_label = tk.Label(stats_bar, image = like_image, bg = bg)
        like_image_label.image = like_image
        like_image_label.pack(side = "left")
        tk.Label(stats_bar, text = "{}     ".format(tweet.get("favorite_count")), bg = bg).pack(side = "left")
        open_tweet_image_open = Image.open("images/link-new-tab.png").resize((20, 20), Image.ANTIALIAS)
        open_tweet_image = ImageTk.PhotoImage(open_tweet_image_open)
        open_tweet_image_label = tk.Button(stats_bar, image = open_tweet_image, command = lambda : browser.open("https://twitter.com/{}/status/{}".format(tweet.get("user").get("screen_name"), tweet.get("id"))), bg = bg)
        open_tweet_image_label.image = open_tweet_image
        open_tweet_image_label.pack(side = "left")
        stats_bar.pack(side = "top", fill = 'x')

        tweet_label.pack(side = "top")




class FramedNotebook(CustomNotebook):

    def __init__(self, master, text = "", close_button = False, width = 200, height = 200, x = 0, y = 0, *args, **kwargs):
        self.labelFrame = tk.LabelFrame(master, text = text)
        self.labelFrame.place(x = x, y = y)
        self.width, self.height = width, height
        self.name = text
        super().__init__(self.labelFrame, close_button = close_button, width = width, height = height, *args, **kwargs)
        self.printed = []
        self.tabies = []
        self.tree = None


    def update(self, data, **kwargs):

        isCommon = kwargs.get("common", False)
        if isCommon:
            if self.tree:
                self.tree.delete(*self.tree.get_children())
                FramedNotebook.populateTreeview(data, self.tree)
            else:
                for child in self.labelFrame.winfo_children():
                    child.destroy()
                self.frame = tk.Frame(self.labelFrame, width = self.width, height = self.height)
                self.frame.grid_propagate(0)
                self.createTreeview(self.frame, data)
                self.frame.pack()


        else:
            if data[2] in self.printed:
                return
            else:
                self.printed.append(data[2])

                if data[1] == "":
                    tab = Tab(self, "%s" % data[0])
                else:
                    tab = Tab(self, "%s, %s" % (data[1], data[0]))

                self.tabies.append(tab)

                self.createTreeview(tab.frame, data[4])

    def createTreeview(self, frame, data):
        width = self.width
        fields = ['name', 'tweet_volume', 'url']
        self.tree = ttk.Treeview(columns=fields, displaycolumns=fields[:2], show=[])
        self.tree.grid(column=0, row=0, sticky='nsew', in_=frame)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        self.tree.column('name', width=int(width*0.75))
        self.tree.column('tweet_volume', width=int(width*0.23))

        self.tree.bind('<Double-Button-1>', lambda event : FramedNotebook.openLink(event.widget, fields))

        FramedNotebook.populateTreeview(data, self.tree)

    # Opens the browser page of the clicked item in a treeview.
    # w here refers to the widget of the event, which here is the treeview element.
    @staticmethod
    def openLink(w, fields):
        values = w.item(w.selection()[0], values=None)
        # The values are converted to a dictionary to automatically locate the url.
        valuesdict = dict(zip(fields, values))
        browser.open(valuesdict['url'])

    @staticmethod
    def populateTreeview(data, treeview):
        for entry in data:
            values = entry['name'], entry['tweet_volume'] or 'No data', entry['url']
            treeview.insert('', 'end', values=values)

class Entrybox:

    xoffset = 300

    def __init__(self, master, *listeners, **kwargs):

        text = kwargs.get('text', "")
        x, y = kwargs.get('x', 0), kwargs.get('y', 0)
        width, height = kwargs.get('width', 200), kwargs.get('height', 140)
        self.labelFrame = tk.LabelFrame(master, text = text)
        self.frame = tk.Frame(self.labelFrame, width = width, height = height)
        self.frame.pack()
        self.labelFrame.place(x = x + self.xoffset, y = y)


        self.listbox = tk.Listbox(self.labelFrame, width = 30, height = 5)
        self.listbox.place(relx = 0.5, anchor = tk.CENTER, y = 50)

        self.entries = []
        self.common_data = []

        self.removeButton = tk.Button(self.labelFrame, text = "Remove entry",
                                      command = lambda: self.removeEntry(listeners))
        self.removeButton.place(x = 10, y = 100)


        self.runButton = tk.Button(self.labelFrame, text = "Begin analysis",
                                   command = lambda: self.generateData(listeners))
        self.runButton.place(x = 100, y = 100)


    def getItems(self):
        items = []
        for i in self.listbox.curselection():
            items.append(self.listbox.get(i))
        return items

    def addEntry(self, data):
        if data[2] in list(map(lambda x: self.entries[x][2], [i for i in range(0, len(self.entries))])):
            pass
        else:
            entry = data
            entry.append("Not_loaded")
            if data[1] == "":
                self.listbox.insert(tk.END, "%s" % entry[0])
                self.entries.append(entry)
            else:
                self.listbox.insert(tk.END, "%s, %s" % (entry[1], entry[0]))
                self.entries.append(entry)


    def removeEntry(self, listeners):
        indecies = []
        for i in self.listbox.curselection():
            indecies.append(i)

        for i in indecies:

            if self.entries[i][3] == "Loaded":
                answer = tk.messagebox.askquestion('Warning', 'If you remove this entry, all loaded data for %s will be lost. Are you sure?'
                                                   %self.listbox.get(i))
                if answer == 'yes':
                    listeners[0].close(tabName = self.listbox.get(i))
                    listeners[1].close(tabName = self.listbox.get(i))
                    listeners[0].printed.pop(i)
                    listeners[1].printed.pop(i)
                    self.listbox.delete(i)
                    self.entries.pop(i)

                else:
                    pass
            else:
                self.listbox.delete(i)
                self.entries.pop(i)

            if len(self.entries) == 0:
                listeners[2].listbox.delete(0,tk.END)
                listeners[3].listbox.delete(0,tk.END)


    def generateData(self, listeners):
        sc.prepare_data(self.entries)
        data = []
        for i in range(0, len(self.entries)):
            listeners[0].update(self.entries[i][0:4] + [self.entries[i][4][0]])
            listeners[1].update(self.entries[i][0:4] + [self.entries[i][4][1]])
            data.append(self.entries[i][4])

        self.common_data = sc.get_common_data(data)
        try:
            listeners[2].listbox.delete(0,tk.END)
            listeners[3].listbox.delete(0,tk.END)
        except:
            pass

        listeners[2].update(self.common_data[0], common = True)
        listeners[3].update(self.common_data[1], common = True)






class Tab:

    xoffset, yoffset, linespaceing = 50, 25, 25

    def __init__ (self, notebook, tabName):
        self.tabName = tabName
        for tab in notebook.tabs:
            if self.tabName == tab.tabName:
                Tab.showAlreadyOpenError(notebook, self.tabName)
                return
        else:
            self.notebook = notebook
            self.frame = tk.Frame(notebook)
            self.notebook.add(self.frame, text=self.tabName)
            notebook.tabs.append(self)
            self.index = self.notebook.tabs.index(self)
            if(self.notebook.abbreviate == True):
                if(self.index == notebook.index(notebook.select())):
                    pass
                else:
                    notebook.tab(self.index, text = self.tabName[0:3] + '...')


    @staticmethod
    def showAlreadyOpenError(notebook, tabName):
        tk.messagebox.showinfo('Error %d'%notebook.notebook_id, 'The tab "%s" is already open!' % tabName)
        return 1



class AnalysisTab(Tab):

    number_of_tabs = 0
    yoffset, linespaceing = 10, 25
    hashtagWidth, hashtagHeight = 250, 230
    keywordWidth, keywordHeight = 250, 230
    tweetWidth, tweetHeight = 300, 0

    def __init__(self, notebook, data):
        AnalysisTab.number_of_tabs += 1
        self.tabName = "Analysis %d" % AnalysisTab.number_of_tabs
        super().__init__(notebook, self.tabName)

        tk.Label(self.frame, text="Country:").place(x = self.xoffset, y = self.yoffset)
        self.countries = ttk.Combobox(self.frame, width=20, state="readonly")

        self.countries['values'] = ("Select...")
        for key, value in data.items():
            self.countries['values'] += (key, )
        self.countries.current(0)
        self.countries.place(x = self.xoffset, y = self.yoffset + self.linespaceing*1)
        self.countries.bind("<<ComboboxSelected>>", lambda _ : self.selectCity(data))

        tk.Label(self.frame, text="City:").place(x = self.xoffset + 150, y = self.yoffset)
        self.cities = ttk.Combobox(self.frame, width=20, state="disabled")
        self.cities['values'] = ("Select...")
        self.cities.current(0)
        self.cities.place(x = self.xoffset + 150, y = self.yoffset + self.linespaceing*1)
        self.cities.bind("<<ComboboxSelected>>", lambda _ : self.enableButton())

        self.add_button = tk.Button(self.frame, text="Add location", state = "disabled",
                                    command = lambda:  self.updateListbox(data))

        self.add_button.place(x = self.xoffset + 300, y = self.yoffset + self.linespaceing*1)



        self.hashtags = FramedNotebook(self.frame, text = "Trending hashtags",
                                      x = self.xoffset, y = self.yoffset + self.linespaceing*2,
                                      width = AnalysisTab.hashtagWidth, height = AnalysisTab.hashtagHeight,
                                      abbreviate = True)
        self.hashtags.pack()

        self.keywords = FramedNotebook(self.frame, text = "Trending keywords",
                                      x = self.xoffset, y = self.yoffset + AnalysisTab.hashtagHeight+ self.linespaceing*4,
                                      width = AnalysisTab.keywordWidth, height = AnalysisTab.keywordHeight,
                                      abbreviate = True)
        self.keywords.pack()

        self.common_hashtags = FramedNotebook(self.frame, text = "Intersecting hashtags",
                                      x = self.xoffset + 300, y = self.yoffset + self.linespaceing*2,
                                      width = AnalysisTab.hashtagWidth, height = AnalysisTab.hashtagHeight,
                                      abbreviate = True)
        self.common_hashtags.pack()

        self.common_keywords = FramedNotebook(self.frame, text = "Intersecting keywords",
                                      x = self.xoffset + 300, y = self.yoffset + AnalysisTab.hashtagHeight+ self.linespaceing*4,
                                      width = AnalysisTab.keywordWidth, height = AnalysisTab.keywordHeight,
                                      abbreviate = True)
        self.common_keywords.pack()

        self.chosenCountries = Entrybox(self.frame, self.hashtags, self.keywords, self.common_hashtags, self.common_keywords,
                                        x = 450, y = self.yoffset, text = "Selected countries",
                                        )

        self.tweets_box = TweetsDisplay(self.frame, text = "Example tweets", x = self.xoffset + 600, y = self.yoffset + self.linespaceing*7,
                                         width = AnalysisTab.tweetWidth, height = AnalysisTab.tweetHeight, abbreviate = True)



    def updateListbox(self, data):
        city = self.cities.get()
        if city == "(None)":
            data = [self.countries.get(),
                    "",
                    data[self.countries.get()]['woeid']
                    ]
        else:
            data = [self.countries.get(),
                    self.cities.get(),
                    data[self.countries.get()]['cities'][self.cities.get()]['woeid']
                    ]

        self.chosenCountries.addEntry(data)

    def selectCity(self, data):
        country = self.countries.get()
        if country == "Select...":
            self.cities['values'] = ("Select...")
            self.cities.current(0)
            self.cities.config(state = "disabled")

        else:
            self.cities['values'] = ("Select...", "(None)")
            self.cities.current(0)
            self.cities.config(state = "readonly")

            for key, value in data[country]['cities'].items():
                self.cities['values'] += (key, )

    def enableButton(self):
        if self.cities.get() == "(--select--)":
            self.add_button.config(state = "disabled")
        else:
            self.add_button.config(state = "normal")


class AdvancedTab(Tab):
    def __init__ (self, notebook, data):
        self.tabName = "Advanced"
        super().__init__(notebook, self.tabName)
        self.dataLabels = []
        self.titleLabels = []
        self.entries = []


        for i in range(0, 4):
            self.titleLabels.append(tk.Label(self.frame, text = data[i][0]))
            self.entries.append(tk.Entry(self.frame, width = 50))
            self.dataLabels.append(tk.Label(self.frame, text = data[i][1]))

        for i in range(0, 4):
            self.titleLabels[i].place(x = self.xoffset, y = self.yoffset + self.linespaceing*i)
            self.entries[i].place(x = self.xoffset + 130, y = self.yoffset + self.linespaceing*i)
            self.dataLabels[i].place(x = self.xoffset + 450, y = self.yoffset + self.linespaceing*i)

        self.apply = tk.Button(self.frame, text="Apply",
               command= lambda: self.setOAUTH(self.dataLabels, self.entries))
        self.apply.place(x = self.xoffset + 200, y = self.yoffset + self.linespaceing*4)



        self.reset = tk.Button(self.frame, text="Restore defaults",
                       command= lambda: self.resetOAUTH(self.dataLabels, data)
                       )
        self.reset.place(x = self.xoffset + 100, y = self.yoffset + self.linespaceing*4)


        self.run = tk.Button(self.frame, text="Run",
                     command = lambda: self.authenticate(self.dataLabels, self.connectionStatus))
        self.run.place(x = self.xoffset + 260, y = self.yoffset + self.linespaceing*4)


        self.connectionStatus = tk.Label(self.frame, text = "Connection statsus: disconnected")
        self.connectionStatus.place(x = self.xoffset + 200, y = self.yoffset + self.linespaceing*5)

    @staticmethod
    def resetOAUTH(labels, data):
        for i in range(0, 4):
            labels[i].config(text = data[i][1])

    @staticmethod
    def setOAUTH(labels, entries):
        for i in range(0, 4):
            if entries[i].get() != "":
                labels[i].config(text = entries[i].get())
            else:
                pass

    @staticmethod
    def authenticate(labels, resultLabel):

        data = []
        for i in range(0,4):
            data.append(labels[i].cget("text"))

        auth = twitter.oauth.OAuth(data[2],
                                   data[3],
                                   data[0],
                                   data[1])

        twitter_api = twitter.Twitter(auth=auth)


        try:
            world_trends = twitter_api.trends.place(_id=1)
            resultLabel.config(text = "Connection status: connection success!")

        except:
            resultLabel.config(text = "Connection status: connection failure...")


