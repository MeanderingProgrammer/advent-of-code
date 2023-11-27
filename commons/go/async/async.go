package async

import (
	"fmt"
	"sync"
)

type Batch[T any] struct {
	Batches        int
	BatchSize      int
	Index          int
	Complete       func() bool
	Work           func(i int, batchSize int) T
	ProcessResults func(results []T)
}

func (b *Batch[T]) Run() {
	fmt.Println(b)
	for !b.Complete() {
		resultChan := make(chan T, b.Batches)
		var wg sync.WaitGroup
		for i := 0; i < b.Batches; i++ {
			wg.Add(1)
			go func(start int) {
				defer wg.Done()
				resultChan <- b.Work(start, b.BatchSize)
			}(b.Index)
			b.Index += b.BatchSize
		}
		wg.Wait()
		close(resultChan)
		results := []T{}
		for result := range resultChan {
			results = append(results, result)
		}
		b.ProcessResults(results)
	}
}
