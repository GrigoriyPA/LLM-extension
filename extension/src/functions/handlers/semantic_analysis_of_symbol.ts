import * as vscode from "vscode";

import { buildRequestWithSymbolContex } from "../request_functions";

import { sendRequest } from "../../utils/http_server/requests_functions";
import { SemanticAnalysisOfSymbol } from "../../utils/http_server/requests_structures";

import { SymbolKind } from "../../utils/lsp/lsp_helpers";

import { applyIndent } from "../../utils/functions";
import { logEntry } from "../../utils/logger";

import { LogLevel, Components } from "../../config";

function logMessage(logLevel: LogLevel, message: string) {
    logEntry(
        logLevel,
        Components.REQUESTS_PROCESSOR,
        `[Semantic Analysis Of Symbol] ${message}`
    );
}

export const semanticAnalysisOfSymbol = async (
    textEditor: vscode.TextEditor,
    edit: vscode.TextEditorEdit
) => {
    logMessage(LogLevel.TRACE, "Compute request");

    const buildRequestPromise = buildRequestWithSymbolContex(
        textEditor.document,
        textEditor.selection.active,
        SymbolKind.VARIABLE
    );

    return buildRequestPromise.then((request) => {
        if (request === undefined) {
            // TODO: @ganvas show this information in pretty window
            logMessage(LogLevel.DEBUG, "Is not a variable defenition");
            return;
        }

        const requestPromise = sendRequest(
            new SemanticAnalysisOfSymbol.Request(request)
        );

        return requestPromise.then((response) => {
            return computeResponse(
                textEditor,
                SemanticAnalysisOfSymbol.Response.deserialize(response)
            );
        });
    });
};

function computeResponse(
    textEditor: vscode.TextEditor,
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

    // TODO: @ganvas | @GrigoriyPA show window with information instead of inserting semantic analysis
    return insertSemanticAnalysis(textEditor, response.content);
}

function insertSemanticAnalysis(
    textEditor: vscode.TextEditor,
    semanticAnalysis: string
) {
    const lineWithSymbol = textEditor.document.lineAt(
        textEditor.selection.active.line
    );

    const suggestionContent = applyIndent(
        lineWithSymbol.firstNonWhitespaceCharacterIndex,
        semanticAnalysis.trimEnd(),
        "# "
    );

    textEditor.edit((edit: vscode.TextEditorEdit) => {
        edit.insert(lineWithSymbol.range.start, suggestionContent);
    });
}
