import { parseArgs } from "util";

export class Reader {
  private readonly path: string;

  constructor() {
    const { values } = parseArgs({
      args: Bun.argv,
      options: {
        test: { type: "boolean", default: false },
      },
      strict: true,
      allowPositionals: true,
    });
    const fileName = values.test ? "sample.txt" : "data.txt";
    const parts = Bun.main.split("/");
    parts.reverse();
    const [year, day] = [parts[2], parts[1]];
    this.path = `data/${year}/${day}/${fileName}`;
  }

  async intLines(): Promise<number[]> {
    const lines = await this.lines();
    return lines.map((line) => parseInt(line));
  }

  async lines(): Promise<string[]> {
    const text = await this.read();
    return text.split("\n");
  }

  async read(): Promise<string> {
    return Bun.file(this.path).text();
  }
}
