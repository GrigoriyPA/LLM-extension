export function sleep(ms: number) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

export function applyIndent(
    indent: number,
    text: string,
    prefix: string = ""
): string {
    const textIndent = " ".repeat(indent);

    let resultText = "";
    for (const textLine of text.split("\n")) {
        if (textLine !== "") {
            resultText += textIndent + prefix + textLine + "\n";
        } else {
            resultText += textIndent + textLine + "\n";
        }
    }

    return resultText;
}
