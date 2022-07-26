s = '111111111110000000000000000'

def task(array: list, value='0'):
    try:
        return array.index(value)
    except ValueError:
        return None

print(task(s))
