use aoc_lib::iter::Iter;

#[test]
fn test_combinations() {
    let values = [0, 1, 2, 3, 4];
    assert_eq!(
        vec![vec![&0], vec![&1], vec![&2], vec![&3], vec![&4],],
        values.iter().combinations(1).vec()
    );
    assert_eq!(
        vec![
            vec![&0, &1],
            vec![&0, &2],
            vec![&0, &3],
            vec![&0, &4],
            vec![&1, &2],
            vec![&1, &3],
            vec![&1, &4],
            vec![&2, &3],
            vec![&2, &4],
            vec![&3, &4]
        ],
        values.iter().combinations(2).vec()
    );
    assert_eq!(
        vec![
            vec![&0, &1, &2],
            vec![&0, &1, &3],
            vec![&0, &1, &4],
            vec![&0, &2, &3],
            vec![&0, &2, &4],
            vec![&0, &3, &4],
            vec![&1, &2, &3],
            vec![&1, &2, &4],
            vec![&1, &3, &4],
            vec![&2, &3, &4],
        ],
        values.iter().combinations(3).vec()
    );
    assert_eq!(
        vec![
            vec![&0, &1, &2, &3],
            vec![&0, &1, &2, &4],
            vec![&0, &1, &3, &4],
            vec![&0, &2, &3, &4],
            vec![&1, &2, &3, &4],
        ],
        values.iter().combinations(4).vec()
    );
    assert_eq!(
        vec![vec![&0, &1, &2, &3, &4]],
        values.iter().combinations(5).vec()
    );
}

#[test]
fn test_permutations() {
    let values = [0, 1, 2, 3];
    assert_eq!(
        vec![
            vec![&0, &1, &2, &3],
            vec![&0, &1, &3, &2],
            vec![&0, &2, &1, &3],
            vec![&0, &2, &3, &1],
            vec![&0, &3, &1, &2],
            vec![&0, &3, &2, &1],
            vec![&1, &0, &2, &3],
            vec![&1, &0, &3, &2],
            vec![&1, &2, &0, &3],
            vec![&1, &2, &3, &0],
            vec![&1, &3, &0, &2],
            vec![&1, &3, &2, &0],
            vec![&2, &0, &1, &3],
            vec![&2, &0, &3, &1],
            vec![&2, &1, &0, &3],
            vec![&2, &1, &3, &0],
            vec![&2, &3, &0, &1],
            vec![&2, &3, &1, &0],
            vec![&3, &0, &1, &2],
            vec![&3, &0, &2, &1],
            vec![&3, &1, &0, &2],
            vec![&3, &1, &2, &0],
            vec![&3, &2, &0, &1],
            vec![&3, &2, &1, &0],
        ],
        values.iter().permutations().vec()
    );
}
