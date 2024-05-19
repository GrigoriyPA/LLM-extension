import * as vscode from "vscode";

import * as vscodelc from "vscode-languageclient/node";

import { FromVscode } from "./lsp_helpers";

import { languageClient } from "../runtime/client_utils";

import { logEntry } from "../../utils/logger";

import { LogLevel, Components } from "../../config";

function logMessage(logLevel: LogLevel, message: string) {
    logEntry(
        logLevel,
        Components.REQUESTS_PROCESSOR,
        `${message}`,
        `[LSP request]`
    );
}

export async function getSymbolsInformation(
    document: vscode.TextDocument
): Promise<vscodelc.DocumentSymbol[] | undefined> {
    let params: vscodelc.DocumentSymbolParams = {
        textDocument: FromVscode.getTextDocumentIdentifier(document),
    };

    const requestPromise = languageClient.sendRequest(
        vscodelc.DocumentSymbolRequest.method,
        params
    );

    return requestPromise
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

    const requestPromise = languageClient.sendRequest(
        vscodelc.ReferencesRequest.method,
        params
    );

    return requestPromise
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

export async function renameSymbol(
    document: vscode.TextDocument,
    position: vscode.Position,
    newName: string
): Promise<vscodelc.WorkspaceEdit | undefined> {
    let params: vscodelc.RenameParams = {
        textDocument: FromVscode.getTextDocumentIdentifier(document),
        position: FromVscode.getPosition(position),
        newName: newName,
    };

    const requestPromise = languageClient.sendRequest(
        vscodelc.RenameRequest.method,
        params
    );

    return requestPromise
        .then((response) => {
            if (!response) {
                return undefined;
            }

            return response as vscodelc.WorkspaceEdit;
        })
        .catch((error) => {
            logMessage(
                LogLevel.WARNING,
                `RenameSymbol request failed with error: ${error}`
            );
            return undefined;
        });
}
