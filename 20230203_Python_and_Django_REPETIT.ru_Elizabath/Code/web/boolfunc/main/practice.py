import numpy as np
from IPython.display import display, HTML


def is_power_of_two(n):
    return (n != 0) and (n & (n - 1) == 0)


def display_sbs(*args):
    'display side by side'
    ''
    html_str = '''\
<div style="display: flex; gap: 2em; align-items: flex-start">
{}
</div>'''.format('\n'.join(arg._repr_html_() for arg in args))

    display(HTML(html_str))


class DNF:
    def __init__(self, masks):
        '''
        masks: ([0, 0, 0, 0], [0, 1, 1, 0], ...)
        '''
        self.n = len(masks[0])
        self.masks = masks

    def __call__(self, arg):
        '''
        Dычисляет значение DNF на векторе x

        arg: int
        '''
        n = self.n
        x = [int(i) for i in f'{arg:0{n}b}']  # бинарное представление числа arg ширины n
        return any(
            all(arg if bit else not arg for arg, bit in zip(x, mask))
            for mask in self.masks
        )

    def to_function(self):
        '''
        Преобразует DNF в BFunction
        '''
        return BFuncion(
            [self(i) for i in range(2 ** self.n)]
        )

    @classmethod
    def from_string(cls, string):
        return cls([
            [
                0 if var.strip()[0] == '~' else 1
                for var in s.split('&')
            ]
            for s in string.split('|')
        ])

    def _repr_latex_(self):
        # 0110 -> \overline{x}_0 x_1 x_2 \overline{x}_3
        n = self.n
        return '$' + ' \lor '.join(
            ' '.join(
                f'x_{k}' if x else f'\\overline{{x}}_{k}'
                for k, x in enumerate(mask)
            )
            for mask in self.masks
        ) + '$'


class CNF:
    def __init__(self, masks):
        '''
        masks: ([0, 0, 0, 0], [0, 1, 1, 0], ...)
        '''
        self.n = len(masks[0])
        self.masks = masks

    def __call__(self, arg):
        '''
        Dычисляет значение CNF на векторе x

        arg: int
        '''
        n = self.n
        x = [int(i) for i in f'{arg:0{n}b}']  # бинарное представление числа arg ширины n
        return all(
            any(arg if bit else not arg for arg, bit in zip(x, mask))
            for mask in self.masks
        )

    def to_function(self):
        '''
        Преобразует DNF в BFunction
        '''
        return BFuncion(
            [self(i) for i in range(2 ** self.n)]
        )

    @classmethod
    def from_string(cls, string):
        return cls([
            [
                0 if var.strip()[0] == '~' else 1
                for var in s.strip(' )(').split('|')
            ]
            for s in string.split('&')
        ])

    def _repr_latex_(self):
        # 0110 -> \overline{x}_0 x_1 x_2 \overline{x}_3
        n = self.n
        return '$' + ' \land '.join(
            '({})'.format(' \lor '.join(
                f'x_{k}' if x else f'\\overline{{x}}_{k}'
                for k, x in enumerate(mask)
            ))
            for mask in self.masks
        ) + '$'


class BFuncion:
    def __init__(self, values):
        '''
        values: [0, 1, ..] или numpy массив
            вектор значений функции
        n: int
            арность функции
        nf: int
            колличество записей в таблице истинности
        '''
        len_values = len(values)
        assert is_power_of_two(len_values), 'Length not power of 2'  # проверка на степень двойки
        self.n = len_values.bit_length() - 1
        self.nf = len_values
        self.values = np.array(values, dtype=np.bool_)

    def __call__(self, arg):
        '''
        arg: int или массив numpy длины n из bool
            аргумент функции
        '''
        n = self.n
        if isinstance(arg, int):
            idx = arg
        else:
            idx = np.inner(arg, np.logspace(n - 1, 0, num=n, base=2, dtype=int))

        return self.values[idx]

    def __eq__(self, other):
        'Проверка функций на равенство f1 == f2'
        assert isinstance(other, type(self))
        return np.array_equal(self.values, other.values)

    @classmethod
    def random(cls, n):
        '''
        Генерирует случайную функцию от n переменных

        n : int
            колличество аргументов функции
        '''
        rng = np.random.default_rng()
        values = rng.integers(0, 2, 2 ** n, dtype=np.bool_)
        return cls(values)

    def partial(self, sigma, index):
        '''
        Получить остаточную функцию

        sigma: bool, 0 or 1
            значение переменной для остаточной функции

        index: int, [0; n)
            индекс переменной в промежутке [0, n)
        '''
        rindex = self.n - 1 - index
        mask = 1 << rindex
        return type(self)([
            v
            for i, v in enumerate(self.values)
            if (i & mask) >> rindex == sigma
        ])

    def dnf(self):
        '''
        Построение СДНФ
        '''
        n = self.n
        return DNF([
            [int(b) for b in f'{i:0{n}b}']  # список из битов i
            for i in range(self.nf)
            if f(i) == 1
        ])

    def cnf(self):
        '''
        Построение СКНФ
        '''
        n = self.n
        return CNF([
            [int(b) for b in f'{i ^ ((1 << n) - 1):0{n}b}']  # список из инвертируемых битов i
            for i in range(self.nf)
            if f(i) == 0
        ])

    # def __str__(self):
    #     return '\n'.join([
    #         '|'.join([f'x{i}' for i in range(1, n+1)] + ['-> f(x)']),
    #         '|'.join(':---:' for _ in range(n + 1)),
    #         *[
    #             '|'.join(list(f'{i:0{n}b}') + [f'-> {self(i):b}'])
    #             for i in range(nf)
    #         ],
    #     ])

    def _repr_html_(self):
        '''
        представление функции в виде таблички
        '''
        n = self.n
        nf = self.nf
        tab = ' ' * 2
        nl = '\n'
        return '\n'.join([
            '''\
            <style>
              td {
                  text-align: center !important;
              }
            
              td:last-child {
                border-left: solid 1px var(--jp-ui-font-color3) !important;
              }
            </style>
            ''',
            '<table>',
            f'{tab}<thead>',
            f'''{2 * tab}<tr>\n{
            nl.join(
                [f'{3 * tab}<th>x<sub>{i}</sub></th>' for i in range(n)] +
                [f'{3 * tab}<th>f(x)</th>']
            )
            }\n{2 * tab}</tr>''',
            f'{tab}</thead>',
            f'{tab}<tbody>',
            *[
                f'''{2 * tab}<tr>\n{
                nl.join(
                    [f'{3 * tab}<td>{x}</td>' for x in f'{i:0{n}b}'] +
                    [f'{3 * tab}<td>{self(i):b}</td>']
                )
                }\n{2 * tab}</tr>'''
                for i in range(nf)
            ],
            f'{tab}</tbody>',
            '</table>',
        ])


def bfunction_from_partials(values0, values1, index):
    '''
    Создание булевой функции из нулевой и единичной остаточной

    values0: [0, 1, ..] или numpy массив
        нулевая остаточная

    values1: [0, 1, ..] или numpy массив
        единичная остаточная

    index: int
        индекс переменной в промежутке [0, n)
    '''
    nf = 2 * len(values0)
    n = nf.bit_length() - 1
    assert index < n
    rindex = n - 1 - index
    mask = 1 << rindex
    values = [values0, values1]
    return BFuncion([
        values[(i & mask) >> rindex][(i >> (rindex + 1) << rindex) + i % mask]
        for i in range(nf)
    ])