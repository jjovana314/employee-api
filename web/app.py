from flask import jsonify, Flask, request
from flask_restful import Resources, Api
from pymongo import MongoClient
from exceptions import SchemaError
from datetime import datetime
from resources.CompanyEmployeeData import CompanyEmployeeData
from resources.PersonalEmployeeData import PersonalEmployeeData
import json
import helper

# todo: write docstrings and comments in all modules
# TODO: finish API

app = Flask(__main__)
api = Api(app)

mongo_client = MongoClient("mongodb:/db:27017")
db = mongo_client.EmployeeData
personal = db["Personal"]
company = db["Company"]

schema = {}
with open("schema.json", "r") as f:
    schema = json.load(f, encoding="utf-8")

company_employee_keys = [
    "_id",
    "index",
    "guid",
    "isActive",
    "balance",
    "company",
    "registered",
    "range",
]

personal_employee_keys = [
    "name",
    "phone",
    "address",
    "email",
    "picture",
    "age",
    "eyeColor",
    "about",
    "latitude",
    "longitude",
    "tags",
    "friends",
    "greeting",
    "favorite_fruit",
]

dict_all_data = {}
list_all_dicts = []


class Employee(Resources):
    def post(self):
        data = request.get_json()

        for dictionary in data:
            try:
                helper.validate_schema(schema, dictionary)
            except SchemaError as ex:
                return jsonify({"message": ex.args[0], "code": ex.args[1]})

            for key, value in dictionary:
                if key in company_employee_keys:
                    company_data.append(value)
                elif key in personal_employee_keys:
                    personal_data.append(value)
            try:
                company_object = CompanyEmployeeData(*company_data)
                personal_object = PersonalEmployeeData(*personal_data)
            except ValueError as ex:
                return jsonify({"message": ex.args[0], "code": ex.args[1]})

            personal_values = personal_object.return_values_personal()
            company_values = company_object.return_values_company()
            personal_dict = zip(personal_employee_keys, personal_values)
            company_dict = zip(company_employee_keys, company_values)
            # todo: merge two dictionaries
            # todo: add them in list
            # todo: test code


api.add_resource("/employee_data", Employee)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
