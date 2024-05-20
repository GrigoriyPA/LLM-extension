import * as vscode from "vscode";

import { getContextForPosition } from "../find_functions";

import { sendRequest } from "../../utils/http_server/requests_functions";
import {
    RequestsBase,
    CompletionSuggestion,
} from "../../utils/http_server/requests_structures";

import { logEntry } from "../../utils/logger";

import { LogLevel, Components } from "../../config";

function logMessage(
    logLevel: LogLevel,
    message: string,
    showInline: boolean = false
) {
    logEntry(
        logLevel,
        Components.REQUESTS_PROCESSOR,
        `${message}`,
        `[Completion Suggestion]`,
        showInline
    );
}

export const completionSuggestion = async (
    textEditor: vscode.TextEditor,
    edit: vscode.TextEditorEdit
) => {
    logMessage(LogLevel.TRACE, "Compute request");

    const document = textEditor.document;
    const position = textEditor.selection.active;

    // TODO: @ZenMan123 | @GrigoriyPA pass more info for suggestion
    const request = new RequestsBase.RequestWithSymbolContextBase(
        getContextForPosition(document, position),
        [getContextForPosition(document, position)]
    );

    const requestPromise = sendRequest(
        new CompletionSuggestion.Request(request)
    );

    return requestPromise.then((response) => {
        return computeResponse(
            CompletionSuggestion.Response.deserialize(response),
            textEditor,
            position
        );
    });
};

async function computeResponse(
    response: CompletionSuggestion.Response,
    textEditor: vscode.TextEditor,
    position: vscode.Position
) {
    if (!response.isSuccess()) {
        logMessage(
            LogLevel.ERROR,
            `Failed to compute request: ${response.getError()}`
        );
        return;
    }

    // TODO: @ZenMan123 | @GrigoriyPA provide symbol completion continuously

    logMessage(
        LogLevel.TRACE,
        `Completion suggestions:\n${response.getDescription()}`
    );

    let snippet = new vscode.SnippetString();
    snippet.appendChoice(response.contents);

    return textEditor.insertSnippet(snippet, position).then((response) => {
        return;
    });
}
