package main

import(
    "advent-of-code/commons/go/answers"
    "advent-of-code/commons/go/files"
    "advent-of-code/commons/go/parsers"
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

func (school School) totalFish() int {
    result := 0
    for _, numFish := range school {
        result += numFish
    }
    return result
}

func main() {
    answers.Part1(345793, fishAfter(80))
    answers.Part2(1572643095893, fishAfter(256))
}

func fishAfter(days int) int {
    school := getSchool()
    for i := 0; i < days; i++ {
        school.runDay()
    }
    return school.totalFish()
}

func getSchool() School {
    school := make(map[int]int)
    fishes := parsers.SubstringAfter(files.Content(), ": ")
    for _, fish := range parsers.IntCsv(fishes) {
        school[fish]++
    }
    return school
}
