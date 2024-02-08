import * as vscode from "vscode";
import * as vscodelc from "vscode-languageclient/node";

import { printToExtentionChannel, sleep } from "./extention_utils";

// TODO: @ganvas install jedi-language-server if does not exist

export const serverOptions: vscodelc.ServerOptions = {
    command: "jedi-language-server",
};
