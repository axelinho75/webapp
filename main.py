from flask import Flask, request

app = Flask(__name__)

def generated_random_page_title():
    return "Index Page Title"

@app.route("/")
def page_index():
    return "<p>Hello, World!</p><a href=\"/pagesb\">Page B</a>"

@app.route("/pagesb")
def page_b():
    nb = int(request.args.get('nb', '0'))
    a_list = ['<a href="/">Index</a>' for _ in range(nb)]

    return "<p>This is Page B</p> ".join(a_list)