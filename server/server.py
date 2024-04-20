from flask import Flask, request
from server_config import REQUIRED_FIELDS
import json

from src.database_entities import Function
from constants.language_models import LanguageModel
from waitress import serve

app = Flask(__name__)

def document_function(function: Function):
    print("Getting document of function...")
    return LanguageModel.codellama_python_7b.value.generate_docstring(function)


def semantic_analysis_of_symbol(some_args=None):
    print("Getting semantic_analysis_of_symbol...")
    return "Some analysis"


def name_suggestion(some_args=None):
    print("Getting name suggestion...")
    return "Some name suggestion"


def generate_tests(some_args=None):
    print("Generating tests for function...")
    return "Some tests"


def completion_suggestion(some_args=None):
    print("Getting completion suggestions...")
    return ["Suggestion 1", "Suggestion 2"]


@app.route("/", methods=['GET', 'POST'])
def handle_request():
    if request.method == 'GET':
        return 'SOME GET REQUEST'
    response = {
        "error_message": "",
        "single_string": "",
        "multiple_strings": []
    }
    data = request.json
    for field in REQUIRED_FIELDS:
        if field not in data:
            response["error_message"] = f"No '{field}' field in request."
            return json.dumps(response)

    request_type = data["type_of_request"]
    symbol_content = data["symbol_content"]
    references_content = data["references_content"]

    try:
        match request_type:
            case "DocumentFunction":
                f = Function("", symbol_content, references_content[0], "")
                response["single_string"] = document_function(f)
            case "SemanticAnalysisOfSymbol":
                response["single_string"] = semantic_analysis_of_symbol(symbol_content)
            case "NameSuggestion":
                response["single_string"] = name_suggestion(symbol_content)
            case "GenerateTests":
                response["single_string"] = generate_tests(symbol_content)
            case "CompletionSuggestion":
                response["multiple_strings"] = completion_suggestion(symbol_content)
            case _:
                response["error_message"] = f"Unknown request type: {request_type}."
    except Exception as error:
        response["error_message"] = str(error)
    return json.dumps(response)


serve(app, port=80)
