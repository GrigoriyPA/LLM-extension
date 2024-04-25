import * as vscode from "vscode";

import * as vscodelc from "vscode-languageclient/node";

export enum SymbolKind {
    UNKNOWN,
    FUNCTION,
    VARIABLE,
}

export namespace FromVscode {
    export function getTextDocumentIdentifier(
        document: vscode.TextDocument
    ): vscodelc.TextDocumentIdentifier {
        return vscodelc.TextDocumentIdentifier.create(document.uri.toString());
    }

    export function getPosition(position: vscode.Position): vscodelc.Position {
        return vscodelc.Position.create(position.line, position.character);
    }

    export function getRange(range: vscode.Range): vscodelc.Range {
        return vscodelc.Range.create(
            getPosition(range.start),
            getPosition(range.end)
        );
    }
}

export namespace FromVscodelc {
    export function getPosition(position: vscodelc.Position): vscode.Position {
        return new vscode.Position(position.line, position.character);
    }

    export function getRange(range: vscodelc.Range): vscode.Range {
        return new vscode.Range(
            getPosition(range.start),
            getPosition(range.end)
        );
    }

    export function getUri(
        textDocumentIdentifier: vscodelc.TextDocumentIdentifier
    ): vscode.Uri {
        return vscode.Uri.parse(textDocumentIdentifier.uri);
    }

    export function isFunctionSymbol(symbolKind: vscodelc.SymbolKind): boolean {
        return (
            symbolKind === vscodelc.SymbolKind.Function ||
            symbolKind === vscodelc.SymbolKind.Method
        );
    }

    export function isVariableSymbol(symbolKind: vscodelc.SymbolKind): boolean {
        return (
            symbolKind === vscodelc.SymbolKind.Variable ||
            symbolKind === vscodelc.SymbolKind.Field ||
            symbolKind === vscodelc.SymbolKind.Constant
        );
    }

    export function isSameSymboKind(
        firstKind: SymbolKind,
        secondKind: vscodelc.SymbolKind
    ): boolean {
        return (
            (firstKind === SymbolKind.FUNCTION &&
                FromVscodelc.isFunctionSymbol(secondKind)) ||
            (firstKind === SymbolKind.VARIABLE &&
                FromVscodelc.isVariableSymbol(secondKind))
        );
    }

    export function getSymbolKind(symbolKind: vscodelc.SymbolKind): SymbolKind {
        if (isFunctionSymbol(symbolKind)) {
            return SymbolKind.FUNCTION;
        }
        if (isVariableSymbol(symbolKind)) {
            return SymbolKind.VARIABLE;
        }
        return SymbolKind.UNKNOWN;
    }
}

export namespace ToString {
    export function convertPosition(position: vscode.Position): string {
        return `${position.line}:${position.character}`;
    }

    export function convertRange(range: vscode.Range): string {
        return `[${convertPosition(range.start)} - ${convertPosition(range.end)}]`;
    }
}
