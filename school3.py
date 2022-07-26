from typing import Iterable

def pairwise(iterable: Iterable):
    iterable = iter(iterable)
    return list(zip(iterable, iterable))


def update_borders(intervals: list, left, right):
    new_inrevals = intervals.copy()

    for interval in intervals:
        if interval[0] <= left <= interval[1]:
            new_inrevals[0] = (left, interval[1])
            break
        if left <= interval[0] and left <= interval[1]:
            break
        new_inrevals.pop(0)

    for interval in reversed(intervals):
        if interval[0] <= right <= interval[1]:
            new_inrevals[-1] = (interval[0], right)
            break
        if interval[0] <= right and interval[1] <= right:
            break
        new_inrevals.pop(-1)

    return new_inrevals


def is_intersect(segment_a, segment_b):
    return segment_a[0] < segment_b[1] and segment_a[1] > segment_b[0]


def count_intersection(segment_a, segment_b):
    return min(segment_a[1], segment_b[1]) - max(segment_a[0], segment_b[0])


def pair_union(segment_a, segment_b):
    return (min(segment_a[0], segment_b[0]), max(segment_a[1], segment_b[1]))


def intersection(intervals1, intervals2):
    result = 0

    for interval_out in intervals1:
        for interval_in in intervals2:
            if is_intersect(interval_out, interval_in):
                result += count_intersection(interval_out, interval_in)
                
    return result


def intersection_opt(intervals_a, intervals_b, right):
    result = 0
    iter_a = iter(intervals_a)
    iter_b = iter(intervals_b)

    try:
        pair_a = next(iter_a)
        pair_b = next(iter_b)
        cursor = min(pair_a[1], pair_b[1])

        while True:
            if is_intersect(pair_a, pair_b):
                result += count_intersection(pair_a, pair_b)

            if cursor < pair_b[1]:
                pair_a = next(iter_a)
                cursor = min(pair_a[1], pair_b[1])
            elif cursor < pair_a[1]:
                pair_b = next(iter_b)
                cursor = min(pair_a[1], pair_b[1])
            elif cursor == right:
                raise StopIteration
    except StopIteration:
        ...
    return result


def validate_intervals(intervals):
    merged = [intervals[0]]

    for current in intervals:
        previous = merged[-1]
        if current[0] <= previous[1]:
            merged[-1] = (previous[0], max(previous[1], current[1]))
        else:
            merged.append(current)
    return merged


def appearance(intervals):
    # допустим все диапазоны - отсортированы по дате начала интервала
    # собрать крайнюю левую и правую границы диапазона
    # провалидировать диапазоны ученика и учителя
    # обрезать интервалы ученика и учителя по уроку
    # найти пересечение ученика и учителя

    lesson = intervals['lesson']
    pupil = intervals['pupil']
    tutor = intervals['tutor']

    left = max(lesson[0], pupil[0], tutor[0])
    right = min(lesson[-1], pupil[-1], tutor[-1])

    result = intersection_opt(
        update_borders(validate_intervals(pairwise(pupil)), left, right),
        update_borders(validate_intervals(pairwise(tutor)), left, right),
        right
    )

    return result


tests = [
    {'data': {
    'lesson': [1594663200, 1594666800],
    'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
    'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'data': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542,
1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582,
1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480,
1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875,
1594706502, 1594706503, 1594706524, 1594706524, 1594706579,
1594706641],
            # 'pupil': [1594702789, 1594704542, 1594704564, 1594706480, 1594706500, 1594706875],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148,
1594705149, 1594706463]},
    'answer': 3577
    },
{'data': {
    'lesson': [1594692000, 1594695600],
    'pupil': [1594692033, 1594696347],
    'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
}, ]


if __name__ == '__main__':
   for i, test in enumerate(tests):
       test_answer = appearance(test['data'])
       assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'

