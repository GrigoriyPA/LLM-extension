import * as vscode from "vscode";
import * as vscodelc from "vscode-languageclient/node";

import { documentFunctionRequest } from "../utils/http_server/requests_functions";

import { FromVscodelc } from "../utils/lsp/lsp_helpers";
import { getSymbolsInformation, getReferences } from "../utils/lsp/lsp_methods";

import { printToExtentionChannel } from "../utils/runtime/extention_utils";

import { findSymbolDescription } from "./common";

function findFunctionNameRange(
    document: vscode.TextDocument,
    position: vscode.Position
): vscode.Range | undefined {
    const wordRange = document.getWordRangeAtPosition(position);
    if (wordRange === undefined || wordRange.start.character < 4) {
        return undefined;
    }

    const functionDefenition = document.getText(
        new vscode.Range(wordRange.start.translate(0, -4), wordRange.start)
    );
    if (functionDefenition !== "def ") {
        return undefined;
    }

    return wordRange;
}

async function findFunctionContentRange(
    document: vscode.TextDocument,
    functionNameRange: vscode.Range
): Promise<vscode.Range | undefined> {
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
        return undefined;
    }

    return FromVscodelc.getRange(symbolDescription.range);
}

async function findFunctionContent(
    document: vscode.TextDocument,
    position: vscode.Position
): Promise<String | undefined> {
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
): Promise<String[]> {
    const references = await getReferences(document, position, true);
    if (references === undefined) {
        return [];
    }

    const referencesRanges: String[] = [];
    for (const reference of references) {
        const referenceRange = FromVscodelc.getRange(reference.range);
        const referenceContentRange = new vscode.Range(
            referenceRange.start.with(undefined, 0),
            document.lineAt(referenceRange.end.line).rangeIncludingLineBreak.end
        );

        referencesRanges.push(document.getText(referenceContentRange));
    }

    return referencesRanges;
}

async function findFunctionContext(
    document: vscode.TextDocument,
    position: vscode.Position
): Promise<[String, String[]] | undefined> {
    const functionContent = await findFunctionContent(document, position);
    if (functionContent === undefined) {
        return undefined;
    }

    const functionReferencesContent = await findFunctionReferencesContent(
        document,
        position
    );

    return [functionContent, functionReferencesContent];
}

export const documentFunction = async (
    textEditor: vscode.TextEditor,
    edit: vscode.TextEditorEdit
) => {
    const functionContext = await findFunctionContext(
        textEditor.document,
        textEditor.selection.active
    );
    if (functionContext === undefined) {
        printToExtentionChannel("Is not function defenition");
        return;
    }

    const response = await documentFunctionRequest({
        FunctionContent: functionContext[0],
        ReferencesContent: functionContext[1],
    });
    if (response === undefined) {
        printToExtentionChannel(
            "Failed to compute function documentation request"
        );
        return;
    }

    printToExtentionChannel(
        `Function documentation:\n${response.FunctionDocumention}`
    );
};
