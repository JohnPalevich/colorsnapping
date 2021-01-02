def get_arr(path: str) -> [str]:
    arr = []
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            arr.append(line.rstrip('\n'))
    #print(arr)
    return arr

def create_dict(arr):
    d = {}
    for line in arr:
        key = line.split(':')[0]
        values = line.split(':')[1].split(',')
        d[key] = values
    return d

print(create_dict(get_arr('colordict.txt')))
