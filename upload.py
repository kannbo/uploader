from bottle import *
@route("/")
def sdjiof():
    return """
<form action="http://localhost:8080/upload" method="POST" enctype="multipart/form-data">
  <input name="file" type="file"><br>
  <input type="submit">
</form>"""
run(port="8000",host="localhost")
