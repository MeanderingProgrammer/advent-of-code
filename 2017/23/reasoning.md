```
b = 109,900
c = 126,900

while b != c:
    f = 1
    d = 2
    while d != b:
        e = 2
        while e != b:
            if d * e == b:
                f = 0
            e += 1
        d += 1
    if f == 0:
        h += 1
    b += 17
```
