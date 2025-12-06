package async

type Batch struct {
	Batches int
	Size    int
	Index   int
}

func (b *Batch) Next() int {
	result := b.Index
	b.Index += b.Size
	return result
}
