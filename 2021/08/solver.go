package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"sort"
	"strings"
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

type Digit struct {
    segments string
}

func (digit Digit) overlap(other Digit) int {
    result := 0
    for _, char1 := range digit.segments {
        for _, char2 := range other.segments {
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
        if len(digit.segments) == n {
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
    inputDigits InputDigits
    outputDigits []Digit
}

func (segmentEntry SegmentEntry) solve() []int {
    mapping := segmentEntry.inputDigits.getMapping()

    var outputDigits []int
    for _, digit := range segmentEntry.outputDigits {
        outputDigits = append(outputDigits, mapping[digit])
    }
    return outputDigits
}

func main() {
    segmentEntries := getData()
    
    part1Solution :=  0
    part2Solution := 0
    for _, segmentEntry := range segmentEntries {
        outputDigits := segmentEntry.solve()
        part1Solution += trackPart1(outputDigits)
        part2Solution += trackPart2(outputDigits)
    }

    fmt.Printf("Part 1 = %d \n", part1Solution)
    fmt.Printf("Part 2 = %d \n", part2Solution)
}

func trackPart1(outputDigits []int) int {
    result := 0
    for _, digit := range outputDigits {
        if digit == 1 || digit == 4 || digit == 7 || digit == 8 {
            result += 1
        }
    }
    return result
}

func trackPart2(outputDigits []int) int {
    result := 0
    for i, digit := range outputDigits {
        exponent := len(outputDigits) - i - 1
        scale := math.Pow(10.0, float64(exponent))
        result += (digit * int(scale))
    }
    return result
}

func getData() []SegmentEntry {
    data, _ := ioutil.ReadFile("data.txt")
    lines := strings.Split(string(data), "\r\n")

    var segmentEntries []SegmentEntry
    for _, line := range lines {
        parts := strings.Split(line, " | ")
        segmentEntry := SegmentEntry{parseDigits(parts[0]), parseDigits(parts[1])}
        segmentEntries = append(segmentEntries, segmentEntry)
    }
    return segmentEntries
}

func parseDigits(raw string) []Digit {
    var digits []Digit
    for _, rawDigit := range strings.Split(raw, " ") {
        digits = append(digits, parseDigit(rawDigit))
    }
    return digits
}

func parseDigit(rawDigit string) Digit {
    var segments []string
    for _, digit := range rawDigit {
        segments = append(segments, string(digit))
    }
    sort.Strings(segments)
    return Digit{strings.Join(segments, "")}
}
