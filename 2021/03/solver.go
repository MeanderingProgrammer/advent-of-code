package main

import (
	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"advent-of-code/commons/go/util"
)

type Binaries []string

func (binaries Binaries) mostCommonAt(position int) string {
	frequency := make(map[string]int)
	for _, binary := range binaries {
		frequency[string(binary[position])]++
	}
	if frequency["1"] >= frequency["0"] {
		return "1"
	} else {
		return "0"
	}
}

func (binaries Binaries) filter(position int, value string) Binaries {
	var filtered Binaries
	for _, binary := range binaries {
		if string(binary[position]) == value {
			filtered = append(filtered, binary)
		}
	}
	return filtered
}

func main() {
	binaries := getBinaries()
	answer.Part1(4006064, calculatePowerConsumption(binaries))
	answer.Part2(5941884, calculateLifeSupport(binaries))
}

func getBinaries() Binaries {
	return file.ReadLines()
}

func calculatePowerConsumption(binaries Binaries) int {
	return constructedValue(binaries, true) * constructedValue(binaries, false)
}

func constructedValue(binaries Binaries, mostCommon bool) int {
	rate := ""
	for i := 0; i < len(binaries[0]) && len(binaries) > 1; i++ {
		value := binaries.mostCommonAt(i)
		if !mostCommon {
			value = invertBit(value)
		}
		rate += value
	}
	return util.BinaryToDecimal(rate)
}

func calculateLifeSupport(binaries Binaries) int {
	return filteredValue(binaries, true) * filteredValue(binaries, false)
}

func filteredValue(binaries Binaries, mostCommon bool) int {
	for i := 0; len(binaries) > 1; i++ {
		value := binaries.mostCommonAt(i)
		if !mostCommon {
			value = invertBit(value)
		}
		binaries = binaries.filter(i, value)
	}
	return util.BinaryToDecimal(binaries[0])
}

func invertBit(value string) string {
	if value == "1" {
		return "0"
	} else {
		return "1"
	}
}
