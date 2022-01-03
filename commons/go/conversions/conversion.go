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

func ToString(value int) string {
	return strconv.Itoa(value)
}

func BinaryToDecimal(value string) int {
	result, err := strconv.ParseInt(value, 2, 64)
	utils.CheckError(err)
	return int(result)
}

func DecimalToBinary(decimal int) string {
	return strconv.FormatInt(int64(decimal), 2)
}

func HexToDecimal(hexadecimal string) int {
    result, err := strconv.ParseInt(hexadecimal, 16, 64)
	utils.CheckError(err)
    return int(result)
}
