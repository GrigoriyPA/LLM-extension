import * as vscodelc from "vscode-languageclient/node";

// TODO: @ganvas install jedi-language-server if does not exist

export const serverOptions: vscodelc.ServerOptions = {
    command: "jedi-language-server",
};
