import * as vscode from "vscode";

import { initializeLogger, LogLevel, Components, logEntry } from "../logger";

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

export function initializeExtention(
    defaultLogLevel: LogLevel,
    componentsLogLevel: Map<Components, LogLevel> = new Map<
        Components,
        LogLevel
    >()
) {
    outputChannel = vscode.window.createOutputChannel("LLM python extension");
    initializeLogger(defaultLogLevel, componentsLogLevel, outputChannel);

    logEntry(
        LogLevel.INFO,
        Components.EXTENSION,
        "Initialization of LLM python extension"
    );
}
