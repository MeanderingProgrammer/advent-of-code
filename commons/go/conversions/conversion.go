package conversions

import (
	"advent-of-code/commons/go/utils"
	"strconv"
)

func ToInt(value string) int {
	result, err := strconv.Atoi(value)
	utils.CheckError(err)
	return result
}
