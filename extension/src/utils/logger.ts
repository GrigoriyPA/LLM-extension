import * as vscode from "vscode";

import { printToExtentionChannel } from "./runtime/extention_utils";

export enum LogLevel {
    ALERT, // Extention level fatal errors
    ERROR, // Request level fatal errors
    WARNING, // Exceptional situations that are guaranteed not to lead to an error
    INFO, // Information about the progress of request computing, only a few messages during the processing of a single request
    DEBUG, // Information about the progress of function execution, only a few messages during the processing of a single function
    TRACE, // Detail information about the progress of function execution, regular messages during the processing of a single function
}

export enum Components {
    REQUESTS_PROCESSOR,
    HTTP_GATEWAY,
    EXTENSION,
}

interface LoggerOptions {
    defaultLogLevel: LogLevel;
    componentsLogLevel: Map<Components, LogLevel>;
    outputChannel: vscode.OutputChannel;
}

let loggerOptions: LoggerOptions;

export function logEntry(
    logLevel: LogLevel,
    component: Components,
    message: string
) {
    let componentLogLevel = loggerOptions.componentsLogLevel.get(component);
    if (componentLogLevel === undefined) {
        componentLogLevel = loggerOptions.defaultLogLevel;
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

export function initializeLogger(
    defaultLogLevel: LogLevel,
    componentsLogLevel: Map<Components, LogLevel>,
    outputChannel: vscode.OutputChannel
) {
    loggerOptions = {
        defaultLogLevel: defaultLogLevel,
        componentsLogLevel: componentsLogLevel,
        outputChannel: outputChannel,
    };
}
