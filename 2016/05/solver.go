package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/files"
	"crypto/md5"
	"encoding/hex"
	"strconv"
	"sync"
)

const (
	batches   = 8
	batchSize = 2048
)

type hashSearch struct {
	prefix string
}

func (h hashSearch) runBatch(start int) []string {
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
	doorId := files.Content()
	answers.Part1("d4cd2ee1", getPassword(doorId, &Part1{}))
	answers.Part2("f2c730e5", getPassword(doorId, &Part2{}))
}

func getPassword(doorId string, populator Populator) string {
	search := hashSearch{
		prefix: doorId,
	}
	index := 0
	passwords := make(map[int]string)
	for len(passwords) < 8 {
		results := make(chan []string, batches)
		var wg sync.WaitGroup
		for i := 0; i < batches; i++ {
			wg.Add(1)
			go func(start int) {
				defer wg.Done()
				results <- search.runBatch(start)
			}(index)
			index += batchSize
		}
		wg.Wait()
		close(results)
		for result := range results {
			for _, hash := range result {
				populator.populate(passwords, hash)
			}
		}
	}
	result := ""
	for i := 0; i < len(passwords); i++ {
		value, _ := passwords[i]
		result += value
	}
	return result
}
