import pandas as pd
import sqlite3

class SaveFile():

    def __init__(self, list1):
        self.list1 = list1

    def SaveToCSV(self):
        cols = ["Job Title", "Company", "Location", "Link"]
        df = pd.DataFrame(self.list1, columns=cols)
        df.to_csv("CSV.csv")
        print("Saved successfully")

    def SaveToSQLite(self):
        self.con = sqlite3.connect("SQLite_db.db")
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS Jobs(Job Title TEXT, Company TEXT, Location TEXT, Link TEXT)")
        self.cur.executemany("INSERT INTO Jobs VALUES (?, ?, ?, ?)", self.list1)
        self.con.commit()
        self.con.close()
        print("Saved successfully")