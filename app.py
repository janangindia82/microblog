import datetime
from flask import Flask, app, render_template, request
from flask import redirect, url_for
from pymongo import MongoClient
import urllib.parse 
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():

 app = Flask(__name__)


 # Use the encoded username and password in the connection string
 client = MongoClient(os.getenv("MONGODB_URI"))


 app.db = client.microblog

 entries = []

 try:
        db= client.get_database('microblog')
        collections= db.list_collection_names()
        print(f"Connected to DB. collections: {collections}") 
 except Exception as e:
        print(f"Error: {e}") 
    

 @app.route("/", methods=["GET","POST"])
 def home():
    
    
    if request.method == "POST":
        entry_content = request.form.get("content")
        format_date= datetime.datetime.today().strftime("%y-%m-%d")
        app.db.entries.insert_many({"content": entry_content, "date": format_date})
        return redirect(url_for("home"))
    entries_with_date= [
        (entry["content"], 
          entry["date"], 
          datetime.datetime.strptime(entry["date"], "%y-%m-%d").strftime("%b %d")
        )
        for entry in app.db.entries.find({})
    ]
    return render_template("home.html", entries=entries_with_date)

 if __name__ == "__main__":
    app.run(debug=True, port=5001)

 return app    
