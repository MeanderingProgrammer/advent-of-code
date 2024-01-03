package lib;

import java.io.File;
import java.util.*;
import java.util.function.Function;
import lombok.SneakyThrows;
import org.apache.commons.cli.*;

public class FileReader {

  private final String fileName;

  @SneakyThrows
  public FileReader(String[] args) {
    Options options = new Options();
    options.addOption(Option.builder().longOpt("test").build());
    CommandLine cmd = new DefaultParser().parse(options, args);
    this.fileName = cmd.hasOption("test") ? "sample" : "data";
  }

  public List<String> read() {
    return read(Function.identity());
  }

  public <T> List<T> read(Function<String, T> f) {
    var lines = getFile().map(FileReader::readFromScanner).orElse(List.of());
    return lines.stream().map(f).toList();
  }

  private Optional<Scanner> getFile() {
    // Fix this to read from data directory
    File file = new File(String.format("%s.txt", this.fileName));
    try {
      return Optional.of(new Scanner(file));
    } catch (Exception e) {
      return Optional.empty();
    }
  }

  private static List<String> readFromScanner(Scanner scanner) {
    List<String> result = new ArrayList<>();
    while (scanner.hasNextLine()) {
      result.add(scanner.nextLine());
    }
    return result;
  }
}
