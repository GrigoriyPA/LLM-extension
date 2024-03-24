import * as vscode from "vscode";

import { sendRequest } from "../../utils/http_server/requests_functions";
import { SemanticAnalysisOfSymbol } from "../../utils/http_server/requests_structures";

import { SymbolKind } from "../../utils/lsp/lsp_helpers";

import { applyIndent } from "../../utils/functions";
import { LogLevel, Components, logEntry } from "../../utils/logger";

import { buildRequestWithSymbolContex } from "../common";

function logMessage(logLevel: LogLevel, message: string) {
    logEntry(
        logLevel,
        Components.REQUESTS_PROCESSOR,
        `[Semantic Analysis Of Symbol] ${message}`
    );
}

async function insertSemanticAnalysis(
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

export const semanticAnalysisOfSymbol = async (
    textEditor: vscode.TextEditor,
    edit: vscode.TextEditorEdit
) => {
    logMessage(LogLevel.TRACE, "Compute request");

    const request = await buildRequestWithSymbolContex(
        textEditor.document,
        textEditor.selection.active,
        SymbolKind.VARIABLE
    );
    if (request === undefined) {
        // TODO: @ganvas show this information in pretty window
        logMessage(LogLevel.DEBUG, "Is not a variable defenition");
        return;
    }

    // TODO: @GrigoriyPA subscribe on promise instead of wait
    const response = SemanticAnalysisOfSymbol.Response.deserialize(
        await sendRequest(new SemanticAnalysisOfSymbol.Request(request))
    );
    if (!response.isSuccess()) {
        logMessage(
            LogLevel.ERROR,
            `Failed to compute request: ${response.getError()}`
        );
        return;
    }

    logMessage(LogLevel.TRACE, `Got semantic analysis:\n${response.content}`);

    // TODO: @ganvas | @GrigoriyPA show window with information instead of inserting semantic analysis
    await insertSemanticAnalysis(textEditor, response.content);
};
