import mariadb
from flask import Flask, request, Response
import json
import dbcreds
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/blog', methods=['GET', 'POST', 'PATCH', 'DELETE'])

def blog():
    if request.method == 'GET':
        conn = None
        cursor = None
        posts = None
        try:
            conn = mariadb.connect(host=dbcreds.host, port=dbcreds.port,user=dbcreds.user, password=dbcreds.password,database=dbcreds.database)
            cursor=conn.cursor()
            cursor.execute("SELECT * FROM blog")
            posts = cursor.fetchall()
        except Exception as error:
            print("Something went error(This is LAZY!): ")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(posts != None):
                return Response(json.dumps(posts, default=str), mimetype="application/json", status=200)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == 'POST':
        conn = None
        cursor = None
        blog_description = request.json.get("blog_description")
        rows=None
        try:
            conn = mariadb.connect(host=dbcreds.host, port=dbcreds.port,user=dbcreds.user, password=dbcreds.password,database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO blog(blog_description) VALUES(?)", [blog_description])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("Something went error(This is LAZY!): ")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("post inserted", mimetype="text/html", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "PATCH":
        conn = None
        cursor = None
        blog_completed = request.json.get("blog_description")
        blog_id = request.json.get("id")
        rows=None
        try:
            conn = mariadb.connect(host=dbcreds.host, port=dbcreds.port,user=dbcreds.user, password=dbcreds.password,database=dbcreds.database)
            cursor = conn.cursor()
          
            if blog_completed != ""and blog_completed != None:
                cursor.execute("UPDATE blog SET blog_description=? WHERE id=?", [blog_completed, blog_id])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("something went wrong(THIS IS LAZY")
            print(error)
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if (rows == 1):
                return Response("updated success", mimetype="text/html", status=204)
            else:
                return Response("update failed", mimetype="text/html", status=500)
    elif request.method == "DELETE":
        conn = None
        cursor = None
        blog_id = request.json.get("id")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, port=dbcreds.port,user=dbcreds.user, password=dbcreds.password,database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM blog WHERE id=?", [blog_id])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("something went wrong(THIS IS LAZY")
            print(error)
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if (rows == 1):
                return Response("Delete success", mimetype="text/html", status=204)
            else:
                return Response("Delete failed", mimetype="text/html", status=500)