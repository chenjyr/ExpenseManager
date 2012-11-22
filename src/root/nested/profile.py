"""
Created on Jun 4, 2012

@author: chenjyr

Profile Class keeps track of profiles (can make a new one, save, load)
A profile is stored as a text file (with a .profile extension)
When a profile is loaded, the file is parsed through 
to find all the parameters of the profile, and displayed in the GUI
"""

import datetime

class Profile:
    
    def __init__(self, string):
        self.name = string
        self.items = []
        self.categories = []
        self.expenseRange = ""
        
        try:
            self.profile = open(self.name + ".profile", "r")
        except IOError:
            self.profile = open(self.name + ".profile", "w")
            self.profile.close()
            self.profile = open(self.name + ".profile", "r")
        
        self.populateProfile()    
        
    # Get profile name
    def getName(self):
        return self.name
    
    # Set profile name
    def setName(self, name):
        self.name = name
    
    # Get receipts
    def getItems(self):
        return self.items
    
    # Add receipt
    def addItem(self, item):
        self.items.append(item)
    
    # Remove receipt
    def removeItem(self, item):
        self.items.remove(item)
    
    # Edit receipt
    def editItem(self, oldItem, newItem):
        self.items[self.items.index(oldItem)] = newItem
        
    # Add category to choose from
    def addCategory(self, category):
        self.categories.append(category)
    
    # Remove category to choose from
    def removeCategory(self, category):
        del self.categories[self.categories.index(category)]
    
    # Get categories
    def getCategories(self):
        return self.categories

    # Set total expense range
    def setExpenseRange(self, month):
        self.expenseRange = month
        
    # Get total expense range
    def getExpenseRange(self):
        return self.expenseRange
    
    # Get total expense
    def getExpense(self):
        totalExpense = 0.0
        curMonth = str(datetime.date.today()).split("-")[1]
        curYear = str(datetime.date.today()).split("-")[0]
        eYear, eMonth = int(curYear), int(curMonth)
        expenseInterval= int(self.getExpenseRange())
        while expenseInterval > 1:
            if eMonth == 0:
                eYear -= 1
                eMonth = 12
            eMonth -= 1
            expenseInterval -= 1
        
        for item in self.items:
            year,month,day = item[0].split("/")
            del day
            if int(year) > eYear or (int(year) == eYear and int(month) >= eMonth):
                totalExpense += float(item[3])
        return str(totalExpense)
    
    # Get date,expense of items for the current month
    def getEachDateExpense(self):
        eItem = []
        curMonth = str(datetime.date.today()).split("-")[1]
        curYear = str(datetime.date.today()).split("-")[0]
        eYear, eMonth = int(curYear), int(curMonth)
        expenseInterval= int(self.getExpenseRange())
        while expenseInterval > 1:
            if eMonth == 0:
                eYear -= 1
                eMonth = 12
            eMonth -= 1
            expenseInterval -= 1
        
        # Set up dates in the month
        mDict = {"01":31,"02":28,"03":31,"04":30,"05":31,"06":30,\
                 "07":31,"08":31,"09":30,"10":31,"11":30,"12":31}
        for day in xrange(1,mDict[curMonth]+1):
            eItem.append(["/".join(["2012",str(int(curMonth)),str(day)]),0.0])
        
        for item in self.items:
            year,month,day = item[0].split("/")
            del day
            if int(year) == eYear and int(month) == eMonth:
                if item[0] in [x[0] for x in eItem]:                    
                    tmp = eItem[[x[0] for x in eItem].index(item[0])][1] + float(item[3])
                    eItem[[x[0] for x in eItem].index(item[0])][1] = tmp
                else:
                    eItem.append([item[0],float(item[3])])
        return eItem
        
    # Save profile
    def saveProfile(self):
        self.profile.close()
        self.profile = open(self.name + ".profile", "w")
        self.profile.write("<name>\n" + self.name + "\n</name>\n")
        # Save expense range
        self.profile.write("<expense_range>\n" + self.expenseRange + "\n</expense_range>\n")
        # Save categories
        self.profile.write("<categories>\n")
        for category in self.categories:
            self.profile.write(category + "\n")
        self.profile.write("</categories>\n")
        # Save receipts
        self.profile.write("<items>\n")
        for item in self.items:
            self.profile.write(",".join(item)+"\n")
        self.profile.write("</items>\n")
        
    # Populate profile with file
    def populateProfile(self):
        s_items = False
        e_range = False
        cat = False
        for line in self.profile:
            if line.find("<expense_range>") != -1: e_range = True
            elif line.find("</expense_range>") != -1: e_range = False
            elif line.find("<categories>") != -1: cat = True
            elif line.find("</categories>") != -1: cat = False
            elif line.find("<items>") != -1: s_items = True
            elif line.find("</items>") != -1: s_items = False
            elif e_range == True: self.expenseRange = line.strip()
            elif cat == True: self.categories.append(line.strip())
            elif s_items == True: self.items.append(line.strip().split(","))
        if self.expenseRange == "": self.setExpenseRange("1")
    
    
    
    
    
    