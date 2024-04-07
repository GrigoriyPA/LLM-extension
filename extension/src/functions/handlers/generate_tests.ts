import * as vscode from "vscode";

import { buildRequestWithSymbolContex } from "../request_functions";
import { findSymbolContentRange } from "../find_functions";

import { sendRequest } from "../../utils/http_server/requests_functions";
import { GenerateTests } from "../../utils/http_server/requests_structures";

import { SymbolKind } from "../../utils/lsp/lsp_helpers";

import { applyIndent } from "../../utils/functions";
import { logEntry } from "../../utils/logger";

import { LogLevel, Components } from "../../config";

function logMessage(logLevel: LogLevel, message: string) {
    logEntry(
        logLevel,
        Components.REQUESTS_PROCESSOR,
        `[Generate Tests] ${message}`
    );
}

async function insertTests(textEditor: vscode.TextEditor, tests: string) {
    const document = textEditor.document;
    const position = textEditor.selection.active;

    const functionContentRange = await findSymbolContentRange(
        document,
        position,
        SymbolKind.FUNCTION
    );
    if (functionContentRange === undefined) {
        logMessage(LogLevel.ERROR, "Failed to find function content");
        return;
    }

    const indentSize = document.lineAt(
        position.line
    ).firstNonWhitespaceCharacterIndex;

    const testsContent = applyIndent(indentSize, "\n\n" + tests.trimEnd());

    textEditor.edit((edit: vscode.TextEditorEdit) => {
        edit.insert(functionContentRange.end, testsContent);
    });
}

export const generateTests = async (
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
    const response = GenerateTests.Response.deserialize(
        await sendRequest(new GenerateTests.Request(request))
    );
    if (!response.isSuccess()) {
        logMessage(
            LogLevel.ERROR,
            `Failed to compute request: ${response.getError()}`
        );
        return;
    }

    logMessage(LogLevel.TRACE, `Generated tests:\n${response.content}`);

    // TODO: @ganvas | @GrigoriyPA show dialog in separate window before inserting tests
    await insertTests(textEditor, response.content);
};
