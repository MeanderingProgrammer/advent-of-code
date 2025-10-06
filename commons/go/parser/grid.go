package parser

import (
	"fmt"
	"strings"

	"advent-of-code/commons/go/grid"
	"advent-of-code/commons/go/point"
	"advent-of-code/commons/go/util"
)

type RowSplitter int

const (
	Field RowSplitter = iota
	Character
)

func (splitter RowSplitter) get() func(string) []string {
	switch splitter {
	case Field:
		return func(row string) []string {
			return strings.Fields(row)
		}
	case Character:
		return func(row string) []string {
			return strings.Split(row, "")
		}
	default:
		panic(fmt.Sprintf("Unknown splitter: %d", splitter))
	}
}

type ValueParser[T comparable] func(point.Point, string) T

func Identity(p point.Point, value string) string {
	return value
}

func ToInt(p point.Point, value string) int {
	return util.ToInt(value)
}

type GridMaker[T comparable] struct {
	Rows        []string
	Splitter    RowSplitter
	Ignore      string
	Transformer ValueParser[T]
}

func (maker GridMaker[T]) Construct() grid.Grid[T] {
	plane, f := make(map[point.Point]T), maker.Splitter.get()
	for y, row := range maker.Rows {
		for x, value := range f(row) {
			if !strings.ContainsAny(value, maker.Ignore) {
				point := point.Point{X: x, Y: y}
				plane[point] = maker.Transformer(point, value)
			}
		}
	}
	return grid.New(plane, len(maker.Rows)-1, len(f(maker.Rows[0]))-1)
}
