package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/conversions"
	"advent-of-code/commons/go/files"
	"advent-of-code/commons/go/parsers"
	"advent-of-code/commons/go/utils"
	"strings"
)

const Boarder = 5

type Enhancer string

func (enhancer Enhancer) edgeBehavior(time int) bool {
	if enhancer[0] == '.' {
		return false
	} else if enhancer[len(enhancer)-1] == '#' || time%2 == 1 {
		return true
	} else {
		return false
	}
}

type Bounds struct {
	minX int
	maxX int
	minY int
	maxY int
}

func (bounds Bounds) out(point parsers.Point) bool {
	return point.X < bounds.minX ||
		point.X > bounds.maxX ||
		point.Y < bounds.minY ||
		point.Y > bounds.maxY
}

type Image struct {
	grid  parsers.Grid
	times int
}

func (image Image) enhance(enhancer Enhancer) Image {
	enhanced := parsers.Grid{}
	bounds := image.getBounds()
	for y := bounds.minY - Boarder; y <= bounds.maxY+Boarder; y++ {
		for x := bounds.minX - Boarder; x <= bounds.maxX+Boarder; x++ {
			point := parsers.Point{X: x, Y: y}
			if image.enhanceValue(point, enhancer, bounds) {
				enhanced.Set(point, "#")
			}
		}
	}
	return Image{
		grid:  enhanced,
		times: image.times + 1,
	}
}

func (image Image) enhanceValue(point parsers.Point, enhancer Enhancer, bounds Bounds) bool {
	var indexCode strings.Builder
	for y := -1; y <= 1; y++ {
		for x := -1; x <= 1; x++ {
			surrounding := point.Add(x, y)
			value := image.grid.Contains(surrounding)
			if value || (bounds.out(surrounding) && enhancer.edgeBehavior(image.times)) {
				indexCode.WriteString("1")
			} else {
				indexCode.WriteString("0")
			}
		}
	}
	index := conversions.BinaryToDecimal(indexCode.String())
	return enhancer[index] == '#'
}

func (image Image) getBounds() Bounds {
	minX, minY, maxX, maxY := 0, 0, 0, 0
	for _, point := range image.grid.Points() {
		minX = utils.Min(minX, point.X)
		maxX = utils.Max(maxX, point.X)
		minY = utils.Min(minY, point.Y)
		maxY = utils.Max(maxY, point.Y)
	}
	return Bounds{
		minX: minX,
		maxX: maxX,
		minY: minY,
		maxY: maxY,
	}
}

func main() {
	answers.Part1(5437, litAfter(2))
	answers.Part2(19340, litAfter(50))
}

func litAfter(times int) int {
	enhancer, image := getEnhancerImage()
	for i := 0; i < times; i++ {
		image = image.enhance(enhancer)
	}
	return image.grid.Len()
}

func getEnhancerImage() (Enhancer, Image) {
	enhancerImage := files.ReadGroups()
	return Enhancer(enhancerImage[0]), parseImage(enhancerImage[1])
}

func parseImage(raw string) Image {
	return Image{
		grid:  parsers.ConstructGrid(parsers.Lines(raw), parsers.Character, "."),
		times: 0,
	}
}
