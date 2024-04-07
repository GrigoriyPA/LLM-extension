import * as vscode from "vscode";

import { buildRequestWithSymbolContex } from "../request_functions";
import { describeSymbolAtPosition } from "../find_functions";

import { sendRequest } from "../../utils/http_server/requests_functions";
import { NameSuggestion } from "../../utils/http_server/requests_structures";

import { SymbolKind, FromVscodelc } from "../../utils/lsp/lsp_helpers";

import { applyIndent } from "../../utils/functions";
import { LogLevel, Components, logEntry } from "../../utils/logger";

function logMessage(logLevel: LogLevel, message: string) {
    logEntry(
        logLevel,
        Components.REQUESTS_PROCESSOR,
        `[Name Suggestion] ${message}`
    );
}

async function insertNameSuggestion(
    textEditor: vscode.TextEditor,
    suggestion: string
) {
    // TODO: @GrigoriyPA refactor symbol name instead of inserting suggestion

    const lineWithSymbol = textEditor.document.lineAt(
        textEditor.selection.active.line
    );

    const suggestionContent = applyIndent(
        lineWithSymbol.firstNonWhitespaceCharacterIndex,
        suggestion.trimEnd(),
        "# "
    );

    textEditor.edit((edit: vscode.TextEditorEdit) => {
        edit.insert(lineWithSymbol.range.start, suggestionContent);
    });
}

export const nameSuggestion = async (
    textEditor: vscode.TextEditor,
    edit: vscode.TextEditorEdit
) => {
    logMessage(LogLevel.TRACE, "Compute request");

    // TODO: @GrigoriyPA suggest many names

    const document = textEditor.document;
    const position = textEditor.selection.active;

    const symbolDescription = await describeSymbolAtPosition(
        document,
        position,
        SymbolKind.UNKNOWN
    );
    if (symbolDescription === undefined) {
        // TODO: @ganvas show this information in pretty window
        logMessage(LogLevel.DEBUG, "Is not a named symbol");
        return;
    }

    const targetSymbol = FromVscodelc.getSymbolKind(symbolDescription.kind);
    if (targetSymbol === SymbolKind.UNKNOWN) {
        // TODO: @ganvas show this information in pretty window
        logMessage(
            LogLevel.DEBUG,
            "Name suggestion is not supported for this symbol"
        );
        return;
    }

    logMessage(LogLevel.TRACE, `Target symbol ${targetSymbol}`);

    const request = await buildRequestWithSymbolContex(
        textEditor.document,
        textEditor.selection.active,
        targetSymbol
    );
    if (request === undefined) {
        // TODO: @ganvas show this information in pretty window
        logMessage(LogLevel.DEBUG, "Is not a named symbol");
        return;
    }

    // TODO: @GrigoriyPA subscribe on promise instead of wait
    const response = NameSuggestion.Response.deserialize(
        await sendRequest(new NameSuggestion.Request(request))
    );
    if (!response.isSuccess()) {
        logMessage(
            LogLevel.ERROR,
            `Failed to compute request: ${response.getError()}`
        );
        return;
    }

    logMessage(LogLevel.TRACE, `Got name suggestion:\n${response.content}`);

    // TODO: @ganvas | @GrigoriyPA show dialog in separate window before inserting name suggestion
    await insertNameSuggestion(textEditor, response.content);
};
