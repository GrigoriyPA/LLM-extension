import * as vscode from 'vscode';


let outputChannel: vscode.OutputChannel;


export function printToExtentionChannel(content: string, reval = true) {
    outputChannel.appendLine(content);
    if (reval) {
        outputChannel.show(true);
    }
};

export function initializeExtention() {
    outputChannel = vscode.window.createOutputChannel("LLM python extension");
    printToExtentionChannel(`Initialization of LLM python extension`);
}
