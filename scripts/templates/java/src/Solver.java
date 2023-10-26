import lib.Answer;
import lib.FileReader;

public class Solver {

  public static void main(String[] args) {
    FileReader fileReader = new FileReader();
    System.out.println(fileReader.read());
    Answer.part1(1, 1);
  }
}
