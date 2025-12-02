package main

import (
	"strings"

	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"advent-of-code/commons/go/grid"
	"advent-of-code/commons/go/parser"
	"advent-of-code/commons/go/point"
	"advent-of-code/commons/go/util"
)

const Boarder = 1

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

func (bounds Bounds) out(p point.Point) bool {
	return p.X < bounds.minX ||
		p.X > bounds.maxX ||
		p.Y < bounds.minY ||
		p.Y > bounds.maxY
}

type Image struct {
	grid.Grid[string]
	times int
}

func (image Image) enhance(enhancer Enhancer) Image {
	enhanced := Image{times: image.times + 1}
	bounds := image.getBounds()
	for y := bounds.minY - Boarder; y <= bounds.maxY+Boarder; y++ {
		for x := bounds.minX - Boarder; x <= bounds.maxX+Boarder; x++ {
			p := point.Point{X: x, Y: y}
			if image.enhanceValue(p, enhancer, bounds) {
				enhanced.Set(p, "#")
			}
		}
	}
	return enhanced
}

func (image Image) enhanceValue(p point.Point, enhancer Enhancer, bounds Bounds) bool {
	var indexCode strings.Builder
	for y := -1; y <= 1; y++ {
		for x := -1; x <= 1; x++ {
			surrounding := p.Add(x, y)
			value := image.Contains(surrounding)
			if value || (bounds.out(surrounding) && enhancer.edgeBehavior(image.times)) {
				indexCode.WriteString("1")
			} else {
				indexCode.WriteString("0")
			}
		}
	}
	index := util.ToDecimal(indexCode.String(), 2)
	return enhancer[index] == '#'
}

func (image Image) getBounds() Bounds {
	minX, minY, maxX, maxY := 0, 0, 0, 0
	for _, p := range image.Points() {
		minX = min(minX, p.X)
		maxX = max(maxX, p.X)
		minY = min(minY, p.Y)
		maxY = max(maxY, p.Y)
	}
	return Bounds{
		minX: minX,
		maxX: maxX,
		minY: minY,
		maxY: maxY,
	}
}

func main() {
	answer.Timer(solution)
}

func solution() {
	groups := file.Default().Groups()
	answer.Part1(5437, litAfter(groups, 2))
	answer.Part2(19340, litAfter(groups, 50))
}

func litAfter(groups []string, times int) int {
	enhancer, image := getEnhancerImage(groups)
	for range times {
		image = image.enhance(enhancer)
	}
	return image.Len()
}

func getEnhancerImage(enhancerImage []string) (Enhancer, Image) {
	return Enhancer(enhancerImage[0]), parseImage(enhancerImage[1])
}

func parseImage(raw string) Image {
	grid := parser.GridMaker[string]{
		Rows:        util.Lines(raw),
		Splitter:    parser.Character,
		Ignore:      ".",
		Transformer: parser.Identity,
	}.Construct()
	return Image{
		Grid:  grid,
		times: 0,
	}
}
