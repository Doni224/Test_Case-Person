import re
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

# inisialisasi object library
app = Flask(__name__)
api = Api(app)

CORS(app)
db = SQLAlchemy(app)

# mongkonfigurasi dulu database
basedir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database

# Membuat database model
class ModelDatabase(db.Model):
    # membuat field/kolom
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.Integer)
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False
db.create_all()
identitas = {}
# Membuat class untuk restfull 
class ContohResource(Resource):
#MEMBUAT DATA
    def post(self):
        query = ModelDatabase.query.all()
        output = [
            {
                "id":data.id,
                "name":data.name,
                 "umur":data.phone  
            } 
            for data in query
        ]
        dataName = request.form["name"]
        dataPhone = request.form["phone"]
        model = ModelDatabase(name=dataName, phone=dataPhone)
        model.save()
        response = {
            "code": 200,
            "msg" : "Berhasil membuat data",
            "data": output
        }
        return response, 200
#INDEX
    def get(self):
        query = ModelDatabase.query.all()
        output = [
            {
                "id":data.id,
                "name":data.name,
                "phone":data.phone 
            } 
            for data in query
        ]

        response = {
            "code" : 200, 
            "msg"  : "Berhasil Manampilkan Data",
            "data" : output
        }

        return response, 200

    #EDIT DATA
class UpdateResource(Resource):
    def put(self, id):
        query = ModelDatabase.query.all()
        output = [
            {
                "id":data.id,
                "name":data.name,
                "phone":data.phone 
            } 
            for data in query
        ]
        query = ModelDatabase.query.all()
        query = ModelDatabase.query.get(id)
        # form untuk pegeditan data
        editNama = request.form["name"]
        editPhone =request.form["phone"]
        # mereplace nilai yang ada di setiap field/kolom
        query.name = editNama
        query.phone = editPhone
        db.session.commit()
        response = {
            "code": 200,
            "msg" : "edit data berhasil"},{
            "data": output
        }
        return response, 200
 # delete by id, bukan delete all
    def delete(self, id):
        query = ModelDatabase.query.all()
        output = [
            {
                "id":data.id,
                "name":data.name,
                "phone":data.phone
            } 
            for data in query
        ]
        queryData = ModelDatabase.query.get(id)
        # panggil methode untuk delete data by id
        db.session.delete(queryData)
        db.session.commit()

        response = {
            "msg" : "delete data berhasil",
            "code" : 200,
            "data": output
        }
        return response, 200
#SHOW
    def show(self):
        query = ModelDatabase.query.all()
        output = [
            {
                "id":data.id,
                "name":data.name,
                "phone":data.phone
            } 
            for data in query
        ]

        response = {
            "code" : 200, 
            "msg"  : "Berhasil Mandapatkan Data",
            "data" : output
        }


api.add_resource(ContohResource, "/api", methods=["GET", "POST", "SHOW"])
api.add_resource(UpdateResource, "/api/<id>", methods=["PUT", "DELETE"])
if __name__ == "__main__":
    app.run(debug=True, port=5005)