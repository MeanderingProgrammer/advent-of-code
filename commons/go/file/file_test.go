package file

import (
	"os"
	"testing"

	"advent-of-code/commons/go/util"

	"github.com/stretchr/testify/assert"
)

func TestContent(t *testing.T) {
	file := newFile([]string{"abcd", "efg"})
	defer os.Remove(file)
	assert.Equal(t, "abcd\nefg\n", New[string](file).Content())
}

func TestReadLines(t *testing.T) {
	file := newFile([]string{"abcd", "efg"})
	defer os.Remove(file)
	assert.Equal(t, []string{"abcd", "efg", ""}, New[string](file).ReadLines())
}

func TestReadGroups(t *testing.T) {
	file := newFile([]string{"abcd", "efg", "", "hij"})
	defer os.Remove(file)
	assert.Equal(t, []string{"abcd\nefg", "hij\n"}, New[string](file).ReadGroups())
}

func newFile(lines []string) string {
	f := util.Must1(os.CreateTemp("", "*"))
	for _, line := range lines {
		util.Must1(f.Write([]byte(line + "\n")))
	}
	util.Must0(f.Close())
	return f.Name()
}
