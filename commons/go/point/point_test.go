package point

import (
	"testing"
)

func TestAdd(t *testing.T) {
	p1 := Point{X: 3, Y: 6}
	p2 := p1.Add(-1, 2)
	expected := Point{X: 2, Y: 8}
	if p2 != expected {
		t.Errorf("got %+v, wanted %+v", p2, expected)
	}
}
