import * as vscode from "vscode";

import { buildRequestWithSymbolContex } from "../request_functions";

import { sendRequest } from "../../utils/http_server/requests_functions";
import { DocumentFunction } from "../../utils/http_server/requests_structures";

import { SymbolKind } from "../../utils/lsp/lsp_helpers";

import { applyIndent } from "../../utils/functions";
import { logEntry } from "../../utils/logger";

import { LogLevel, Components } from "../../config";

function logMessage(logLevel: LogLevel, message: string) {
    logEntry(
        logLevel,
        Components.REQUESTS_PROCESSOR,
        `[Document Function] ${message}`
    );
}

export const documentFunction = async (
    textEditor: vscode.TextEditor,
    edit: vscode.TextEditorEdit
) => {
    logMessage(LogLevel.TRACE, "Compute request");

    const position = textEditor.selection.active;

    const buildRequestPromise = buildRequestWithSymbolContex(
        textEditor.document,
        position,
        SymbolKind.FUNCTION
    );

    return buildRequestPromise.then((request) => {
        if (request === undefined) {
            // TODO: @ganvas show this information in pretty window
            logMessage(LogLevel.DEBUG, "Is not a function defenition");
            return;
        }

        const requestPromise = sendRequest(
            new DocumentFunction.Request(request)
        );

        return requestPromise.then((response) => {
            return computeResponse(
                textEditor,
                position,
                DocumentFunction.Response.deserialize(response)
            );
        });
    });
};

function computeResponse(
    textEditor: vscode.TextEditor,
    position: vscode.Position,
    response: DocumentFunction.Response
) {
    if (!response.isSuccess()) {
        logMessage(
            LogLevel.ERROR,
            `Failed to compute request: ${response.getError()}`
        );
        return;
    }

    logMessage(LogLevel.TRACE, `Function documentation:\n${response.content}`);

    // TODO: @ganvas | @GrigoriyPA show dialog in separate window before inserting documentation
    return insertFunctionDocumentation(textEditor, position, response.content);
}

function insertFunctionDocumentation(
    textEditor: vscode.TextEditor,
    position: vscode.Position,
    documentation: string
) {
    const functionNameLine = textEditor.document.lineAt(position.line);

    let indentSize = textEditor.options.indentSize as number | undefined;
    if (indentSize === undefined) {
        logMessage(LogLevel.ERROR, "Failed to get text editor indent size");
        return;
    }
    indentSize += functionNameLine.firstNonWhitespaceCharacterIndex;

    const documentationContent = applyIndent(
        indentSize,
        "'''\n" + documentation.trimEnd() + "\n'''"
    );

    // TODO: @GrigoriyPA insert text in case of multiline function defenition
    // TODO: @GrigoriyPA replace function documentation
    textEditor.edit((edit: vscode.TextEditorEdit) => {
        edit.insert(
            functionNameLine.rangeIncludingLineBreak.end,
            documentationContent + "\n"
        );
    });
}
