import * as vscode from "vscode";

import { logEntry } from "../logger";

import { completionSuggestionProvider } from "../../functions/handlers/completion_suggestion";

import { supportedFunctions } from "../../functions/functions_description";

import { LogLevel, Components } from "../../config";

let outputChannel: vscode.OutputChannel;

export function printToExtentionChannel(
    content: string,
    reval: boolean = false
) {
    outputChannel.appendLine(content);
    if (reval) {
        outputChannel.show(true);
    }
}

export function initializeExtention(context: vscode.ExtensionContext) {
    outputChannel = vscode.window.createOutputChannel("LLM python extension");

    logEntry(
        LogLevel.INFO,
        Components.EXTENSION,
        "Initialization of LLM python extension"
    );

    // TODO: @GrigoriyPA add hotkeys
    for (const [functionName, functionImpl] of supportedFunctions) {
        context.subscriptions.push(
            vscode.commands.registerTextEditorCommand(
                `llm-extension.${functionName}`,
                functionImpl
            )
        );
    }

    vscode.languages.registerCompletionItemProvider(
        "python",
        completionSuggestionProvider
    );
}
