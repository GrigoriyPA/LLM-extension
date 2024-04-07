import * as vscode from "vscode";

import { printToExtentionChannel } from "./runtime/extention_utils";

import { extensionConfig, LogLevel, Components } from "../config";

export function logEntry(
    logLevel: LogLevel,
    component: Components,
    message: string
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
        `${timeString} | ${logLevelString}| [${Components[component]}] ${message}`,
        logLevel >= LogLevel.WARNING
    );

    if (logLevel === LogLevel.ALERT) {
        vscode.window.showErrorMessage(message);
    } else if (logLevel === LogLevel.ERROR) {
        vscode.window.showWarningMessage(message);
    }
}
