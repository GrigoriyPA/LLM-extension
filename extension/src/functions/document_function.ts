import * as vscode from "vscode";
import * as vscodelc from "vscode-languageclient/node";

import { sendRequest } from "../utils/http_server/requests_functions";
import { DocumentFunction } from "../utils/http_server/requests_structures";

import { FromVscodelc, ToString } from "../utils/lsp/lsp_helpers";
import { getSymbolsInformation, getReferences } from "../utils/lsp/lsp_methods";

import { LogLevel, Components, logEntry } from "../utils/logger";

import { findSymbolDescription } from "./common";

function logMessage(logLevel: LogLevel, message: string) {
    logEntry(
        logLevel,
        Components.REQUESTS_PROCESSOR,
        `[Document Function] ${message}`
    );
}

function findFunctionNameRange(
    document: vscode.TextDocument,
    position: vscode.Position
): vscode.Range | undefined {
    logMessage(
        LogLevel.TRACE,
        `Try to find function name at position ${ToString.convertPosition(position)}`
    );

    const wordRange = document.getWordRangeAtPosition(position);
    if (wordRange === undefined || wordRange.start.character < 4) {
        logMessage(LogLevel.DEBUG, "Function name not found");
        return undefined;
    }

    const functionDefenition = document.getText(
        new vscode.Range(wordRange.start.translate(0, -4), wordRange.start)
    );
    if (functionDefenition !== "def ") {
        logMessage(LogLevel.DEBUG, "Function name is not starts from 'def '");
        return undefined;
    }

    logMessage(
        LogLevel.TRACE,
        `Found function name at ${ToString.convertRange(wordRange)}`
    );

    return wordRange;
}

async function findFunctionContentRange(
    document: vscode.TextDocument,
    functionNameRange: vscode.Range
): Promise<vscode.Range | undefined> {
    logMessage(
        LogLevel.TRACE,
        `Try to find description of symbol ${ToString.convertRange(functionNameRange)}`
    );

    const documentSymbols = await getSymbolsInformation(document);
    const symbolDescription = findSymbolDescription(
        documentSymbols,
        functionNameRange
    );
    if (
        symbolDescription === undefined ||
        (symbolDescription.kind !== vscodelc.SymbolKind.Function &&
            symbolDescription.kind !== vscodelc.SymbolKind.Method)
    ) {
        logMessage(
            LogLevel.DEBUG,
            "Symbol description not foud, or it is not a Function | Method"
        );
        return undefined;
    }

    const contentRange = FromVscodelc.getRange(symbolDescription.range);

    logMessage(
        LogLevel.TRACE,
        `Found function content at ${ToString.convertRange(contentRange)}`
    );

    return contentRange;
}

async function findFunctionContent(
    document: vscode.TextDocument,
    position: vscode.Position
): Promise<string | undefined> {
    logMessage(
        LogLevel.TRACE,
        `Try to find function content at position ${ToString.convertPosition(position)}`
    );

    const functionNameRange = findFunctionNameRange(document, position);
    if (functionNameRange === undefined) {
        return undefined;
    }

    const functionContentRange = await findFunctionContentRange(
        document,
        functionNameRange
    );
    if (functionContentRange === undefined) {
        return undefined;
    }

    return document.getText(functionContentRange);
}

async function findFunctionReferencesContent(
    document: vscode.TextDocument,
    position: vscode.Position
): Promise<string[]> {
    logMessage(
        LogLevel.TRACE,
        `Find function references at position ${ToString.convertPosition(position)}`
    );

    const references = await getReferences(document, position, true);
    if (references === undefined) {
        return [];
    }

    const referencesRanges: string[] = [];
    for (const reference of references) {
        const referenceRange = FromVscodelc.getRange(reference.range);
        logMessage(
            LogLevel.TRACE,
            `Got refernece range ${ToString.convertRange(referenceRange)} in document ${reference.uri}`
        );

        const referenceDocument = await vscode.workspace.openTextDocument(
            vscode.Uri.parse(reference.uri)
        );

        const referenceContentRange = new vscode.Range(
            referenceRange.start.with(undefined, 0),
            referenceDocument.lineAt(
                referenceRange.end.line
            ).rangeIncludingLineBreak.end
        );

        referencesRanges.push(referenceDocument.getText(referenceContentRange));
    }

    return referencesRanges;
}

async function findFunctionContext(
    document: vscode.TextDocument,
    position: vscode.Position
): Promise<DocumentFunction.Request | undefined> {
    const functionContent = await findFunctionContent(document, position);
    if (functionContent === undefined) {
        logMessage(LogLevel.TRACE, "Function content not found");
        return undefined;
    }

    const functionReferencesContent = await findFunctionReferencesContent(
        document,
        position
    );

    return new DocumentFunction.Request(
        functionContent,
        functionReferencesContent
    );
}

export const documentFunction = async (
    textEditor: vscode.TextEditor,
    edit: vscode.TextEditorEdit
) => {
    logMessage(LogLevel.TRACE, "Compute request");

    const request = await findFunctionContext(
        textEditor.document,
        textEditor.selection.active
    );
    if (request === undefined) {
        logMessage(LogLevel.DEBUG, "Is not a function defenition");
        return;
    }

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

    logMessage(
        LogLevel.TRACE,
        `Function documentation:\n${response.functionDocumention}`
    );
};
