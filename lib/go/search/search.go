package search

import (
	"advent-of-code/lib/go/queue"
)

type Hashable interface {
	Hash() uint64
}

type Bfs[T Hashable] struct {
	Initial    T
	Done       func(T) bool
	NextStates func(T) []T
}

func (search Bfs[T]) Run() []T {
	traversal := Traversal[T]{
		initial:    search.Initial,
		done:       search.Done,
		nextStates: search.NextStates,
		firstOnly:  false,
	}
	q := &queue.FifoQueue[T]{}
	return traversal.run(q)
}

type State interface {
	Hashable
	queue.Prioritized
}

type Dijkstra[T State] struct {
	Initial    T
	Done       func(T) bool
	NextStates func(T) []T
}

func (search Dijkstra[T]) Run() T {
	traversal := Traversal[T]{
		initial:    search.Initial,
		done:       search.Done,
		nextStates: search.NextStates,
		firstOnly:  true,
	}
	q := &queue.PriorityQueue[T]{}
	return traversal.run(q)[0]
}

type Traversal[T Hashable] struct {
	initial    T
	done       func(T) bool
	nextStates func(T) []T
	firstOnly  bool
}

func (search Traversal[T]) run(q queue.Queue[T]) []T {
	completed := []T{}
	seen := make(map[uint64]bool)
	q.Add(search.initial)
	for !q.Empty() {
		state := q.Next()
		hashState := state.Hash()
		_, ok := seen[hashState]
		if ok {
			continue
		}
		seen[hashState] = true
		if search.done(state) {
			completed = append(completed, state)
			if search.firstOnly {
				break
			}
		} else {
			for _, adjacent := range search.nextStates(state) {
				_, ok := seen[adjacent.Hash()]
				if !ok {
					q.Add(adjacent)
				}
			}
		}
	}
	return completed
}
