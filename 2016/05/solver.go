package main

import (
	"crypto/md5"
	"encoding/hex"
	"strconv"

	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/async"
	"advent-of-code/commons/go/file"
)

type Search struct {
	prefix string
}

func (s Search) runBatch(start int, batchSize int) []string {
	results := []string{}
	for i := start; i < start+batchSize; i++ {
		digest := s.getDigest(i)
		if digest[0:5] == "00000" {
			results = append(results, digest)
		}
	}
	return results
}

func (s Search) getDigest(i int) string {
	value := s.prefix + strconv.Itoa(i)
	result := md5.Sum([]byte(value))
	return hex.EncodeToString(result[:4])
}

func main() {
	answer.Timer(solution)
}

func solution() {
	prefix := file.Default().Content()
	answer.Part1("d4cd2ee1", getPassword(prefix, part1))
	answer.Part2("f2c730e5", getPassword(prefix, part2))
}

func getPassword(prefix string, update func(map[int]string, string)) string {
	search := Search{prefix}
	password := make(map[int]string)
	batch := async.Batch[[]string]{
		Batches:   8,
		BatchSize: 16384,
		Index:     0,
		Complete: func() bool {
			return len(password) == 8
		},
		Work: search.runBatch,
		ProcessResults: func(results [][]string) {
			for _, result := range results {
				for _, digest := range result {
					update(password, digest)
				}
			}
		},
	}
	batch.Run()
	result := ""
	for i := 0; i < len(password); i++ {
		value := password[i]
		result += value
	}
	return result
}

func part1(password map[int]string, digest string) {
	password[len(password)] = string(digest[5])
}

func part2(password map[int]string, digest string) {
	index, err := strconv.Atoi(string(digest[5]))
	if err != nil || index > 7 {
		return
	}
	_, ok := password[index]
	if ok {
		return
	}
	password[index] = string(digest[6])
}
