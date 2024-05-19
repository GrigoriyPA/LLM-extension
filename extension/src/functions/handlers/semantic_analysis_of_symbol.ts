import * as vscode from "vscode";

import { buildRequestWithSymbolContex } from "../request_functions";

import { sendRequest } from "../../utils/http_server/requests_functions";
import { SemanticAnalysisOfSymbol } from "../../utils/http_server/requests_structures";

import { SymbolKind } from "../../utils/lsp/lsp_helpers";

import { logEntry } from "../../utils/logger";

import { LogLevel, Components } from "../../config";

function logMessage(logLevel: LogLevel, message: string) {
    logEntry(
        logLevel,
        Components.REQUESTS_PROCESSOR,
        `${message}`,
        `[Semantic Analysis Of Symbol]`
    );
}

export const semanticAnalysisOfSymbol = async (
    textEditor: vscode.TextEditor,
    edit: vscode.TextEditorEdit
) => {
    logMessage(LogLevel.TRACE, "Compute request");

    const position = textEditor.selection.active;

    const buildRequestPromise = buildRequestWithSymbolContex(
        textEditor.document,
        position,
        SymbolKind.UNKNOWN
    );

    return buildRequestPromise.then((request) => {
        if (request === undefined) {
            // TODO: @ganvas show this information in pretty window
            logMessage(LogLevel.DEBUG, "Is not a symbol definition");
            return;
        }

        const requestPromise = sendRequest(
            new SemanticAnalysisOfSymbol.Request(request)
        );

        return requestPromise.then((response) => {
            return computeResponse(
                textEditor,
                position,
                SemanticAnalysisOfSymbol.Response.deserialize(response)
            );
        });
    });
};

function computeResponse(
    textEditor: vscode.TextEditor,
    position: vscode.Position,
    response: SemanticAnalysisOfSymbol.Response
) {
    if (!response.isSuccess()) {
        logMessage(
            LogLevel.ERROR,
            `Failed to compute request: ${response.getError()}`
        );
        return;
    }

    logMessage(LogLevel.TRACE, `Got semantic analysis:\n${response.content}`);

    return showSemanticAnalysis(textEditor, position, response.content);
}

function showSemanticAnalysis(
    textEditor: vscode.TextEditor,
    position: vscode.Position,
    semanticAnalysis: string
) {
    // TODO: @ganvas | @GrigoriyPA show window with information in text editor

    const semanticAnalysisPanel = vscode.window.createWebviewPanel(
        "markdown.preview",
        "Semantic analysis",
        vscode.ViewColumn.Beside
    );
    semanticAnalysisPanel.webview.html = semanticAnalysis;
}
