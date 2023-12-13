type direction = UP | DOWN | LEFT | RIGHT
type point = { x : int; y : int }

let adjacent (p : point) : (direction * point) list =
  [
    (UP, { x = p.x; y = p.y - 1 });
    (DOWN, { x = p.x; y = p.y + 1 });
    (LEFT, { x = p.x - 1; y = p.y });
    (RIGHT, { x = p.x + 1; y = p.y });
  ]
