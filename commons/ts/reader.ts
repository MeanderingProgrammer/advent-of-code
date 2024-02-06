import { parseArgs } from "util";

export class Reader {
  private readonly file_path: string;

  constructor() {
    const { values } = parseArgs({
      args: Bun.argv,
      options: {
        test: { type: "boolean", default: false },
      },
      strict: true,
      allowPositionals: true,
    });
    const file_name = values.test ? "sample.txt" : "data.txt";
    const executable_path = Bun.main.split("/");
    executable_path.reverse();
    const [year, day] = [executable_path[2], executable_path[1]];
    this.file_path = `data/${year}/${day}/${file_name}`;
  }

  async read_int(): Promise<number[]> {
    const lines = await this.read_lines();
    return lines.map((line) => parseInt(line));
  }

  async read_lines(): Promise<string[]> {
    return this.read().then((text) => text.split("\n"));
  }

  async read(): Promise<string> {
    return Bun.file(this.file_path).text();
  }
}
