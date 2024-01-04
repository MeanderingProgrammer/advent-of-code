package lib;

import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
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
    return getLines().stream().map(f).toList();
  }

  @SneakyThrows
  private List<String> getLines() {
    return Files.readAllLines(getFilePath(), StandardCharsets.UTF_8);
  }

  private Path getFilePath() {
    var project = Paths.get("").toAbsolutePath();
    var day = project.getFileName();
    var year = project.getParent().getFileName();
    var root = project.getParent().getParent();
    var fileName = String.format("%s.txt", this.fileName);
    return root.resolve("data").resolve(year).resolve(day).resolve(fileName);
  }
}
