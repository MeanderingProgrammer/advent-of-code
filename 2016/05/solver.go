package main

import (
	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/async"
	"advent-of-code/commons/go/file"
	"crypto/md5"
	"encoding/hex"
	"strconv"
)

type hashSearch struct {
	prefix string
}

func (h hashSearch) runBatch(start int, batchSize int) []string {
	results := []string{}
	for i := start; i < start+batchSize; i++ {
		hash := h.getHash(i)
		if hash[0:5] == "00000" {
			results = append(results, hash)
		}
	}
	return results
}

func (h hashSearch) getHash(i int) string {
	value := h.prefix + strconv.Itoa(i)
	result := md5.Sum([]byte(value))
	return hex.EncodeToString(result[:])
}

type Populator interface {
	populate(passwords map[int]string, hash string)
}

type Part1 struct{}

func (p *Part1) populate(passwords map[int]string, hash string) {
	passwords[len(passwords)] = string(hash[5])
}

type Part2 struct{}

func (p *Part2) populate(passwords map[int]string, hash string) {
	index, err := strconv.Atoi(string(hash[5]))
	if err != nil || index > 7 {
		return
	}
	_, ok := passwords[index]
	if ok {
		return
	}
	passwords[index] = string(hash[6])
}

func main() {
	doorId := file.Content()
	answer.Part1("d4cd2ee1", getPassword(doorId, &Part1{}))
	answer.Part2("f2c730e5", getPassword(doorId, &Part2{}))
}

func getPassword(doorId string, populator Populator) string {
	search := hashSearch{
		prefix: doorId,
	}
	passwords := make(map[int]string)
	batch := async.Batch[[]string]{
		Batches:   8,
		BatchSize: 2048,
		Index:     0,
		Complete: func() bool {
			return len(passwords) == 8
		},
		Work: search.runBatch,
		ProcessResults: func(results [][]string) {
			for _, result := range results {
				for _, hash := range result {
					populator.populate(passwords, hash)
				}
			}
		},
	}
	batch.Run()
	result := ""
	for i := 0; i < len(passwords); i++ {
		value, _ := passwords[i]
		result += value
	}
	return result
}
