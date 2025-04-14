from scraper import search
from flask import Flask, render_template, request
import sqlite3
import os
from db import get_db

'''
if __name__ == "__main__":
    p = search("New York, NY")
    for y in range(len(p)):
        for x in range(len(p[0])):
            info = p[y][x]["hdpData"]["homeInfo"]
            print(info)
            if 'rentZestimate' not in info:
                print("Not in property")
'''
def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'zillow.db'),
        )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route("/", methods=('GET', 'POST'))
    def home():
        if request.method == 'POST':
            print("Worked")
            address = request.form['address'] 
            info = search(address)
            db = get_db()
            if info:
                print(info[0][0]["zpid"])
                try:
                    sql = ''' INSERT INTO property(id,price,otherinfo)
                              VALUES(?,?,?) '''
                    db.execute(
                        sql,
                        (info[0][0]["zpid"], info[0][0]["unformattedPrice"], info[0][0]["address"]),
                    )
                    db.commit()
                    print("Worked")
                except:
                    print("Didnt work")
        return render_template('index.html')
    
    import db
    db.init_app(app)

   
    return app