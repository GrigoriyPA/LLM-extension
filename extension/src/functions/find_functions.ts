import * as vscode from "vscode";

import * as vscodelc from "vscode-languageclient/node";

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

function ensureIsFunctionDefenition(
    document: vscode.TextDocument,
    wordRange: vscode.Range
): boolean {
    if (wordRange.start.character < 4) {
        return false;
    }

    const functionDefenition = document.getText(
        new vscode.Range(wordRange.start.translate(0, -4), wordRange.start)
    );
    return functionDefenition === "def ";
}

function findSymbolNameRange(
    document: vscode.TextDocument,
    position: vscode.Position,
    targetSymbol: SymbolKind
): vscode.Range | undefined {
    const wordRange = document.getWordRangeAtPosition(position);
    if (wordRange === undefined) {
        return undefined;
    }

    if (targetSymbol === SymbolKind.FUNCTION) {
        if (!ensureIsFunctionDefenition(document, wordRange)) {
            return undefined;
        }
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

export function getContextForPosition(
    document: vscode.TextDocument,
    position: vscode.Position
): string {
    // TODO: @GrigoriyPA | @ZenMan123 extract larger range with context
    const contextRange = new vscode.Range(
        position.with(undefined, 0),
        document.lineAt(position.line).rangeIncludingLineBreak.end
    );

    return document.getText(contextRange);
}

export async function findSymbolReferencesContent(
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
