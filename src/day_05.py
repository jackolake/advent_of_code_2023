from typing import Dict, List, Tuple

resolution_order = ['seed', 'soil', 'fertilizer', 'water', 'light', 'temperature', 'humidity', 'location']

def intersect(current_range: Tuple[int, int], test_range: Tuple[int, int]) -> Tuple[int, int]:
    ''' intersect(current_range=(1, 5), test_range=(2, 3)) ==> (2, 3) '''
    start, end = max(current_range[0], test_range[0]), min(current_range[1], test_range[1])
    return (start, end) if start <= end else (None, None)

def subtract(current_range: Tuple[int, int], test_range: Tuple[int, int]) -> List[Tuple[int, int]]:
    ''' subtract(current_range=(1, 5), test_range=(2, 3)) => [(1, 1), (4, 5)] '''
    intersect_start, intersect_end = intersect(current_range, test_range)
    results = []
    if (intersect_start, intersect_end) == (None, None):
        return [current_range]
    elif (intersect_start, intersect_end) == current_range:
        return []
    if intersect_start > current_range[0]:
        results.append((current_range[0], intersect_start - 1))
    if intersect_end < current_range[1]:
        results.append((intersect_end + 1, current_range[1]))
    return results

def transform(start_end_list: List[Tuple[int, int]], mapping_rules: List[Tuple[int, int, int]]):
    ''' transform([(1, 5), [(2, 12, 2)]] => [(1, 1), (12, 13), (4, 5)] '''
    transformed_ranges = []
    for from_start, from_end in start_end_list:
        unmapped_ranges = [(from_start, from_end)]
        for map_from_start, map_to_start, map_range in mapping_rules:
            map_from_end = map_from_start + map_range - 1
            transformational_shift = map_to_start - map_from_start
            overlap_start, overlap_end = intersect((from_start, from_end), (map_from_start, map_from_end))
            if (overlap_start, overlap_end) != (None, None):
                # Transform according to mapping rule specified
                transformed_ranges.append((overlap_start + transformational_shift, overlap_end + transformational_shift))
                # Reduce unmapped ranges
                unmapped_ranges = [survivor for unmapped_range in unmapped_ranges for survivor in subtract(unmapped_range, (overlap_start, overlap_end))]
        # Not mapped => leave them as-is
        transformed_ranges.extend(unmapped_ranges)
    return transformed_ranges


def find_min_location(seed_ranges: List[Tuple[int, int]], map_dict: Dict[Tuple[str, str], List[Tuple[int, int, int]]]) -> int:
    current_ranges = seed_ranges  # [(start1, end1), (start2, end2), ...]
    for i in range(len(resolution_order) - 1):
        from_key, to_key = resolution_order[i], resolution_order[i + 1]
        current_ranges = transform(current_ranges, map_dict[(from_key, to_key)])
    return min([start for start, end in current_ranges])

def part1(seed_list: List[int], map_dict: Dict[Tuple[str, str], Tuple[int, int, int]]) -> int:
    return find_min_location([(s, s) for s in seed_list], map_dict)
        
def part2(seed_list: List[int], map_dict: Dict[int, Tuple[int, int]]) -> int:
    return find_min_location([(seed_list[2 * i], seed_list[2 * i] + seed_list[2 * i + 1] - 1) for i in range(int(len(seed_list) / 2))], map_dict)

if __name__ == '__main__':
    seed_list = list()
    map_dict = dict()   # {('seed', 'soil'): (source_start, destination_start, range_length)}}
    with open('input/day_05.txt', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('seeds: '):
                seed_list = [int(n) for n in line.split(': ')[-1].split(' ')]
            elif line.endswith('map:'):
                from_key, to_key = line.split(' ')[0].split('-to-') # e.g. 'seed-to-soil map:'
                map_dict[(from_key, to_key)] = []
                mapping_rules = map_dict[(from_key, to_key)]
            elif line:
                destination_start_string, source_start_string, range_length_string = line.split(' ')
                mapping_rules.append((int(source_start_string), int(destination_start_string), int(range_length_string)))

    # Start
    print(f'Part 1: {part1(seed_list, map_dict)}')
    print(f'Part 2: {part2(seed_list, map_dict)}')
