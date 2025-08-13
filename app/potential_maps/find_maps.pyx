def find_potential_maps(unpacked):
    cdef int i = 0
    cdef int y_axis, x_axis, j, whole_size
    cdef bint found_y_axis, found_x_axis
    cdef list potential_maps_start = []
    cdef list potential_maps_end = []

    while i < len(unpacked) - 90:
        y_axis = 0
        x_axis = 0
        found_y_axis = False
        found_x_axis = False

        # Search for the Y-axis
        for j in range(17):
            if unpacked[i + j] >= unpacked[i + j + 1]:
                if j < 7:
                    found_y_axis = False
                    break
                else:
                    found_y_axis = True
                    y_axis = j + 1
                    break
            elif j == 16:
                found_y_axis = False

        # If Y-axis is found, search for the X-axis
        if found_y_axis:
            for j in range(17):
                if unpacked[i + j + y_axis] >= unpacked[i + j + 1 + y_axis]:
                    if j < 7:
                        found_x_axis = False
                        break
                    else:
                        found_x_axis = True
                        x_axis = j + 1
                        break
                elif j == 16:
                    found_x_axis = False

        # If both X and Y axes are found and the conditions are met
        if found_x_axis and found_y_axis and not (unpacked[i] != 0 and unpacked[i] < 500):
            whole_size = x_axis + y_axis + (x_axis * y_axis)
            potential_maps_start.append(i + x_axis + y_axis)
            potential_maps_end.append(i + whole_size - 1)
            i += whole_size
        else:
            i += 1

    return potential_maps_start, potential_maps_end
