from Scraper.Linkedin_scraper import Linkdin
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import os

class LoginWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("400x300")
        self.login()
        self.configure(bg="gray")
    def login(self):
        Label(self, text="Username", font=("Tahoma"),bg="white").pack(pady=10)
        self.username = Entry(self)
        self.username.pack()
        Label(self, text="Password", font=("Tahoma"),bg="white").pack(pady=10)
        self.password = Entry(self, show="*")
        self.password.pack()
        self.button1 = Button(self, text="Login", command=self.login_check).pack(pady=20)
    def login_check(self):
        User = self.username.get()
        PW = self.password.get()
        if User and PW:
            self.destroy()
            app = LinkdinApp(User, PW)
            app.mainloop()
        else:
            self.label = Label(self, text="Enter Your Information", fg="red").pack()

class LinkdinApp(Tk):
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        self.title("Linkdin Job Search")
        self.geometry("700x500")
        self.Structure()
    def Structure(self):
        Label(self, text="Welcome", font=("Tahoma",15)).pack(pady=5)
        Label(self, text="Enter Your Job : ", font=("Tahoma")).pack(pady=10)
        self.enter1 = Entry(self)
        self.enter1.pack()
        Label(self, text="Enter Your Result : ", font=("Tahoma")).pack(pady=10)
        self.enter2 = Entry(self)
        self.enter2.pack()
        self.entry_level = IntVar()
        check1 = Checkbutton(self, text="Entry", variable=self.entry_level)
        check1.pack()
        self.mid_senior_level = IntVar()
        check2 = Checkbutton(self, text="Mid-senior", variable=self.mid_senior_level)
        check2.pack()
        self.modes = [("CSV","CSV"),("SQLite","SQLite")]
        self.choice = StringVar()
        self.choice.set("CSV")
        for text,mode in self.modes:
            Radiobutton(self,text=text,variable=self.choice,value=mode).pack()

        self.button2 = (Button(self, text="Search",command=self.Operation, font=("tahoma")))
        self.button2.pack()
        Button(self, text="Open File", command=self.OpenFile, font=("tahoma")).pack(pady=10)

        menubar = Menu(self)
        filemenu = Menu(menubar,tearoff=0)
        filemenu.add_command(label="info",command=self.Info)
        filemenu.add_command(label="exit", command=self.Quit)
        menubar.add_cascade(label="File",menu=filemenu)
        menubar.add_cascade(label="Help",command=self.Help)
        self.config(menu=menubar)
    def Operation(self):
        username = self.username
        password = self.password
        titel_job = self.enter1.get()
        result = self.enter2.get()
        entry = self.entry_level.get()
        mid_senior = self.mid_senior_level.get()
        CSV_SQLite = self.choice.get()
        scraper = Linkdin(username,password)
        try :
            scraper.SearchJob(titel_job)
            scraper.FilterLevel(entry, mid_senior)
            scraper.Information(result)
            scraper.SaveResults(CSV_SQLite)
            self.button2.config(bg="green", fg="white")
            scraper.CloseChrome()
            messagebox.showinfo("Info","Your file has been saved successfully.")
        except :
            messagebox.showerror("Error", "The error might be due to a slow internet connection or the job title may not exist. Please try a different job title or Please close the app and try again.")
            self.button2.config(bg="red", fg="white")

    def Info(self):
        messagebox.showinfo("Info",
        "This application allows you to search for LinkedIn job postings by entering a job title and the number of results you want. You can choose to save the results in either CSV or SQLite format.\n\n Developed by Taymaz\n\n Tay.nobari@gmail.com")

    def Help(self):
        messagebox.showinfo("Help",
        "🔹 How to Use the Application:\n\n"
        "1. Enter your LinkedIn username and password on the login screen.\n"
        "2. Type the job title you're searching for.\n"
        "3. Specify how many job results you want.\n"
        "4. Choose the job experience level:\n"
        "   - Entry: For beginner/entry-level roles\n"
        "   - Mid-senior: For more experienced professionals\n"
        "   -(You can select one or both)\n"
        "5. Choose where to save the results: CSV file or SQLite database.\n"
        "6. Click the 'Search' button to start searching.\n"
        "7. Click the 'Open File' button to view the saved file.\n\n"
        "The program will collect job information from LinkedIn and save it accordingly.\n\n"
        "⚠️ Make sure your LinkedIn account is accessible and not protected by extra security.\n\n"
        "💡 Tip: Be patient while it loads the data. If login takes time, don't close the browser window and complete the checkpoint if shown.\n\n"
        " Help by Taymaz")

    def Quit(self):
        answer = messagebox.askyesno("Quit","Do want to exit?")
        if answer:
            self.destroy()

    def OpenFile(self):
        Openfile = filedialog.askopenfilename(title="Open File",filetypes=[("CSV Files", "*.csv"), ("DB Files", "*.db")])
        if Openfile:
            os.startfile(Openfile)