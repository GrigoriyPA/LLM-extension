import * as vscode from "vscode";

import { logEntry } from "../logger";

import { supportedFunctions } from "../../functions/functions_description";

import { LogLevel, Components } from "../../config";

import { ensureJediIsInstalled } from "../lsp/installation";

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

export async function createProgressIndicator<T>(
    title: string,
    promise: Promise<T>
) {
    let progressOptions: vscode.ProgressOptions = {
        location: vscode.ProgressLocation.Window,
        title: title,
    };

    return vscode.window.withProgress(progressOptions, () => {
        return promise;
    });
}

export function initializeExtention(context: vscode.ExtensionContext): Promise<boolean> {
    outputChannel = vscode.window.createOutputChannel("LLM python extension");

    return ensureJediIsInstalled().then((value: boolean) => {
        if (!value) {
            logEntry(
                LogLevel.CRIT,
                Components.EXTENSION,
                "Jedi is not installed"
            );
            return false;
        }
        logEntry(
            LogLevel.INFO,
            Components.EXTENSION,
            "Initialization of LLM python extension"
        );

        for (const [functionName, functionImpl] of supportedFunctions) {
            context.subscriptions.push(
                vscode.commands.registerTextEditorCommand(
                    `llm-extension.${functionName}`,
                    functionImpl
                )
            );
        }
        return true;
    });
}
