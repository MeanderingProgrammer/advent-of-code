package main

import (
	"crypto/md5"
	"strconv"
	"sync"

	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/async"
	"advent-of-code/commons/go/file"
)

type Hasher struct {
	prefix string
	mask   byte
}

func NewHasher(prefix string, zeros int) Hasher {
	masks := map[int]byte{
		5: 0xF0,
		6: 0xFF,
	}
	mask, ok := masks[zeros]
	if !ok {
		panic("invalid zeros")
	}
	return Hasher{prefix: prefix, mask: mask}
}

func (h Hasher) Next(batch *async.Batch) <-chan int {
	result := make(chan int)
	var wg sync.WaitGroup
	for range batch.Batches {
		start := batch.Next()
		wg.Go(func() {
			for i := start; i < start+batch.Size; i++ {
				if h.Match(i) {
					result <- i
				}
			}
		})
	}
	go func() {
		wg.Wait()
		close(result)
	}()
	return result
}

func (h Hasher) Match(i int) bool {
	data := h.prefix + strconv.Itoa(i)
	hash := md5.Sum([]byte(data))
	return hash[0] == 0 && hash[1] == 0 && hash[2]&h.mask == 0
}

func main() {
	answer.Timer(solution)
}

func solution() {
	prefix := file.Default().Content()
	batch := async.Batch{
		Batches: 8,
		Size:    1024,
		Index:   1,
	}
	answer.Part1(346386, firstIndex(NewHasher(prefix, 5), &batch))
	answer.Part2(9958218, firstIndex(NewHasher(prefix, 6), &batch))
}

func firstIndex(hasher Hasher, batch *async.Batch) int {
	var first *int
	for first == nil {
		// assumes there will not be multiple results in single batch set
		for result := range hasher.Next(batch) {
			first = &result
		}
	}
	return *first
}
