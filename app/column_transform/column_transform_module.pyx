def gather_values(int shift_count, int columns, list values):
    cdef list current_values = [None] * shift_count
    cdef int i, j

    for row in values:
        for col in row:
            if col is not None:
                current_values.append(col)

    cdef list rows = [current_values[i:i + columns] for i in
                      range(0, len(current_values), columns)]

    if len(rows) > 0 and len(rows[-1]) < columns:
        rows[-1].extend([None] * (columns - len(rows[-1])))

    return current_values, rows
