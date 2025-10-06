package util

func Filter[T any](values []T, f func(T) bool) []T {
	var result []T
	for _, value := range values {
		if f(value) {
			result = append(result, value)
		}
	}
	return result
}

func Map[T any, U any](values []T, f func(T) U) []U {
	var result []U
	for _, value := range values {
		result = append(result, f(value))
	}
	return result
}

func Sum(values []int) int {
	total := 0
	for _, value := range values {
		total += value
	}
	return total
}
