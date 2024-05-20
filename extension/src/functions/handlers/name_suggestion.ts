import * as vscode from "vscode";

import * as vscodelc from "vscode-languageclient/node";

import { buildRequestWithSymbolContex } from "../request_functions";
import { describeSymbolAtPosition } from "../find_functions";

import { sendRequest } from "../../utils/http_server/requests_functions";
import { NameSuggestion } from "../../utils/http_server/requests_structures";

import { SymbolKind, FromVscodelc } from "../../utils/lsp/lsp_helpers";
import { renameSymbol } from "../../utils/lsp/lsp_methods";

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
        `[Name Suggestion]`,
        showInline
    );
}

export const nameSuggestion = async (
    textEditor: vscode.TextEditor,
    edit: vscode.TextEditorEdit
) => {
    logMessage(LogLevel.TRACE, "Compute request");

    const position = textEditor.selection.active;

    const symbolDescriptionPromise = describeSymbolAtPosition(
        textEditor.document,
        position,
        SymbolKind.UNKNOWN
    );

    return symbolDescriptionPromise.then((symbolDescription) => {
        if (symbolDescription === undefined) {
            // TODO: @ganvas show this information in pretty window
            logMessage(LogLevel.DEBUG, "Is not a named symbol", true);
            return;
        }

        return doNameSuggestion(textEditor, position, symbolDescription);
    });
};

async function doNameSuggestion(
    textEditor: vscode.TextEditor,
    position: vscode.Position,
    symbolDescription: vscodelc.DocumentSymbol
) {
    const targetSymbol = FromVscodelc.getSymbolKind(symbolDescription.kind);
    if (targetSymbol === SymbolKind.UNKNOWN) {
        // TODO: @ganvas show this information in pretty window
        logMessage(
            LogLevel.DEBUG,
            "Name suggestion is not supported for this symbol",
            true
        );
        return;
    }

    logMessage(LogLevel.TRACE, `Target symbol ${targetSymbol}`);

    const buildRequestPromise = buildRequestWithSymbolContex(
        textEditor.document,
        position,
        targetSymbol
    );

    return buildRequestPromise.then((request) => {
        if (request === undefined) {
            // TODO: @ganvas show this information in pretty window
            logMessage(LogLevel.DEBUG, "Is not a named symbol", true);
            return;
        }

        const requestPromise = sendRequest(new NameSuggestion.Request(request));

        return requestPromise.then((response) => {
            return computeResponse(
                textEditor,
                position,
                NameSuggestion.Response.deserialize(response)
            );
        });
    });
}

async function computeResponse(
    textEditor: vscode.TextEditor,
    position: vscode.Position,
    response: NameSuggestion.Response
) {
    if (!response.isSuccess()) {
        logMessage(
            LogLevel.ERROR,
            `Failed to compute request: ${response.getError()}`
        );
        return;
    }

    logMessage(
        LogLevel.TRACE,
        `Got name suggestion:\n${response.getDescription()}`
    );

    const selectionPromise = vscode.window.showQuickPick(response.contents, {
        canPickMany: false,
    });

    return selectionPromise.then((response) => {
        if (response === undefined) {
            return;
        }
        return insertNameSuggestion(textEditor, position, response);
    });
}

async function insertNameSuggestion(
    textEditor: vscode.TextEditor,
    position: vscode.Position,
    suggestion: string
) {
    const renameSymbolPromise = renameSymbol(
        textEditor.document,
        position,
        suggestion
    );

    return renameSymbolPromise.then((response) => {
        if (response === undefined || response.documentChanges === undefined) {
            return;
        }

        const renameSymbolEdit = new vscode.WorkspaceEdit();
        for (const change of response.documentChanges as vscodelc.TextDocumentEdit[]) {
            const refactorUri = FromVscodelc.getUri(change.textDocument);

            for (const edit of change.edits as vscodelc.TextEdit[]) {
                renameSymbolEdit.replace(
                    refactorUri,
                    FromVscodelc.getRange(edit.range),
                    edit.newText
                );
            }
        }

        return vscode.workspace.applyEdit(renameSymbolEdit).then((response) => {
            if (!response) {
                // TODO: @ganvas show this information in pretty window
                logMessage(LogLevel.DEBUG, "Failed to rename symbol", true);
                return;
            }
        });
    });
}
