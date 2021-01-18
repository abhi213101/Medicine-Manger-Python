from tkinter import *
from tkinter import messagebox
from datetime import *
from datetime import datetime
from tkcalendar import Calendar
from DBMS import *
from AutocomplteEntry import *
import datetime as dt
import reportlab
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER, landscape, LEGAL, portrait, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
import os


class GradientFrame(Canvas):
    '''A gradient frame which uses a canvas to draw the background'''
    def __init__(self, parent, color1="red", color2="black", **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self._color1 = color1
        self._color2 = color2
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        '''Draw the gradient'''
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        limit = width
        (r1,g1,b1) = self.winfo_rgb(self._color1)
        (r2,g2,b2) = self.winfo_rgb(self._color2)
        r_ratio = float(r2-r1) / limit
        g_ratio = float(g2-g1) / limit
        b_ratio = float(b2-b1) / limit

        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr,ng,nb)
            self.create_line(i,0,i,height, tags=("gradient",), fill=color)
        self.lower("gradient")

MainScreen = Tk()
MainScreen.geometry("1000x640+200+10")
MainScreen.title("ESIS BALANCE BOOK")

def LoginPage():
    # Creating Frame for login page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label    
    pageFrame.create_text(50, 50, text="Welcome!", fill="blue", anchor='nw', font=('Calibri', 30, 'underline', 'bold'))
    
    # Entry Field Username
    pageFrame.create_text(70, 193, text="Username :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    username = Entry(pageFrame)
    username.place(x=200, y=200)

    # Entry Field Password
    pageFrame.create_text(70, 243, text="Password :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    password = Entry(pageFrame, show="*")
    password.place(x=200, y=250)

    def login():
        if (len(username.get()) == 0):
            messagebox.showerror(title='Error', message='Missing Username!!')
            username.delete(0, 'end')
            username.focus()
            return

        elif (len(password.get()) == 0):
            messagebox.showerror(title='Error', message='Missing Password!!')
            password.delete(0, 'end')
            password.focus()
            return

        else:
            output = LoginDB(username.get(), password.get())
            
            if(output == "Invalid username"):
                messagebox.showerror(title='Error', message='Invalid Username!!')
                username.delete(0, 'end')
                username.focus()
                return

            elif(output == "Invalid password"):
                messagebox.showerror(title='Error', message='Invalid Password!!')
                password.delete(0, 'end')
                password.focus()
                return

            else:
                messagebox.showinfo(title='Done',message='You have logged in succesfully!')
                pageFrame.destroy()
                HomePage()

    # Button login
    Button(pageFrame, text="Login", width=15, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [login()]).place(x=198, y=300)

    # Button sign up
    pageFrame.create_text(49, 403, text="New User ?", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    Button(pageFrame, text="Sign Up", width=15, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), SignupPage()]).place(x=198,y=400)

    # Button password reset
    pageFrame.create_text(29, 453, text="Forgot Password ?", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    Button(pageFrame, text="Check Password", width=15, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), passwordResetPage()]).place(x=198, y=450)

def SignupPage():
    # Creating Frame for login page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label
    pageFrame.create_text(50, 60, text="Register", fill="blue", anchor='nw', font=('Calibri', 30, 'underline'))

    # Entry Field Username
    pageFrame.create_text(50, 150, text="Username :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    username = Entry(pageFrame)
    username.place(x=270, y=150)

    # Entry Field Dispensary
    pageFrame.create_text(50, 200, text="Dispensary :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    dispensary = Entry(pageFrame)
    dispensary.place(x=270, y=200)

    # Entry Field Password
    pageFrame.create_text(50, 250, text="Password :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    password1 = Entry(pageFrame, show="*")
    password1.place(x=270, y=250)
    pageFrame.create_text(50, 300, text="Confirm Password :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    password2 = Entry(pageFrame, show="*")
    password2.place(x=270, y=300)

    # Entry Field Security Question
    pageFrame.create_text(50, 350, text="Security Question :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    securityQue = Entry(pageFrame)
    securityQue.place(x=270, y=350)
    pageFrame.create_text(50, 400, text="Answer :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    answer = Entry(pageFrame)
    answer.place(x=270, y=400)

    # Local Function for inside validation and of the form and calling the database
    def Registration():
        
        # checking validity of the form
        if len(username.get()) == 0:
            messagebox.showerror(title='Error', message='Missing Username!!')
            username.delete(0, 'end')
            username.focus()
            return
        
        elif len(dispensary.get()) == 0:
            messagebox.showerror(title='Error', message='Missing Dispensary!!')
            dispensary.delete(0, 'end')
            dispensary.focus()
            return

        elif len(password1.get()) == 0:
            messagebox.showerror(title='Error', message='Missing Password!!')
            password1.delete(0, 'end')
            password1.focus()
            return

        elif len(password2.get()) == 0:
            messagebox.showerror(title='Error', message='Missing Password Confirmation!!')
            password2.delete(0, 'end')
            password2.focus()
            return

        elif len(securityQue.get()) == 0:
            messagebox.showerror(title='Error', message='Missing Security Question!!')
            securityQue.delete(0, 'end')
            securityQue.focus()
            return

        elif len(answer.get()) == 0:
            messagebox.showerror(title='Error', message='Missing Answer!!')
            answer.delete(0, 'end')
            answer.focus() 
            return

        elif password1.get() != password2.get():
            messagebox.showerror(title='Error', message="Your Password Didn't Match Please Retype!!")
            password2.delete(0, 'end')
            password1.delete(0, 'end')
            password1.focus()
            return

        else:
            if(RegistrationDB(username.get(),password1.get(), securityQue.get(), answer.get(), dispensary.get())):
                messagebox.showinfo(title='Done',message='You have registered in succesfully!')
                pageFrame.destroy()
                newDatabasePage()
            
            else:
                messagebox.showerror(title="Error", message="Username already exists try another!")
                return
    
    # Sign Up Button
    Button(pageFrame, text="Sign Up", width=15, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [Registration()]).place(x=165, y=480)

    # Back Button
    Button(pageFrame, text="Back", width=15, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), LoginPage()]).place(x=50, y=20)

def passwordResetPage():
    # Creating Frame for Reset password page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label
    pageFrame.create_text(50, 80, text="Reset Password", fill="blue", anchor='nw', font=('Calibri', 20, 'underline'))

    # Entry Field Username
    pageFrame.create_text(50, 176, text="Username :", fill="white", anchor='nw', font=('Calibri', 14), justify='center', tag="username")
    username = Entry(pageFrame)
    username.place(x=190, y=180)
    
    def passwordReset():
        output = passwordResetDB(username.get())

        if(output == "None"):
            messagebox.showerror(title='Error', message="Username Doesn't Exists, Enter Correct Username!")
            username.delete(0, 'end')
            username.focus()
            return
        
        else:
            # destroying username and submit button
            submit.destroy()
            username.destroy()
            pageFrame.delete("username")

            # Question Display
            pageFrame.create_text(50, 180, text="Security Question: ", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
            pageFrame.create_text(220, 180, text=output[0], fill="white", anchor='nw', font=('Calibri', 14), justify='center')

            # Answer Field
            pageFrame.create_text(50, 246, text="Answer :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
            answer = Entry(pageFrame)
            answer.place(x=220, y=250)

            def passwordShower():
                if(answer.get() == output[1]):
                    messagebox.showinfo(title='Password',message='Your password is '+ output[2])
                    pageFrame.destroy()
                    LoginPage()

                else:
                    messagebox.showerror(title='Error', message='Wrong Answer Try Again!!')
                    answer.delete(0, 'end')
                    answer.focus() 
                    return        

            # Change password button
            Button(pageFrame, text="Show Password", width=15, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [passwordShower()]).place(x=218, y=320)
    
    # Submit username Button
    submit = Button(pageFrame, text="Submit", width=15, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [passwordReset()])
    submit.place(x=188, y=250)

    # Back Button
    Button(pageFrame, text="Back", width=15, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), LoginPage()]).place(x=50, y=20)

def newDatabasePage():
    # Creating Frame for newDatabasePage
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()
    pageFrame.create_text(400, 50, text="Data-Base Creation", fill="blue", anchor='nw', font=('Calibri', 20, 'underline'))
    
    # Adding calendar for start of the year
    pageFrame.create_text(325, 150, text="Select the start date for Data :", fill="white", anchor='nw', font=('Calibri', 16), justify='center')
    startYear = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black",font="Arial 16 bold")
    startYear.place(x=325,y=180)

    def DatabaseCreator():
        if(createDataBase(int(startYear.get_date()[:4]),int(startYear.get_date()[:4])+1)):
            messagebox.showinfo(title='Done',message='Database Created and added as your current Database.')
            pageFrame.destroy()
            HomePage()

        else:
            messagebox.showerror(title='Error', message='Database for selected year already exists!!')


    # Submit button
    submit = Button(pageFrame, text="Submit", width=15, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda:[DatabaseCreator()] )
    submit.place(x=450, y=480)

    # Back button
    back_button = Button(pageFrame, text='Back', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), LoginPage()])
    back_button.place(x=10, y=10)

def HomePage():
    # Creating frame for home page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app (welcome)
    pageFrame.create_text(410, 50, text="Welcome!", fill="blue", anchor='nw', font=('Calibri', 30, 'underline', 'bold'))

    # Data-Entry Button
    dataEntryButton = Button(pageFrame,text='''Data
Entry''', width=10, height=5, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(),dataEntryPage()])
    dataEntryButton.place(x=250, y=150)

    # Indent Maker Button
    indentMakerButton = Button(pageFrame, text='''Indent
Maker''', width=10, height=5, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(),indentMakerPage()])
    indentMakerButton.place(x=450, y=150)

    # Indent PDF Button
    indentPDF = Button(pageFrame, text='''Others''', width=10, height=5, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), othersPage()])
    indentPDF.place(x=650, y=150)

    # New Medicicne Button
    newMedicineEntry = Button(pageFrame, text='''Enter New
Medicine''', width=10, height=5, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(),medicineNameCreatorPage_1()])
    newMedicineEntry.place(x=250, y=330)

    # Store Account Button
    storeAccountButton = Button(pageFrame, text='''Store
Account
Maker''', width=10, height=5, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), storeAccountPage_1()])
    storeAccountButton.place(x=450, y=330)

    # New Database Button
    newDBButton = Button(pageFrame, text='''Make New
Database''', width=10, height=5, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(),nextDatabasePage()])
    newDBButton.place(x=650, y=330)

def dataEntryPage():
    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app (Data-Entry)
    pageFrame.create_text(383, 50, text='Data-Entry' , fill="blue", anchor='nw', font=('Calibri', 30, 'underline', 'bold'))

    # Button for receive data entry
    receiveButton = Button(pageFrame, text='''Recieved
Stock''', width=20, height=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), receivePage()])
    receiveButton.place(x=250, y=200)

    # Button for usage data entry
    useButton = Button(pageFrame, text='''Consumption
&
Transfer''', width=20, height=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), usePage()])
    useButton.place(x=550, y=200)

    # Back button
    backButton = Button(pageFrame, text='Back', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), HomePage()])
    backButton.place(x=50, y=20)

def indentMakerPage():
    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app (Consumption & Transfer)
    pageFrame.create_text(50, 70, text="Indent Maker", fill="blue", anchor='nw', font=('Calibri', 20, 'underline', 'bold'))

    # Drop down for deciding emergency or bi-monthly
    indentType = ['emergency', 'schedule']
    var = StringVar()
    var.set(indentType[0])
    pageFrame.create_text(50, 136, text="Type Of Indent :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    indent = OptionMenu(pageFrame, var, *indentType)
    indent.place(x=260, y=140, width=300)

    # Entry Field for Indent no
    pageFrame.create_text(50, 186, text="Indent No. :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    indentNo = Entry(pageFrame)
    indentNo.place(x=260, y=190)

    # Entry Field Dispensary Name
    pageFrame.create_text(50, 236, text="Dispensary Name :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    dispensary = Entry(pageFrame)
    dispensary.place(x=260, y=240, width=500)

    # Entry field for date
    pageFrame.create_text(50, 286, text="Date :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    indentDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    indentDate.place(x=260, y=290)

    # Entry field for pdf name
    pageFrame.create_text(50, 476, text="Name Of PDF:", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    pdfName = Entry(pageFrame)
    pdfName.place(x=260, y=480)

    # indent Maker for validation and submition
    def indentMakerValidation():
        if(len(indentNo.get())==0):
            messagebox.showerror(title='Error', message='Missing Indent No.!!')
            indentNo.delete(0, 'end')
            indentNo.focus()
            return

        elif(len(dispensary.get())==0):
            messagebox.showerror(title='Error', message='Missing Dispensary Name !!')
            dispensary.delete(0, 'end')
            dispensary.focus()
            return

        elif(len(pdfName.get())==0):
            messagebox.showerror(title='Error', message='Missing PDF Name !!')
            pdfName.delete(0, 'end')
            pdfName.focus()
            return

        indentDataEntryPage_1(pageFrame, indentNo.get(), pdfName.get(), dispensary.get(), var.get(), indentDate.get_date())

    # submit button from form submition
    submitButton = Button(pageFrame, text='Submit', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [indentMakerValidation()])
    submitButton.place(x=260, y=530)

    # back button
    backButton = Button(pageFrame, text='  Back  ',width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), HomePage()])
    backButton.place(x=50, y=20)

def indentDataEntryPage_1(pageFrame, indentNo, pdfName, dispensary, indentType, indentDate):
    # Creating frame for DataEntry Page
    pageFrame.destroy()
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Get Data of the indent
    indentData = indentDataGet(indentType)

    if(len(indentData)==0):
        messagebox.showinfo(title='Done',message='All the medicines have current balance above buffer stock..!')
        return indentDataEntryPage_2(pageFrame, indentNo, pdfName, dispensary, indentType, indentDate)

    i = 0

    # Title Label for the app (welcome)
    pageFrame.create_text(50, 95, text="Indent Data Entry", fill="blue", anchor='nw', font=('Calibri', 20, 'underline'))
    
    def submitIndentRequirementAndDestroyer(i, requirement, submitButton, skipButton):       
        if(indentRequirementSubmitionDB(indentType, indentData[i][1], requirement.get())):
            messagebox.showinfo(title='Done',message='Requirement added to the indent..!')
        
        else:
            messagebox.showerror(title="Error", message="An error occurred in submition...!")
        
        pageFrame.delete("name")
        pageFrame.delete("currentBalance")
        pageFrame.delete("bufferStock")
        pageFrame.delete("expDate")
        requirement.destroy()
        pageFrame.delete("requirementLabel")
        submitButton.destroy()
        skipButton.destroy()
        
        i = i + 1
        
        if(i<len(indentData)):
            dataAndFormCreator(i)
        
        else:
            indentDataEntryPage_2(pageFrame, indentNo, pdfName, dispensary, indentType, indentDate)

    def skipAndDestroyer(i, requirement, submitButton, skipButton):       
        pageFrame.delete("name")
        pageFrame.delete("currentBalance")
        pageFrame.delete("bufferStock")
        pageFrame.delete("expDate")
        requirement.destroy()
        pageFrame.delete("requirementLabel")
        submitButton.destroy()
        skipButton.destroy()
        
        i = i + 1
        
        if(i<len(indentData)):
            dataAndFormCreator(i)
        
        else:
            indentDataEntryPage_2(pageFrame, indentNo, pdfName, dispensary, indentType, indentDate)

    def dataAndFormCreator(i):
        expDate = closeExpDateGet(indentData[i][1])

        # label for name
        pageFrame.create_text(50, 140, text="Name :                        "+indentData[i][1], fill="white", anchor='nw', font=('Calibri', 14), justify='center', tag="name")

        # Label for current Balance
        pageFrame.create_text(50, 190, text="Current Balance :       "+str(indentData[i][4]), fill="white", anchor='nw', font=('Calibri', 14), justify='center', tag="currentBalance")

        # Label for buffer stock
        pageFrame.create_text(50, 240, text="Buffer Stock :             "+str(indentData[i][3]), fill="white", anchor='nw', font=('Calibri', 14), justify='center', tag="bufferStock")

        # Label for buffer stock
        try:
            pageFrame.create_text(50, 290, text="Expiry Date :               "+dt.datetime.strftime(dt.datetime.strptime(expDate, "%Y-%m-%d"), "%d/%m/%Y")+"  (dd/mm/yyyy)", fill="white", anchor='nw', font=('Calibri', 14), justify='center', tag="expDate")
        except:
            pageFrame.create_text(50, 290, text="Expiry Date :               NA", fill="white", anchor='nw', font=('Calibri', 14), justify='center', tag="expDate")
    

        # Entry field for requirement
        pageFrame.create_text(50, 336, text="Requirement :", fill="white", anchor='nw', font=('Calibri', 14), justify='center', tag="requirementLabel")
        requirement = Entry(pageFrame)
        requirement.insert(0,"0")
        requirement.place(x=200, y=340)

        # submit button from form submition
        submitButton = Button(pageFrame, text='Submit', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [submitIndentRequirementAndDestroyer(i, requirement, submitButton, skipButton)])
        submitButton.place(x=200, y=390)

        # submit button from form submition
        skipButton = Button(pageFrame, text='  Skip  ', width=10, bg='yellow', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [skipAndDestroyer(i, requirement, submitButton, skipButton)])
        skipButton.place(x=200, y=480)

    # back button
    backButton = Button(pageFrame, text='  Back  ',width=10,bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), HomePage()])
    backButton.place(x=50, y=20)

    dataAndFormCreator(i)

def indentDataEntryPage_2(pageFrame, indentNo, pdfName, dispensary, indentType, indentDate):
        # suggestions for name field
        suggestion = indentSuggestions()

        pageFrame.create_text(50, 135, text="*Add any medicines manually in case they are left", fill="yellow", anchor='nw', font=('Calibri', 12), justify='center')
        
        # Entry Field
        pageFrame.create_text(50, 196, text="Name :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
        name = AutocompleteEntry(suggestion, pageFrame)
        name.place(x=220, y=200, width=500)

        # Requirement Field
        pageFrame.create_text(50, 246, text="Requirement :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
        requirement = Entry(pageFrame)
        requirement.place(x=220, y=250)

        def otherMedicineSubmitionAndValidation():
            if(len(name.get())==0):
                messagebox.showerror(title='Error', message='Name Missing...!')
                name.delete(0,'end')
                name.focus()
                return

            elif(len(requirement.get())==0):
                messagebox.showerror(title='Error', message='Requirement Missing...!')
                requirement.delete(0,'end')
                requirement.focus()
                return

            if(indentRequirementSubmitionDB(indentType, name.get(), requirement.get())):
                messagebox.showinfo(title='Done', message='Requirement added to indent successfully..!')
                requirement.delete(0,'end')
                name.delete(0,'end')
                name.focus()
                return

            else:
                messagebox.showerror(title='Error', message='An error occurred in submition..!')
                requirement.delete(0,'end')
                requirement.focus()
                return

        # submit button from form submition
        submitButton = Button(pageFrame, text='Submit', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [otherMedicineSubmitionAndValidation()])
        submitButton.place(x=220, y=300)

        # Done button from form submition
        doneButton = Button(pageFrame, text='  Get PDF  ', width=10, bg='yellow', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [indentPDFCreator(pageFrame,indentNo, pdfName, dispensary, indentType, indentDate)])
        doneButton.place(x=220, y=400)

def indentPDFCreator(pageFrame, indentNo, pdfName, dispensary, indentType, indentDate):
    try:
        # getting data and arraging it
        styles = getSampleStyleSheet()
        data = []
    
        result = indentPDFData(indentType)

        for i in range(len(result)):
            subData = []

            for j in range(1, 19):
                if j == 2:
                    subData.append(i + 1)

                elif j == 3:
                    subData.append(Paragraph(result[i][j], styles['Normal']))

                elif j == 8:
                    subData.append(' ')

                else:
                    subData.append(result[i][j])

            data.append(subData)

        # table style decorations
        elements = []
        t = Table(data, colWidths=[50, 30, 235, 40, 40, 40, 40, 40, 40, 50, 64, 35, 40, 35, 50, 50, 50, 64])

        t.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                            ]))
        elements.append(t)

        # class for footer and header
        class FooterCanvas(canvas.Canvas):

            def __init__(self, *args, **kwargs):
                canvas.Canvas.__init__(self, *args, **kwargs)
                self.pages = []

            def showPage(self):
                self.pages.append(dict(self.__dict__))
                self._startPage()

            def save(self):
                page_count = len(self.pages)
                for page in self.pages:
                    self.__dict__.update(page)
                    self.draw_canvas(page_count)
                    canvas.Canvas.showPage(self)
                canvas.Canvas.save(self)

            # designing footer and header
            def draw_canvas(self, page_count):
                page = "Page %s of %s" % (self._pageNumber, page_count)
                self.saveState()
                self.setStrokeColorRGB(0, 0, 0)
                self.setLineWidth(0.5)
                self.setFont('Times-Roman', 10)
                self.drawString(250, 35, 'Sign. Of Pharmacist:')
                self.drawString(500, 35, 'Sign. Of IMO :')
                self.drawString(750, 35, 'Sign. Of CMS Store Officer :')
                self.drawString(10, 35, page)
                self.drawString(21, 510, 'SCH.')
                self.drawString(23, 500, 'NO.')
                self.drawString(64, 510, 'SR.')
                self.drawString(64, 500, 'NO.')
                self.drawString(154, 505, 'NAME OF MEDICINE')
                self.drawString(327, 485, 'YEAR')
                self.drawString(328, 495, 'LAST')
                self.drawString(333, 505, 'OF')
                self.drawString(327, 515, 'CONS.')
                self.drawString(328, 525, 'REAL')
                self.drawString(365.5, 525, 'AS PER')
                self.drawString(366.5, 515, 'COL. 3')
                self.drawString(366, 505, 'BUF.+2')
                self.drawString(364.5, 495, 'MONTH')
                self.drawString(371.5, 485, 'REQ.')
                self.drawString(410, 515, 'BAL.')
                self.drawString(412, 505, 'ON')
                self.drawString(407.5, 495, 'HAND')
                self.drawString(451.5, 500, 'REQ.')
                self.drawString(486, 520, 'STOCK')
                self.drawString(487, 510, 'SENC.')
                self.drawString(492, 500, 'BY')
                self.drawString(489, 490, 'CMS')
                self.drawString(525, 510, 'BRAND')
                self.drawString(528, 500, 'NAME')
                self.drawString(572, 515, 'NAME')
                self.drawString(577, 505, 'OF')
                self.drawString(571, 495, 'COMP.')
                self.drawString(627, 510, 'BATCH')
                self.drawString(636, 500, 'NO.')
                self.drawString(677, 510, 'MANU.')
                self.drawString(680, 500, 'DATE')
                self.drawString(721, 510, 'EXP.')
                self.drawString(718, 500, 'DATE')
                self.drawString(755, 520, 'DATE BOOK NO.')
                self.drawString(758, 510, 'AND PAGE NO.')
                self.drawString(761, 500, 'OF CMS/DISP.')
                self.drawString(770, 490, 'LEDGER')
                self.drawString(846, 515, 'SIGN.')
                self.drawString(852, 505, 'OF')
                self.drawString(838, 495, 'PHARMA.')
                self.drawString(898, 525, 'SIGN.')
                self.drawString(902, 515, 'OF')
                self.drawString(900, 505, 'IMO')
                self.drawString(900, 485, 'CMS')
                self.drawString(902, 495, 'OF')
                self.drawString(947, 505, 'REMARK')
                self.line(1002, 45, 7.5, 45)
                self.line(1002, 15, 7.5, 15)
                self.line(1002, 535, 7.5, 535)
                self.line(1002, 605, 7.5, 605)
                self.line(7.5, 605, 7.5, 15)
                self.line(58, 481, 58, 535)
                self.line(88, 481, 88, 535)
                self.line(323, 481, 323, 535)
                self.line(363, 481, 363, 535)
                self.line(402, 481, 402, 535)
                self.line(442, 481, 442, 535)
                self.line(482, 481, 482, 535)
                self.line(522.5, 481, 522.5, 535)
                self.line(562.5, 481, 562.5, 535)
                self.line(612, 481, 612, 535)
                self.line(676.5, 481, 676.5, 535)
                self.line(711, 481, 711, 535)
                self.line(751, 481, 751, 535)
                self.line(836, 481, 836, 535)
                self.line(886.5, 481, 886.5, 535)
                self.line(936.5, 481, 936.5, 535)
                self.line(1000.5, 605, 1000.5, 15)
                self.setFont('Times-Roman', 13)
                self.drawString(10, 595, str.upper(dispensary))
                self.drawString(350, 595, 'EMPLOYEE STATE INSURANCE SCHEME')
                self.drawString(350, 570, 'INDENT FORM TO RECEIVE MEDICINE FROM CMS')
                self.drawString(10, 545, 'NUMBER OF I.P : 2530')
                self.drawString(350, 545, 'MONTH :  ' + dt.datetime.now().strftime('%B') + '-' + dt.datetime.now().strftime('%y'))
                self.drawString(550, 545, str.upper(indentType)+' INDENT')
                self.drawString(770, 595, 'SPECIAL E.S.I.S 54')
                self.drawString(770, 570, 'INDENT NO. : ' + str(indentNo))
                self.drawString(770, 545, 'DATE :  ' + str(dt.datetime.strftime(dt.datetime.strptime(indentDate , "%Y-%m-%d"), "%d/%m/%Y")))

                self.restoreState()

        # Building PDF
        save_name = os.path.join(os.path.expanduser("~"), "Desktop/", pdfName+".pdf")
        doc = SimpleDocTemplate(save_name, pagesize=landscape(LEGAL), topMargin=125, leftMargin=10, rightMargin=10)
        doc.multiBuild(elements, canvasmaker=FooterCanvas)

        messagebox.showinfo(title="Done",message="Your PDF is saved on desktop with '"+pdfName+"' name..!")
        pageFrame.destroy()
        HomePage()

    # exception in building pdf
    except:
        messagebox.showerror(title='Error!', message='An error occurred in making PDF..!')
        pageFrame.destroy()
        HomePage()
            
def receivePage():
    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app (Receive)
    pageFrame.create_text(370, 50, text='Receieved Data' , fill="blue", anchor='nw', font=('Calibri', 30, 'underline', 'bold'))

    # Button for RFCMS
    CMSButton = Button(pageFrame, text='''Recieved
From
CMS''', width=14, height=7, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda:[pageFrame.destroy(), RFCMSPage_1()])
    CMSButton.place(x=440, y=350)

    # Button for LP/PMJAK
    LPButton = Button(pageFrame, text='''Local
Purchase
&
PMJAK''', width=14, height=7, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda:[pageFrame.destroy(), LPPage()])
    LPButton.place(x=290, y=150)

    # Button for RFODButton
    RFODButton = Button(pageFrame, text='''Recieved
From
Other
Dispensary''', width=14, height=7, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda:[pageFrame.destroy(),RFODPage()])
    RFODButton.place(x=590, y=150)

    # Back button
    backButton = Button(pageFrame, text='Back', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), dataEntryPage()])
    backButton.place(x=50, y=20)

def usePage():
    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app (Consumption & Transfer)
    pageFrame.create_text(390, 50, text='Usage Data' , fill="blue", anchor='nw', font=('Calibri', 30, 'underline', 'bold'))

    # button for cosumption
    consumptionButton = Button(pageFrame, text='''Cosumption''', width=20, height=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), consumptionPage()])
    consumptionButton.place(x=250, y=200)

    # button for transfer
    transferButton = Button(pageFrame, text='''Transfer
Medicine''', width=20, height=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), transferPage()])
    transferButton.place(x=550, y=200)

    # Back button
    backButton = Button(pageFrame, text='Back', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), dataEntryPage()])
    backButton.place(x=50, y=20)

def RFCMSPage_1():
    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app
    pageFrame.create_text(50, 95, text="Received From CMS", fill="blue", anchor='nw', font=('Calibri', 20, 'underline', 'bold'))

    # Entry Field 
    pageFrame.create_text(50, 196, text="Indent No :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    indentNo = Entry(pageFrame)
    indentNo.place(x=220, y=200, width=500)

    # Requirement Field
    pageFrame.create_text(50, 246, text="Indent Type :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    indentType = ['emergency', 'schedule']
    var = StringVar()
    var.set(indentType[0])
    indent = OptionMenu(pageFrame, var, *indentType)
    indent.place(x=220, y=250, width=300)
    
    def indentDetailSubmitionValidation(indentNo):
        if(len(indentNo.get()) == 0):
            messagebox.showerror(title='Error', message='Missing Indent No...!')
            indentNo.focus()
            return

        indentType = var.get()
        indentNo = indentNo.get()

        pageFrame.destroy()
        RFCMSPage_2(indentType, indentNo)

    # submit button from form submition
    submitButton = Button(pageFrame, text='Submit', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [indentDetailSubmitionValidation(indentNo)])
    submitButton.place(x=220, y=320)

    # Back button
    backButton = Button(pageFrame, text='Back', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), receivePage()])
    backButton.place(x=50, y=20)

def RFCMSPage_2(indentType, indentNo):
    # Suggestions Required from Database for auto complete entery
    suggestionData = RFCMSData(indentType)

    if(len(suggestionData)==0):
        messagebox.showwarning(title='Warning!', message='You have not prepared selected indent but you can manually add medicines..!')
        return RFCMSPage_3(indentType, indentNo)
        
    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app 
    pageFrame.create_text(50, 75, text="Received From CMS", fill="blue", anchor='nw', font=('Calibri', 20, 'underline', 'bold'))

    # Entry Field 
    pageFrame.create_text(50, 146, text="Name :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    name = Entry(pageFrame)
    name.place(x=200, y=150, width=500)

    # Entry Field Quantity
    pageFrame.create_text(50, 196, text="Quantity :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    quantity = Entry(pageFrame)
    quantity.place(x=200, y=200)

    # Entry Field Quantity
    pageFrame.create_text(50, 246, text="Batch No:", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    batch = Entry(pageFrame)
    batch.place(x=200, y=250)

    # Entry field for expiry date
    pageFrame.create_text(50, 296, text="Expiry Date :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    expDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    expDate.place(x=200, y=300)

    # Entry field for purchase date
    pageFrame.create_text(490, 296, text="Receive Date:", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    purchaseDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    purchaseDate.place(x=640, y=300)

    i = 0

    def RFCMSFormValidatioSubmition(i):
        # Validation process
        if(len(name.get()) == 0):
            messagebox.showerror(title='Error', message='Missing Name!!')
            name.delete(0, 'end')
            name.focus()
            return
            
        elif(len(quantity.get()) == 0):
            messagebox.showerror(title='Error', message='Missing Quantity!!')
            quantity.delete(0, 'end')
            quantity.focus()
            return

        elif(len(batch.get()) == 0):
            messagebox.showerror(title='Error', message='Missing Batch No!!')
            batch.delete(0, 'end')
            batch.focus()
            return
        
        if(RFCMSSubmitionDB(name.get(),batch.get(),quantity.get(),expDate.get_date(),purchaseDate.get_date(),indentNo,indentType)):
            messagebox.showinfo(title='Done', message='Medicine added successfully, your current balance is ' +currentBalanceGet(name.get()) +'..!')

        else:
            messagebox.showerror(title='Error', message='An error occurred in submition..!')
        
        i = i + 1
        
        if(i<len(suggestionData)):
            dataCreator(i,expDate,purchaseDate)

        else:
            pageFrame.destroy()
            RFCMSPage_3(indentType, indentNo)
    
    def skipAndDestroyer(i):
        i = i + 1
        
        if(i<len(suggestionData)):
            dataCreator(i,expDate,purchaseDate)

        else:
            pageFrame.destroy()
            RFCMSPage_3(indentType, indentNo)
            

    def dataCreator(i,expDate,purchaseDate):
        name.delete(0,'end')
        name.insert(0,suggestionData[i][0])
        quantity.delete(0,'end')
        quantity.insert(0,str(suggestionData[i][1]))
        expDate.destroy()
        purchaseDate.destroy()
        expDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
        expDate.place(x=200, y=300)
        purchaseDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
        purchaseDate.place(x=640, y=300)
        batch.delete(0,'end')

        # Submit button from form submition
        submitButton = Button(pageFrame, text='Submit', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [RFCMSFormValidatioSubmition(i)])
        submitButton.place(x=500, y=530)

        # skip button from form submition
        skipButton = Button(pageFrame, text='  Skip  ', width=10, bg='yellow', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [skipAndDestroyer(i)])
        skipButton.place(x=870, y=530)
        
    dataCreator(i, expDate, purchaseDate)    

    # Back button
    backButton = Button(pageFrame, text='Back', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), receivePage()])
    backButton.place(x=50, y=20)

def RFCMSPage_3(indentType, indentNo):
    # Name suggestions
    suggestion = RFCMSSuggestion()

    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app 
    pageFrame.create_text(50, 75, text="Received From CMS", fill="blue", anchor='nw', font=('Calibri', 20, 'underline', 'bold'))

    # Entry Field 
    pageFrame.create_text(50, 146, text="Name :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    name = AutocompleteEntry(suggestion, pageFrame)
    name.place(x=200, y=150, width=500)

    # Entry Field Quantity
    pageFrame.create_text(50, 196, text="Quantity :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    quantity = Entry(pageFrame)
    quantity.place(x=200, y=200)

    # Entry Field Quantity
    pageFrame.create_text(50, 246, text="Batch No. :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    batch = Entry(pageFrame)
    batch.place(x=200, y=250)

    # Entry field for expiry date
    pageFrame.create_text(50, 296, text="Expiry Date :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    expDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    expDate.place(x=200, y=300)

    # Entry field for purchase date
    pageFrame.create_text(490, 296, text="Receive Date :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    purchaseDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    purchaseDate.place(x=640, y=300)

    def RFCMSFormValidatioSubmition():
    # Validation process
        if(len(name.get()) == 0):
            messagebox.showerror(title='Error', message='Missing Name!!')
            name.delete(0, 'end')
            name.focus()
            return
            
        elif(len(quantity.get()) == 0):
            messagebox.showerror(title='Error', message='Missing Quantity!!')
            quantity.delete(0, 'end')
            quantity.focus()
            return

        elif(len(batch.get()) == 0):
            messagebox.showerror(title='Error', message='Missing Batch No!!')
            batch.delete(0, 'end')
            batch.focus()
            return
        
        if(RFCMSSubmitionDB(name.get(),batch.get(),quantity.get(),expDate.get_date(),purchaseDate.get_date(),indentNo,indentType)):
            messagebox.showinfo(title='Done', message='Medicine added successfully..!')
            name.delete(0,'end')
            quantity.delete(0,'end')
            expDate.destroy()
            purchaseDate.destroy()
            expDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
            expDate.place(x=180, y=290)
            purchaseDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
            purchaseDate.place(x=570, y=290)
            batch.delete(0,'end')

        else:
            messagebox.showerror(title='Error', message='An error occurred in submition..!')

    # Submit button from form submition
    submitButton = Button(pageFrame, text='Submit', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [RFCMSFormValidatioSubmition()])
    submitButton.place(x=500, y=530)

    # done button from form submition
    doneButton = Button(pageFrame, text='  Done  ', width=10, bg='yellow', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), receivePage()])
    doneButton.place(x=870, y=530)

    # Back button
    backButton = Button(pageFrame, text='Back', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), receivePage()])
    backButton.place(x=50, y=20)

def LPPage():
    # Suggestions Required from Database for auto complete entery
    suggestion = LPPMJAKSuggestions()

    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app (LP/PMJAK)
    pageFrame.create_text(50, 65, text="Local Purchase & PMJAK", fill="blue", anchor='nw', font=('Calibri', 20, 'underline', 'bold'))

    # Drop down for deciding lp or pmjak
    options = ['LP', 'PMJAK']
    var = StringVar()
    var.set(options[0])
    pageFrame.create_text(50, 116, text="Type :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    LPOrPMJAK = OptionMenu(pageFrame, var, *options)
    LPOrPMJAK.place(x=200, y=120, width=300)

    # Entry Field 
    pageFrame.create_text(50, 166, text="Name :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    name = AutocompleteEntry(suggestion, pageFrame)
    name.place(x=200, y=170, width=500)

    # Entry Field Quantity
    pageFrame.create_text(50, 216, text="Quantity :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    quantity = Entry(pageFrame)
    quantity.place(x=200, y=220)

    # Entry Field Price
    pageFrame.create_text(50, 266, text="Price :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    price = Entry(pageFrame)
    price.place(x=200, y=270)

    # Entry Field Batch
    pageFrame.create_text(50, 316, text="Batch No:", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    batch = Entry(pageFrame)
    batch.place(x=200, y=320)

    # Entry field for expiry date
    pageFrame.create_text(50, 366, text="Expiry Date :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    expDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    expDate.place(x=200, y=370)

    # Entry field for purchase date
    pageFrame.create_text(490, 366, text="Receive Date:", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    purchaseDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    purchaseDate.place(x=640, y=370)

    def LPPMJAKValidationAndSubmition():
        # Validation process
        if(len(name.get()) == 0):
            messagebox.showerror(title='Error', message='Missing Name!!')
            name.delete(0, 'end')
            name.focus()
            return
            
        elif(len(quantity.get()) == 0):
            messagebox.showerror(title='Error', message='Missing Quantity!!')
            quantity.delete(0, 'end')
            quantity.focus()
            return

        elif(len(price.get()) == 0):
            messagebox.showerror(title='Error', message='Missing Price!!')
            price.delete(0, 'end')
            price.focus()
            return

        elif(len(batch.get()) == 0):
            messagebox.showerror(title='Error', message='Missing Batch No!!')
            batch.delete(0, 'end')
            batch.focus()
            return

        if(LPPMJAKSubmitionDB(name.get(),batch.get(),quantity.get(),expDate.get_date(),purchaseDate.get_date(),var.get(),price.get())):
            messagebox.showinfo(title='Done',message='Medicine added successfully, your current balance is'+currentBalanceGet(name.get()) +'..!')
            pageFrame.destroy()
            receivePage()
        
        else:
            messagebox.showerror(title='Error', message='An error occurred in submition!!')
            batch.delete(0, 'end')
            price.delete(0, 'end')
            quantity.delete(0, 'end')
            name.delete(0, 'end')
            return

    # Submit button from form submition
    submitButton = Button(pageFrame, text='Submit', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [LPPMJAKValidationAndSubmition()])
    submitButton.place(x=500, y=560)

    # Back button
    backButton = Button(pageFrame, text='Back', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), receivePage()])
    backButton.place(x=50, y=20)

def RFODPage():
    # Suggestions Required from Database for auto complete entery
    suggestion = RFODSuggestions()

    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app (RFOD)
    pageFrame.create_text(50, 75, text="Received From Other Disp.", fill="blue", anchor='nw', font=('Calibri', 20, 'underline', 'bold'))

    # Entry Field 
    pageFrame.create_text(50, 146, text="Name  :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    name = AutocompleteEntry(suggestion, pageFrame)
    name.place(x=200, y=150, width=500)

    # Entry Field Quantity
    pageFrame.create_text(50, 196, text="Quantity :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    quantity = Entry(pageFrame)
    quantity.place(x=200, y=200)

    # Entry Field Batch No.
    pageFrame.create_text(50, 246, text="Batch No :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    batch = Entry(pageFrame)
    batch.place(x=200, y=250)

    # Entry Field Disp. No.
    pageFrame.create_text(50, 296, text="Disp. Name :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    dispensary = Entry(pageFrame)
    dispensary.place(x=200, y=300)

    # Entry field for expiry date
    pageFrame.create_text(50, 346, text="Expiry Date :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    expDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    expDate.place(x=200, y=350)

    # Entry field for purchase date
    pageFrame.create_text(490, 346, text="Receieve Date :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    purchaseDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    purchaseDate.place(x=640, y=350)

    def RFODValidationAndSubmition():
        # Validation process
        if(len(name.get()) == 0):
            messagebox.showerror(title='Error', message='Missing Name!!')
            name.delete(0, 'end')
            name.focus()
            return
            
        elif(len(quantity.get()) == 0):
            messagebox.showerror(title='Error', message='Missing Quantity!!')
            quantity.delete(0, 'end')
            quantity.focus()
            return

        elif(len(dispensary.get()) == 0):
            messagebox.showerror(title='Error', message='Missing Price!!')
            dispensary.delete(0, 'end')
            dispensary.focus()
            return

        elif(len(batch.get()) == 0):
            messagebox.showerror(title='Error', message='Missing Batch No!!')
            batch.delete(0, 'end')
            batch.focus()
            return

        if(RFODSubmitionDB(name.get(),batch.get(),quantity.get(),expDate.get_date(),purchaseDate.get_date(),dispensary.get())):
            messagebox.showinfo(title='Done',message='Medicine added successfully, your current balance is'+currentBalanceGet(name.get()) +'..!')
            pageFrame.destroy()
            receivePage()
        
        else:
            messagebox.showerror(title='Error', message='An error occurred in submition!!')
            batch.delete(0, 'end')
            dispensary.delete(0, 'end')
            quantity.delete(0, 'end')
            name.delete(0, 'end')
            return

    # Submit button from form submition
    submitButton = Button(pageFrame, text='Submit', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [RFODValidationAndSubmition()])
    submitButton.place(x=500, y=570)

    # Back button
    backButton = Button(pageFrame, text='Back', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), receivePage()])
    backButton.place(x=50, y=20)

def consumptionPage():
    # Suggestions Required from Database for auto complete entery
    suggestion = consumptionSuggestions()

    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app
    pageFrame.create_text(50, 75, text="Consumption Data", fill="blue", anchor='nw', font=('Calibri', 20, 'underline', 'bold'))

    # Entry Field 
    pageFrame.create_text(50, 146, text="Name :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    name = AutocompleteEntry(suggestion, pageFrame)
    name.place(x=220, y=150, width=500)

    # Entry Field Quantity
    pageFrame.create_text(50, 196, text="Quantity :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    quantity = Entry(pageFrame)
    quantity.place(x=220, y=200)

    # Entry field for purchase date
    pageFrame.create_text(50, 246, text="Use Date:", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    useDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    useDate.place(x=220, y=250)

    # Validator and submition function
    def consumptionFormValidationAndSubmition():
    
        # Validation process
        if(len(name.get()) == 0):
            messagebox.showerror(title='Error', message='Missing name!!')
            name.delete(0, 'end')
            name.focus()
            return

        elif(len(quantity.get()) == 0):
            messagebox.showerror(title='Error', message='Missing quantity!!')
            quantity.delete(0, 'end')
            quantity.focus()
            return

        elif(int(quantity.get()) > int(currentBalanceGet(name.get()))):
            messagebox.showerror(title='Error', message='Your current balance is only '+str(currentBalanceGet(name.get()))+'!!')
            quantity.delete(0, 'end')
            quantity.focus()
            return

        # Submition Process
        if(consumptionSubmitionDB(name.get(), int(quantity.get()), useDate.get_date())):
            messagebox.showinfo(title='Done',message='Entry added successfully, Current Balance is ' + str(currentBalanceGet(name.get())) + '!')
            quantity.delete(0, 'end')
            name.delete(0,'end')
            name.focus()

        else:
            quantity.delete(0, 'end')
            messagebox.showerror(title='Error', message='An error occurred in submition!!')

    # Submit button from form submition
    submitButton = Button(pageFrame, text='Submit', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [consumptionFormValidationAndSubmition()])
    submitButton.place(x=220, y=460)

    # Back button
    backButton = Button(pageFrame, text='Back', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), usePage()])
    backButton.place(x=50, y=20)

def transferPage():
    # Suggestions Required from Database for auto complete entery
    suggestion = transferSuggestion()

    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app 
    pageFrame.create_text(50, 75, text="Transfer Data", fill="blue", anchor='nw', font=('Calibri', 20, 'underline', 'bold'))

    # Entry Field 
    pageFrame.create_text(50, 146, text="Name :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    name = AutocompleteEntry(suggestion, pageFrame)
    name.place(x=220, y=150, width=500)

    # Go button
    goButton = Button(pageFrame, text='Go', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [batchCreator()])
    goButton.place(x=780, y=140)

    def batchCreator():
        goButton.destroy()

        if(len(name.get())==0):
            messagebox.showerror(title='Error!', message='Missing Name')
            name.delete(0,'end')
            name.focus()
            return

        # Entry Field Quantity
        pageFrame.create_text(50, 196, text="Quantity :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
        quantity = Entry(pageFrame)
        quantity.place(x=220, y=200)

        # Entry Field Batch
        pageFrame.create_text(50, 246, text="Batch No. :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
        options = transferBatchSuggestion(name.get())
        batch = AutocompleteEntry(options,pageFrame)
        batch.place(x=220, y=250, width=300)

        # Entry field for transfer date
        pageFrame.create_text(50, 296, text="Transfer Date :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
        transferDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
        transferDate.place(x=220, y=300)

        def transferValidationSubmition():
            if(len(quantity.get())==0):
                messagebox.showerror(title='Error!', message='Missing Quantity')
                quantity.delete(0,'end')
                quantity.focus()
                return

            elif(int(quantity.get()) > getBatchQuantity(batch.get(), name.get())):
                messagebox.showerror(title='Error!', message='Selected Batch has only '+str(getBatchQuantity(batch.get(), name.get()))+" quantity" )
                quantity.delete(0,'end')
                quantity.focus()
                return

            if(transferSubmitionDB(name.get(),batch.get(),quantity.get(),transferDate.get_date(),getBatchExpDate(batch.get(),name.get()))):
                messagebox.showinfo(title='Done',message='Medicine transferred successfully , your current Balnce is '+str(currentBalanceGet(name.get())))
                pageFrame.destroy()
                usePage()

            else:
                messagebox.showerror(title='Error!', message='An error occurred in submition..!')
                pageFrame.destroy()
                usePage()

        # Submit button from form submition
        submitButton = Button(pageFrame, text='Submit', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [transferValidationSubmition()])
        submitButton.place(x=220, y=510)

    # Back button
    backButton = Button(pageFrame, text='Back', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), usePage()])
    backButton.place(x=10, y=10)

def medicineNameCreatorPage_1():
    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    pageFrame.create_text(50, 65, text="New Medicine Entry", fill="blue", anchor='nw', font=('Calibri', 20, 'underline'))

    # label form the spinbox:
    pageFrame.create_text(50, 126, text="Select No. Of Molecules In Medicine :", fill="white", anchor='nw', font=('Calibri', 14), justify='center', tag="label")

    # spin box for new medicines
    spin = Spinbox(pageFrame, from_=1, to=5, width=2)
    spin.place(x=350, y=130)

    # button to submit no. of molecules
    go = Button(pageFrame, text='Go', width=5, height=1, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.delete("label"),medicineNameCreatorPage_2(pageFrame, spin, go)])
    go.place(x=400, y=124)

    # back button
    backButton = Button(pageFrame, text='Back', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(),HomePage()])
    backButton.place(x=50, y=20)
    
def medicineNameCreatorPage_2(pageFrame, spin, go):
    # No. of molecules from spinBox
    molecule = int(spin.get())

    if(molecule > 5):
        molecule = 5
    spin.destroy()
    go.destroy()

    # creating schedule_no field
    pageFrame.create_text(50, 146, text="Schedule No. :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    schNo = Entry(pageFrame)
    schNo.place(x=220, y=150, width=95)

    # creating medicine_type field
    pageFrame.create_text(460, 146, text="Type Of Medicine :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    medicineTypelist = ['Tab.', 'Cap.', 'Drops', 'Film', 'Infusion', 'Inh.', 'Inj.', 'Jelly', 'Liq.', 'Lotion',
                          'M.W.', 'Oint.', 'Paint', 'Powder', 'Resp.', 'Roto.', 'Sachet', 'Scrub', 'Spray', 'Syp.',
                          'Syringe', 'Than']
    var = StringVar()
    var.set(medicineTypelist[0])
    medicineType = OptionMenu(pageFrame, var, *medicineTypelist)
    medicineType.place(x=630, y=145)

    # list of power units
    powerUnits = ['','mg', 'gm', 'mcg', 'ml', 'l', 'million', 'miu', 'lacs IU', 'IU', 'lac units', '%']

    # list of symbols
    symbols = ['','/', '%']

    # lists for creating name
    names = []
    power1 = []
    power1Value = []
    var1 = []
    power2 = []
    power2Value = []
    var2 = []
    symbol = []
    var3 = []

    for i in range(molecule):

        names.append(Entry(pageFrame))
        power1Value.append(Entry(pageFrame))
        var1.append(StringVar())
        var1[i].set(powerUnits[0])
        power1.append(OptionMenu(pageFrame,var1[i],*powerUnits))
        power2Value.append(Entry(pageFrame))
        var2.append(StringVar())
        var2[i].set(powerUnits[0])
        power2.append(OptionMenu(pageFrame,var2[i],*powerUnits))
        var3.append(StringVar())
        var3[i].set(symbols[0])
        symbol.append(OptionMenu(pageFrame,var3[i],*symbols))

        # name_placement
        pageFrame.create_text(50, 226 + (i * 50), text="Name :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
        names[i].place(x=130, y=230 + (i * 50), width=250)

        # power1_placement
        pageFrame.create_text(460, 226 + (i * 50), text="Power :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
        power1Value[i].place(x=534, y=230 + (i * 50), width=40)
        power1[i].place(x=580, y=225 + (i * 50), width=100)

        # middle symbol between two powers
        symbol[i].place(x=685, y=225 + (i * 50), width=60)

        # power2_placement
        power2Value[i].place(x=754, y=230 + (i * 50), width=40)
        power2[i].place(x=800, y=225 + (i * 50), width=100)

    # Entry for last year Consumption
    pageFrame.create_text(50, 246+(molecule*50), text="Last Year Consumption :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    lastYearConsumption = Entry(pageFrame)
    lastYearConsumption.place(x=250, y=250+(molecule*50))

    # Entry for Old price
    pageFrame.create_text(460, 246+(molecule*50), text="Old Price :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    oldPrice = Entry(pageFrame)
    oldPrice.place(x=550, y=250+(molecule*50))

    # Function for validation of form:
    def submitValidationAndDatabaseInsertion():
        if(len(schNo.get()) == 0):
            messagebox.showerror(title='Error', message='Missing Details!!')
            schNo.delete(0, 'end')
            schNo.focus()
            return

        elif(len(lastYearConsumption.get()) == 0):
            messagebox.showerror(title='Error', message='Missing Details!!')
            lastYearConsumption.delete(0, 'end')
            lastYearConsumption.focus()
            return
        
        elif(len(oldPrice.get()) == 0):
            messagebox.showerror(title='Error', message='Missing Details!!')
            oldPrice.delete(0, 'end')
            oldPrice.focus()
            return

        medicine = []

        for j in range(molecule):

            if(len(names[j].get()) == 0):
                messagebox.showerror(title='Error', message='Missing Details!!')
                names[j].delete(0, 'end')
                names[j].focus()
                return

            medicine.append(names[j].get()+" "+power1Value[j].get()+var1[j].get()+var3[j].get()+power2Value[j].get()+var2[j].get())

        medicine = ' + '.join(medicine)

        medicineNameInsertionDB(schNo.get(), var.get(), medicine.upper(), oldPrice.get(), lastYearConsumption.get())
        ID = IDGet(medicine.upper())

        pageFrame.destroy()
        medicineOBPage(ID)


    # Submit button from form submition
    nextButton = Button(pageFrame, text='  Next  ', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [submitValidationAndDatabaseInsertion()])
    nextButton.place(x=390, y=330+(molecule*50)) 

def medicineOBPage(ID):
    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    pageFrame.create_text(50, 75, text="Opening Balance Entry", fill="blue", anchor='nw', font=('Calibri', 20, 'underline'))
    pageFrame.create_text(50, 125, text="*Enter the Opening balance of all available batches of medicine one by one", fill="yellow", anchor='nw', font=('Calibri', 12), justify='center')
    
    # Entry Field Quantity
    pageFrame.create_text(50, 146, text="Quantity :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    quantity = Entry(pageFrame)
    quantity.place(x=200, y=150)

    # Entry Field Quantity
    pageFrame.create_text(50, 196, text="Batch No:", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    batch = Entry(pageFrame)
    batch.place(x=200, y=200)

    # Entry field for expiry date
    pageFrame.create_text(50, 246, text="Expiry Date :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    expDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    expDate.place(x=200, y=250)

    # Entry field for purchase date
    pageFrame.create_text(490, 246, text="Receive Date:", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    purchaseDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black",day=1,month=4)
    purchaseDate.place(x=640, y=250)
    
    # Validator and submition function
    def OBFormValidationAndSubmition():
        # Validation process
        if(len(quantity.get()) == 0):
            messagebox.showerror(title='Error', message='Missing Quantity!!')
            quantity.delete(0, 'end')
            quantity.focus()
            return

        elif(len(batch.get()) == 0):
            messagebox.showerror(title='Error', message='Missing Batch No!!')
            batch.delete(0, 'end')
            batch.focus()
            return

        # Submition Process
        if(OBSubmitionDB(ID,batch.get(),quantity.get(),expDate.get_date(),purchaseDate.get_date())):
            batch.delete(0, 'end')
            quantity.delete(0, 'end')
            messagebox.showinfo(title='Done',message='Batch added successfully, Enter the next batch!')

        else:
            messagebox.showerror(title='Error', message='An error occurred in submition!!')


    # Submit button from form submition
    addButton = Button(pageFrame, text='  Add  ', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [OBFormValidationAndSubmition()])
    addButton.place(x=500, y=470)

    # Done button from form exit
    addButton = Button(pageFrame, text='  Done  ', width=10, bg='yellow', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), medicineNameCreatorPage_1()])
    addButton.place(x=800, y=470)

    # Back button
    backButton = Button(pageFrame, text='  Back  ', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), HomePage()])
    backButton.place(x=50, y=20)

def storeAccountPage_1():
    # Creating frame for store account Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app (Consumption & Transfer)
    pageFrame.create_text(50, 75, text="Store Account Entry", fill="blue", anchor='nw', font=('Calibri', 20, 'underline'))

    # Entry field for date
    pageFrame.create_text(50, 146, text="Date :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    stroreAccountDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    stroreAccountDate.place(x=200, y=150)

    # Entry field for pdf name
    pageFrame.create_text(50, 346, text="Name Of PDF:", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    pdfName = Entry(pageFrame)
    pdfName.place(x=200, y=350)

    # indent Maker for validation and submition
    def indentMakerValidation():
        if(len(pdfName.get())==0):
            messagebox.showerror(title='Error', message='Missing PDF Name !!')
            pdfName.delete(0, 'end')
            pdfName.focus()
            return

        storeAccountPage_2(pageFrame, pdfName.get(), stroreAccountDate.get_date())

    # submit button from form submition
    submitButton = Button(pageFrame, text='Submit', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [indentMakerValidation()])
    submitButton.place(x=200, y=420)

    # back button
    backButton = Button(pageFrame, text='  Back  ',width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), HomePage()])
    backButton.place(x=50, y=20)

def storeAccountPage_2(pageFrame, pdfName, storeAccountDate):

    # medicine names
    storeAccountName = storeAccountNames()

    # Creating frame for store account Page
    pageFrame.destroy()
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    if(len(storeAccountName)==0):
        messagebox.showwarning(title='Warning!', message='You have not entered any medicine to the database..!')
        pageFrame.destroy()
        return HomePage()

    # Title Label for the app
    pageFrame.create_text(50, 75, text="Store Account Entry", fill="blue", anchor='nw', font=('Calibri', 20, 'underline'))

    # New Price Field
    pageFrame.create_text(50, 196, text="New Price :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    newPrice = Entry(pageFrame)
    newPrice.place(x=200, y=200)

    i = 0

    def storeAccountFormValidatioSubmition(i):
        # Validation process
        if(len(newPrice.get())==0):
            messagebox.showerror(title='Error', message='Missing Price..!')
            newPrice.delete(0,'end')
            newPrice.focus()
            return
        
        if(storeAccountSubmitionDB(newPrice.get(), storeAccountName[i])):
            messagebox.showinfo(title='Done', message='New Price Added successfully..!')
            i = i + 1
        
            if(i<len(storeAccountName)):
                pageFrame.delete("name")
                newPrice.delete(0,'end')
                dataCreator(i)

            else:
                storeAccountPDF(pageFrame, pdfName, storeAccountDate)

        else:
            messagebox.showerror(title='Error', message='An error occurred in submition..!')
            newPrice.focus()
            newPrice.delete(0,'end')
                    
    def dataCreator(i):
    
        pageFrame.create_text(50, 146, text="Name :                        "+storeAccountName[i], fill="white", anchor='nw', font=('Calibri', 14), justify='center', tag="name")

        # Submit button from form submition
        submitButton = Button(pageFrame, text='Submit', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [storeAccountFormValidatioSubmition(i)])
        submitButton.place(x=200, y=300)
        
    dataCreator(i)    

    # Back button
    backButton = Button(pageFrame, text='Back', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), HomePage()])
    backButton.place(x=50, y=20)

def storeAccountPDF(pageFrame, pdfName, storeAccountDate):
    try:
        result = storeAccountPDFData()
        data = []
        sum = ['', 'Total', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        styles = getSampleStyleSheet()

        # getting data from database and arranging it
        for i in range(len(result)):

            sub_data = []
            for j in range(0, 22):

                if(j == 0):
                    sub_data.append(result[i][j])
                
                elif(j==1):
                    sub_data.append(Paragraph(result[i][j], styles['Normal']))

                elif j in (2,4,6,8):
                    sub_data.append(result[i][j])
                    sum[j] = sum[j] + result[i][j]

                elif j in (3,5,7,9):
                    sub_data.append(float("{0:.2f}".format(result[i][j])))
                    sum[j] = sum[j] + float("{0:.2f}".format(result[i][j]))

                elif (j == 10):
                    sub_data[8] = sub_data[8] + result[i][j]
                    sum[8] = sum[8] + result[i][j]

                elif (j == 11):
                    sub_data[9] = sub_data[9] + result[i][j]
                    sum[9] = sum[9] + result[i][j]

                elif j in (12,14,16,18,20):
                    sub_data.append(result[i][j])
                    sum[j-2] = sum[j-2] + result[i][j]

                elif j in (13,15,17,19,21):
                    sub_data.append(float("{0:.2f}".format(result[i][j])))
                    sum[j-2] = sum[j-2] + float("{0:.2f}".format(result[i][j]))

            data.append(sub_data)
        data.append(sum)

        # table style decorations
        elements = []
        t = Table(data, colWidths=[30, 199, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42])

        t.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                ]))
        elements.append(t)

        # class for footer and header
        class FooterCanvas(canvas.Canvas):

            def __init__(self, *args, **kwargs):
                canvas.Canvas.__init__(self, *args, **kwargs)
                self.pages = []

            def showPage(self):
                self.pages.append(dict(self.__dict__))
                self._startPage()

            def save(self):
                page_count = len(self.pages)
                for page in self.pages:
                    self.__dict__.update(page)
                    self.draw_canvas(page_count)
                    canvas.Canvas.showPage(self)
                canvas.Canvas.save(self)

            # designing footer and header
            def draw_canvas(self, page_count):
                page = "Page %s of %s" % (self._pageNumber, page_count)
                self.saveState()
                self.setStrokeColorRGB(0, 0, 0)
                self.setLineWidth(0.5)
                self.setFont('Times-Roman', 10)
                self.drawString(14.5, 35, page)
                self.line(11.5, 45, 996.5, 45)
                self.line(996.5, 45, 11.5, 45)
                self.line(996.5, 15, 11.5, 15)
                self.line(996.5, 535, 11.5, 535)
                self.line(996.5, 605, 11.5, 605)
                self.line(11.5, 605, 11.5, 15)
                self.line(996.5, 605, 996.5, 15)
                self.setFont('Times-Roman', 14)
                self.drawString(448, 590, 'STORE ACCOUNT ' +str(int(str(storeAccountDate)[:4])-1) +"-"+(str(storeAccountDate)[:4]))
                self.drawString(448, 565, 'ALOPHATIC MEDICINE')
                self.drawString(430, 540, getDisp())
                self.line(41.5, 481, 41.5, 535)
                self.line(240.5, 481, 240.5, 535)
                self.line(240.5, 501, 996.5, 501)
                self.line(324.5, 481, 324.5, 535)
                self.line(408.5, 481, 408.5, 535)
                self.line(492.5, 481, 492.5, 535)
                self.line(576.5, 481, 576.5, 535)
                self.line(660.5, 481, 660.5, 535)
                self.line(744.5, 481, 744.5, 535)
                self.line(828.5, 481, 828.5, 535)
                self.line(912.5, 481, 912.5, 535)
                self.setFont('Times-Roman', 10)
                for x in range(1, 21):
                    self.line(198.5+(x*42), 501, 198.5+(x*42), 481)

                    if x < 19 and x % 2 != 0:
                        self.drawString(207+(x*42), 487, 'QTY.')

                    elif x < 19 and x % 2 == 0:
                        self.drawString(207+(x*42), 487, 'VAL.')

                self.drawString(15.5, 510, 'SR.')
                self.drawString(15.5, 500, 'NO.')
                self.drawString(85.5, 505, 'NAME OF MEDICINE')
                self.drawString(260.5, 520, 'OPENING')
                self.drawString(260.5, 510, 'BALANCE')
                self.drawString(339.5, 520, 'REC. FROM')
                self.drawString(337.5, 510, 'OTHER DISP.')
                self.drawString(423.5, 520, 'REC. FROM')
                self.drawString(435.5, 510, 'CMS')
                self.drawString(515.5, 520, 'LOCAL')
                self.drawString(509.5, 510, 'PURCHASE')
                self.drawString(599.5, 520, 'TOTAL')
                self.drawString(593.5, 510, 'RECEIVED')
                self.drawString(666.5, 515, 'CONSUMPTION')
                self.drawString(761.5, 515, 'TRANSFER')
                self.drawString(851.5, 520, 'TOTAL')
                self.drawString(855.5, 510, 'USED')
                self.drawString(929.5, 515, 'CLOSING')

        # Building PDF
        save_name = os.path.join(os.path.expanduser("~"), "Desktop/", pdfName+".pdf")
        doc = SimpleDocTemplate(save_name, pagesize=landscape(LEGAL), topMargin=125, leftMargin=10, rightMargin=10)
        doc.multiBuild(elements, canvasmaker=FooterCanvas)
        messagebox.showinfo(title='Success!', message='Your PDF Has Been Created Successfully on desktop with name "'+pdfName+'" ..!')
        pageFrame.destroy()
        HomePage()
    
    except:
        messagebox.showerror(title='Error', message='An error occurred in creating PDF')
        pageFrame.destroy()
        HomePage()

def usageRegisterPage():

    # Suggestions Required from Database for auto complete entery
    suggestion = RFODSuggestions()

    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app (RFOD)
    pageFrame.create_text(50, 75, text="Usage Register", fill="blue", anchor='nw', font=('Calibri', 20, 'underline'))

    # Entry Field For name
    pageFrame.create_text(50, 146, text="Name :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    name = AutocompleteEntry(suggestion, pageFrame)
    name.place(x=200, y=150, width=500)

    # Entry Field for pdf name
    pageFrame.create_text(50, 396, text="PDF Name :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    PDFName = Entry(pageFrame)
    PDFName.place(x=200, y=400)

    # Entry field for start date
    pageFrame.create_text(50, 196, text="From :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    startDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    startDate.place(x=200, y=200)

    # Entry field for end date
    pageFrame.create_text(540, 196, text="To :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    endDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    endDate.place(x=640, y=200)

    def usageRegisterValidation():
        # Validation process
        if(len(name.get()) == 0):
            messagebox.showerror(title='Error', message='Missing Name!!')
            name.delete(0, 'end')
            name.focus()
            return

        elif(len(PDFName.get()) == 0):
            messagebox.showerror(title='Error', message='Missing PDF Name!!')
            PDFName.delete(0, 'end')
            PDFName.focus()
            return

        usageRegisterPDF(pageFrame, PDFName.get(), name.get(), startDate.get_date(), endDate.get_date())     

    # Submit button from form submition
    submitButton = Button(pageFrame, text='Submit', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [usageRegisterValidation()])
    submitButton.place(x=200, y=470)

    # Back button
    backButton = Button(pageFrame, text='Back', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), othersPage()])
    backButton.place(x=50, y=20)

def usageRegisterPDF(pageFrame, PDFName, name, startDate, endDate):
    try:
        # getting data and arraging it
        result = usageRegisterData(name, startDate, endDate)
        styles = getSampleStyleSheet()
        data = []

        for i in range(len(result)):
            subDate = []
            for j in range(7):
                if(j==0):
                    subDate.append(dt.datetime.strftime(dt.datetime.strptime(result[i][j], "%Y-%m-%d"), "%d/%m/%Y"))

                elif(j==1):
                    subDate.append(Paragraph(result[i][j], styles['Normal']))

                elif(result[i][j] == 0):
                    subDate.append(" ")

                else:
                    subDate.append(result[i][j])
            
            data.append(subDate)
        
        # table style decorations
        elements = []
        t = Table(data, colWidths=[80,200,50,50,50,50,60])

        t.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                            ]))
        elements.append(t)

        # class for footer and header
        class FooterCanvas(canvas.Canvas):

            def __init__(self, *args, **kwargs):
                canvas.Canvas.__init__(self, *args, **kwargs)
                self.pages = []

            def showPage(self):
                self.pages.append(dict(self.__dict__))
                self._startPage()

            def save(self):
                page_count = len(self.pages)
                for page in self.pages:
                    self.__dict__.update(page)
                    self.draw_canvas(page_count)
                    canvas.Canvas.showPage(self)
                canvas.Canvas.save(self)

            # designing footer and header
            def draw_canvas(self, page_count):
                page = "Page %s of %s" % (self._pageNumber, page_count)
                self.saveState()
                self.setStrokeColorRGB(0, 0, 0)
                self.setLineWidth(0.5)
                self.setFont('Times-Roman', 10)
                self.drawString(10, 10, page)
                self.drawString(55, 720, "DATE")
                self.drawString(200, 720, "INFO")
                self.drawString(318, 720, "PRICE")
                self.drawString(358, 720, "RECEIVED")
                self.drawString(421, 720, "USED")
                self.drawString(468, 720, "FINAL")
                self.drawString(527, 720, "SIGN")
                self.line(27.5,710,27.5,735)
                self.line(107.5,710,107.5,735)
                self.line(307.5,710,307.5,735)
                self.line(357.5,710,357.5,735)
                self.line(407.5,710,407.5,735)
                self.line(457.5,710,457.5,735)
                self.line(507.5,710,507.5,735)
                self.line(567.5,710,567.5,735)
                self.line(27.5,735,567.5,735)
                self.setFont('Times-Roman', 13)
                self.drawString(28, 745, "MEDICINE: "+name)
                self.drawString(260, 770, "USAGE REGISTER")

                self.restoreState()

        # Building PDF
        save_name = os.path.join(os.path.expanduser("~"), "Desktop/", PDFName+".pdf")
        doc = SimpleDocTemplate(save_name, pagesize=portrait(A4), topMargin=125, leftMargin=10, rightMargin=10)
        doc.multiBuild(elements, canvasmaker=FooterCanvas)
        messagebox.showinfo(title='Success!', message='Your PDF Has Been Created Successfully on desktop with name "'+PDFName+'" ..!')
        pageFrame.destroy()
        HomePage()
    
    except:
        messagebox.showerror(title='Error', message='An error occurred in creating PDF')
        pageFrame.destroy()
        HomePage()

def mistakeCorrectorPage():
    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app (Receive)
    pageFrame.create_text(340, 50, text="Mistake Correction", fill="blue", anchor='nw', font=('Calibri', 30, 'underline', 'bold'))

    # RFCMSCorrection Button
    RFCMSCorrection = Button(pageFrame,text='''RFCMS
Correction''', width=11, height=5, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), RFCMSCorrectorPage()])
    RFCMSCorrection.place(x=250, y=150)

    # LP/PMJAK Correction Button
    LPPMJAKCorrectionButton = Button(pageFrame, text='''LP/PMJAK
Correction''', width=11, height=5, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), LPPMJAKCorrectorPage()])
    LPPMJAKCorrectionButton.place(x=450, y=150)

    # RFOD Correction Button
    RFODCorrectionButton = Button(pageFrame, text='''RFOD
Correction''', width=11, height=5, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), RFODCorrectorPage()])
    RFODCorrectionButton.place(x=650, y=150)

    # OB Correction Button
    OBCorrectionButton = Button(pageFrame, text='''Opening
Balance
Correction''', width=11, height=5, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), OBCorrectorPage()])
    OBCorrectionButton.place(x=250, y=300)

    # consumptionCorrection Button
    consumptionCorrectionButton = Button(pageFrame, text='''Consumption
Correction''', width=11, height=5, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), consumptionCorrectorPage()])
    consumptionCorrectionButton.place(x=450, y=300)

    # transfer Correction Button
    transferCorrectionButton = Button(pageFrame, text='''Transfer
Correction''', width=11, height=5, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), transferCorrectorPage()])
    transferCorrectionButton.place(x=650, y=300)

    # other Correction Button
    otherCorrectionButton = Button(pageFrame, text='''Other
Correction''', width=11, height=5, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), otherCorrectorPage()])
    otherCorrectionButton.place(x=350, y=450)

    # delete medicine Button
    deleteMedicineButton = Button(pageFrame, text='''Delete
Medicine''', width=11, height=5, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), deleteMedicinePage()])
    deleteMedicineButton.place(x=550, y=450)
    
    # Back button
    backButton = Button(pageFrame, text='Back', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), othersPage()])
    backButton.place(x=50, y=20)

def nextDatabasePage():

    # Creating Frame for newDatabasePage
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()
    pageFrame.create_text(400, 50, text="Data-Base Creation", fill="blue", anchor='nw', font=('Calibri', 20, 'underline'))
    
    # Adding calendar for start of the year
    pageFrame.create_text(325, 150, text="Select the start date for Data :", fill="white", anchor='nw', font=('Calibri', 16), justify='center')
    startYear = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black",font="Arial 16 bold")
    startYear.place(x=325,y=180)

    def DatabaseCreator():
        if(nextDataBaseCreator(int(startYear.get_date()[:4]),int(startYear.get_date()[:4])+1)):
            messagebox.showinfo(title='Done',message='Database Created and added as your current Database.')
            pageFrame.destroy()
            HomePage()

        else:
            messagebox.showerror(title='Error', message='Database for selected year already exists!!')


    # Submit button
    submit = Button(pageFrame, text="Submit", width=15, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda:[DatabaseCreator()] )
    submit.place(x=450, y=480)

    # Back button
    back_button = Button(pageFrame, text='Back', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), HomePage()])
    back_button.place(x=10, y=10)

def consumptionCorrectorPage(): 
    suggestion = RFODSuggestions()

    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app (Consumption & Transfer)
    pageFrame.create_text(50, 75, text="Consumption Correction", fill="blue", anchor='nw', font=('Calibri', 20, 'underline'))

    # Drop down for deciding increase or decrease
    changeType = ['Increase', 'Decrease']
    var = StringVar()
    var.set(changeType[0])
    pageFrame.create_text(50, 396, text="Type Of Change :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    typeOfChange = OptionMenu(pageFrame, var, *changeType)
    typeOfChange.place(x=220, y=395, width=300)

    # Entry Field for Name.
    pageFrame.create_text(50, 146, text="Name :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    name = AutocompleteEntry(suggestion, pageFrame)
    name.place(x=220, y=150, width=500)

    # Entry Field Quantity
    pageFrame.create_text(50, 446, text="Quantity Of Change :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    quantity = Entry(pageFrame)
    quantity.place(x=220, y=450)

    # Entry field for date
    pageFrame.create_text(50, 196, text="Entry Date :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    entryDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    entryDate.place(x=220, y=200)

    # indent Maker for validation and submition
    def consumptionCorrectorValidationAndSubmition():
        if(len(name.get())==0):
            messagebox.showerror(title='Error', message='Missing Name!!')
            name.delete(0, 'end')
            name.focus()
            return

        elif(len(quantity.get())==0):
            messagebox.showerror(title='Error', message='Missing Qunatity Change !!')
            quantity.delete(0, 'end')
            quantity.focus()
            return
        
        currentQuantity = getConsumptionQuantity(name.get(), entryDate.get_date())

        if(currentQuantity < int(quantity.get()) and var.get() == "Decrease"):
            messagebox.showerror(title='Error', message='You have only '+str(currentQuantity)+' medicines used on the selected date..!')
            quantity.delete(0, 'end')
            quantity.focus()
            return

        elif(int(currentBalanceGet(name.get())) < int(quantity.get()) and var.get() == "Increase"):
            messagebox.showerror(title='Error', message='You have only '+str(currentBalanceGet(name.get()))+' medicines left in balance!')
            quantity.delete(0, 'end')
            quantity.focus()
            return 

        if(var.get() == "Increase"):
            confirmation = consumptionIncreaseDB(name.get(), int(quantity.get()), entryDate.get_date(), dt.datetime.now().strftime("%Y-%m-%d"))
            
        else:
            confirmation = consumptionDecreaseDB(name.get(), int(quantity.get()), entryDate.get_date(), dt.datetime.now().strftime("%Y-%m-%d"))
        
        if(confirmation):
            messagebox.showinfo(title='Done', message='Changes done successfully your current balance is '+currentBalanceGet(name.get())+'!')
            pageFrame.destroy()
            mistakeCorrectorPage()

        else:
            messagebox.showerror(title='Error', message='An error occurred in correction..!')
            
    # submit button from form submition
    submitButton = Button(pageFrame, text='Submit', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [consumptionCorrectorValidationAndSubmition()])
    submitButton.place(x=220, y=500)

    # back button
    backButton = Button(pageFrame, text='  Back  ',width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), mistakeCorrectorPage()])
    backButton.place(x=50, y=20)

def RFODCorrectorPage():
    suggestion = RFODSuggestions()

    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app (Consumption & Transfer)
    pageFrame.create_text(50, 75, text="RFOD Correction", fill="blue", anchor='nw', font=('Calibri', 20, 'underline'))

    # Drop down for deciding increase or decrease
    changeType = ['Increase', 'Decrease']
    var = StringVar()
    var.set(changeType[0])
    pageFrame.create_text(50, 396, text="Type Of Change :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    typeOfChange = OptionMenu(pageFrame, var, *changeType)
    typeOfChange.place(x=220, y=395, width=300)

    # Entry Field for Name.
    pageFrame.create_text(50, 146, text="Name :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    name = AutocompleteEntry(suggestion, pageFrame)
    name.place(x=220, y=150, width=500)

    # Entry Field Quantity
    pageFrame.create_text(50, 446, text="Batch No :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    batch = Entry(pageFrame)
    batch.place(x=220, y=450)

    # Entry Field Batch No.
    pageFrame.create_text(50, 496, text="Quantity Of Change :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    quantity = Entry(pageFrame)
    quantity.place(x=220, y=500)

    # Entry field for date
    pageFrame.create_text(50, 196, text="Entry Date :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    entryDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    entryDate.place(x=220, y=200)

    # indent Maker for validation and submition
    def RFODCorrectorValidationAndSubmition():
        if(len(name.get())==0):
            messagebox.showerror(title='Error', message='Missing Name!!')
            name.delete(0, 'end')
            name.focus()
            return

        elif(len(batch.get())==0):
            messagebox.showerror(title='Error', message='Missing Batch No !!')
            batch.delete(0, 'end')
            batch.focus()
            return

        elif(len(quantity.get())==0):
            messagebox.showerror(title='Error', message='Missing Quantity of change!!')
            quantity.delete(0, 'end')
            quantity.focus()
            return
        
        currentQuantity = getCurrentQuantity(name.get(), entryDate.get_date(), batch.get())
        receivedQuantity = getReceivedQuantity(name.get(), entryDate.get_date(), batch.get())
        currentBalance = int(currentBalanceGet(name.get()))

        if(receivedQuantity <= 0):
            messagebox.showerror(title='Error', message='Enter details properly..!')
            quantity.delete(0, 'end')
            batch.delete(0, 'end')
            quantity.focus()
            return

        if(receivedQuantity < int(quantity.get()) and var.get() == 'Decrease'):
            messagebox.showerror(title='Error', message='You have only received '+str(receivedQuantity)+' medicines..!')
            quantity.delete(0, 'end')
            quantity.focus()
            return

        elif(currentBalance < int(quantity.get()) and var.get() == 'Decrease'):
            messagebox.showerror(title='Error', message='Can not make change due to low balance..!')
            quantity.delete(0, 'end')
            quantity.focus()
            return

        if(var.get() == "Increase"):
            confirmation = RFODIncreaseDB(name.get(), int(quantity.get()), entryDate.get_date(), dt.datetime.now().strftime("%Y-%m-%d"), batch.get())
            
        else:
            confirmation = RFODDecreaseDB(name.get(), int(quantity.get()), entryDate.get_date(), dt.datetime.now().strftime("%Y-%m-%d"), batch.get(), currentQuantity)
        
        if(confirmation):
            messagebox.showinfo(title='Done', message='Changes done successfully your current balance is '+currentBalanceGet(name.get())+'!')
            pageFrame.destroy()
            mistakeCorrectorPage()

        else:
            messagebox.showerror(title='Error', message='An error occurred in correction..!')
             
    # submit button from form submition
    submitButton = Button(pageFrame, text='Submit', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [RFODCorrectorValidationAndSubmition()])
    submitButton.place(x=220, y=550)

    # back button
    backButton = Button(pageFrame, text='  Back  ',width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), mistakeCorrectorPage()])
    backButton.place(x=50, y=20)

def othersPage():
    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app (Receive)
    pageFrame.create_text(380, 50, text="Other Options", fill="blue", anchor='nw', font=('Calibri', 30, 'underline', 'bold'))

    # Button for Register
    usageRegisterButton = Button(pageFrame, text='''Usage
Register''', width=14, height=7, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda:[pageFrame.destroy(), usageRegisterPage()])
    usageRegisterButton.place(x=290, y=150)

    # Button for Mistake
    mistakeCorrectionButton = Button(pageFrame, text='''Mistake
Corrections''', width=14, height=7, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda:[pageFrame.destroy(), mistakeCorrectorPage()])
    mistakeCorrectionButton.place(x=590, y=150)

    # Button for details
    detailsButton = Button(pageFrame, text='''Get
Details''', width=14, height=7, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda:[pageFrame.destroy(), getDetailsPage()])
    detailsButton.place(x=290, y=350)

    # Button for currentBalance
    currentBalanceButton = Button(pageFrame, text='''Check
Current
Balance''', width=14, height=7, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda:[pageFrame.destroy(), checkBalancePage()])
    currentBalanceButton.place(x=590, y=350)

    # Back button
    backButton = Button(pageFrame, text='Back', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), HomePage()])
    backButton.place(x=50, y=20)

def RFCMSCorrectorPage():
    suggestion = RFODSuggestions()

    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app (Consumption & Transfer)
    pageFrame.create_text(50, 75, text="RFCMS Correction", fill="blue", anchor='nw', font=('Calibri', 20, 'underline'))

    # Drop down for deciding increase or decrease
    changeType = ['Increase', 'Decrease']
    var = StringVar()
    var.set(changeType[0])
    pageFrame.create_text(50, 396, text="Type Of Change :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    typeOfChange = OptionMenu(pageFrame, var, *changeType)
    typeOfChange.place(x=220, y=395, width=300)

    # Entry Field for Name.
    pageFrame.create_text(50, 146, text="Name :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    name = AutocompleteEntry(suggestion, pageFrame)
    name.place(x=220, y=150, width=500)

    # Entry Field Quantity
    pageFrame.create_text(50, 446, text="Batch No :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    batch = Entry(pageFrame)
    batch.place(x=220, y=450)

    # Entry Field Batch No.
    pageFrame.create_text(50, 496, text="Quantity Of Change :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    quantity = Entry(pageFrame)
    quantity.place(x=220, y=500)

    # Entry field for date
    pageFrame.create_text(50, 196, text="Entry Date :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    entryDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    entryDate.place(x=220, y=200)

    # indent Maker for validation and submition
    def RFCMSCorrectorValidationAndSubmition():
        if(len(name.get())==0):
            messagebox.showerror(title='Error', message='Missing Name!!')
            name.delete(0, 'end')
            name.focus()
            return

        elif(len(batch.get())==0):
            messagebox.showerror(title='Error', message='Missing Batch No !!')
            batch.delete(0, 'end')
            batch.focus()
            return

        elif(len(quantity.get())==0):
            messagebox.showerror(title='Error', message='Missing Quantity of change!!')
            quantity.delete(0, 'end')
            quantity.focus()
            return
        
        currentQuantity = getCurrentQuantity(name.get(), entryDate.get_date(), batch.get())
        receivedQuantity = getReceivedQuantity(name.get(), entryDate.get_date(), batch.get())
        currentBalance = int(currentBalanceGet(name.get()))

        if(receivedQuantity <= 0):
            messagebox.showerror(title='Error', message='Enter details properly..!')
            quantity.delete(0, 'end')
            batch.delete(0, 'end')
            quantity.focus()
            return

        if(receivedQuantity < int(quantity.get()) and var.get() == 'Decrease'):
            messagebox.showerror(title='Error', message='You have only received '+str(receivedQuantity)+' medicines..!')
            quantity.delete(0, 'end')
            quantity.focus()
            return

        elif(currentBalance < int(quantity.get()) and var.get() == 'Decrease'):
            messagebox.showerror(title='Error', message='Can not make change due to low balance..!')
            quantity.delete(0, 'end')
            quantity.focus()
            return

        if(var.get() == "Increase"):
            confirmation = RFCMSIncreaseDB(name.get(), int(quantity.get()), entryDate.get_date(), dt.datetime.now().strftime("%Y-%m-%d"), batch.get())
            
        else:
            confirmation = RFCMSDecreaseDB(name.get(), int(quantity.get()), entryDate.get_date(), dt.datetime.now().strftime("%Y-%m-%d"), batch.get(), currentQuantity)
        
        if(confirmation):
            messagebox.showinfo(title='Done', message='Changes done successfully your current balance is '+currentBalanceGet(name.get())+'!')
            pageFrame.destroy()
            mistakeCorrectorPage()

        else:
            messagebox.showerror(title='Error', message='An error occurred in correction..!')
             
    # submit button from form submition
    submitButton = Button(pageFrame, text='Submit', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [RFCMSCorrectorValidationAndSubmition()])
    submitButton.place(x=220, y=550)

    # back button
    backButton = Button(pageFrame, text='  Back  ',width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), mistakeCorrectorPage()])
    backButton.place(x=50, y=20)

def LPPMJAKCorrectorPage():
    suggestion = RFODSuggestions()

    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app (Consumption & Transfer)
    pageFrame.create_text(50, 75, text="LP/PMJAK Correction", fill="blue", anchor='nw', font=('Calibri', 20, 'underline'))

    # Drop down for deciding increase or decrease
    changeType = ['Increase', 'Decrease']
    var = StringVar()
    var.set(changeType[0])
    pageFrame.create_text(50, 446, text="Type Of Change :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    typeOfChange = OptionMenu(pageFrame, var, *changeType)
    typeOfChange.place(x=220, y=445, width=300)

    # Drop down for deciding lp or pmjak
    options = ['LP', 'PMJAK']
    var1 = StringVar()
    var1.set(options[0])
    pageFrame.create_text(50, 196, text="Type Of Purchase :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    LPOrPMJAK = OptionMenu(pageFrame, var1, *options)
    LPOrPMJAK.place(x=220, y=195, width=300)

    # Entry Field for Name.
    pageFrame.create_text(50, 146, text="Name :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    name = AutocompleteEntry(suggestion, pageFrame)
    name.place(x=220, y=150, width=500)

    # Entry Field Quantity
    pageFrame.create_text(50, 496, text="Batch No :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    batch = Entry(pageFrame)
    batch.place(x=220, y=500)

    # Entry Field Batch No.
    pageFrame.create_text(50, 546, text="Quantity Of Change :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    quantity = Entry(pageFrame)
    quantity.place(x=220, y=550)

    # Entry field for date
    pageFrame.create_text(50, 246, text="Entry Date :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    entryDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    entryDate.place(x=220, y=250)

    # indent Maker for validation and submition
    def LPPMJAKCorrectorValidationAndSubmition():
        if(len(name.get())==0):
            messagebox.showerror(title='Error', message='Missing Name!!')
            name.delete(0, 'end')
            name.focus()
            return

        elif(len(batch.get())==0):
            messagebox.showerror(title='Error', message='Missing Batch No !!')
            batch.delete(0, 'end')
            batch.focus()
            return

        elif(len(quantity.get())==0):
            messagebox.showerror(title='Error', message='Missing Quantity of change!!')
            quantity.delete(0, 'end')
            quantity.focus()
            return
        
        currentQuantity = getCurrentQuantity(name.get(), entryDate.get_date(), batch.get())
        receivedQuantity = getReceivedQuantity(name.get(), entryDate.get_date(), batch.get())
        currentBalance = int(currentBalanceGet(name.get()))

        if(receivedQuantity <= 0):
            messagebox.showerror(title='Error', message='Enter details properly..!')
            quantity.delete(0, 'end')
            batch.delete(0, 'end')
            quantity.focus()
            return

        if(receivedQuantity < int(quantity.get()) and var.get() == 'Decrease'):
            messagebox.showerror(title='Error', message='You have only received '+str(receivedQuantity)+' medicines..!')
            quantity.delete(0, 'end')
            quantity.focus()
            return

        elif(currentBalance < int(quantity.get()) and var.get() == 'Decrease'):
            messagebox.showerror(title='Error', message='Can not make change due to low balance..!')
            quantity.delete(0, 'end')
            quantity.focus()
            return

        if(var.get() == "Increase"):
            if(var1.get() == "LP"):
                confirmation = LPIncreaseDB(name.get(), int(quantity.get()), entryDate.get_date(), dt.datetime.now().strftime("%Y-%m-%d"), batch.get())
            else:
                confirmation = PMJAKIncreaseDB(name.get(), int(quantity.get()), entryDate.get_date(), dt.datetime.now().strftime("%Y-%m-%d"), batch.get())
            
        else:
            if(var1.get() == "LP"):
                confirmation = LPDecreaseDB(name.get(), int(quantity.get()), entryDate.get_date(), dt.datetime.now().strftime("%Y-%m-%d"), batch.get(), currentQuantity)
            else:
                confirmation = PMJAKDecreaseDB(name.get(), int(quantity.get()), entryDate.get_date(), dt.datetime.now().strftime("%Y-%m-%d"), batch.get(), currentQuantity)
        
        if(confirmation):
            messagebox.showinfo(title='Done', message='Changes done successfully your current balance is '+currentBalanceGet(name.get())+'!')
            pageFrame.destroy()
            mistakeCorrectorPage()

        else:
            messagebox.showerror(title='Error', message='An error occurred in correction..!')
            quantity.delete(0, 'end')
            batch.delete(0, 'end')
            name.delete(0, 'end')
            name.focus()
            return
      
    # submit button from form submition
    submitButton = Button(pageFrame, text='Submit', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [LPPMJAKCorrectorValidationAndSubmition()])
    submitButton.place(x=220, y=600)

    # back button
    backButton = Button(pageFrame, text='  Back  ',width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), mistakeCorrectorPage()])
    backButton.place(x=50, y=20)

def OBCorrectorPage():
    suggestion = RFODSuggestions()

    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app (Consumption & Transfer)
    pageFrame.create_text(50, 75, text="OB Correction", fill="blue", anchor='nw', font=('Calibri', 20, 'underline'))

    # Drop down for deciding increase or decrease
    changeType = ['Increase', 'Decrease']
    var = StringVar()
    var.set(changeType[0])
    pageFrame.create_text(50, 396, text="Type Of Change :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    typeOfChange = OptionMenu(pageFrame, var, *changeType)
    typeOfChange.place(x=220, y=395, width=300)

    # Entry Field for Name.
    pageFrame.create_text(50, 146, text="Name :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    name = AutocompleteEntry(suggestion, pageFrame)
    name.place(x=220, y=150, width=500)

    # Entry Field Quantity
    pageFrame.create_text(50, 446, text="Batch No :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    batch = Entry(pageFrame)
    batch.place(x=220, y=450)

    # Entry Field Batch No.
    pageFrame.create_text(50, 496, text="Quantity Of Change :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    quantity = Entry(pageFrame)
    quantity.place(x=220, y=500)

    # Entry field for date
    pageFrame.create_text(50, 196, text="Entry Date :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    entryDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    entryDate.place(x=220, y=200)


    # indent Maker for validation and submition
    def OBCorrectorValidationAndSubmition():
        if(len(name.get())==0):
            messagebox.showerror(title='Error', message='Missing Name!!')
            name.delete(0, 'end')
            name.focus()
            return

        elif(len(batch.get())==0):
            messagebox.showerror(title='Error', message='Missing Batch No !!')
            batch.delete(0, 'end')
            batch.focus()
            return

        elif(len(quantity.get())==0):
            messagebox.showerror(title='Error', message='Missing Quantity of change!!')
            quantity.delete(0, 'end')
            quantity.focus()
            return
        
        currentQuantity = getCurrentQuantity(name.get(), entryDate.get_date(), batch.get())
        receivedQuantity = getReceivedQuantity(name.get(), entryDate.get_date(), batch.get())
        currentBalance = int(currentBalanceGet(name.get()))

        if(receivedQuantity <= 0):
            messagebox.showerror(title='Error', message='Enter details properly..!')
            quantity.delete(0, 'end')
            batch.delete(0, 'end')
            quantity.focus()
            return

        if(receivedQuantity < int(quantity.get()) and var.get() == 'Decrease'):
            messagebox.showerror(title='Error', message='You have only received '+str(receivedQuantity)+' medicines..!')
            quantity.delete(0, 'end')
            quantity.focus()
            return

        elif(currentBalance < int(quantity.get()) and var.get() == 'Decrease'):
            messagebox.showerror(title='Error', message='Can not make change due to low balance..!')
            quantity.delete(0, 'end')
            quantity.focus()
            return

        if(var.get() == "Increase"):
            confirmation = OBIncreaseDB(name.get(), int(quantity.get()), entryDate.get_date(), dt.datetime.now().strftime("%Y-%m-%d"), batch.get())
            
        else:
            confirmation = OBDecreaseDB(name.get(), int(quantity.get()), entryDate.get_date(), dt.datetime.now().strftime("%Y-%m-%d"), batch.get(), currentQuantity)
        
        if(confirmation):
            messagebox.showinfo(title='Done', message='Changes done successfully your current balance is '+currentBalanceGet(name.get())+'!')
            pageFrame.destroy()
            mistakeCorrectorPage()

        else:
            messagebox.showerror(title='Error', message='An error occurred in correction..!')
              
    # submit button from form submition
    submitButton = Button(pageFrame, text='Submit', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [OBCorrectorValidationAndSubmition()])
    submitButton.place(x=220, y=550)

    # back button
    backButton = Button(pageFrame, text='  Back  ',width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), mistakeCorrectorPage()])
    backButton.place(x=50, y=20)

def transferCorrectorPage():
    suggestion = RFODSuggestions()

    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app (Consumption & Transfer)
    pageFrame.create_text(50, 75, text="Transfer Correction", fill="blue", anchor='nw', font=('Calibri', 20, 'underline'))

    # Drop down for deciding increase or decrease
    changeType = ['Increase', 'Decrease']
    var = StringVar()
    var.set(changeType[0])
    pageFrame.create_text(50, 396, text="Type Of Change :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    typeOfChange = OptionMenu(pageFrame, var, *changeType)
    typeOfChange.place(x=220, y=395, width=300)

    # Entry Field for Name.
    pageFrame.create_text(50, 146, text="Name :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    name = AutocompleteEntry(suggestion, pageFrame)
    name.place(x=220, y=150, width=500)

    # Entry Field Quantity
    pageFrame.create_text(50, 446, text="Batch No :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    batch = Entry(pageFrame)
    batch.place(x=220, y=450)

    # Entry Field Batch No.
    pageFrame.create_text(50, 496, text="Quantity Of Change :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    quantity = Entry(pageFrame)
    quantity.place(x=220, y=500)

    # Entry field for date
    pageFrame.create_text(50, 196, text="Entry Date :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    entryDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    entryDate.place(x=220, y=200)

    # indent Maker for validation and submition
    def transferCorrectorValidationAndSubmition():
        if(len(name.get())==0):
            messagebox.showerror(title='Error', message='Missing Name!!')
            name.delete(0, 'end')
            name.focus()
            return

        elif(len(batch.get())==0):
            messagebox.showerror(title='Error', message='Missing Batch No !!')
            batch.delete(0, 'end')
            batch.focus()
            return

        elif(len(quantity.get())==0):
            messagebox.showerror(title='Error', message='Missing Quantity of change!!')
            quantity.delete(0, 'end')
            quantity.focus()
            return
        
        currentBalance = int(currentBalanceGet(name.get()))
        transferQuantity = getTransferQuantity(name.get(), entryDate.get_date())

        if(currentBalance < int(quantity.get()) and var.get() == 'Increase'):
            messagebox.showerror(title='Error', message='Can not make change due to low balance..!')
            quantity.delete(0, 'end')
            quantity.focus()
            return

        elif(transferQuantity < int(quantity.get()) and var.get() == 'Decrease'):
            messagebox.showerror(title='Error', message='You have only transfered '+ str(transferQuantity) +' medicines..!')
            quantity.delete(0, 'end')
            quantity.focus()
            return

        if(var.get() == "Increase"):
            confirmation = transferIncreaseDB(name.get(), int(quantity.get()), entryDate.get_date(), dt.datetime.now().strftime("%Y-%m-%d"))
            
        else:
            confirmation = transferDecreaseDB(name.get(), int(quantity.get()), entryDate.get_date(), dt.datetime.now().strftime("%Y-%m-%d"))
        
        if(confirmation):
            messagebox.showinfo(title='Done', message='Changes done successfully your current balance is '+currentBalanceGet(name.get())+'!')
            pageFrame.destroy()
            mistakeCorrectorPage()

        else:
            messagebox.showerror(title='Error', message='An error occurred in correction..!')
              
    # submit button from form submition
    submitButton = Button(pageFrame, text='Submit', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [transferCorrectorValidationAndSubmition()])
    submitButton.place(x=220, y=550)

    # back button
    backButton = Button(pageFrame, text='  Back  ',width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), mistakeCorrectorPage()])
    backButton.place(x=50, y=20)

def otherCorrectorPage():
    suggestion = RFODSuggestions()

    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app (Corrections)
    pageFrame.create_text(50, 58, text="Other Correction", fill="blue", anchor='nw', font=('Calibri', 20, 'underline'))

    # Entry Field for Name.
    pageFrame.create_text(50, 106, text="Name :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    name = AutocompleteEntry(suggestion, pageFrame)
    name.place(x=220, y=110, width=500)

    # Entry Field Quantity
    pageFrame.create_text(50, 336, text="Batch No(old) :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    batchOld = Entry(pageFrame)
    batchOld.place(x=220, y=340)

    # Entry Field Batch No.
    pageFrame.create_text(490, 336, text="Batch No(New) :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    batchNew = Entry(pageFrame)
    batchNew.place(x=640, y=340)

    # Entry field for date
    pageFrame.create_text(50, 146, text="Entry Date :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    entryDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    entryDate.place(x=220, y=150)

    # Entry field for date
    pageFrame.create_text(50, 376, text="Expiry Date(old) :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    expDateOld = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    expDateOld.place(x=220, y=380)

    # Entry field for date
    pageFrame.create_text(490, 376, text="Expiry Date(new) :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    expDateNew = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    expDateNew.place(x=640, y=380)

    # indent Maker for validation and submition
    def otherCorrectorValidationAndSubmition():
        if(len(name.get())==0):
            messagebox.showerror(title='Error', message='Missing Name!!')
            name.delete(0, 'end')
            name.focus()
            return

        elif(len(batchOld.get())==0):
            messagebox.showerror(title='Error', message='Missing Batch No !!')
            batchOld.delete(0, 'end')
            batchOld.focus()
            return

        elif(len(batchNew.get())==0):
            messagebox.showerror(title='Error', message='Missing Batch No !!')
            batchNew.delete(0, 'end')
            batchNew.focus()
            return

        if(otherChangesDB(name.get(), expDateOld.get_date(), expDateNew.get_date(), entryDate.get_date(), batchOld.get(), batchNew.get())):
            messagebox.showinfo(title='Done',message='Changes Done Successfully..!')
            pageFrame.destroy()
            return mistakeCorrectorPage()

        else:
            messagebox.showerror(title='Error', message='Error occurred in changes(May be incorrect details)..!!')
            batchNew.delete(0, 'end')
            batchNew.focus()
            batchOld.delete(0, 'end')
            batchOld.focus()
            name.delete(0, 'end')
            name.focus()
            return
                      
    # submit button from form submition
    submitButton = Button(pageFrame, text='Submit', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [otherCorrectorValidationAndSubmition()])
    submitButton.place(x=500,y=580)

    # back button
    backButton = Button(pageFrame, text='  Back  ',width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), mistakeCorrectorPage()])
    backButton.place(x=50, y=20)

def deleteMedicinePage():
    suggestion = RFODSuggestions()

    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app (Corrections)
    pageFrame.create_text(50, 75, text="Delete Medicine", fill="blue", anchor='nw', font=('Calibri', 20, 'underline'))

    # Entry Field for Name.
    pageFrame.create_text(50, 146, text="Name :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    name = AutocompleteEntry(suggestion, pageFrame)
    name.place(x=220, y=150, width=500)

    # indent Maker for validation and submition
    def deleteMedicineValidationAndSubmition():
        if(len(name.get())==0):
            messagebox.showerror(title='Error', message='Missing Name!!')
            name.delete(0, 'end')
            name.focus()
            return

        if(deleteMedicineDB(name.get())):
            messagebox.showinfo(title='Done',message='Medicine Deleted Successfully..!')
            pageFrame.destroy()
            return mistakeCorrectorPage()

        else:
            messagebox.showerror(title='Error', message='Error occurred in changes(May be incorrect details)..!!')
            name.delete(0, 'end')
            name.focus()
            return

    # submit button from form submition
    submitButton = Button(pageFrame, text='Submit', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [deleteMedicineValidationAndSubmition()])
    submitButton.place(x=220, y=220)

    # back button
    backButton = Button(pageFrame, text='  Back  ',width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), mistakeCorrectorPage()])
    backButton.place(x=50, y=20)

def checkBalancePage():
    suggestion = RFODSuggestions()

    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app (Corrections)
    pageFrame.create_text(50, 75, text="Current Balance", fill="blue", anchor='nw', font=('Calibri', 20, 'underline'))

    # Entry Field for Name.
    pageFrame.create_text(50, 146, text="Username :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    name = AutocompleteEntry(suggestion, pageFrame)
    name.place(x=200, y=150, width=500)

    # indent Maker for validation and submition
    def checkBalanceValidationAndSubmition():
        if(len(name.get())==0):
            messagebox.showerror(title='Error', message='Missing Name!!')
            name.delete(0, 'end')
            name.focus()
            return

        try:
            messagebox.showinfo(title='Done',message= "your current Balnce is "+str(currentBalanceGet(name.get())))
            pageFrame.destroy()
            return othersPage()

        except:
            messagebox.showerror(title='Error', message='Error occurred (May be incorrect details)..!!')
            name.delete(0, 'end')
            name.focus()
            return

    # submit button from form submition
    submitButton = Button(pageFrame, text='Submit', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [checkBalanceValidationAndSubmition()])
    submitButton.place(x=200, y=220)

    # back button
    backButton = Button(pageFrame, text='  Back  ', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), othersPage()])
    backButton.place(x=50, y=20)

def getDetailsPage():
    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app (Data-Entry)
    pageFrame.create_text(400, 50, text="Get Details", fill="blue", anchor='nw', font=('Calibri', 30, 'underline', 'bold'))

    # Button for receive data entry
    receiveButton = Button(pageFrame, text='''Current
Stock''', width=20, height=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), currentStockPage()])
    receiveButton.place(x=250, y=200)

    # Button for usage data entry
    useButton = Button(pageFrame, text='''Used
Stock''', width=20, height=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), usedStockPage()])
    useButton.place(x=550, y=200)

    # Back button
    backButton = Button(pageFrame, text='Back', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), othersPage()])
    backButton.place(x=50, y=20)

def currentStockPage():
    suggestion = RFODSuggestions()

    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app (Corrections)
    pageFrame.create_text(50, 75, text="Current Stock Details", fill="blue", anchor='nw', font=('Calibri', 20, 'underline'))

    # Entry Field for Name.
    pageFrame.create_text(50, 146, text="Name :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    name = AutocompleteEntry(suggestion, pageFrame)
    name.place(x=200, y=150, width=500)

    # Entry field for PDF name
    pageFrame.create_text(50, 196, text="PDF Name :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    PDFName = Entry(pageFrame)
    PDFName.place(x=200, y=200)

    # indent Maker for validation and submition
    def currentStockValidationAndSubmition():
        if(len(name.get())==0):
            messagebox.showerror(title='Error', message='Missing Name!!')
            name.delete(0, 'end')
            name.focus()
            return

        elif(len(name.get())==0):
            messagebox.showerror(title='Error', message='Missing PDF Name!!')
            PDFName.delete(0, 'end')
            PDFName.focus()
            return

        currentStockPDF(pageFrame, name.get(), PDFName.get())

    # submit button from form submition
    submitButton = Button(pageFrame, text='Submit', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [currentStockValidationAndSubmition()])
    submitButton.place(x=200, y=260)

    # back button
    backButton = Button(pageFrame, text='  Back  ', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), getDetailsPage()])
    backButton.place(x=50, y=20)

def currentStockPDF(pageFrame, name, PDFName):
    try:
        # getting data and arraging it
        result = currentStockData(name)
        styles = getSampleStyleSheet()
        data = []
        
        for i in range(len(result)):
            subData = []
            subData.append(i)
            subData.append(dt.datetime.strftime(dt.datetime.strptime(result[i][0], "%Y-%m-%d"), "%d/%m/%Y"))
            subData.append(Paragraph(result[i][1], styles['Normal']))
            subData.append(Paragraph(result[i][2], styles['Normal']))
            subData.append(result[i][3])
            subData.append(dt.datetime.strftime(dt.datetime.strptime(result[i][4], "%Y-%m-%d"), "%d/%m/%Y"))
            data.append(subData)
        
        # table style decorations
        elements = []
        
        t = Table(data, colWidths=[40,85,120,90,70,85])

        t.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                            ]))
        elements.append(t)

        # class for footer and header
        class FooterCanvas(canvas.Canvas):

            def __init__(self, *args, **kwargs):
                canvas.Canvas.__init__(self, *args, **kwargs)
                self.pages = []

            def showPage(self):
                self.pages.append(dict(self.__dict__))
                self._startPage()

            def save(self):
                page_count = len(self.pages)
                for page in self.pages:
                    self.__dict__.update(page)
                    self.draw_canvas(page_count)
                    canvas.Canvas.showPage(self)
                canvas.Canvas.save(self)

            # designing footer and header
            def draw_canvas(self, page_count):
                page = "Page %s of %s" % (self._pageNumber, page_count)
                self.saveState()
                self.setStrokeColorRGB(0, 0, 0)
                self.setLineWidth(0.5)
                self.setFont('Times-Roman', 10)
                self.drawString(10, 10, page)
                self.drawString(57, 720, "INDEX")
                self.drawString(120, 720, "DATE")
                self.drawString(210, 720, "BATCH NO.")
                self.drawString(330, 720, "TYPE")
                self.drawString(395, 720, "QUANTITY")
                self.drawString(475, 720, "EXP. DATE")
                self.line(52.5,710,52.5,735)
                self.line(92.5,710,92.5,735)
                self.line(177.5,710,177.5,735)
                self.line(297.5,710,297.5,735)
                self.line(387.5,710,387.5,735)
                self.line(457.5,710,457.5,735)
                self.line(542.5,710,542.5,735)
                self.line(52.5,735,542.5,735)
                self.setFont('Times-Roman', 13)
                self.drawString(57, 745, "MEDICINE: "+name)
                self.drawString(260, 770, "CURRENT STOCK")

                self.restoreState()

        # Building PDF
        save_name = os.path.join(os.path.expanduser("~"), "Desktop/", PDFName+".pdf")
        doc = SimpleDocTemplate(save_name, pagesize=portrait(A4), topMargin=125, leftMargin=10, rightMargin=10)
        doc.multiBuild(elements, canvasmaker=FooterCanvas)
        messagebox.showinfo(title='Success!', message='Your PDF Has Been Created Successfully on desktop with name "'+PDFName+'" ..!')
        pageFrame.destroy()
        getDetailsPage()

    except:
        messagebox.showerror(title='Error', message='An error occurred in creating PDF')
        pageFrame.destroy()
        getDetailsPage()

def usedStockPage():
    suggestion = RFODSuggestions()

    # Creating frame for DataEntry Page
    pageFrame = GradientFrame(MainScreen, "black", "grey", borderwidth=0.05, relief="sunken", width=1000, height= 640)
    pageFrame.pack()

    # Title Label for the app (Corrections)
    pageFrame.create_text(50, 75, text="Used Stock Details", fill="blue", anchor='nw', font=('Calibri', 20, 'underline'))

    # Entry Field for Name.
    pageFrame.create_text(50, 146, text="Name :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    name = AutocompleteEntry(suggestion, pageFrame)
    name.place(x=200, y=150, width=500)

    # Entry field for PDF name
    pageFrame.create_text(50, 396, text="PDF Name :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    PDFName = Entry(pageFrame)
    PDFName.place(x=200, y=400)

    # Entry field for date
    pageFrame.create_text(50, 196, text="From:", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    startDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    startDate.place(x=200, y=200)

    # Entry field for date
    pageFrame.create_text(540, 196, text="To :", fill="white", anchor='nw', font=('Calibri', 14), justify='center')
    endDate = Calendar(pageFrame,state="normal",firstweekday="monday",showweeknumbers=False,date_pattern="y-mm-dd",foreground="black")
    endDate.place(x=650, y=200)

    # indent Maker for validation and submition
    def usedStockValidationAndSubmition():
        if(len(name.get())==0):
            messagebox.showerror(title='Error', message='Missing Name!!')
            name.delete(0, 'end')
            name.focus()
            return

        elif(len(name.get())==0):
            messagebox.showerror(title='Error', message='Missing PDF Name!!')
            PDFName.delete(0, 'end')
            PDFName.focus()
            return

        usedStockPDF(pageFrame, name.get(), PDFName.get(), startDate.get_date(), endDate.get_date())

    # submit button from form submition
    submitButton = Button(pageFrame, text='Submit', width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [usedStockValidationAndSubmition()])
    submitButton.place(x=200, y=460)

    # back button
    backButton = Button(pageFrame, text='  Back  ',width=10, bg='grey', fg='black', justify='center', font=('Calibri', 12, 'bold', 'underline'), command=lambda: [pageFrame.destroy(), getDetailsPage()])
    backButton.place(x=50, y=20)

def usedStockPDF(pageFrame, name, PDFName, startDate, endDate):
    try:
        # getting data and arraging it
        result = usedStockData(name, startDate, endDate)
        styles = getSampleStyleSheet()
        data = []

        for i in range(len(result)):
            subData = []
            subData.append(i)
            subData.append(dt.datetime.strftime(dt.datetime.strptime(result[i][0], "%Y-%m-%d"), "%d/%m/%Y"))
            subData.append(Paragraph(result[i][1], styles['Normal']))
            subData.append(Paragraph(result[i][2], styles['Normal']))
            subData.append(result[i][3])
            subData.append(dt.datetime.strftime(dt.datetime.strptime(result[i][4], "%Y-%m-%d"), "%d/%m/%Y"))
            data.append(subData)
        # table style decorations
        elements = []
        t = Table(data, colWidths=[40,85,120,90,70,85])

        t.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                            ]))
        elements.append(t)

        # class for footer and header
        class FooterCanvas(canvas.Canvas):

            def __init__(self, *args, **kwargs):
                canvas.Canvas.__init__(self, *args, **kwargs)
                self.pages = []

            def showPage(self):
                self.pages.append(dict(self.__dict__))
                self._startPage()

            def save(self):
                page_count = len(self.pages)
                for page in self.pages:
                    self.__dict__.update(page)
                    self.draw_canvas(page_count)
                    canvas.Canvas.showPage(self)
                canvas.Canvas.save(self)

            # designing footer and header
            def draw_canvas(self, page_count):
                page = "Page %s of %s" % (self._pageNumber, page_count)
                self.saveState()
                self.setStrokeColorRGB(0, 0, 0)
                self.setLineWidth(0.5)
                self.setFont('Times-Roman', 10)
                self.drawString(10, 10, page)
                self.drawString(57, 720, "INDEX")
                self.drawString(120, 720, "DATE")
                self.drawString(210, 720, "BATCH NO.")
                self.drawString(330, 720, "TYPE")
                self.drawString(395, 720, "QUANTITY")
                self.drawString(475, 720, "EXP. DATE")
                self.line(52.5,710,52.5,735)
                self.line(92.5,710,92.5,735)
                self.line(177.5,710,177.5,735)
                self.line(297.5,710,297.5,735)
                self.line(387.5,710,387.5,735)
                self.line(457.5,710,457.5,735)
                self.line(542.5,710,542.5,735)
                self.line(52.5,735,542.5,735)
                self.setFont('Times-Roman', 13)
                self.drawString(57, 745, "MEDICINE: "+name)
                self.drawString(260, 770, "USED STOCK")

                self.restoreState()

        # Building PDF
        save_name = os.path.join(os.path.expanduser("~"), "Desktop/", PDFName+".pdf")
        doc = SimpleDocTemplate(save_name, pagesize=portrait(A4), topMargin=125, leftMargin=10, rightMargin=10)
        doc.multiBuild(elements, canvasmaker=FooterCanvas)
        messagebox.showinfo(title='Success!', message='Your PDF Has Been Created Successfully on desktop with name "'+PDFName+'" ..!')
        pageFrame.destroy()
        getDetailsPage()

    except:
        messagebox.showerror(title='Error', message='An error occurred in creating PDF')
        pageFrame.destroy()
        getDetailsPage()

LoginPage()
MainScreen.mainloop()
adminDataBase.close()

