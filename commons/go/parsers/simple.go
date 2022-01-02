package parsers

import(
	"advent-of-code/commons/go/conversions"
	"strings"
)

func SubstringAfter(s, sep string) string {
	return strings.SplitN(s, sep, 2)[1]
}

func IntCsv(s string) []int {
	var result []int
	for _, value := range strings.Split(s, ",") {
		result = append(result, conversions.ToInt(value))
    }
	return result
}
