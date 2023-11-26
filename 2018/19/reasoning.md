# Initial Notes

Immediate instructions `i` use the exact value in the instruction.

Register instructions `r` use the value as an index in the registers.

# Instruction Info

```
 0: addi 3 16 3 -> ip += 16
 1: seti 1  2 1 ->  B  =  1
 2: seti 1  1 2 ->  C  =  1
 3: mulr 1  2 5 ->  F = B*C
 4: eqrr 5  4 5 -> F = E==F
 5: addr 5  3 3 -> ip +=  F
 6: addi 3  1 3 -> ip +=  1
 7: addr 1  0 0 ->  A +=  B
 8: addi 2  1 2 ->  C +=  1
 9: gtrr 2  4 5 ->  F = C>E
10: addr 3  5 3 -> ip +=  F
11: seti 2  3 3 -> ip  =  2
12: addi 1  1 1 ->  B +=  1
13: gtrr 1  4 5 ->  F = B>E
14: addr 5  3 3 -> ip +=  F
15: seti 1  6 3 -> ip  =  1
16: mulr 3  3 3 -> ip *= ip
17: addi 4  2 4 ->  E +=  2
18: mulr 4  4 4 ->  E *=  E
19: mulr 3  4 4 ->  E *= ip
20: muli 4 11 4 ->  E *= 11
21: addi 5  5 5 ->  F +=  5
22: mulr 5  3 5 ->  F *= ip
23: addi 5 15 5 ->  F += 15
24: addr 4  5 4 ->  E +=  F
25: addr 3  0 3 -> ip +=  A
26: seti 0  6 3 -> ip  =  0
27: setr 3  5 5 ->  F  = ip
28: mulr 5  3 5 ->  F *= ip
29: addr 3  5 5 ->  F += ip
30: mulr 3  5 5 ->  F *= ip
31: muli 5 14 5 ->  F *= 14
32: mulr 5  3 5 ->  F *= ip
33: addr 4  5 4 ->  E +=  F
34: seti 0  5 0 ->  A  =  0
35: seti 0  1 3 -> ip  =  0
```

# Part 1

We loop for all B & C up to a given integer, in this case 961.

Anytime there is a C such that B * C equals the number, we increment register A.

Therefore A is tracking the sum of factors up to the given number.

## Setup

```
    #ip 3            ; {A: 0, B: 0, C: 0, ip:  0, E:   0, F:   0}
 0: ip += 16; ip += 1; {A: 0, B: 0, C: 0, ip: 17, E:   0, F:   0}
17:  E +=  2; ip += 1; {A: 0, B: 0, C: 0, ip: 18, E:   2, F:   0}
18:  E *=  E; ip += 1; {A: 0, B: 0, C: 0, ip: 19, E:   4, F:   0}
19:  E *= ip; ip += 1; {A: 0, B: 0, C: 0, ip: 20, E:  76, F:   0}
20:  E *= 11; ip += 1; {A: 0, B: 0, C: 0, ip: 21, E: 836, F:   0}
21:  F +=  5; ip += 1; {A: 0, B: 0, C: 0, ip: 22, E: 836, F:   5}
22:  F *= ip; ip += 1; {A: 0, B: 0, C: 0, ip: 23, E: 836, F: 110}
23:  F += 15; ip += 1; {A: 0, B: 0, C: 0, ip: 24, E: 836, F: 125}
24:  E +=  F; ip += 1; {A: 0, B: 0, C: 0, ip: 25, E: 961, F: 125}
25: ip +=  A; ip += 1; {A: 0, B: 0, C: 0, ip: 26, E: 961, F: 125}
26: ip  =  0; ip += 1; {A: 0, B: 0, C: 0, ip:  1, E: 961, F: 125}
```

## Outer Loop

Init: B = 1

```
 1:  B  =  1; ip += 1; {A: 0, B: 1, C: 0, ip:  2, E: 961, F: 125}
```

Body: B += 1

```
12:  B +=  1; ip += 1; {A: 1, B: 2, C: 962, ip: 13, E: 961, F: 1}
```

Condition: B <= 961

```
13:  F = B>E; ip += 1; {A: 1, B: 2, C: 962, ip: 14, E: 961, F: 0}
14: ip +=  F; ip += 1; {A: 1, B: 2, C: 962, ip: 15, E: 961, F: 0}
15: ip  =  1; ip += 1; {A: 1, B: 2, C: 962, ip:  2, E: 961, F: 0}
```

```
13:  F = B>E; ip += 1; {A: 993, B: 962, C: 962, ip:  14, E: 961, F: 1}
14: ip +=  F; ip += 1; {A: 993, B: 962, C: 962, ip:  16, E: 961, F: 1}
16: ip *= ip; ip += 1; {A: 993, B: 962, C: 962, ip: 257, E: 961, F: 1}
```

## Inner Loop

Init: C = 1

```
 2:  C  =  1; ip += 1; {A: 0, B: 1, C: 1, ip:  3, E: 961, F: 125}
```

Special Case: B * C == 961 -> A += B

```
 3:  F = B*C; ip += 1; {A: 0, B: 1, C: 1, ip:  4, E: 961, F: 1}
 4: F = E==F; ip += 1; {A: 0, B: 1, C: 1, ip:  5, E: 961, F: 0}
 5: ip +=  F; ip += 1; {A: 0, B: 1, C: 1, ip:  6, E: 961, F: 0}
 6: ip +=  1; ip += 1; {A: 0, B: 1, C: 1, ip:  8, E: 961, F: 0}
```

```
 3:  F = B*C; ip += 1; {A: 0, B: 1, C: 961, ip:  4, E: 961, F: 961}
 4: F = E==F; ip += 1; {A: 0, B: 1, C: 961, ip:  5, E: 961, F:   1}
 5: ip +=  F; ip += 1; {A: 0, B: 1, C: 961, ip:  7, E: 961, F:   1}
 7:  A +=  B; ip += 1; {A: 1, B: 1, C: 961, ip:  8, E: 961, F:   1}
```

Body: C += 1

```
 8:  C += 1; ip += 1; {A: 0, B: 1, C: 2, ip:  9, E: 961, F: 0}
```

Condition: C <= 961

```
 9:  F = C>E; ip += 1; {A: 0, B: 1, C: 2, ip: 10, E: 961, F: 0}
10: ip +=  F; ip += 1; {A: 0, B: 1, C: 2, ip: 11, E: 961, F: 0}
11: ip  =  2; ip += 1; {A: 0, B: 1, C: 2, ip:  3, E: 961, F: 0}
```

```
 9:  F = C>E; ip += 1; {A: 1, B: 1, C: 962, ip: 10, E: 961, F:   1}
10: ip +=  F; ip += 1; {A: 1, B: 1, C: 962, ip: 12, E: 961, F:   1}
```

# Part 2

Largely the same in that the code sums the factors of a number.

However, the number is much larger.
