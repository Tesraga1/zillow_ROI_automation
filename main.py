from scraper import search
from flask import Flask, render_template
import os

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
    
    @app.route("/")
    def home():
        p = search("New York, NY")
        print(p)
        return render_template('index.html', input_list = p)
    
    import db
    db.init_app(app)

   
    return app