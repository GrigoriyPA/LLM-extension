import * as vscode from "vscode";

import * as cp from "child_process";
import * as util from "util";
import * as path from "path";

import { logEntry } from "../logger";
import { Components, LogLevel } from "../../config";

import { exec } from "child_process";

const exec_promise = util.promisify(exec);

function logMessage(logLevel: LogLevel, message: string) {
    logEntry(logLevel, Components.EXTENSION, `${message}`, `[Installation]`);
}

function isJediInstalled(): Promise<boolean> {
    logMessage(LogLevel.TRACE, `ABOBA`);
    return exec_promise("pip show jedi-language-server").then(
        (value: { stdout: string; stderr: string }) => {
            logMessage(
                LogLevel.TRACE,
                `pip show jedi-language-server stdout: ${value.stdout}`
            );
            return true;
        },
        (reason: any) => {
            logMessage(LogLevel.DEBUG, `pip show jedi-language-server failed`);
            return false;
        }
    );
}

function installJedi(): PromiseLike<boolean> {
    return vscode.window
        .withProgress(
            {
                location: vscode.ProgressLocation.Notification,
                title: "Installing jedi-language-server...",
                cancellable: false,
            },
            (progress) => {
                return exec_promise("pip install jedi-language-server").then(
                    (value: { stdout: string; stderr: string }) => {
                        logMessage(
                            LogLevel.TRACE,
                            `pip install jedi-language-server stdout: ${value.stdout}`
                        );
                        return true;
                    },
                    (reason: any) => {
                        return reason;
                    }
                );
            }
        )
        .then((value) => {
            if (value === true) {
                vscode.window.showInformationMessage(
                    "Jedi has been installed successfully."
                );
            } else {
                vscode.window.showErrorMessage(
                    `Failed to install Jedi: ${value}`
                );
            }
            return value;
        });
}

export function ensureJediIsInstalled(): Promise<boolean> {
    logMessage(LogLevel.INFO, `AMOGUS`);
    return isJediInstalled().then((value: boolean) => {
        if (value) {
            logMessage(LogLevel.INFO, "language server already installed");
            return true;
        } else {
            logMessage(LogLevel.INFO, "TEST1");
            return vscode.window
                .showErrorMessage(
                    "Python Jedi Server is not intalled. Do you want to install it now?",
                    "Yes",
                    "No"
                )
                .then(
                    (value) => {
                        logMessage(LogLevel.INFO, "TEST2");
                        if (value === "Yes") {
                            return installJedi();
                        } else {
                            return false;
                        }
                    },
                    () => {
                        return false;
                    }
                );
        }
    });
}
