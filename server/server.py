from flask import Flask, request

app = Flask(__name__)


def get_docstring(some_args=None):
    print("Getting docstring...")
    return 0


@app.route("/", methods=['POST'])
def handle_request():
    args = [(el, request.form[el]) for el in request.form.keys()]
    if "type_of_request" in request.form and request.form["type_of_request"] == "get_docstring":
        get_docstring()
    return "POST ARGUMENTS: " + str(args)


app.run()
