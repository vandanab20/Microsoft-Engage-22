from flask import Flask, render_template, request, flash
from models import *
from flask_moment import Moment
import requests
import os
import face_recognition
from sklearn import svm
from datetime import datetime
import logging
from lmao import *
# logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
# logging.debug('This message should go to the log file')

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
moment = Moment(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'urlinfo.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.secret_key = "super secret key"

db.init_app(app)


@app.route('/')
def home():
    return render_template("Home.html")

@app.route('/About')
def about():
    return render_template("About.html")

@app.route('/Contact_Us')
def contactus():
    return render_template("Contact_Us.html")


@app.route('/Attendance', methods=["GET", "POST"])
def capture():
    print("hellooooooo")
    # return "Hello"
    """Display UI to capture/save an image"""
    if request.method == "POST":
        try:
            imgur_id = request.values.get("imageID")
            latitude = request.values.get("latitude")
            longitude = request.values.get("longitude")

            print(f"Image id is {imgur_id}")

            img_link = f"https://i.imgur.com/{imgur_id}.jpg"
            # Download the image from img_link
            resp = requests.get(img_link)
            with open('./images/' + imgur_id + '.jpg', 'wb') as f:
                f.write(resp.content)

            name = f_recognize('./images/train/',f'./images/{imgur_id}.jpg')

            print(f"After f_recognize ||||| {name[:-5]}")

            # return render_template("test.html",uname = name)

            # save image path along with latitude longitude in the database
            image = CameraImage(imgur_id=imgur_id, latitude=latitude, longitude=longitude)

            db.session.add(image)
            db.session.commit()
            return name

        except Exception as e:
            return "And error occurred!"
            # return apology("An error occured....")
            # pass

    else:
        print("hello")
        return render_template("capture.html")

@app.route('/lmao')
def lmao():
    return render_template("test.html")

@app.route('/display')
def display():
    """Display all captured images"""
    images = CameraImage.query.order_by(CameraImage.id.desc()).all()

    if len(images) == 0:
        flash("No captured images found !")
    else:
        flash("Showing all captured images......")

    return render_template("display.html", images=images)

def main():
    """Create initial database tables"""
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()
    app.run(port=8080)
