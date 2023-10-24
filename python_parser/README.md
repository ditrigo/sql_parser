если(x + y < z, то a, иначе b)
если(x + y < z, то a, иначе если(m > n, то c, иначе d))
если(если(k + l = m, то q, иначе w) + y < z, то a, иначе b)

input_str = "(if (if x + y == z then q else r) > b then x else (if c < d then y else z)) + (if e < f then g else h)"

[
    ['cond', 
        [
            ['add_before', 'a + '], 
            ['cond', 'вклад>300'], 
            ['res1', '5'], 
            ['res2', 
            [
                ['cond', 'выручка>123'], 
                ['res1', '333'], 
                ['res2', '444']
            ]
            ], 
            ['add_after', ' + b>100']
        ]
    ], 
    ['res1', '2'], 
    ['res2', '10']
]

-----------------------------------------



[
    'cond', 
    [
        'add_before', 'a + ', 
        'cond', 'вклад>300', 
        'res1', '5', 
        'res2', 
        [
            'cond', 'выручка>123', 
            'res1', '333', 
            'res2', '444'
        ], 
        'add_after', 
        ' + b>100'
    ], 
    'res1', '2', 
    'res2', '10'
]