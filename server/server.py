from flask import Flask, request
from server_config import REQUIRED_FIELDS
import json

from src.database.database_entities import Function, SemanticSense, AutoComplete
from src.constants.language_models import DocstringModels, TestGenerationModels, AutoCompleteModels, SemanticSenseModels
from waitress import serve

app = Flask(__name__)

def document_function(function: Function):
    print("Getting document of function...")
    return DocstringModels.finetuned_microsoft_phi3.value.generate_result(function)


def semantic_analysis_of_symbol(variable: SemanticSense):
    print("Getting semantic_analysis_of_symbol...")
    result = SemanticSenseModels.microsoft_phi3.value.generate_result(variable).replace('\n', '<br />')
    return "<p>" + result + "</p>"


def generate_tests(function: Function):
    print("Generating tests for function...")
    return TestGenerationModels.finetuned_microsoft_phi3.value.generate_result(function)


def completion_suggestion(variable: AutoComplete):
    print("Getting completion suggestions...")
    return [AutoCompleteModels.microsoft_phi3.value.generate_result(variable)]


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
                f = Function(function_name="", code=symbol_content)
                response["single_string"] = document_function(f)
            case "SemanticAnalysisOfSymbol":
                f = SemanticSense(symbol_content, json.dumps(references_content))
                response["single_string"] = semantic_analysis_of_symbol(f)
            case "GenerateTests":
                f = Function(function_name="", code=symbol_content, context=json.dumps(references_content))
                response["single_string"] = generate_tests(f)
            case "CompletionSuggestion":
                f = AutoComplete(code=symbol_content)
                response["multiple_strings"] = completion_suggestion(f)
            case _:
                response["error_message"] = f"Unknown request type: {request_type}."
    except Exception as error:
        response["error_message"] = str(error)
    return json.dumps(response)


serve(app, port=80, threads=1)
