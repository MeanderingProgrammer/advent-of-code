package file

import (
	"advent-of-code/commons/go/util"
	"os"
	"testing"

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
	f, err := os.CreateTemp("", "*")
	util.CheckError(err)
	for _, line := range lines {
		_, err = f.Write([]byte(line + "\n"))
		util.CheckError(err)
	}
	err = f.Close()
	util.CheckError(err)
	return f.Name()
}
