import { RequestsBase, ResponseBase } from "./requests_structures";

import { LogLevel, Components, logEntry } from "../logger";

import fetch from "node-fetch";

function logMessage(logLevel: LogLevel, functionName: string, message: string) {
    logEntry(logLevel, Components.HTTP_GATEWAY, `[${functionName}] ${message}`);
}

export async function sendRequest(
    request: RequestsBase.RequestInterface
): Promise<ResponseBase.HttpResponse> {
    logMessage(LogLevel.DEBUG, "Send Request", `${request.getName()}`);
    logMessage(
        LogLevel.TRACE,
        "SendRequest",
        `Request description:\n${request.getDescription()}`
    );

    // TODO: @dffTu implement request sending and error message passing
    // TODO: @ganvas show status bar when we wait for http response
    const response_raw = await fetch('http://dfftu.pythonanywhere.com', {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: request.serialize()
    });

    const response = new ResponseBase.HttpResponse(
        await response_raw.text()
    );
    response.setSuccess();

    logMessage(LogLevel.TRACE, "SendRequest", `Request successfully finished`);

    return response;
}
