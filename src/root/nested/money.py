""" 
Created on May 20, 2012

@author: chenjyr

EXPENSE MANAGER

This program allows the user to manage his spending
by adding and removing receipts from the system,
and viewing the spending in various forms.

Features implemented:
    Manage different profiles (New/Save/Save as/Load)
    Add/Remove/Edit receipts
    Display statistics
        - Total spent for the last <amount> mounts
    
Features to be implemented:
    Plot graphs
        - Money spent by <interval> over the last <interval>, by category (or no)
        - Projected spending

        - Optional budget feature
        - Again, by category, time, etc.
    Compose own categories list to choose from

Program is made to be very flexible. 
User can choose to include extra information, 
or choose to omit certain information.
"""

PROFILE_NAME = "Jackie"

import pygtk
pygtk.require('2.0')
import gtk
from profile import *
import random
from glob import *
import gobject
import matplotlib.pyplot as plt


""" GUI Class displays the saved information
    in the loaded profile class in a graphical user interface
"""

class GUI:

    def on_window_destroy(self, widget, data=None):
        gtk.main_quit()
     
    def __init__(self):
            
        self.profile = Profile(PROFILE_NAME)
        self.recentSaved = True
        
        # Create Window
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_border_width(1)
        window.set_default_size(770, 500)
        window.set_title("Expense Manager")
        window.set_position(gtk.WIN_POS_CENTER)

        # Fixed Container
        fixed = gtk.Fixed()
        window.add(fixed)

        # To hold menu->File items
        fileMenu = gtk.Menu()
        
        # Menu - File->New Profile
        fileMenu_newProfile = gtk.MenuItem("New Profile")
        fileMenu.append(fileMenu_newProfile)
        fileMenu_newProfile.connect("activate", self.new_profile)
        fileMenu_newProfile.show()
        
        #Menu - File->Load Profile
        fileMenu_openProfile = gtk.MenuItem("Load Profile")
        fileMenu.append(fileMenu_openProfile)
        fileMenu_openProfile.connect("activate", self.load_profile)
        fileMenu_openProfile.show()
        
        #Menu - File->Save Profile
        fileMenu_saveProfile = gtk.MenuItem("Save Profile")
        fileMenu.append(fileMenu_saveProfile)
        fileMenu_saveProfile.connect("activate", self.save_profile)
        fileMenu_saveProfile.show()
        
        #Menu - File->Save Profile As
        fileMenu_saveProfileAs = gtk.MenuItem("Save Profile As..")
        fileMenu.append(fileMenu_saveProfileAs)
        fileMenu_saveProfileAs.connect("activate", self.save_profile_as)
        fileMenu_saveProfileAs.show()
        
        #Menu - File->Exit
        fileMenu_exit = gtk.MenuItem("Exit")
        fileMenu.append(fileMenu_exit)
        fileMenu_exit.connect("activate", self.exit_program)
        fileMenu_exit.show()
        
        #Menu - File
        root_fileMenu = gtk.MenuItem("File")
        root_fileMenu.show()
        root_fileMenu.set_submenu(fileMenu)
        
        # To hold Menu->Edit items
        editMenu = gtk.Menu()
        
        # Menu - Edit->Expense Range
        editMenu_expenseRange = gtk.MenuItem("Expense Range")
        editMenu.append(editMenu_expenseRange)
        editMenu_expenseRange.connect("activate", self.expense_range)
        editMenu_expenseRange.show()
        
        # Menu - Edit->Categories
        editMenu_categories = gtk.MenuItem("Categories")
        editMenu.append(editMenu_categories)
        editMenu_categories.connect("activate", self.categories)
        editMenu_categories.show()
        
        # Menu - Edit
        root_editMenu = gtk.MenuItem("Edit")
        root_editMenu.show()
        root_editMenu.set_submenu(editMenu)
                
        # To hold Menu->Graph items
        viewMenu = gtk.Menu()
        
        # Menu - View->Graph  
        viewMenu_graph = gtk.MenuItem("Graph")
        viewMenu.append(viewMenu_graph)
        viewMenu_graph.connect("activate", self.plot_graph)
        viewMenu_graph.show()
              
        # Menu - View
        root_viewMenu = gtk.MenuItem("View")
        root_viewMenu.show()
        root_viewMenu.set_submenu(viewMenu)
        
        # Menu bar
        menu_bar = gtk.MenuBar()
        menu_bar.append(root_fileMenu)
        menu_bar.append(root_editMenu)
        menu_bar.append(root_viewMenu)
        menu_bar.set_size_request(770, 20)
        fixed.put(menu_bar, 0, 0)
        menu_bar.show()

        # Button - Add
        button_add = gtk.Button("Add")
        button_add.set_size_request(100, 25)
        button_add.connect("clicked", self.add_item, "Added!")
        fixed.put(button_add, 130, 460)
        button_add.show()
        
        # Button - Remove
        button_remove = gtk.Button("Remove")
        button_remove.set_size_request(100, 25)
        button_remove.connect("clicked", self.remove_item)
        fixed.put(button_remove, 250, 460)
        button_remove.show()
        
        # Button - Exit
        button_exit = gtk.Button("Exit")
        button_exit.set_size_request(100, 25)
        button_exit.connect("clicked", self.exit_program)
        fixed.put(button_exit, 620, 460)
        button_exit.show()
        
        # Scrollable treeview for placing receipts
        self.liststore = gtk.ListStore(str, str, str, str, str)
        self.treeview = gtk.TreeView(self.liststore)
        # Item Column
        column_date = gtk.TreeViewColumn('Date')
        cell_icon = gtk.CellRendererPixbuf()
        cell_icon.set_property('cell-background', 'light blue')
        column_date.pack_start(cell_icon, False)
        column_date.set_attributes(cell_icon, stock_id = 0)
        cell_date = gtk.CellRendererText()
        cell_date.set_property('cell-background', 'white')
        column_date.pack_start(cell_date, True)
        column_date.set_attributes(cell_date, text = 1)
        # Description Column
        column_description = gtk.TreeViewColumn('Description')
        cell_description = gtk.CellRendererText()
        cell_description.set_property('cell-background', 'white')
        column_description.pack_start(cell_description, True)
        column_description.set_attributes(cell_description, text = 2)
        # Category Column
        column_category = gtk.TreeViewColumn("Category")
        cell_category = gtk.CellRendererText()
        cell_category.set_property("cell-background", "white")
        column_category.pack_start(cell_category, True)
        column_category.set_attributes(cell_category, text = 3)
        # Price Column
        column_price = gtk.TreeViewColumn("Price")
        cell_price = gtk.CellRendererText()
        cell_price.set_property("cell-background", "white")
        column_price.pack_start(cell_price, True)
        column_price.set_attributes(cell_price, text = 4)      
        #Set up treeview
        self.treeview.append_column(column_date)
        self.treeview.append_column(column_description)
        self.treeview.append_column(column_category)
        self.treeview.append_column(column_price)
        self.treeview.set_search_column(0)
        self.treeview.set_reorderable(True)
        self.treeview.set_size_request(530, 390)
        self.treeview.connect("row-activated", self.edit_item)
        # Embed treeview in scrollable window
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.add(self.treeview)
        fixed.put(sw, 10, 60)
        
        # Display profile currently in use
        self.profile_label = gtk.Label("Profile: " + self.profile.getName())
        fixed.put(self.profile_label, 20, 30)
        
        aLabel = gtk.Label()
        aLabel.set_markup('<span color="#002200" size="large"> Total expense for the last </span>')
        bLabel = gtk.Label()
        bLabel.set_markup('<span color="#002200" size="large"> month(s): </span>')
        self.expenseDaysLabel = gtk.Label()
        self.expenseDaysLabel.set_markup('<span color="#AA0000" size="x-large">' + \
                                         self.profile.expenseRange +  '</span>')
        self.priceLabel = gtk.Label()
        self.priceLabel.set_markup('<span color="#009A00" size="x-large">$' + \
                                   self.profile.getExpense() + '</span>')
        fixed.put(aLabel, 560, 70)
        fixed.put(bLabel, 595, 100)
        fixed.put(self.expenseDaysLabel, 565, 98)
        fixed.put(self.priceLabel, 675, 98)
                
        window.show_all()
        window.set_keep_above(True)
        window.set_keep_above(False)

        self.display_items()
        #self.liststore.reorder(range(len(self.liststore))[::-1])
        
    # Print a string when a menu item is selected
    def menuitem_response(self, widget, string):
        print "%s" % string
    
    def exit_program(self, widget, string=""):
        if self.recentSaved == False and string == "":
            self.exitWindow = gtk.Window()
            self.exitWindow.set_border_width(1)
            self.exitWindow.set_default_size(215, 250)
            self.exitWindow.set_title("Exit")
            self.exitWindow.set_position(gtk.WIN_POS_CENTER)
            exitFixed = gtk.Fixed()
            self.exitWindow.add(exitFixed)
            label = gtk.Label("Save before exiting?")
            exitFixed.put(label, 50, 25)
            saveButton = gtk.Button("Save and exit")
            exitButton = gtk.Button("Exit without saving")
            cancelButton = gtk.Button("Cancel")
            saveButton.set_size_request(125, 25)
            exitButton.set_size_request(125, 25)
            cancelButton.set_size_request(125, 25)
            exitFixed.put(saveButton, 45, 60)
            exitFixed.put(exitButton, 45, 95)
            exitFixed.put(cancelButton, 45, 130)
            saveButton.connect("clicked", self.exit_program, "SAVE")
            exitButton.connect("clicked", self.exit_program, "EXIT")
            cancelButton.connect("clicked", self.exit_program, "CANCEL")
            self.exitWindow.show_all()
        elif string == "SAVE":
            self.save_profile()
            gtk.main_quit()
        elif string == "CANCEL":
            self.exitWindow.destroy()
        else:
            gtk.main_quit()
    
    # Prompt user to enter new profile name
    def new_profile(self, widget, string=""):
        if string == "":
            try:
                if self.newProfile_window:
                    pass
            except AttributeError:
                self.newProfile_window = gtk.Window()
                self.newProfile_window.set_border_width(1)
                self.newProfile_window.set_default_size(350, 150)
                self.newProfile_window.set_title("New Profile")
                self.newProfile_window.set_position(gtk.WIN_POS_CENTER)
            finally:
                newProfile_fixed = gtk.Fixed()
                self.newProfile_window.add(newProfile_fixed)
                self.newProfile_entry = gtk.Entry(max = 50)
                self.newProfile_entry.connect("activate", self.new_profile, "CONFIRM")
                newProfile_fixed.put(self.newProfile_entry, 90, 60)
                newProfile_label = gtk.Label("Enter profile name:")
                newProfile_fixed.put(newProfile_label, 110, 30)
                newProfile_buttonConfirm = gtk.Button("Confirm")
                newProfile_buttonConfirm.connect("clicked", self.new_profile, "CONFIRM")
                newProfile_fixed.put(newProfile_buttonConfirm, 200, 110)
                newProfile_buttonCancel = gtk.Button("Cancel ")
                newProfile_buttonCancel.connect("clicked", self.new_profile, "CANCEL")
                newProfile_fixed.put(newProfile_buttonCancel, 270, 110)
                self.newProfile_window.show_all()
        elif string == "CONFIRM":
            try:
                # If profile already exists, notify the user and do not overwrite profile
                exists = open(self.newProfile_entry.get_text() + ".profile", "r")
                exists.close()  
                self.newProfileCreated_window = gtk.Window()
                self.newProfileCreated_window.set_border_width(1)
                self.newProfileCreated_window.set_default_size(200, 100)
                self.newProfileCreated_window.set_title("New Profile")
                self.newProfileCreated_window.set_position(gtk.WIN_POS_CENTER)
                newProfileCreated_fixed = gtk.Fixed()
                self.newProfileCreated_window.add(newProfileCreated_fixed)
                newProfileCreated_button = gtk.Button("Ok")
                newProfileCreated_button.connect("clicked", self.new_profile, "UNSUCCESSFUL")
                newProfileCreated_fixed.put(newProfileCreated_button, 90, 50)
                newProfileCreated_label = gtk.Label("Profile Already Exists!")
                newProfileCreated_fixed.put(newProfileCreated_label, 25, 20)
                self.newProfileCreated_window.show_all()
            except IOError:
                # If profile does not exist, then create new profile with .profile extension
                self.profile = Profile(self.newProfile_entry.get_text())
                self.profile_label.set_label("Profile: " + self.profile.getName())
                self.newProfileCreated_window = gtk.Window()
                self.newProfileCreated_window.set_border_width(1)
                self.newProfileCreated_window.set_default_size(200, 100)
                self.newProfileCreated_window.set_title("New Profile")
                self.newProfileCreated_window.set_position(gtk.WIN_POS_CENTER)
                newProfileCreated_fixed = gtk.Fixed()
                self.newProfileCreated_window.add(newProfileCreated_fixed)
                newProfileCreated_button = gtk.Button("Ok")
                newProfileCreated_button.connect("clicked", self.new_profile, "SUCCESSFUL")
                newProfileCreated_fixed.put(newProfileCreated_button, 90, 50)
                newProfileCreated_label = gtk.Label("Profile Created!")
                newProfileCreated_fixed.put(newProfileCreated_label, 50, 20)
                self.newProfileCreated_window.show_all()
        elif string == "CANCEL":
            self.newProfile_window.destroy()
        elif string == "SUCCESSFUL":
            self.newProfileCreated_window.destroy()
            self.newProfile_window.destroy()
            self.display_items()
            self.recentSaved = True
        elif string == "UNSUCCESSFUL":
            self.newProfileCreated_window.destroy()

    # Load existing profile from system
    def load_profile(self, widget):
        self.loadProfile_window = gtk.Window()
        self.loadProfile_window.set_border_width(1)
        self.loadProfile_window.set_default_size(330,200)
        self.loadProfile_window.set_title("Load Profile")
        self.loadProfile_window.set_position(gtk.WIN_POS_CENTER)
        loadFixed = gtk.Fixed()
        self.loadProfile_window.add(loadFixed)
        
        # Scrollable treeview for displaying existing profiles
        self.loadList = gtk.ListStore(str, str)
        self.loadTreeview = gtk.TreeView(self.loadList)
        # Item Column
        column_item = gtk.TreeViewColumn()
        cell_icon = gtk.CellRendererPixbuf()
        cell_icon.set_property('cell-background', 'light blue')
        column_item.pack_start(cell_icon, False)
        column_item.set_attributes(cell_icon, stock_id = 0)
        cell_item = gtk.CellRendererText()
        cell_item.set_property('cell-background', 'white')
        column_item.pack_start(cell_item, True)
        column_item.set_attributes(cell_item, text = 1)
        #Set up treeview
        self.loadTreeview.append_column(column_item)
        self.loadTreeview.set_search_column(0)
        self.loadTreeview.set_size_request(300, 120)
        # Embed treeview in scrollable window
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.add(self.loadTreeview)
        loadFixed.put(sw, 15, 20)
        
        for f in glob("*.profile"):
            self.loadList.append([gtk.STOCK_FILE, str(f).split(".")[0]])
        
        confirmButton = gtk.Button("Confirm")
        confirmButton.connect("clicked", self.confirmLoad)
        loadFixed.put(confirmButton, 100, 160)
        cancelButton = gtk.Button("Cancel")
        cancelButton.connect("clicked", self.cancelLoad)
        loadFixed.put(cancelButton, 190, 160)
        
        
        self.loadProfile_window.show_all()
    
    def confirmLoad(self, widget):
        result = self.loadTreeview.get_selection().get_selected()
        model, tmp = result
        profileName = str(model.get_value(tmp,1))
        self.profile = Profile(profileName)
        self.profile_label.set_label("Profile: " + self.profile.getName())
        self.display_items()
        self.priceLabel.set_markup('<span color="#009A00" size="x-large">$' + \
                       self.profile.getExpense() + '</span>')
        self.expenseDaysLabel.set_markup('<span color="#AA0000" size="x-large">' + \
                                         self.profile.expenseRange +  '</span>')
        self.loadProfile_window.destroy()
        self.recentSaved = True

    def cancelLoad(self, widget):
        self.loadProfile_window.destroy()
        
    # Save profile
    def save_profile(self, widget=None):
        tmp = gtk.Window()
        tmp.set_border_width(1)
        tmp.set_default_size(200, 100)
        tmp.set_title("Saving")
        tmp.set_position(gtk.WIN_POS_CENTER)
        tmpfixed = gtk.Fixed()
        tmp.add(tmpfixed)
        tmplabel = gtk.Label("Saving...")
        tmpfixed.put(tmplabel, 70, 40)
        tmp.show_all()
        self.profile.saveProfile()
        tmp.destroy()
        self.recentSaved = True
    
    # Save profile as new name
    def save_profile_as(self, widget):
        try:
            if self.saveAs_window:
                pass
        except AttributeError:
            self.saveAs_window = gtk.Window()
            self.saveAs_window.set_border_width(1)
            self.saveAs_window.set_default_size(350, 150)
            self.saveAs_window.set_title("Save Profile as..")
            self.saveAs_window.set_position(gtk.WIN_POS_CENTER)
        finally:
            saveProfile_fixed = gtk.Fixed()
            self.saveAs_window.add(saveProfile_fixed)
            self.saveAs_entry = gtk.Entry(max = 50)
            self.saveAs_entry.connect("activate", self.saveAs_confirmButton)
            saveProfile_fixed.put(self.saveAs_entry, 90, 60)
            saveProfile_label = gtk.Label("Enter profile name:")
            saveProfile_fixed.put(saveProfile_label, 110, 30)
            saveProfile_buttonConfirm = gtk.Button("Confirm")
            saveProfile_buttonConfirm.connect("clicked", self.saveAs_confirmButton)
            saveProfile_fixed.put(saveProfile_buttonConfirm, 200, 110)
            saveProfile_buttonCancel = gtk.Button("Cancel ")
            saveProfile_buttonCancel.connect("clicked", self.saveAs_cancelButton)
            saveProfile_fixed.put(saveProfile_buttonCancel, 270, 110)
            self.saveAs_window.show_all()
    
    # When user presses confirm button to save as
    def saveAs_confirmButton(self, widget):
        try:
            # If profile already exists, notify the user and do not overwrite profile
            exists = open(self.saveAs_entry.get_text() + ".profile", "r")
            exists.close()  
            self.saveAsExists_window = gtk.Window()
            self.saveAsExists_window.set_border_width(1)
            self.saveAsExists_window.set_default_size(200, 100)
            self.saveAsExists_window.set_title("Save Profile as..")
            self.saveAsExists_window.set_position(gtk.WIN_POS_CENTER)
            saveAsExists_fixed = gtk.Fixed()
            self.saveAsExists_window.add(saveAsExists_fixed)
            saveAsExists_button = gtk.Button("Ok")
            saveAsExists_button.connect("clicked", self.saveAs_sou, "")
            saveAsExists_fixed.put(saveAsExists_button, 90, 50)
            saveAsExists_label = gtk.Label("Profile Already Exists!")
            saveAsExists_fixed.put(saveAsExists_label, 25, 20)
            self.saveAsExists_window.show_all()
        except IOError:
            # If profile does not exist, then save existing profile as specified name
            self.profile.setName(self.saveAs_entry.get_text())
            self.save_profile()
            self.profile_label.set_label("Profile: " + self.profile.getName())
            self.saveAsCreated_window = gtk.Window()
            self.saveAsCreated_window.set_border_width(1)
            self.saveAsCreated_window.set_default_size(200, 100)
            self.saveAsCreated_window.set_title("Save Profile as..")
            self.saveAsCreated_window.set_position(gtk.WIN_POS_CENTER)
            saveAsCreated_fixed = gtk.Fixed()
            self.saveAsCreated_window.add(saveAsCreated_fixed)
            saveAsCreated_button = gtk.Button("Ok")
            saveAsCreated_button.connect("clicked", self.saveAs_sou, "SUCCESSFUL")
            saveAsCreated_fixed.put(saveAsCreated_button, 90, 50)
            saveAsCreated_label = gtk.Label("Profile Saved!")
            saveAsCreated_fixed.put(saveAsCreated_label, 50, 20)
            self.saveAsCreated_window.show_all()
        
    # Notify user of (un)successful creation of profile
    def saveAs_sou(self, widget, string):
        if string == "SUCCESSFUL":
            self.saveAsCreated_window.destroy()
            self.saveAs_window.destroy()
            self.display_items()
            self.recentSaved = True
        else:
            self.saveAsExists_window.destroy()

    # Exit out of creating new profile
    def saveAs_cancelButton(self, widget):
        self.saveAs_window.destroy()
    
    # Add receipt
    def add_item(self, widget, string):
        self.addWindow = gtk.Window()
        self.addWindow.set_border_width(1)
        self.addWindow.set_default_size(300, 390)
        self.addWindow.set_title("Add Receipt")
        self.addWindow.set_position(gtk.WIN_POS_CENTER)
        addFixed = gtk.Fixed()
        self.addWindow.add(addFixed)
        
        priceLabel = gtk.Label("Price:")
        descriptionLabel = gtk.Label("Description:")
        categoryLabel = gtk.Label("Category:")
        
        self.priceEntry = gtk.Entry(max = 20)
        self.descriptionEntry = gtk.Entry(max = 100)

        categories = self.profile.getCategories()
        categoriesList = gtk.ListStore(gobject.TYPE_STRING)
        for category in categories: categoriesList.append([category])
        self.categoryEntry = gtk.ComboBoxEntry(categoriesList)
        self.categoryEntry.set_size_request(160,25)
        self.categoryEntry.set_active(0)
        self.calendarEntry = gtk.Calendar()

        self.priceEntry.connect("activate", self.confirm_add_item)
        self.descriptionEntry.connect("activate", self.confirm_add_item)
        
        self.errorLabel = gtk.Label()
        
        addFixed.put(priceLabel, 15, 40)
        addFixed.put(self.priceEntry, 100, 35)
        addFixed.put(descriptionLabel, 15, 75)
        addFixed.put(self.descriptionEntry, 100, 70)
        addFixed.put(categoryLabel, 15, 110)
        addFixed.put(self.categoryEntry, 100, 105)
        addFixed.put(self.calendarEntry, 35, 155)
        addFixed.put(self.errorLabel, 105, 10)
        
        confirmButton = gtk.Button("Confirm")
        cancelButton = gtk.Button("Cancel")
        confirmButton.connect("clicked", self.confirm_add_item)
        cancelButton.connect("clicked", self.cancel_add_item)
        addFixed.put(confirmButton, 80, 340)
        addFixed.put(cancelButton, 170, 340)
        
        self.addWindow.show_all()
    
    def confirm_add_item(self, widget):   
        try:
            year, month, day = str(self.calendarEntry.get_date()).strip("()").replace(", ", "/").split("/")
            corrected_month = str(int(month) + 1)
            date = "/".join([year,corrected_month,day])
            description = self.descriptionEntry.get_text()
            category = self.categoryEntry.get_active_text()
            price = self.priceEntry.get_text()
            float(price)
            item = [date, description, category, price]
            self.profile.addItem(item)
            self.liststore.insert(0,[gtk.STOCK_FILE] + item)
            self.treeview.set_cursor(0)
            self.addWindow.destroy()
            self.priceLabel.set_markup('<span color="#009A00" size="x-large">$' + \
                                   self.profile.getExpense() + '</span>')
            self.recentSaved = False
            print self.recentSaved
            
        except ValueError:
            self.errorLabel.set_markup('<span color="red">Invalid Price</span>')

    def cancel_add_item(self, widget):
        self.addWindow.destroy()
        
    # Remove receipt
    def remove_item(self, widget):
        result = self.treeview.get_selection().get_selected()
        try:
            model, tmp = result
            item = [model.get_value(tmp,1),model.get_value(tmp,2),model.get_value(tmp,3),model.get_value(tmp,4)]
            self.profile.removeItem(item)
            num, garbage = self.treeview.get_cursor()
            del garbage
            if int(str(num).strip("(,)")) > 0: self.treeview.set_cursor(int(str(num).strip("(,)"))-1)
            else: self.treeview.set_cursor(1)
            model.remove(tmp)
            self.priceLabel.set_markup('<span color="#009A00" size="x-large">$' + \
                                       self.profile.getExpense() + '</span>')     
            self.recentSaved = False
                   
        except TypeError:
            print "No selection made"
        
    def edit_item(self, it, path, userdata):
        self.editWindow = gtk.Window()
        self.editWindow.set_border_width(1)
        self.editWindow.set_default_size(300, 390)
        self.editWindow.set_title("Edit Receipt")
        self.editWindow.set_position(gtk.WIN_POS_CENTER)
        editFixed = gtk.Fixed()
        self.editWindow.add(editFixed)
        
        priceLabel = gtk.Label("Price:")
        descriptionLabel = gtk.Label("Description:")
        categoryLabel = gtk.Label("Category:")
        
        self.priceEntry = gtk.Entry(max = 20)
        self.descriptionEntry = gtk.Entry(max = 100)

        categories = self.profile.getCategories()
        categoriesList = gtk.ListStore(gobject.TYPE_STRING)
        for category in categories: categoriesList.append([category])
        self.categoryEntry = gtk.ComboBoxEntry(categoriesList)
        self.categoryEntry.set_size_request(160,25)
        self.categoryEntry.set_active(0)
        self.calendarEntry = gtk.Calendar()

        self.priceEntry.connect("activate", self.confirm_edit_item)
        self.descriptionEntry.connect("activate", self.confirm_edit_item)
        
        self.errorLabel = gtk.Label()
        
        editFixed.put(priceLabel, 15, 40)
        editFixed.put(self.priceEntry, 100, 35)
        editFixed.put(descriptionLabel, 15, 75)
        editFixed.put(self.descriptionEntry, 100, 70)
        editFixed.put(categoryLabel, 15, 110)
        editFixed.put(self.categoryEntry, 100, 105)
        editFixed.put(self.calendarEntry, 35, 155)
        editFixed.put(self.errorLabel, 105, 10)
        
        confirmButton = gtk.Button("Confirm")
        cancelButton = gtk.Button("Cancel")
        confirmButton.connect("clicked", self.confirm_edit_item)
        cancelButton.connect("clicked", self.cancel_edit_item)
        editFixed.put(confirmButton, 80, 340)
        editFixed.put(cancelButton, 170, 340)
        
        model, tmp = self.treeview.get_selection().get_selected()
 
        date = model.get_value(tmp,1).split("/")
        self.calendarEntry.select_month(int(date[1]) - 1, int(date[0]))
        self.calendarEntry.select_day(int(date[2]))
        self.descriptionEntry.set_text(model.get_value(tmp, 2))
        self.categoryEntry.set_active(self.profile.getCategories().index(model.get_value(tmp, 3)))
        self.priceEntry.set_text(model.get_value(tmp, 4))

        year, month, day = str(self.calendarEntry.get_date()).strip("()").replace(", ", "/").split("/")
        corrected_month = str(int(month) + 1)
        date = "/".join([year,corrected_month,day])        
        description = self.descriptionEntry.get_text()
        category = self.categoryEntry.get_active_text()
        price = self.priceEntry.get_text()
        self.oldItem = [date, description, category, price]
        
        self.editWindow.show_all()
        
    def confirm_edit_item(self, widget):
        try:
            year, month, day = str(self.calendarEntry.get_date()).strip("()").replace(", ", "/").split("/")
            corrected_month = str(int(month) + 1)
            date = "/".join([year,corrected_month,day])
            description = self.descriptionEntry.get_text()
            category = self.categoryEntry.get_active_text()
            price = self.priceEntry.get_text()
            float(price)
            newItem = [date, description, category, price]

            self.profile.editItem(self.oldItem, newItem)
            model, tmp = self.treeview.get_selection().get_selected()
            model.set_value(tmp, 1, date)
            model.set_value(tmp, 2, description)
            model.set_value(tmp, 3, category)
            model.set_value(tmp, 4, price)

            self.editWindow.destroy()
            self.priceLabel.set_markup('<span color="#009A00" size="x-large">$' + \
                                   self.profile.getExpense() + '</span>')
            self.recentSaved = False
            
        except ValueError:
            self.errorLabel.set_markup('<span color="red">Invalid Price</span>')
    
    def cancel_edit_item(self, widget):
        self.editWindow.destroy()
    
    # Method to display the receipts as a list
    def display_items(self):
        self.liststore.clear()
        for item in self.profile.getItems():
            self.liststore.insert(0,[gtk.STOCK_FILE, item[0], item[1], item[2], item[3]])

    def expense_range(self, widget):
        self.erWindow = gtk.Window()
        self.erWindow.set_border_width(1)
        self.erWindow.set_default_size(200, 110)
        self.erWindow.set_title("Expense Range")
        self.erWindow.set_position(gtk.WIN_POS_CENTER)
        erFixed = gtk.Fixed()
        self.erWindow.add(erFixed)
        
        adj = gtk.Adjustment(float(self.profile.getExpenseRange()), 1.0, 999.0, 1.0, 1.0, 0.0)
        self.erSpinner = gtk.SpinButton(adj, 1.0, 0)
        self.erSpinner.set_wrap(True)
        erFixed.put(self.erSpinner, 50, 25)
        
        label = gtk.Label("month(s)")
        erFixed.put(label, 130, 30)
        confirmButton = gtk.Button("Confirm")
        cancelButton = gtk.Button("Cancel")
        confirmButton.connect("clicked", self.confirm_expense_range)
        cancelButton.connect("clicked", self.cancel_expense_range)
        erFixed.put(confirmButton, 40, 70)
        erFixed.put(cancelButton, 115, 70)
        
        self.erWindow.show_all()
        
    def confirm_expense_range(self, widget):
        self.profile.setExpenseRange(str(int(self.erSpinner.get_value())))
        self.erWindow.destroy()
        self.expenseDaysLabel.set_markup('<span color="#AA0000" size="x-large">' + \
                                         self.profile.expenseRange +  '</span>')
        self.priceLabel.set_markup('<span color="#009A00" size="x-large">$' + \
                                   self.profile.getExpense() + '</span>')
        self.recentSaved = False
    
    def cancel_expense_range(self, widget):
        self.erWindow.destroy()
        
    def categories(self, widget):
        self.catWindow = gtk.Window()
        self.catWindow.set_border_width(1)
        self.catWindow.set_default_size(300, 220)
        self.catWindow.set_title("Categories")
        self.catWindow.set_position(gtk.WIN_POS_CENTER)
        catFixed = gtk.Fixed()
        self.catWindow.add(catFixed)

        # Scrollable treeview for displaying existing profiles
        self.catList = gtk.ListStore(str, str)
        self.catTreeView = gtk.TreeView(self.catList)
        # Item Column
        column_cat = gtk.TreeViewColumn()
        cell_icon = gtk.CellRendererPixbuf()
        cell_icon.set_property('cell-background', 'light blue')
        column_cat.pack_start(cell_icon, False)
        column_cat.set_attributes(cell_icon, stock_id = 0)
        cell_cat = gtk.CellRendererText()
        cell_cat.set_property('cell-background', 'white')
        column_cat.pack_start(cell_cat, True)
        column_cat.set_attributes(cell_cat, text = 1)
        #Set up treeview
        self.catTreeView.append_column(column_cat)
        self.catTreeView.set_search_column(0)
        self.catTreeView.set_size_request(260, 120)
        # Embed treeview in scrollable window
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.add(self.catTreeView)
        catFixed.put(sw, 15, 20)
        
        for f in self.profile.getCategories():
            self.catList.append([gtk.STOCK_FILE, f])
        
        addButton = gtk.Button("Add   ")
        addButton.connect("clicked", self.add_categories)
        catFixed.put(addButton, 45, 180)
        removeButton = gtk.Button("Remove")
        removeButton.connect("clicked", self.remove_categories)
        catFixed.put(removeButton, 115, 180)
        doneButton = gtk.Button("Done  ")
        doneButton.connect("clicked", self.done_categories)
        catFixed.put(doneButton, 195, 180)

        self.addEntry = gtk.Entry(max = 100)
        self.addEntry.set_size_request(260, 20)
        self.addEntry.connect("activate", self.add_categories)
        catFixed.put(self.addEntry, 15, 150)
        
        self.catWindow.show_all()

    def add_categories(self, widget):
        if self.addEntry.get_text() != "":
            self.profile.addCategory(self.addEntry.get_text())
            self.catList.append([gtk.STOCK_FILE, self.addEntry.get_text()])
            self.addEntry.set_text("")
            self.recentSaved = False
        
    def remove_categories(self, widget):
        result = self.catTreeView.get_selection().get_selected()
        try:
            model, tmp = result
            self.profile.removeCategory(model.get_value(tmp, 1))
            model.remove(tmp)
            self.recentSaved = False
        except TypeError:
            print "No selection Made"

    def done_categories(self, widget):
        self.catWindow.destroy()
        
    def plot_graph(self, widget):
        items = self.profile.getEachDateExpense()
        dates = []
        expenses = []
        for item in items:
            dates.append(item[0])
            expenses.append(item[1])

        plt.bar(range(len(expenses)), expenses, align='center', facecolor='green', edgecolor='black')
        plt.xticks(range(len(dates)), dates, size='small', rotation=45)
        plt.show()

        
    def on_press(self, event):
        print 'you pressed', event.button, event.xdata, event.ydata
        event.canvas.figure.clear()
        # select new curves to plot, in this example [1,2,3] [0,0,0]
        event.canvas.figure.gca().plot([1,2,3],[0,0,0], 'ro-')
        event.canvas.figure.gca().grid()
        event.canvas.figure.gca().legend()
        event.canvas.draw()

    
if __name__ == "__main__":
    editor = GUI()
    gtk.main()