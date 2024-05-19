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

export const generateTests = async (
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

        const requestPromise = sendRequest(new GenerateTests.Request(request));

        return requestPromise.then((response) => {
            return computeResponse(
                textEditor,
                position,
                GenerateTests.Response.deserialize(response)
            );
        });
    });
};

async function computeResponse(
    textEditor: vscode.TextEditor,
    position: vscode.Position,
    response: GenerateTests.Response
) {
    if (!response.isSuccess()) {
        logMessage(
            LogLevel.ERROR,
            `Failed to compute request: ${response.getError()}`
        );
        return;
    }

    logMessage(LogLevel.TRACE, `Generated tests:\n${response.content}`);

    // TODO: @ganvas | @GrigoriyPA show dialog in separate window before inserting tests
    return insertTests(textEditor, position, response.content);
}

async function insertTests(
    textEditor: vscode.TextEditor,
    position: vscode.Position,
    tests: string
) {
    const document = textEditor.document;

    const functionContentRangePromise = findSymbolContentRange(
        document,
        position,
        SymbolKind.FUNCTION
    );

    return functionContentRangePromise.then((functionContentRange) => {
        if (functionContentRange === undefined) {
            logMessage(LogLevel.ERROR, "Failed to find function content");
            return;
        }

        const indentSize = document.lineAt(
            position.line
        ).firstNonWhitespaceCharacterIndex;

        const testsContent = applyIndent(
            indentSize,
            "\n\n" + tests.trimEnd(),
            "# "
        );

        textEditor.edit((edit: vscode.TextEditorEdit) => {
            edit.insert(functionContentRange.end, testsContent);
        });
    });
}
