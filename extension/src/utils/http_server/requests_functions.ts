import fetch from "node-fetch";

import { RequestsBase, ResponseBase } from "./requests_structures";

import { createProgressIndicator } from "../runtime/extention_utils";

import { logEntry } from "../logger";

import { extensionConfig, LogLevel, Components } from "../../config";

function logMessage(logLevel: LogLevel, functionName: string, message: string) {
    logEntry(logLevel, Components.HTTP_GATEWAY, `[${functionName}] ${message}`);
}

function getErrorResponse(error: string): ResponseBase.HttpResponse {
    logEntry(
        LogLevel.ERROR,
        Components.HTTP_GATEWAY,
        `Failed to compute HTTP request with error: ${error}`
    );

    const response = new ResponseBase.HttpResponse();
    response.setError(error);
    return response;
}

async function computeRawResponse(
    response_raw: fetch.Response
): Promise<ResponseBase.HttpResponse> {
    // TODO: @dffTu set error in case of bad request status

    const textPromise = response_raw.text();

    return textPromise
        .then((result) => {
            logMessage(
                LogLevel.TRACE,
                "SendRequest",
                "Request successfully finished"
            );

            const response = new ResponseBase.HttpResponse(result);
            response.setSuccess();
            return response;
        })
        .catch((error) => {
            return getErrorResponse(error);
        });
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

    const fetchPromise = fetch(extensionConfig.llmServerUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: request.serialize(),
    });

    const fetchProgressPromise = createProgressIndicator(
        `${request.getName()} request`,
        fetchPromise
    );

    return fetchProgressPromise.then(computeRawResponse).catch((error) => {
        return getErrorResponse(error);
    });
}

export async function initializeHttpGateway() {
    logEntry(
        LogLevel.INFO,
        Components.HTTP_GATEWAY,
        "Initialization of http gateway"
    );

    // TODO: @dffTu implement http gateway initialization (like access verification)
}
