import * as vscode from "vscode";

import { buildRequestWithSymbolContex } from "../request_functions";

import { sendRequest } from "../../utils/http_server/requests_functions";
import { DocumentFunction } from "../../utils/http_server/requests_structures";

import { SymbolKind } from "../../utils/lsp/lsp_helpers";

import { applyIndent } from "../../utils/functions";
import { LogLevel, Components, logEntry } from "../../utils/logger";

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

export const documentFunction = async (
    textEditor: vscode.TextEditor,
    edit: vscode.TextEditorEdit
) => {
    logMessage(LogLevel.TRACE, "Compute request");

    const request = await buildRequestWithSymbolContex(
        textEditor.document,
        textEditor.selection.active,
        SymbolKind.FUNCTION
    );
    if (request === undefined) {
        // TODO: @ganvas show this information in pretty window
        logMessage(LogLevel.DEBUG, "Is not a function defenition");
        return;
    }

    // TODO: @GrigoriyPA subscribe on promise instead of wait
    const response = DocumentFunction.Response.deserialize(
        await sendRequest(new DocumentFunction.Request(request))
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
    await insertFunctionDocumentation(textEditor, response.content);
};
