import numpy as np

np_map = np.zeros((8, 8, 8))

np_map[0][0][0] = 4
np_map[0][1][1] = 4
np_map[0][2][2] = 4
np_map[0][3][3] = 4

def search_arr(arr: list, query):
    locationarr = np.where(np_map == 4)
    li = []
    for i in range(0, len(locationarr[0])):
        tmpli = []
        for j in range(0, 3):
            tmpli.append(locationarr[j][i])
        li.append(tmpli)
    return li


print(np_map)