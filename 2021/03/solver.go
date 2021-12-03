package main

import(
    "fmt"
	"io/ioutil"
	"strings"
	"strconv"
)

type Binary string

func (binary Binary) toInt() int64 {
	result, _ := strconv.ParseInt(string(binary), 2, 64)
	return result
}

type Binaries []Binary

func (binaries Binaries) mostCommonAt(position int) string {
	frequency := make(map[string]int)
	for _, binary := range binaries {
		char := string(binary[position])
		frequency[char]++
	}
	return asBit(frequency["1"] >= frequency["0"])
}

func (binaries Binaries) filter(position int, value string) Binaries {
	var filtered Binaries
	for _, binary := range binaries {
		char := string(binary[position])
		if char == value {
			filtered = append(filtered, binary)
		}
	}
	return filtered
}

func main() {
	binaries := getBinaries()

	fmt.Printf("Part 1 = %d \n", calculatePowerConsumption(binaries))
	fmt.Printf("Part 2 = %d \n", calculateLifeSupport(binaries))
}

func getBinaries() Binaries {
	content, _ := ioutil.ReadFile("data.txt")

	var binaries Binaries
	for _, binary := range strings.Split(string(content), "\r\n") {
		binaries = append(binaries, Binary(binary))
	}
    return binaries
}

func calculatePowerConsumption(binaries Binaries) int64 {
	gammaRate := ""
	epsilonRate := ""
	for i := 0; i < len(binaries[0]); i++ {
		result := binaries.mostCommonAt(i)
		gammaRate += result
		epsilonRate += asBit(result == "0")
	}
	return Binary(gammaRate).toInt() * Binary(epsilonRate).toInt()
}

func calculateLifeSupport(binaries Binaries) int64 {
	return filterRating(binaries, true).toInt() * filterRating(binaries, false).toInt()
}

func filterRating(binaries Binaries, mostCommon bool) Binary {
	position := 0
	for len(binaries) > 1 {
		value := binaries.mostCommonAt(position)
		if !mostCommon {
			value = asBit(value == "0")
		}
		binaries = binaries.filter(position, value)
		position++;
	}
	return binaries[0]
}

func asBit(value bool) string {
	if value {
		return "1"
	} else {
		return "0"
	}
}
