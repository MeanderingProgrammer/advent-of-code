package main

import(
    "fmt"
    "io/ioutil"
    "strings"
    "strconv"
)

type School map[int]int

func (school *School) runDay() {
    nextSchool := make(map[int]int)

    for counter, numFish := range *school {
        if counter == 0 {
            nextSchool[6] += numFish
            nextSchool[8] += numFish
        } else {
            nextSchool[counter - 1] += numFish
        }
    }

    *school = nextSchool
}

func (school *School) totalFish() int {
    result := 0
    for _, numFish := range *school {
        result += numFish
    }
    return result
}

func (school *School) print() {
    fmt.Println(*school)
}

func main() {
    // Part 1: 345793
    fmt.Printf("Part 1: %d \n", fishAfter(80))
    // Part 2: 1572643095893
    fmt.Printf("Part 2: %d \n", fishAfter(256))
}

func fishAfter(days int) int {
    school := getData()
    for i := 0; i < days; i++ {
        school.runDay()
    }
    return school.totalFish()
}

func getData() School {
    data, _ := ioutil.ReadFile("data.txt")
    rawFishes := strings.Split(string(data), ": ")[1]
    fishes := strings.Split(rawFishes, ",")

    result := make(map[int]int)
    for _, fish := range fishes {
        counter, _ := strconv.Atoi(fish)
        result[counter]++
    }
    return result
}
