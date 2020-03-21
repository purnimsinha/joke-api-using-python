#all the libraries*********************************************
#****************************************************************
from flask import Flask, jsonify, request
import pymysql
import datetime
from flask_restful import Resource, Api
import random
import functools

#***********************************************************************

#initialize the main app********************************************
app = Flask(__name__)
api = Api(app)


# class initialization********************************************
class Getjoke(Resource):
    def get(self):
        db =pymysql.connect("remotemysql.com","LiPpX6hf3B","IxgBOHqjsj","LiPpX6hf3B")
        cursor = db.cursor()
        query = """SELECT count(j_id) FROM joke_tbl"""
        cursor.execute(query)
        data = cursor.fetchall()
        db.commit()

        
        #to convert the tuple into integer*********************************************
        res = functools.reduce(lambda sub, ele: sub * 10 + ele, data)
        res2 = functools.reduce(lambda sub, ele: sub * 10 + ele, res)

        
        #to select the random number************************************************
        random_id=random.randint(1,res2)
        
        query = """SELECT * FROM joke_tbl where j_id={}""".format(random_id)
        cursor.execute(query)
        data = cursor.fetchall()
        payload = []
        content = {}
        for row in data:
            print(row)
            content = { 'j_title': row[1], 'j_desc': row[2]}
            payload.append(content)
        db.close()
        return jsonify(payload)

   

class Postjoke(Resource):
     def post(self):
        some_json = request.get_json()
        today_date = datetime.date.today()
        db = pymysql.connect("remotemysql.com","LiPpX6hf3B","IxgBOHqjsj","LiPpX6hf3B")
        cursor = db.cursor()
        query = """insert into joke_tbl(j_title,j_desc,j_date) values('{}','{}','{}')""".format(some_json["j_title"],some_json["j_desc"],str(today_date))
        print(query)
        cursor.execute(query)
        db.commit()
        return{'response': "record inserted successfully!"},202


api.add_resource(Getjoke, '/jokes/api/V1.0/joke')
api.add_resource(Postjoke, '/jokes/api/V1.0/joke')


if __name__ == "__main__":
    app.run(debug=True)
    
