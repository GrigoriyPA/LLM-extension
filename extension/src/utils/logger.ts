import * as vscode from "vscode";

import { printToExtentionChannel } from "./runtime/extention_utils";

import { extensionConfig, LogLevel, Components } from "../config";

export function logEntry(
    logLevel: LogLevel,
    component: Components,
    message: string,
    logPrefix: string = ""
) {
    let componentLogLevel = extensionConfig.componentsLogLevel.get(component);
    if (componentLogLevel === undefined) {
        componentLogLevel = extensionConfig.defaultLogLevel;
    }
    if (logLevel > componentLogLevel) {
        return;
    }

    const logLevelString = LogLevel[logLevel].padEnd(8, " ");
    const timeString = new Date().toISOString();

    printToExtentionChannel(
        `${timeString} | ${logLevelString}| [${Components[component]}] ${logPrefix} ${message}`,
        logLevel >= LogLevel.WARNING
    );

    const hintPos = vscode.window.activeTextEditor?.selection.active;
    const hintLine = hintPos
        ? vscode.window.activeTextEditor?.document.lineAt(hintPos.line).range
        : undefined;

    if (hintLine && logLevel == LogLevel.DEBUG) {
        const decorationType = vscode.window.createTextEditorDecorationType({
            after: {
                contentText: message,
                margin: "1em",
                color: "red",
                backgroundColor: "rgba(255,0,0,0.1)",
            },
        });

        vscode.window.activeTextEditor?.setDecorations(decorationType, [
            { range: hintLine, hoverMessage: message },
        ]);
        const activeWindow = vscode.window.activeTextEditor;

        setTimeout(() => {
            decorationType.dispose();
        }, 3000);
    } else if (logLevel === LogLevel.CRIT) {
        vscode.window.showErrorMessage(message);
    } else if (logLevel === LogLevel.ERROR) {
        vscode.window.showWarningMessage(message);
    }
}
