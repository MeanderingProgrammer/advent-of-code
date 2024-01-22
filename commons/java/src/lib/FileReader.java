package lib;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.function.Function;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;

import lombok.AllArgsConstructor;
import lombok.SneakyThrows;

@AllArgsConstructor
public class FileReader {

    private final Path path;

    @SneakyThrows
    public FileReader(String[] args) {
        Options options = new Options();
        options.addOption(Option.builder().longOpt("test").build());
        CommandLine cmd = new DefaultParser().parse(options, args);
        var fileName = cmd.hasOption("test") ? "sample" : "data";
        var project = Paths.get("").toAbsolutePath();
        this.path = project.getParent().getParent()
                .resolve("data")
                .resolve(project.getParent().getFileName())
                .resolve(project.getFileName())
                .resolve(String.format("%s.txt", fileName));
    }

    public List<String> read() {
        return read(Function.identity());
    }

    public <T> List<T> read(Function<String, T> f) {
        return getLines().stream().map(f).toList();
    }

    @SneakyThrows
    private List<String> getLines() {
        return Files.readAllLines(this.path, StandardCharsets.UTF_8);
    }
}
