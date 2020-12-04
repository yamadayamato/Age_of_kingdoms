

class GameMap(list):
    def __call__(self, position):
        x, y = position.value
        return self[y][x]

    def __str__(self):
        rows = [''.join(map(str, ls)) for ls in self]
        return '\n'.join(rows)

    def print_centered_at(self, position, width=100, height=24):

        # The following is used to print the same number of digits when
        # printing row or column numbers:
        num_digits = 2 if len(self) <= 100 else 3
        def int_to_str(i):
            """Returns the i as a string with num_digits digits if i % 5 == 0.

            Otherwise this returns num_digits spaces"""
            if i % 5 == 0:
                return str(i).zfill(num_digits)
            else:
                return ' ' * num_digits

        if not position.is_on_the_map(self):
            print('You must choose a position that is on the map.')
            return

        horizontal_delta = width // 2
        vertical_delta = height // 2

        x0, y0 = position.value

        y_min = max(0, y0 - vertical_delta)
        y_max = min(len(self) - 1, y0 + vertical_delta)

        x_start = max(0, x0 - horizontal_delta)
        x_stop = min(len(self[0]), x0 + horizontal_delta)

        def print_column_numbers():
            for digit in range(num_digits):
                # The following line is to print an offset for the margin, which
                # (in the main part) is used to print the row numbers.
                print(' ' * num_digits, end='')
                for x in range(x_start, x_stop):
                    end = '' if x < x_stop - 1 else '\n'
                    print(int_to_str(x)[digit], end=end)

        def print_row(i):
            margin = int_to_str(i)
            row_content = ''.join(map(str, self[i][x_start:x_stop]))
            print(margin + row_content + margin)

        print_column_numbers()
        for i in range(y_max, y_min - 1, -1):
            print_row(i)
        print_column_numbers()