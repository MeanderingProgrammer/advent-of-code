package maze;

import lombok.Value;

@Value
public class Edge {

  Node destination;
  int length;
}
