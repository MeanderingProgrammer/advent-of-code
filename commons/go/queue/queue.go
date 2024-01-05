package queue

import (
	"container/heap"
)

type State interface {
	Cost() int
	Hash() uint64
}

type Queue[T State] []T

// Methods needed by container/heap module

func (q Queue[T]) Len() int {
	return len(q)
}

func (q Queue[T]) Less(i, j int) bool {
	return q[i].Cost() < q[j].Cost()
}

func (q Queue[T]) Swap(i, j int) {
	q[i], q[j] = q[j], q[i]
}

func (q *Queue[T]) Pop() interface{} {
	length := len(*q)
	result := (*q)[length-1]
	*q = (*q)[:length-1]
	return result
}

func (q *Queue[T]) Push(state any) {
	*q = append(*q, state.(T))
}

// Methods that we actually interact with

func (q *Queue[T]) Add(state T) {
	heap.Push(q, state)
}

func (q *Queue[T]) Next() T {
	return heap.Pop(q).(T)
}

func (q Queue[T]) Empty() bool {
	return q.Len() == 0
}
