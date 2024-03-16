import * as vscode from "vscode";

import * as vscodelc from "vscode-languageclient/node";

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
}

export namespace ToString {
    export function convertPosition(position: vscode.Position): string {
        return `${position.line}:${position.character}`;
    }

    export function convertRange(range: vscode.Range): string {
        return `[${convertPosition(range.start)} - ${convertPosition(range.end)}]`;
    }
}
