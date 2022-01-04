package utils

func CheckError(err error) {
	if err != nil {
		panic(err)
	}
}

func Abs(value int) int {
	result := value
	if value < 0 {
		return result * -1
	}
	return result
}

func Max(v1, v2 int) int {
	result := v1
	if v2 > v1 {
		result = v2
	}
	return result
}

func Min(v1, v2 int) int {
	result := v1
	if v2 < v1 {
		result = v2
	}
	return result
}
