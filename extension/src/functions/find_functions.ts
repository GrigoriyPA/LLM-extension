import * as vscode from "vscode";

import * as vscodelc from "vscode-languageclient/node";

import { FromVscodelc, SymbolKind } from "../utils/lsp/lsp_helpers";
import { getSymbolsInformation, getReferences } from "../utils/lsp/lsp_methods";

import { extensionConfig } from "../config";

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

    const symbolsInformationPromise = getSymbolsInformation(document);

    return symbolsInformationPromise.then((documentSymbols) => {
        return findSymbolDescription(documentSymbols, symbolNameRange);
    });
}

export async function findSymbolContentRange(
    document: vscode.TextDocument,
    position: vscode.Position,
    targetSymbol: SymbolKind
): Promise<vscode.Range | undefined> {
    const symbolDescriptionPromise = describeSymbolAtPosition(
        document,
        position,
        targetSymbol
    );

    return symbolDescriptionPromise.then((symbolDescription) => {
        if (symbolDescription === undefined) {
            if (targetSymbol === SymbolKind.UNKNOWN) {
                return document.getWordRangeAtPosition(position);
            }
            return undefined;
        }

        const symbolKind = symbolDescription.kind;
        if (
            !FromVscodelc.isSameSymboKind(targetSymbol, symbolKind) &&
            targetSymbol !== SymbolKind.UNKNOWN
        ) {
            return undefined;
        }

        return FromVscodelc.getRange(symbolDescription.range);
    });
}

function extractLineContext(
    document: vscode.TextDocument,
    topLine: number,
    bottomLine: number,
    rangeSize: number = extensionConfig.symbolContentRangeSize
): vscode.Range {
    // TODO: @ZenMan123 | @GrigoriyPA pass smarter line context

    let lineDelta = 0;
    while (lineDelta < rangeSize && topLine > 0) {
        topLine -= 1;
        if (!document.lineAt(topLine).isEmptyOrWhitespace) {
            lineDelta += 1;
        }
    }

    lineDelta = 0;
    while (lineDelta < rangeSize && bottomLine + 1 < document.lineCount) {
        bottomLine += 1;
        if (!document.lineAt(bottomLine).isEmptyOrWhitespace) {
            lineDelta += 1;
        }
    }

    return new vscode.Range(
        new vscode.Position(topLine, 0),
        document.lineAt(bottomLine).rangeIncludingLineBreak.end
    );
}

export function getContextForPosition(
    document: vscode.TextDocument,
    position: vscode.Position
): string {
    const contextRange = extractLineContext(
        document,
        position.line,
        position.line,
        extensionConfig.positionContentRangeSize
    );

    return document.getText(contextRange.with(undefined, position));
}

function computeReferencesContent(
    documents: vscode.TextDocument[],
    references: vscodelc.Location[]
): string[] {
    let documentsMap = new Map<string, vscode.TextDocument>();
    for (const document of documents) {
        documentsMap.set(document.uri.toString(), document);
    }

    const referencesContent: string[] = [];
    for (const reference of references) {
        const referenceRange = FromVscodelc.getRange(reference.range);
        const referenceDocument = documentsMap.get(
            FromVscodelc.getUri(reference).toString()
        );

        if (referenceDocument === undefined) {
            continue;
        }

        const referenceContentRange = extractLineContext(
            referenceDocument,
            referenceRange.start.line,
            referenceRange.end.line
        );

        referencesContent.push(
            referenceDocument.getText(referenceContentRange)
        );
    }

    return referencesContent;
}

export async function findSymbolReferencesContent(
    document: vscode.TextDocument,
    position: vscode.Position
): Promise<string[]> {
    const referencesPromise = getReferences(document, position, true);

    return referencesPromise.then((references) => {
        if (references === undefined) {
            return [];
        }

        const referenceDocuments: Thenable<vscode.TextDocument>[] = [];
        for (const reference of references) {
            const referenceDocument = vscode.workspace.openTextDocument(
                FromVscodelc.getUri(reference)
            );

            referenceDocuments.push(referenceDocument);
        }

        return Promise.all(referenceDocuments).then((documents) => {
            return computeReferencesContent(documents, references);
        });
    });
}
