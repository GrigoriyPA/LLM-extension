import {
    NetConnectOpts,
    connect
} from 'node:net';

import {
    ChildProcess,
    exec
} from 'child_process';

import {
    StreamInfo
} from 'vscode-languageclient/node';

import {
    printToExtentionChannel,
    sleep
} from './extention_utils';


class ServerProcess {
    private process: ChildProcess | undefined;
    private host: string;
    private port: number;

    options: () => Promise<StreamInfo>;

    private createOptions(): () => Promise<StreamInfo> {
        return () => {
            let connetcOptions: NetConnectOpts = { port: this.port, host: this.host };
            let socket = connect(connetcOptions);
            let result: StreamInfo = {
                writer: socket,
                reader: socket
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
            this.process = exec(`jedi-language-server --tcp --host ${this.host} --port ${this.port}`);

            await sleep(1000);

            printToExtentionChannel(`LS started on host ${this.host}, port ${this.port} with pid ${this.process.pid}`);
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
