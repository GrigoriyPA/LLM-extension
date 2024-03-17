import * as vscode from "vscode";

import { sendRequest } from "../utils/http_server/requests_functions";
import { DocumentFunction } from "../utils/http_server/requests_structures";

import { LogLevel, Components, logEntry } from "../utils/logger";

import { SymbolKind, buildRequestWithSymbolContex } from "./common";

function logMessage(logLevel: LogLevel, message: string) {
    logEntry(
        logLevel,
        Components.REQUESTS_PROCESSOR,
        `[Document Function] ${message}`
    );
}

async function insertFunctionDocumentation(
    textEditor: vscode.TextEditor,
    documentation: string
) {
    const functionNameLine = textEditor.document.lineAt(
        textEditor.selection.active.line
    );

    const indentSize = textEditor.options.indentSize as number | undefined;
    if (indentSize === undefined) {
        logMessage(LogLevel.ERROR, "Failed to get text editor indent size");
        return;
    }

    const documentationIndent = " ".repeat(
        functionNameLine.firstNonWhitespaceCharacterIndex + indentSize
    );

    let documentationContent = documentationIndent + "'''\n";
    for (const documentationLine of documentation.split("\n")) {
        documentationContent += documentationIndent + documentationLine + "\n";
    }
    documentationContent += documentationIndent + "'''\n\n";

    // TODO: @GrigoriyPA insert text in case of multiline function defenition
    // TODO: @GrigoriyPA replace function documentation
    textEditor.edit((edit: vscode.TextEditorEdit) => {
        edit.insert(
            functionNameLine.rangeIncludingLineBreak.end,
            documentationContent
        );
    });
}

export const documentFunction = async (
    textEditor: vscode.TextEditor,
    edit: vscode.TextEditorEdit
) => {
    logMessage(LogLevel.TRACE, "Compute request");

    const doucument = textEditor.document;
    const position = textEditor.selection.active;
    const request = await buildRequestWithSymbolContex(
        doucument,
        position,
        SymbolKind.FUNCTION
    );
    if (request === undefined) {
        // TODO: @ganvas show this information in pretty window
        logMessage(LogLevel.DEBUG, "Is not a function defenition");
        return;
    }

    // TODO: @GrigoriyPA subscribe on promise instead of wait
    const response = DocumentFunction.Response.deserialize(
        await sendRequest(request)
    );
    if (!response.isSuccess()) {
        logMessage(
            LogLevel.ERROR,
            `Failed to compute request: ${response.getError()}`
        );
        return;
    }

    logMessage(LogLevel.TRACE, `Function documentation:\n${response.content}`);

    // TODO: @ganvas | @GrigoriyPA show dialog in separate window before inserting documentation
    insertFunctionDocumentation(textEditor, response.content);
};
