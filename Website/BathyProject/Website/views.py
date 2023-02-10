from flask import Blueprint, render_template, request, redirect, url_for
import os
import matplotlib
import matplotlib.pyplot
from .FullScript import sub80samples
from .FullScript import Script_3000
matplotlib.use('Agg')

path = os.getcwd() + "\\Website\\static\\DataFiles"
entries = os.listdir(path)
views = Blueprint('views', __name__)


@views.route("/BathymetryML/", defaults={'filename': None, 'filename2': None}, methods=['GET', 'POST'])
@views.route("/BathymetryML/<filename>/<filename2>", methods=['GET', 'POST'])
def BathymetryML(filename, filename2):
    if request.method == 'POST':
        print(request.form)

        for i in request.form:
            if i == "PythonGo":
                machine(filename, filename2)
                return render_template("BathymetryML.html", parseComplete=True)

        return render_template("BathymetryML.html")

    return render_template("BathymetryML.html")


@views.route("/dragAndDrop/", methods=['GET', 'POST'])
def dragAndDrop():
    return redirect(url_for("views.home"))


@views.route("/", methods=['GET', 'POST'])
def home():
    for i in request.form:
        if i == "filePick":
            userInput = request.form.get("filePick")
            userOutput = request.form.get("filePick2")
            print(userInput)
            return redirect(url_for("views.BathymetryML", filename=userInput, filename2=userOutput))

    return render_template("dragAndDrop.html", len=len(entries), entries=entries)


@views.route("/testPage/", methods=['GET', 'POST'])
def testPage():
    if request.method == 'POST':
        for i in request.form:
            if i == "loadAnimation":
                return render_template("testPage.html", a="../static/BrainAnimationVid0001-0125.mp4")

    return render_template("testPage.html")


@views.route("/outputPage/", methods=['GET', 'POST'])
def outputPage():
    return render_template("outputPage.html")


def machine(filename, filename2):
    dfMain = sub80samples(filename)
    dfMain = dfMain['sample']
    dfMain.to_csv('Website/static/CleanData/clean80.csv')
    DF_3000 = Script_3000(filename2)
    DF_3000.to_csv('Website/static/CleanData/DF_3000.csv')
