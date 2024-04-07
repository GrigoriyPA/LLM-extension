import * as vscode from "vscode";

import { sendRequest } from "../../utils/http_server/requests_functions";
import {
    RequestsBase,
    CompletionSuggestion,
} from "../../utils/http_server/requests_structures";

import { LogLevel, Components, logEntry } from "../../utils/logger";

import { getContextForPosition } from "../find_functions";

function logMessage(logLevel: LogLevel, message: string) {
    logEntry(
        logLevel,
        Components.REQUESTS_PROCESSOR,
        `[Completion Suggestion] ${message}`
    );
}

async function completionSuggestion(
    document: vscode.TextDocument,
    position: vscode.Position,
    token: vscode.CancellationToken,
    context: vscode.CompletionContext
) {
    logMessage(LogLevel.TRACE, "Compute request");

    // TODO: @GrigoriyPA pass more info for suggestion
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

    const completionItems: vscode.CompletionItem[] = [];
    for (const suggestion of response.contents) {
        completionItems.push(new vscode.CompletionItem(suggestion));
    }

    return completionItems;
}

export const completionSuggestionProvider: vscode.CompletionItemProvider = {
    provideCompletionItems: completionSuggestion,
};
