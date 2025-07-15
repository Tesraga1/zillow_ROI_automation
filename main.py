from scraper import search, scrape_page, scrape_property_from_page
from flask import Flask, render_template, request
import sqlite3
import os
from db import get_db
from utils import calc_ROI

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
            address = request.form['address']
            if "www.zillow.com" in address:
                info = scrape_property_from_page(address)
                tax = scrape_page(address)
                db = get_db()
                if "rentZestimate" in info and "streetAddress" in info and "zpid" in info and "price" in info:
                    sql = ''' INSERT OR IGNORE INTO property(id,price,adr,imgid,roi)
                                        VALUES(?,?,?,?,?) '''
                    if tax != None:
                        roi = calc_ROI(info["price"], tax, info["rentZestimate"])
                        print(roi)
                        db.execute(
                            sql,
                            (info["zpid"], info["price"], info["streetAddress"], info["responsivePhotos"][0]["url"], roi),
                        )
                        db.commit()
                        cursor = db.execute('SELECT id,price,adr,imgid,roi FROM property')
                        return render_template("content.html", items = cursor.fetchall())
            else:
                info = search(address)
                db = get_db()
                if info:
                    #print(info[0][0]["zpid"])
                    try:
                        #print(info[0][0])
                        for x in info:
                            for prop in x:
                                sql = ''' INSERT OR IGNORE INTO property(id,price,adr,imgid,roi)
                                        VALUES(?,?,?,?,?) '''
                                if "hdpData" in prop and "address" in prop and "zpid" in prop and "imgSrc" in prop and "unformattedPrice" in prop:
                                    if "homeInfo" in prop["hdpData"]:
                                        if "rentZestimate" in prop["hdpData"]["homeInfo"]:
                                            print(f"Scraping {prop['detailUrl']}")
                                            tax = scrape_page(prop["detailUrl"])
                                            print(f"Finished scraping {prop['detailUrl']}")
                                            if tax != None:
                                                roi = calc_ROI(prop["unformattedPrice"], tax, prop["hdpData"]["homeInfo"]["rentZestimate"])
                                                print(prop["zpid"])
                                                db.execute(
                                                    sql,
                                                    (prop["zpid"], prop["unformattedPrice"], prop["address"], prop["imgSrc"], roi),
                                                )
                                                db.commit()
                        print("Worked")
                    except Exception as e:
                        print("Didnt work cause of ", e)
                    else:
                        cursor = db.execute('SELECT id,price,adr,imgid,roi FROM property')
                        return render_template("content.html", items = cursor.fetchall())
        return render_template('index.html')
    import db
    db.init_app(app)

    return app