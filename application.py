#this is to be treated as the MAIN FILE. This is what the user will interact with... integrate with the ANExtension files in another project file.


#https://www.tutorialspoint.com/flask/flask_application.htm
#Concider use of a FLASK APPLICATION... this will run seperately of the extension... but serve data to the background of the extension.
#Therefore it will need to implement the MESSAGING to the context.js that will be necessary.

#HELPFUL BREAKDOWN: https://vsupalov.com/flask-web-server-in-production/
#Even more helpful breakdown of the Production STACK!!!: https://levelup.gitconnected.com/serving-flask-applications-with-gunicorn-and-nginx-reverse-proxy-fe26217af226

from flask import Flask, request, json, jsonify, Response, render_template
from annotator import Annotator
#from user import User

#BERT in python: NLP and future work impact
#Paper includes follow-on study and detailed explaination of program/structure
#Working Demo
#Performance Impacts --> does this significantly slow down browsing/the web
#does it take too long to load..

#Show that it's useful and also don't impact performance too much

application = Flask(__name__)


def home():
    return render_template("home.html")

def about():
    return render_template("about.html")

def studyInfo():
    return render_template("information.html")

def study():
    #The user enters their unique pin.
    #They fill out a corresponding survey that populates.
    #those survey results then determine which URLs populate for a user to view.
    #They are presented with a link to download the extension.
    #They enter their study pin into the Extension as well.
    #Then they go through the URLS.
    return render_template("study.html")

def loadExtension():
    # error = None
    print(request.form)
    if request.method == 'POST':
        data = request.form
        if data['user_current_url'] and data['user_token']:
            #the treatment sent by the server is a function of the URL and User's Study Pin
            url = data['user_current_url']
            entirewebsitestring = data['website_contents']
            studyPin = data['user_token']

            #giving the Annotator the studyPin might be useful if linking Pre-Survey data
            #actually will determine some of the annotation content.
            annotator = Annotator(url, studyPin)
            return json.dumps(annotator.getDataObject())
        else:
            return "ERROR"

application.add_url_rule("/", view_func=home)
application.add_url_rule("/about/", view_func=about)
application.add_url_rule("/study-information/", view_func=studyInfo)
application.add_url_rule("/study/", view_func=study)
application.add_url_rule("/loadextension", view_func=loadExtension, methods=["POST"])

if __name__ == '__main__':
    application.debug = True
    application.run()
