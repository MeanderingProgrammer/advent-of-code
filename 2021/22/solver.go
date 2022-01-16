package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/conversions"
	"advent-of-code/commons/go/files"
	"advent-of-code/commons/go/parsers"
	"advent-of-code/commons/go/utils"
	"strings"
)

type Range [2]int

func (r Range) start() int {
	return r[0]
}

func (r Range) end() int {
	return r[1]
}

func (r Range) valid() bool {
	return r.start() <= r.end()
}

func (r Range) length() int {
	return (r.end() - r.start()) + 1
}

func (r1 Range) overlap(r2 Range) Range {
	return [2]int{
		utils.Max(r1.start(), r2.start()),
		utils.Min(r1.end(), r2.end()),
	}
}

type Bound struct {
	count int
	xs    Range
	ys    Range
	zs    Range
}

func (bound Bound) disabledOverlap(newBound Bound) (Bound, bool) {
	xs := bound.xs.overlap(newBound.xs)
	ys := bound.ys.overlap(newBound.ys)
	zs := bound.zs.overlap(newBound.zs)
	if xs.valid() && ys.valid() && zs.valid() {
		return Bound{count: -bound.count, xs: xs, ys: ys, zs: zs}, true
	} else {
		return Bound{}, false
	}
}

func (bound Bound) area() int {
	length := bound.xs.length()
	width := bound.ys.length()
	height := bound.zs.length()
	return (length * width * height) * bound.count
}

type Bounds []Bound

func (bounds Bounds) disabledOverlappingBounds(newBound Bound) Bounds {
	var overlappingBounds Bounds
	for _, bound := range bounds {
		overlap, exists := bound.disabledOverlap(newBound)
		if exists {
			overlappingBounds = append(overlappingBounds, overlap)
		}
	}
	return overlappingBounds
}

func (bounds Bounds) area() int {
	result := 0
	for _, bound := range bounds {
		result += bound.area()
	}
	return result
}

func main() {
	finalBounds := getFinalBounds()
	answers.Part1(561032, limitedBoundsArea(finalBounds))
	answers.Part2(1322825263376414, finalBounds.area())
}

func getFinalBounds() Bounds {
	bounds := getBounds()
	finalBounds := Bounds{bounds[0]}
	for _, bound := range bounds[1:] {
		finalBounds = append(finalBounds, finalBounds.disabledOverlappingBounds(bound)...)
		if bound.count > 0 {
			finalBounds = append(finalBounds, bound)
		}
	}
	return finalBounds
}

func limitedBoundsArea(bounds Bounds) int {
	limitingBound := Bound{
		xs: [2]int{-50, 50},
		ys: [2]int{-50, 50},
		zs: [2]int{-50, 50},
	}
	boundsDisabled := bounds.disabledOverlappingBounds(limitingBound)
	// Need the negative to handle the fact that this will track the
	// area disabled by our limited bound
	return -boundsDisabled.area()
}

func getBounds() Bounds {
	toBound := func(line string) Bound {
		enableWhere := strings.Split(line, " ")
		count := -1
		if enableWhere[0] == "on" {
			count = 1
		}
		where := strings.Split(enableWhere[1], ",")
		return Bound{
			count: count,
			xs:    parseRange(where[0]),
			ys:    parseRange(where[1]),
			zs:    parseRange(where[2]),
		}
	}
	return files.Read(toBound)
}

func parseRange(rawRange string) Range {
	rangePortion := parsers.SubstringAfter(rawRange, "=")
	bounds := strings.Split(rangePortion, "..")
	return [2]int{
		conversions.ToInt(bounds[0]),
		conversions.ToInt(bounds[1]),
	}
}
