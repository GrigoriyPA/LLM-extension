export interface RequestInterface {
    name: string;

    getDescription(): string;
    serialize(): string;
}

class HttpResponseStatus {
    private success: boolean = false;
    private errorMessage: string = "";

    public setSuccess() {
        this.success = true;
    }

    public setError(errorMessage: string) {
        this.success = false;
        this.errorMessage = errorMessage;
    }

    public isSuccess(): boolean {
        return this.success;
    }

    public getError(): string {
        return this.errorMessage;
    }
}

export class HttpResponse extends HttpResponseStatus {
    content: string;

    constructor(content: string = "") {
        super();
        this.content = content;
    }
}

class RequestResponseBase extends HttpResponseStatus {
    constructor(status: HttpResponseStatus) {
        super();
        if (status.isSuccess()) {
            this.setSuccess();
        } else {
            this.setError(status.getError());
        }
    }
}

export namespace DocumentFunction {
    export class Request implements RequestInterface {
        name: string = "DocumentFunction";

        functionContent: string;
        referencesContent: string[];

        constructor(functionContent: string, referencesContent: string[]) {
            this.functionContent = functionContent;
            this.referencesContent = referencesContent;
        }

        public getDescription(): string {
            let description = `Function content:\n${this.functionContent}\n`;
            for (const referenceContent of this.referencesContent) {
                description += `Reference content: ${referenceContent}`;
            }
            return description;
        }

        public serialize(): string {
            // TODO: @dffTu implement request serialization
            return "";
        }
    }

    export class Response extends RequestResponseBase {
        functionDocumention: string = "";

        public static deserialize(response: HttpResponse): Response {
            const result = new Response(response);
            if (!response.isSuccess()) {
                return result;
            }

            // TODO: @dffTu implement request deserialization
            result.functionDocumention = response.content;

            return result;
        }
    }
}
