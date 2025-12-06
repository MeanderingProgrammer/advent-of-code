package main

import (
	"sort"
	"strings"

	"advent-of-code/lib/go/answer"
	"advent-of-code/lib/go/file"
	"advent-of-code/lib/go/util"
)

/*
 *  aaaa
 * b    c
 * b    c
 *  dddd
 * e    f
 * e    f
 *  gggg
 */

type Digit string

func (digit Digit) overlap(other Digit) int {
	result := 0
	for _, char1 := range digit {
		for _, char2 := range other {
			if char1 == char2 {
				result += 1
			}
		}
	}
	return result
}

type InputDigits []Digit

func (inputDigits InputDigits) getMapping() map[Digit]int {
	mapping := make(map[int]Digit)

	mapping[1] = inputDigits.getOfLength(2)[0]
	mapping[4] = inputDigits.getOfLength(4)[0]
	mapping[7] = inputDigits.getOfLength(3)[0]
	mapping[8] = inputDigits.getOfLength(7)[0]

	// 2, 3, 5
	length5 := inputDigits.getOfLength(5)
	// Only 2 overlaps with 4 for 2 segments, both 3 & 5 have 3 overlap
	mapping[2] = length5.getOverlapping(mapping[4], 2)[0]
	// Only 3 overlaps fully with 7, 2 & 5 both miss one segment
	mapping[3] = length5.getOverlapping(mapping[7], 3)[0]
	// Only 5 overlaps with 2 for 3 segments, 2 overlaps for 5 and 3 for 4
	mapping[5] = length5.getOverlapping(mapping[2], 3)[0]

	// 0, 6, 9
	length6 := inputDigits.getOfLength(6)
	// Only 0 overlaps with 5 for 4 segments, both 6 & 9 overlap for all 5 of 5s segments
	mapping[0] = length6.getOverlapping(mapping[5], 4)[0]
	// Only 6 overlaps with 7 for 2 segments, both 0 & 9 overlap for all 3 of 7s segments
	mapping[6] = length6.getOverlapping(mapping[7], 2)[0]
	// Only 9 overlaps fully with 4, 0 & 6 both miss one segment
	mapping[9] = length6.getOverlapping(mapping[4], 4)[0]

	reversed := make(map[Digit]int)
	for k, v := range mapping {
		reversed[v] = k
	}
	return reversed
}

func (inputDigits InputDigits) getOfLength(n int) InputDigits {
	var digits []Digit
	for _, digit := range inputDigits {
		if len(digit) == n {
			digits = append(digits, digit)
		}
	}
	return digits
}

func (inputDigits InputDigits) getOverlapping(other Digit, amount int) InputDigits {
	var digits []Digit
	for _, digit := range inputDigits {
		if digit.overlap(other) == amount {
			digits = append(digits, digit)
		}
	}
	return digits
}

type SegmentEntry struct {
	inputDigits  InputDigits
	outputDigits []Digit
}

func (segmentEntry SegmentEntry) solve() string {
	mapping := segmentEntry.inputDigits.getMapping()
	outputNumber := strings.Builder{}
	for _, digit := range segmentEntry.outputDigits {
		outputNumber.WriteString(util.ToString(mapping[digit]))
	}
	return outputNumber.String()
}

func main() {
	answer.Timer(solution)
}

func solution() {
	lines := file.Default().Lines()
	segmentEntries := util.Map(lines, func(line string) SegmentEntry {
		parts := strings.Split(line, " | ")
		return SegmentEntry{
			inputDigits:  parseDigits(parts[0]),
			outputDigits: parseDigits(parts[1]),
		}
	})
	part1, part2 := 0, 0
	for _, segmentEntry := range segmentEntries {
		outputNumber := segmentEntry.solve()
		part1 += trackPart1(outputNumber)
		part2 += trackPart2(outputNumber)
	}
	answer.Part1(344, part1)
	answer.Part2(1048410, part2)
}

func parseDigits(raw string) []Digit {
	var digits []Digit
	for rawDigit := range strings.SplitSeq(raw, " ") {
		digits = append(digits, parseDigit(rawDigit))
	}
	return digits
}

func parseDigit(rawDigit string) Digit {
	segments := strings.Split(rawDigit, "")
	sort.Strings(segments)
	return Digit(strings.Join(segments, ""))
}

func trackPart1(outputNumber string) int {
	result := 0
	for _, digit := range []string{"1", "4", "7", "8"} {
		result += strings.Count(outputNumber, digit)
	}
	return result
}

func trackPart2(outputNumber string) int {
	return util.ToInt(outputNumber)
}
