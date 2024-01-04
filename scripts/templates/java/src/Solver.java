import lib.Answer;
import lib.FileReader;

public class Solver {

  public static void main(String[] args) {
    Answer.timer(() -> solution(args));
  }

  private static void solution(String[] args) {
    FileReader fileReader = new FileReader(args);
    System.out.println(fileReader.read());
    Answer.part1(1, 1);
  }
}
