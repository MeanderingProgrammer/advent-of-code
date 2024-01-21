package point

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestAdd(t *testing.T) {
	p1 := Point{X: 3, Y: 6}
	p2 := p1.Add(-1, 2)
	expected := Point{X: 2, Y: 8}
	assert.Equal(t, p2, expected)
}
