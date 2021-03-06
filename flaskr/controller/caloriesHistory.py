from flask import request, jsonify, Blueprint
import datetime

caloriesHistory_page = Blueprint('caloriesHistory.py', __name__, template_folder='templates')

calories_dict = {}


@caloriesHistory_page.route("/home/storeCalories", methods=['POST'])
def store_calories():
    data = request.get_json()
    body = data['body']
    date = body['key']
    currDate = datetime.datetime.now()
    if len(date) == 0:
        date = str(currDate.month) + "/" + str(currDate.day)
    if(body['value'] == ''):
        return jsonify({'state': 'Please type in Calories or Search food'})
    if date in calories_dict.keys():
        calories = body['value']
        calories_dict[date] = int(calories_dict[date]) + int(calories)
        return jsonify({'state': 'successful updated'})
    calories = body['value']
    calories_dict[date] = calories
    return jsonify({'state': 'successful stored'})


@caloriesHistory_page.route("/home/getAllCalories", methods=['GET'])
def get_all_calories():
    calories_list = []
    for key in calories_dict:
        date_calories = str(key) + ": " + str(calories_dict[key])
        calories_list.append(date_calories)
    return jsonify({'state': calories_list})


@caloriesHistory_page.route("/home/getCalories", methods=['POST'])
def get_date_calories():
    data = request.get_json()
    date = data['body']
    if date in calories_dict:
        print(calories_dict)
        return jsonify({'state': calories_dict[date]})
    else:
        return jsonify({'state': 'please enter date or store data first'})