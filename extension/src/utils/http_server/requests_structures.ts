export namespace RequestsBase {
    export interface RequestInterface {
        getName(): string;
        getDescription(): string;
        serialize(): string;
    }

    export class RequestWithSymbolContextBase implements RequestInterface {
        name: string = "RequestWithSymbolContextBase";
        symbolContent: string;
        referencesContent: string[];

        constructor(symbolContent: string, referencesContent: string[]) {
            this.symbolContent = symbolContent;
            this.referencesContent = referencesContent;
        }

        public getName(): string {
            return this.name;
        }

        public getDescription(): string {
            let description = `Function content:\n${this.symbolContent}\n`;
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
}

export namespace ResponseBase {
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

    export class RequestResponseBase extends HttpResponseStatus {
        constructor(status: HttpResponseStatus) {
            super();
            if (status.isSuccess()) {
                this.setSuccess();
            } else {
                this.setError(status.getError());
            }
        }
    }

    export class SingleStringRequestResponseBase extends RequestResponseBase {
        content: string = "";

        public static deserialize(
            response: ResponseBase.HttpResponse
        ): SingleStringRequestResponseBase {
            const result = new SingleStringRequestResponseBase(response);
            if (!response.isSuccess()) {
                return result;
            }

            // TODO: @dffTu implement request deserialization
            result.content = response.content;

            return result;
        }
    }

    export class MultiStringRequestResponseBase extends RequestResponseBase {
        contents: string[] = [];

        public getDescription(): string {
            let description = "";
            for (const content of this.contents) {
                description += `${content}\n`;
            }
            return description;
        }

        public static deserialize(
            response: ResponseBase.HttpResponse
        ): MultiStringRequestResponseBase {
            const result = new MultiStringRequestResponseBase(response);
            if (!response.isSuccess()) {
                return result;
            }

            // TODO: @dffTu implement request deserialization
            result.contents.push(response.content);

            return result;
        }
    }
}

export namespace DocumentFunction {
    export class Request extends RequestsBase.RequestWithSymbolContextBase {
        constructor(request: RequestsBase.RequestWithSymbolContextBase) {
            super(request.symbolContent, request.referencesContent);
            this.name = "DocumentFunction";
        }
    }

    export class Response extends ResponseBase.SingleStringRequestResponseBase {}
}

export namespace SemanticAnalysisOfSymbol {
    export class Request extends RequestsBase.RequestWithSymbolContextBase {
        constructor(request: RequestsBase.RequestWithSymbolContextBase) {
            super(request.symbolContent, request.referencesContent);
            this.name = "SemanticAnalysisOfSymbol";
        }
    }

    export class Response extends ResponseBase.SingleStringRequestResponseBase {}
}

export namespace NameSuggestion {
    export class Request extends RequestsBase.RequestWithSymbolContextBase {
        constructor(request: RequestsBase.RequestWithSymbolContextBase) {
            super(request.symbolContent, request.referencesContent);
            this.name = "NameSuggestion";
        }
    }

    export class Response extends ResponseBase.SingleStringRequestResponseBase {}
}

export namespace GenerateTests {
    export class Request extends RequestsBase.RequestWithSymbolContextBase {
        constructor(request: RequestsBase.RequestWithSymbolContextBase) {
            super(request.symbolContent, request.referencesContent);
            this.name = "GenerateTests";
        }
    }

    export class Response extends ResponseBase.SingleStringRequestResponseBase {}
}

export namespace CompletionSuggestion {
    export class Request extends RequestsBase.RequestWithSymbolContextBase {
        constructor(request: RequestsBase.RequestWithSymbolContextBase) {
            super(request.symbolContent, request.referencesContent);
            this.name = "CompletionSuggestion";
        }
    }

    export class Response extends ResponseBase.MultiStringRequestResponseBase {}
}
