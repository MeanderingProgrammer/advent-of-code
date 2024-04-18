package lib;

import java.nio.file.*;
import java.util.List;

import org.junit.jupiter.api.*;
import org.junit.jupiter.api.io.TempDir;

import lombok.SneakyThrows;

class FileReaderTest {

    @Test
    void testRead(@TempDir Path tempDir) {
        var reader = newReader(tempDir, List.of("abcd", "efg"));
        Assertions.assertEquals(List.of("abcd", "efg"), reader.read());
    }

    @SneakyThrows
    private static FileReader newReader(Path directory, List<String> lines) {
        Path path = directory.resolve("data.txt");
        Files.write(path, lines);
        return new FileReader(path);
    }
}
