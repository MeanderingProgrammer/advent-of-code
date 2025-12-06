package queue

import (
	"container/heap"
)

type Queue[T any] interface {
	Add(value T)
	Next() T
	Empty() bool
}

// Basic queue implementation

type FifoQueue[T any] []T

func (q *FifoQueue[T]) Add(value T) {
	*q = append(*q, value)
}

func (q *FifoQueue[T]) Next() T {
	result := (*q)[0]
	*q = (*q)[1:]
	return result
}

func (q FifoQueue[T]) Empty() bool {
	return len(q) == 0
}

// Priority queue implementation

type Prioritized interface {
	Cost() int
}

type PriorityQueue[T Prioritized] []T

// Methods needed by container/heap module

func (q PriorityQueue[T]) Len() int {
	return len(q)
}

func (q PriorityQueue[T]) Less(i, j int) bool {
	return q[i].Cost() < q[j].Cost()
}

func (q PriorityQueue[T]) Swap(i, j int) {
	q[i], q[j] = q[j], q[i]
}

func (q *PriorityQueue[T]) Pop() any {
	length := len(*q)
	result := (*q)[length-1]
	*q = (*q)[:length-1]
	return result
}

func (q *PriorityQueue[T]) Push(state any) {
	*q = append(*q, state.(T))
}

// Methods that we actually interact with

func (q *PriorityQueue[T]) Add(state T) {
	heap.Push(q, state)
}

func (q *PriorityQueue[T]) Next() T {
	return heap.Pop(q).(T)
}

func (q PriorityQueue[T]) Empty() bool {
	return q.Len() == 0
}
