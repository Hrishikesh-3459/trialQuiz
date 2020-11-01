import xlrd
from flask import Flask, render_template, request, jsonify
import requests
import pymongo
from pymongo import MongoClient
from flask_cors import CORS
from flask_cors import cross_origin


app = Flask(__name__)
CORS(app)

location = ("Question bank.xlsx")
wb = xlrd.open_workbook(location)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)

client = pymongo.MongoClient(
    "mongodb+srv://trialquiz:sharad@cluster0.wxjq5.mongodb.net/dbquiz?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.dbquiz

db.test.insert_one({"name": "Yajat"})

questions = []

for r in range(5, 15):
    tmp = {}
    tmp["question"] = str(sheet.cell_value(r, 1))

    i = 1
    for c in range(2, 6):
        tmp[f"choice{i}"] = (str(sheet.cell_value(r, c)))
        if str(sheet.cell_value(r, 6)) == str(sheet.cell_value(r, c)):
            tmp["answer"] = i
        i += 1

    # tmp["answer"] = str(sheet.cell_value(r, c+1))

    # tmp = jsonify(question=q, choice1=choices[0], choice2=choices[1],
    #   choice3 = choices[2], choice4 = choices[3], answer = answer)
    questions.append(tmp)

# print(questions)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/getQuestions')
def game():
    return jsonify(questions)


@app.route('/updateScores', methods=["GET", "POST"])
def highscores():
    postData = request.get_json()
    print(postData)
    return jsonify(True)
