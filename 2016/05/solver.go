package main

import (
	"crypto/md5"
	"strconv"
	"sync"

	"advent-of-code/lib/go/answer"
	"advent-of-code/lib/go/async"
	"advent-of-code/lib/go/file"
	"advent-of-code/lib/go/util"
)

type Hasher struct {
	prefix string
}

func (h Hasher) Next(batch *async.Batch) <-chan []byte {
	result := make(chan []byte)
	var wg sync.WaitGroup
	for range batch.Batches {
		start := batch.Next()
		wg.Go(func() {
			for i := start; i < start+batch.Size; i++ {
				digest := h.Digest(i)
				if digest != nil {
					result <- *digest
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

func (h Hasher) Digest(i int) *[]byte {
	data := h.prefix + strconv.Itoa(i)
	hash := md5.Sum([]byte(data))
	if hash[0] == 0 && hash[1] == 0 && hash[2]&0xF0 == 0 {
		digest := util.HexDigest(hash)
		return &digest
	}
	return nil
}

func main() {
	answer.Timer(solution)
}

func solution() {
	prefix := file.Default().Content()
	hasher := Hasher{prefix}
	batch := async.Batch{
		Batches: 8,
		Size:    16384,
		Index:   0,
	}
	answer.Part1("d4cd2ee1", getPassword(hasher, batch, part1))
	answer.Part2("f2c730e5", getPassword(hasher, batch, part2))
}

func getPassword(hasher Hasher, batch async.Batch, update func(map[int]string, []byte)) string {
	password := make(map[int]string)
	for len(password) < 8 {
		for digest := range hasher.Next(&batch) {
			update(password, digest)
		}
	}

	result := ""
	for i := 0; i < len(password); i++ {
		result += password[i]
	}
	return result
}

func part1(password map[int]string, digest []byte) {
	password[len(password)] = string(digest[5])
}

func part2(password map[int]string, digest []byte) {
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
