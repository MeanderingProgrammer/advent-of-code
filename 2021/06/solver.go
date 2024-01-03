package main

import (
	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"advent-of-code/commons/go/util"
)

type School map[int]int

func (school *School) runDay() {
	nextSchool := make(map[int]int)
	for counter, numFish := range *school {
		if counter == 0 {
			nextSchool[6] += numFish
			nextSchool[8] += numFish
		} else {
			nextSchool[counter-1] += numFish
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
	answer.Part1(345793, fishAfter(80))
	answer.Part2(1572643095893, fishAfter(256))
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
	fishes := util.SubstringAfter(file.Content(), ": ")
	for _, fish := range util.IntCsv(fishes) {
		school[fish]++
	}
	return school
}
