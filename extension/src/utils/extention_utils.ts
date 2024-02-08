import * as vscode from "vscode";

let outputChannel: vscode.OutputChannel;

export function printToExtentionChannel(
    content: string,
    reval: boolean = true
) {
    outputChannel.appendLine(content);
    if (reval) {
        outputChannel.show(true);
    }
}

export function sleep(ms: number) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

export function initializeExtention() {
    outputChannel = vscode.window.createOutputChannel("LLM python extension");
    printToExtentionChannel(`Initialization of LLM python extension`);
}
