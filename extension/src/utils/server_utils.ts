import { NetConnectOpts, connect } from "node:net";

import { ChildProcess, exec } from "child_process";

import * as vscodelc from "vscode-languageclient/node";

import { printToExtentionChannel, sleep } from "./extention_utils";

class ServerProcess {
    private process: ChildProcess | undefined;
    private host: string;
    private port: number;

    options: () => Promise<vscodelc.StreamInfo>;

    private createOptions(): () => Promise<vscodelc.StreamInfo> {
        return () => {
            const connetcOptions: NetConnectOpts = {
                port: this.port,
                host: this.host,
            };
            const socket = connect(connetcOptions);
            const result: vscodelc.StreamInfo = {
                writer: socket,
                reader: socket,
            };
            return Promise.resolve(result);
        };
    }

    constructor(host: string, port: number) {
        this.host = host;
        this.port = port;
        this.process = undefined;

        this.options = this.createOptions();
    }

    async start() {
        if (!this.process) {
            this.process = exec(
                `jedi-language-server --tcp --host ${this.host} --port ${this.port}`
            );

            await sleep(1000);

            printToExtentionChannel(
                `LS started on host ${this.host}, port ${this.port} with pid ${this.process.pid}`
            );
        }
    }

    stop() {
        if (this.process && this.process.exitCode === null) {
            this.process.kill();
        }
    }
}

export let serverProcess: ServerProcess;

export async function initializeServer() {
    printToExtentionChannel(`Initialization of Jedi LS`);

    const host = "127.0.0.1";
    const port = 8089;
    serverProcess = new ServerProcess(host, port);

    await serverProcess.start();
}
