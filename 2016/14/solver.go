package main

import (
	"crypto/md5"
	"strconv"
	"sync"

	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/async"
	"advent-of-code/commons/go/file"
	"advent-of-code/commons/go/queue"
	"advent-of-code/commons/go/util"
)

type HashInfo struct {
	index     int
	triple    byte
	quintuple *byte
}

func (h HashInfo) Cost() int {
	return h.index
}

type Hasher struct {
	prefix string
	n      int
}

func NewHasher(prefix string, n int) Hasher {
	return Hasher{prefix, n}
}

func (h Hasher) Next(batch *async.Batch) <-chan HashInfo {
	result := make(chan HashInfo)
	var wg sync.WaitGroup
	for range batch.Batches {
		start := batch.Next()
		wg.Go(func() {
			for i := start; i < start+batch.Size; i++ {
				hash := h.Hash(i)
				if hash != nil {
					result <- *hash
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

func (h Hasher) Hash(i int) *HashInfo {
	data := []byte(h.prefix + strconv.Itoa(i))
	for i := 0; i < h.n; i++ {
		data = util.HexDigest(md5.Sum(data))
	}
	triple := repeat(data, 3)
	if triple == nil {
		return nil
	}
	return &HashInfo{
		index:     i,
		triple:    *triple,
		quintuple: repeat(data, 5),
	}
}

func repeat(value []byte, length int) *byte {
	for i := 0; i <= len(value)-length; i++ {
		if same(value, i, length) {
			return &value[i]
		}
	}
	return nil
}

func same(value []byte, start int, length int) bool {
	first := value[start]
	for i := start + 1; i < start+length; i++ {
		if value[i] != first {
			return false
		}
	}
	return true
}

func main() {
	answer.Timer(solution)
}

func solution() {
	prefix := file.Default().Content()
	batch := async.Batch{
		Batches: 8,
		Size:    64,
		Index:   0,
	}
	answer.Part1(15168, generate(NewHasher(prefix, 1), batch))
	answer.Part2(20864, generate(NewHasher(prefix, 2_017), batch))
}

func generate(hasher Hasher, batch async.Batch) int {
	hashes := &queue.PriorityQueue[HashInfo]{}
	for hashes.Empty() {
		for next := range hasher.Next(&batch) {
			hashes.Add(next)
		}
	}

	keys := []int{}
	for len(keys) < 64 {
		hash := hashes.Next()
		hashEnd := hash.index + 1_000

		for batch.Index <= hashEnd {
			for other := range hasher.Next(&batch) {
				hashes.Add(other)
			}
		}

		for _, other := range *hashes {
			if other.index <= hashEnd {
				value := other.quintuple
				if value != nil && hash.triple == *value {
					keys = append(keys, hash.index)
					break
				}
			}
		}
	}
	return keys[63]
}
