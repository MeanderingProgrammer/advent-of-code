package graphs

import (
	"container/heap"
)

type State interface {
	Positions() map[Vertex]interface{}
	Cost() int
}

type Queue []State

// Methods needed by container/heap module

func (q Queue) Len() int {
	return len(q)
}

func (q Queue) Less(i, j int) bool {
	return q[i].Cost() < q[j].Cost()
}

func (q Queue) Swap(i, j int) {
	q[i], q[j] = q[j], q[i]
}

func (q *Queue) Pop() interface{} {
	length := len(*q)
	result := (*q)[length-1]
	*q = (*q)[:length-1]
	return result
}

func (q *Queue) Push(state interface{}) {
	*q = append(*q, state.(State))
}

// Methods that we actually interact with

func (q *Queue) Add(state State) {
	heap.Push(q, state)
}

func (q *Queue) Next() State {
	return heap.Pop(q).(State)
}
