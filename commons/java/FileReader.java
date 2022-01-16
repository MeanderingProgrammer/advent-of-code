package io;

import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.Scanner;

public class FileReader {

    private final boolean testMode;

    public FileReader() {
        this(false);
    }

    public FileReader(boolean testMode) {
        this.testMode = testMode;
    }

    public List<String> read() {
        return getFile()
                .map(FileReader::readFromScanner)
                .orElse(new ArrayList<>());
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
