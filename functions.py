def getindex(coords: tuple[int, int, int], array) -> tuple[int, int, int]:
    for i in coords:
        if i >= len(array):
            raise IndexError('coordinates out of bounds')
    return (coords[2], len(array)-(coords[1]+1), coords[0])
