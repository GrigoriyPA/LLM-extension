import * as vscode from "vscode";

import * as vscodelc from "vscode-languageclient/node";

import { RequestsBase } from "../utils/http_server/requests_structures";

import { FromVscodelc, SymbolKind } from "../utils/lsp/lsp_helpers";
import { getSymbolsInformation, getReferences } from "../utils/lsp/lsp_methods";

function findSymbolDescription(
    documentSymbols: vscodelc.DocumentSymbol[] | undefined,
    wordRange: vscode.Range
): vscodelc.DocumentSymbol | undefined {
    if (documentSymbols === undefined) {
        return undefined;
    }

    for (const documentSymbol of documentSymbols) {
        const isTargetRange = wordRange.isEqual(
            FromVscodelc.getRange(documentSymbol.selectionRange)
        );

        if (isTargetRange) {
            return documentSymbol;
        }

        const result = findSymbolDescription(
            documentSymbol.children,
            wordRange
        );
        if (result !== undefined) {
            return result;
        }
    }

    return undefined;
}

function findSymbolNameRange(
    document: vscode.TextDocument,
    position: vscode.Position,
    targetSymbol: SymbolKind
): vscode.Range | undefined {
    const wordRange = document.getWordRangeAtPosition(position);
    if (wordRange === undefined || wordRange.start.character < 4) {
        return undefined;
    }

    const functionDefenition = document.getText(
        new vscode.Range(wordRange.start.translate(0, -4), wordRange.start)
    );
    if (targetSymbol === SymbolKind.FUNCTION && functionDefenition !== "def ") {
        return undefined;
    }

    return wordRange;
}

export async function describeSymbolAtPosition(
    document: vscode.TextDocument,
    position: vscode.Position,
    targetSymbol: SymbolKind
): Promise<vscodelc.DocumentSymbol | undefined> {
    const symbolNameRange = findSymbolNameRange(
        document,
        position,
        targetSymbol
    );
    if (symbolNameRange === undefined) {
        return undefined;
    }

    const documentSymbols = await getSymbolsInformation(document);
    return findSymbolDescription(documentSymbols, symbolNameRange);
}

export async function findSymbolContentRange(
    document: vscode.TextDocument,
    position: vscode.Position,
    targetSymbol: SymbolKind
): Promise<vscode.Range | undefined> {
    const symbolDescription = await describeSymbolAtPosition(
        document,
        position,
        targetSymbol
    );
    if (symbolDescription === undefined) {
        return undefined;
    }

    const symbolKind = symbolDescription.kind;
    if (
        (targetSymbol === SymbolKind.FUNCTION &&
            !FromVscodelc.isFunctionSymbol(symbolKind)) ||
        (targetSymbol === SymbolKind.VARIABLE &&
            !FromVscodelc.isVariableSymbol(symbolKind))
    ) {
        return undefined;
    }

    return FromVscodelc.getRange(symbolDescription.range);
}

async function findSymbolReferencesContent(
    document: vscode.TextDocument,
    position: vscode.Position
): Promise<string[]> {
    const references = await getReferences(document, position, true);
    if (references === undefined) {
        return [];
    }

    const referencesContent: string[] = [];
    for (const reference of references) {
        const referenceRange = FromVscodelc.getRange(reference.range);
        const referenceDocument = await vscode.workspace.openTextDocument(
            vscode.Uri.parse(reference.uri)
        );

        // TODO: @GrigoriyPA | @ZenMan123 extract larger range with context
        const referenceContentRange = new vscode.Range(
            referenceRange.start.with(undefined, 0),
            referenceDocument.lineAt(
                referenceRange.end.line
            ).rangeIncludingLineBreak.end
        );

        referencesContent.push(
            referenceDocument.getText(referenceContentRange)
        );
    }

    return referencesContent;
}

export async function buildRequestWithSymbolContex(
    document: vscode.TextDocument,
    position: vscode.Position,
    targetSymbol: SymbolKind
): Promise<RequestsBase.RequestWithSymbolContextBase | undefined> {
    const symbolContentRange = await findSymbolContentRange(
        document,
        position,
        targetSymbol
    );
    if (symbolContentRange === undefined) {
        return undefined;
    }

    const symbolReferencesContent = await findSymbolReferencesContent(
        document,
        position
    );

    return new RequestsBase.RequestWithSymbolContextBase(
        document.getText(symbolContentRange),
        symbolReferencesContent
    );
}
