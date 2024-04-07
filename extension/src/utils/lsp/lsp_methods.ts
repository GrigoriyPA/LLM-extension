import * as vscode from "vscode";

import * as vscodelc from "vscode-languageclient/node";

import { FromVscode } from "./lsp_helpers";

import { languageClient } from "../runtime/client_utils";

import { LogLevel, Components, logEntry } from "../../utils/logger";

function logMessage(logLevel: LogLevel, message: string) {
    logEntry(
        logLevel,
        Components.REQUESTS_PROCESSOR,
        `[LSP request] ${message}`
    );
}

export async function getSymbolsInformation(
    document: vscode.TextDocument
): Promise<vscodelc.DocumentSymbol[] | undefined> {
    let params: vscodelc.DocumentSymbolParams = {
        textDocument: FromVscode.getTextDocumentIdentifier(document),
    };

    return languageClient
        .sendRequest(vscodelc.DocumentSymbolRequest.method, params)
        .then((response) => {
            if (!response) {
                return undefined;
            }
            return response as vscodelc.DocumentSymbol[];
        })
        .catch((error) => {
            logMessage(
                LogLevel.WARNING,
                `GetSymbolsInformation request failed with error: ${error}`
            );
            return undefined;
        });
}

export async function getReferences(
    document: vscode.TextDocument,
    position: vscode.Position,
    includeDeclaration: boolean
): Promise<vscodelc.Location[] | undefined> {
    let params: vscodelc.ReferenceParams = {
        textDocument: FromVscode.getTextDocumentIdentifier(document),
        position: FromVscode.getPosition(position),
        context: {
            includeDeclaration: includeDeclaration,
        },
    };

    return languageClient
        .sendRequest(vscodelc.ReferencesRequest.method, params)
        .then((response) => {
            if (!response) {
                return undefined;
            }

            return response as vscodelc.Location[];
        })
        .catch((error) => {
            logMessage(
                LogLevel.WARNING,
                `GetReferences request failed with error: ${error}`
            );
            return undefined;
        });
}
