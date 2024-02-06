export class Reader {
  private readonly file_path: string;

  constructor() {
    // TODO: handle --test flag
    // console.log(Bun.argv);
    const executable_path = Bun.main.split("/");
    executable_path.reverse();
    const [year, day] = [executable_path[2], executable_path[1]];
    this.file_path = `data/${year}/${day}/data.txt`;
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
