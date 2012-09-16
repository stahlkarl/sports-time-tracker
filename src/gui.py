try:
    import wx
except ImportError:
    raise ImportError, "Could not find the wxPython module"

import abstraction_layer as AL
import datetime

class StartPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        #Create widgets:
        self.cBtn = wx.Button(self, label='Avsluta')
        self.addBtn = wx.Button(self, label='Ny Elev')
        self.stopBtn = wx.Button(self, label='Stoppa Elev')
        self.exportBtn = wx.Button(self, label='Spara Till Excel')
        self.clearBtn = wx.Button(self, label='Rensa Databas')

        self.exportDial = wx.MessageDialog(None, 'Databasen Sparad', 'Info', wx.OK)
        self.cDial = wx.MessageDialog(None, 'Vill du avsluta?', 'Info', wx.YES_NO)
        self.clearDial = wx.MessageDialog(None, 'Vill du RADERA HELA DATABASEN?', 'VARNING', wx.YES_NO)

        #Outer sizer containing all four buttons:
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.addBtn, 1, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.stopBtn, 1, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.exportBtn, 1, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.clearBtn, 1, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.cBtn, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(self.sizer)

###########################################################################

class AddingPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        #Create widgets:
        self.nameFldF = wx.TextCtrl(self, -1)
        self.nameFldS = wx.TextCtrl(self, -1)
        self.nameFldT = wx.TextCtrl(self, -1)

        self.classFldF = wx.TextCtrl(self, -1)
        self.classFldS = wx.TextCtrl(self, -1)
        self.classFldT = wx.TextCtrl(self, -1)

        self.courseMnu = wx.ComboBox(self, choices=("Bana 1", "Bana 2", "Bana 3"), style=wx.CB_READONLY)

        self.saveBtn = wx.Button(self, label='Spara')
        self.backBtn = wx.Button(self, label='Tillbaka')

        self.chkBoxS = wx.CheckBox(self)
        self.chkBoxT = wx.CheckBox(self)

        self.saveDial = wx.MessageDialog(None, 'Sparat', 'Info', wx.OK)

        self.fields = [self.nameFldS, self.nameFldT, self.classFldS, self.classFldT]

        #Default text field vals:
        self.resetFields()

        #Sizer for the first set of input fields:
        self.hSizerF = wx.BoxSizer(wx.HORIZONTAL)
        self.hSizerF.Add(self.nameFldF, 1, wx.ALL, 2)
        self.hSizerF.Add(self.classFldF, 1, wx.ALL, 2)
        self.hSizerF.Add(self.courseMnu, 1, wx.ALL, 2)

        #Sizer for the second set of input fields:
        self.hSizerS = wx.BoxSizer(wx.HORIZONTAL)
        self.hSizerS.Add(self.chkBoxS, 0, wx.ALL, 2)
        self.hSizerS.Add(self.nameFldS, 1, wx.ALL, 2)
        self.hSizerS.Add(self.classFldS, 1, wx.ALL, 2)

        #Sizer for the third set of input fields:
        self.hSizerT = wx.BoxSizer(wx.HORIZONTAL)
        self.hSizerT.Add(self.chkBoxT, 0, wx.ALL, 2)
        self.hSizerT.Add(self.nameFldT, 1, wx.ALL, 2)
        self.hSizerT.Add(self.classFldT, 1, wx.ALL, 2)

        #Sizer for the buttons:
        self.hSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.hSizer2.Add(self.saveBtn, 1, wx.EXPAND |wx.ALL, 5)
        self.hSizer2.Add(self.backBtn, 1, wx.EXPAND | wx.ALL, 5)

        #Outer sizer:
        self.vSizer = wx.BoxSizer(wx.VERTICAL)
        self.vSizer.Add(self.hSizerF, 1, wx.EXPAND | wx.ALL, 5)
        self.vSizer.Add(self.hSizerS, 1, wx.EXPAND | wx.ALL, 5)
        self.vSizer.Add(self.hSizerT, 1, wx.EXPAND | wx.ALL, 5)
        self.vSizer.Add(self.hSizer2, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(self.vSizer)

    def resetFields(self):
        self.nameFldF.ChangeValue("Namn")
        self.classFldF.ChangeValue("Klass")
        self.courseMnu.SetSelection(0)
        for field in self.fields:
            field.Clear()

    def focusField(self):
        self.nameFldF.SetFocus()
        self.nameFldF.SetSelection(-1, -1)

###########################################################################

class StoppingPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        #Create widgets:
        self.usrLst = wx.ListBox(self) #Append from DB using: usrLst.Append(text)
        self.stopBtn = wx.Button(self, label='Stoppa Denna Elev')
        self.backBtn = wx.Button(self, label='Tillbaka')
        self.timeLst = wx.ListBox(self)

        self.errDial = wx.MessageDialog(None, 'Ingen vald elev!', 'Info', wx.OK)

        #Vertical sizer for the buttons:
        self.vSizer = wx.BoxSizer(wx.VERTICAL)
        self.vSizer.Add(self.stopBtn, 1, wx.EXPAND | wx.ALL, 5)
        self.vSizer.Add(self.backBtn, 1, wx.EXPAND | wx.ALL, 5)

        #Outer sizer:
        self.hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.hSizer.Add(self.usrLst, 1, wx.EXPAND)
        self.hSizer.Add(self.vSizer, 1, wx.EXPAND)
        self.hSizer.Add(self.timeLst, 1, wx.EXPAND)

        self.SetSizer(self.hSizer)

###########################################################################

class Frame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
        self.parent = parent

        #Initiate the db handler module:
        self.al = AL.AL()

        #Panels init:
        self.startPnl = StartPanel(self) #Start Menu Panel
        self.addPnl = AddingPanel(self) #Add Runner Panel
        self.stopPnl = StoppingPanel(self) #Stop Runner Panel

        #Only show the Start Menu Panel in the beginning:
        self.addPnl.Hide()
        self.stopPnl.Hide()

        #Window properties:
        self.SetSize((540, 350))
        self.SetBackgroundColour((200, 200, 200, 255))

        #Main window sizer:
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.Add(self.startPnl, 1, wx.EXPAND)
        self.mainSizer.Add(self.addPnl, 1, wx.EXPAND)
        self.mainSizer.Add(self.stopPnl, 1, wx.EXPAND)

        self.SetSizer(self.mainSizer)

        #Bind the correct events to the correct buttons:
        self.binds()

        #Show and center the window:
        self.Center()
        self.Show(True)

    def binds(self):
        #Main menu binds:
        self.startPnl.cBtn.Bind(wx.EVT_BUTTON, self.onClose)
        self.startPnl.addBtn.Bind(wx.EVT_BUTTON, self.onAddSwitch)
        self.startPnl.stopBtn.Bind(wx.EVT_BUTTON, self.onStopSwitch)
        self.startPnl.exportBtn.Bind(wx.EVT_BUTTON, self.onExport)
        self.startPnl.clearBtn.Bind(wx.EVT_BUTTON, self.onClearDB)

        #Add menu binds:
        self.addPnl.saveBtn.Bind(wx.EVT_BUTTON, self.onSave)
        self.addPnl.backBtn.Bind(wx.EVT_BUTTON, self.onStartSwitch)

        #Stop menu binds:
        self.stopPnl.stopBtn.Bind(wx.EVT_BUTTON, self.onStop)
        self.stopPnl.backBtn.Bind(wx.EVT_BUTTON, self.onStartSwitch)

    def onClose(self, event): #Close the window
        if self.startPnl.cDial.ShowModal() == wx.ID_YES: #Check for confirmation
            self.Close(True)
        else:
            pass

    def onAddSwitch(self, event): #Switch panels -> Add Runner Panel
        self.startPnl.Hide()
        self.addPnl.Show()
        self.addPnl.focusField()
        self.Layout()

    def onStopSwitch(self, event): #Switch panels -> Stop Runner Panel
        self.startPnl.Hide()
        self.appendRunners()
        self.updateFinished()
        self.stopPnl.Show()
        self.Layout()

    def onStartSwitch(self, event): #Switch panels -> Start Menu Panel
        if self.stopPnl.IsShown():
            self.stopPnl.Hide()
        else:
            self.addPnl.Hide()
            self.addPnl.resetFields()

        self.startPnl.Show()
        self.Layout()

    def onExport(self, event): #Simply export db to excel document
        self.al.export_db()
        self.startPnl.exportDial.ShowModal()

    def onClearDB(self, event): #Clear entire DB
        if self.startPnl.clearDial.ShowModal() == wx.ID_YES:
            self.al.remove_all_runners_from_db()
        else:
            pass

    def onSave(self, event): #Save the runner in the db
        name = self.addPnl.nameFldF.GetValue()
        school_class = self.addPnl.classFldF.GetValue()
        course = self.addPnl.courseMnu.GetSelection()

        if self.addPnl.chkBoxS.IsChecked() or self.addPnl.chkBoxT.IsChecked():
            gid = self.al.next_group_id()

            #If both check boxes are checked:
            if self.addPnl.chkBoxS.IsChecked() and self.addPnl.chkBoxT.IsChecked():

                #Get values: (TODO: Make a fucking method of this crap)
                nameS = self.addPnl.nameFldS.GetValue()
                school_classS = self.addPnl.classFldS.GetValue()

                #Get moar values: (TODO: Make a fucking method of this crap)
                nameT = self.addPnl.nameFldT.GetValue()
                school_classT = self.addPnl.classFldT.GetValue()

                #Save runners to DB:
                self.al.start_runner(name, school_class, course, gid)
                self.al.start_runner(nameS, school_classS, course, gid)
                self.al.start_runner(nameT, school_classT, course, gid)

            #If the first check box is checked but not the second:
            elif self.addPnl.chkBoxS.IsChecked():

                #Get values: (TODO: Make a fucking method of this crap)
                nameS = self.addPnl.nameFldS.GetValue()
                school_classS = self.addPnl.classFldS.GetValue()

                #Save runners to DB:
                self.al.start_runner(name, school_class, course, gid)
                self.al.start_runner(nameS, school_classS, course, gid)

            #If the second check box is checked but not the first:
            elif self.addPnl.chkBoxT.IsChecked():

                #Get values: (TODO: Make a fucking method of this crap)
                nameT = self.addPnl.nameFldT.GetValue()
                school_classT = self.addPnl.classFldT.GetValue()

                #Save runners to DB:
                self.al.start_runner(name, school_class, course, gid)
                self.al.start_runner(nameT, school_classT, course, gid)

        else: #Do this if no boxes are checked
            self.al.start_runner(name, school_class, course, 0)

        self.addPnl.saveDial.ShowModal()

        self.addPnl.resetFields()

    def onStop(self, event): #Stop the selectet runner
        try:
            temp = self.stopPnl.usrLst.GetString(self.stopPnl.usrLst.GetSelection()).split("  --  ")
            if temp[0] == "Grupp":
                self.al.stop_group(int(temp[1]))
                self.appendRunners()
            else:    
                temp = temp[0].split("-")
                self.al.stop_runner(int(temp[1]))
                self.appendRunners()
        except:
            self.stopPnl.errDial.ShowModal()
        self.updateFinished()
        self.Layout()

    def appendRunners(self): #Refresh the listbox (to the left) in the Stop Runner Panel with current runners
        runners = self.al.running_runners()
        self.stopPnl.usrLst.Clear()
        cgid0 = 0
        for runner in runners:
            if runner["group_id"] == 0:
                self.stopPnl.usrLst.Append(("-" + str(runner["id"]) + "  --  " + runner["name"] + " - " + runner["class"]))
            else:
                cgid = runner["group_id"]
                if cgid != cgid0:
                    cgid0 = cgid
                    self.stopPnl.usrLst.Append(("Grupp" + "  --  " + str(cgid)))
                self.stopPnl.usrLst.Append(("    -" + str(runner["id"]) + "  --  " + runner["name"] + " - " + runner["class"]))
                

    def updateFinished(self): #Refresh the listbox (to the right) in the Stop Runner Panel with recently finished runner
        runners = self.al.last_finished_runners(20)
        self.stopPnl.timeLst.Clear()
        self.stopPnl.timeLst.Append("SENASTE TIDER:")
        for runner in runners:
            xTime = str(datetime.timedelta(seconds=(runner['stop_time'] - runner['start_time'])))
            self.stopPnl.timeLst.Append((runner["name"] + " - " + runner["class"] + " - " + xTime))

###########################################################################

if __name__ == "__main__":
    app = wx.App()
    frame = Frame(None, -1, "Orientering - TG")
    app.MainLoop()
