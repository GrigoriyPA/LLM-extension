import * as vscode from "vscode";

import * as vscodelc from "vscode-languageclient/node";

import { sendRequest } from "../utils/http_server/requests_functions";
import {
    RequestsBase,
    CompletionSuggestion,
} from "../utils/http_server/requests_structures";

import { LogLevel, Components, logEntry } from "../utils/logger";

import { getContextForPosition } from "./common";

function logMessage(logLevel: LogLevel, message: string) {
    logEntry(
        logLevel,
        Components.REQUESTS_PROCESSOR,
        `[Completion Suggestion] ${message}`
    );
}

export const completionSuggestion = async (
    document: vscode.TextDocument,
    position: vscode.Position,
    context: vscode.CompletionContext,
    token: vscode.CancellationToken,
    next: vscodelc.ProvideCompletionItemsSignature
) => {
    logMessage(LogLevel.TRACE, "Compute request");

    // TODO: @GrigoriyPA move logic out of normal suggestion
    // TODO: @GrigoriyPA support cancellation token

    const result = (await next(
        document,
        position,
        context,
        token
    )) as vscode.CompletionList;

    const request = new RequestsBase.RequestWithSymbolContextBase(
        getContextForPosition(document, position),
        []
    );

    // TODO: @GrigoriyPA subscribe on promise instead of wait
    const response = CompletionSuggestion.Response.deserialize(
        await sendRequest(new CompletionSuggestion.Request(request))
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
        `Completion suggestions:\n${response.getDescription()}`
    );

    for (const suggestion of response.contents) {
        result.items.push(new vscode.CompletionItem(suggestion));
    }

    return result;
};
