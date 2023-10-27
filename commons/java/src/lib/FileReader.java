package lib;

import java.io.File;
import java.util.*;
import lombok.AllArgsConstructor;

@AllArgsConstructor
public class FileReader {

  private final boolean testMode;

  public FileReader() {
    this(false);
  }

  public List<String> read() {
    return getFile().map(FileReader::readFromScanner).orElse(List.of());
  }

  private Optional<Scanner> getFile() {
    String fileName = testMode ? "sample" : "data";
    File file = new File(String.format("%s.txt", fileName));
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
