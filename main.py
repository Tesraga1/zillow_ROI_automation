from scraper import search
from flask import Flask, render_template


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

app = Flask(__name__)
@app.route("/")
def home():
    return render_template('index.html')
if __name__ == '__main__':
   app.run()