from flask import Flask, request, Blueprint
from datetime import date
import psycopg2
import json
from .logReg import _getUsername

nutrition_page = Blueprint('nutrition_page', __name__, template_folder='templates')


# Function handles GET and POST requests from react. POST updates database with new user info. GET returns current
# user history
@nutrition_page.route('/profile/nutrition/submit', methods=['POST', 'GET'])
def nutritionSubmit():
    if request.method == 'GET':
        number = _getUsername()
        conn = psycopg2.connect(
            database='teamfit',
            user='root',
            port=26257,
            host='localhost',
            sslmode='disable'
        )
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM teamfit.nutrition")
            row = cur.fetchall()
            for i in range(len(row)):
                if number in row[i]:
                    idXtra, nutHistory = row[i]
                    data = json.dumps(nutHistory)
                    jsonData = json.loads(data)
                    #finishedData = json.dumps(jsonData)
                    finishedData = {'calories': [1804, 361], 'date': ['12/06/20', '12/07/20'],
                                    'weight': [201, 150]}

                    return finishedData
        #newHistory = """{"calories": [], "date": [], "weight": []}"""
        newHistory = {'calories': [1804, 361], 'date': ['12/06/20', '12/07/20'],
                                    'weight': [201, 150]}
        return newHistory
    if request.method == 'POST':
        nutritionInfo = request.get_json()
        protein = nutritionInfo['protein']
        carbs = nutritionInfo['carbs']
        fat = nutritionInfo['fat']
        weight = nutritionInfo['weight']
        number = _getUsername()
        today = date.today()
        dateformat = today.strftime("%m/%d/%y")
        calories = ((9 * int(fat)) + (4 * int(protein)) + (4 * int(carbs)))
        # Save this info to user  in database
        conn = psycopg2.connect(
            database='teamfit',
            user='root',
            port=26257,
            host='localhost',
            sslmode='disable'
        )
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM teamfit.nutrition")
            row = cur.fetchall()
            for i in range(len(row)):
                if number in row[i]:
                    idXtra, nutHistory = row[i]
                    data = json.dumps(nutHistory)
                    jsonData = json.loads(data)
                    jsonData['date'].append(dateformat)
                    jsonData['calories'].append(int(calories))
                    jsonData['weight'].append(int(weight))
                    finishedData = json.dumps(jsonData)
                    sql = 'UPDATE nutrition set history = %s WHERE id =%s'
                    val = (finishedData, number)
                    cur.execute(sql, val)
                    conn.commit()
                    return "Info has been processed"
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM teamfit.nutrition")
            newData = """{"calories": [], "date": [], "weight": []}"""
            newjsonData = json.loads(newData)
            newjsonData['date'].append(dateformat)
            newjsonData['calories'].append(int(calories))
            newjsonData['weight'].append(int(weight))
            finaljsonData = json.dumps(newjsonData)
            sql2 = 'INSERT INTO teamfit.nutrition (id, history) VALUES (%s,%s)'
            val2 = (number, finaljsonData)
            cur.execute(sql2, val2)
            conn.commit()
        return "User added to database with new info"
    newHistory = """{"calories": [], "date": [], "weight": []}"""
    return newHistory
