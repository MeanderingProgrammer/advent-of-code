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

func BinaryToDecimal(value string) int {
	result, err := strconv.ParseInt(value, 2, 64)
	utils.CheckError(err)
	return int(result)
}
