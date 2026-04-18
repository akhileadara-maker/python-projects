"""
Name: [Your Name]
Class: [Your Class]
Period: [Your Period]
Program: Sorting Project (Final Version)

This program compares:
Insertion Sort
Selection Sort
Bubble Sort
Merge Sort
Quick Sort (Median-of-Three)

Tracks:
- Comparisons
- Movements
- Execution Time
"""

import random
import time
import sys

sys.setrecursionlimit(10**8)

# Global counters
comparisons = 0
movements = 0


# ============================
# INSERTION SORT
# ============================

def insertion_sort(lst):
    global comparisons, movements

    for i in range(1, len(lst)):
        key = lst[i]
        movements += 1
        j = i - 1

        while j >= 0 and lst[j] > key:
            comparisons += 1
            lst[j + 1] = lst[j]
            movements += 1
            j -= 1

        if j >= 0:
            comparisons += 1

        lst[j + 1] = key
        movements += 1

    return lst


# ============================
# SELECTION SORT
# ============================

def selection_sort(arr):
    global comparisons, movements

    n = len(arr)

    for i in range(n - 1):
        min_index = i

        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_index]:
                min_index = j

        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]
            movements += 3

    return arr


# ============================
# BUBBLE SORT (NO EARLY EXIT)
# ============================

def bubble_sort(arr):
    global comparisons, movements

    n = len(arr)

    for i in range(n - 1):
        for j in range(n - i - 1):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                movements += 3

    return arr


# ============================
# MERGE SORT
# ============================

def merge_sort(lst):
    global comparisons, movements

    if len(lst) <= 1:
        return lst

    mid = len(lst) // 2
    left = merge_sort(lst[:mid])
    right = merge_sort(lst[mid:])

    return merge(left, right)


def merge(left, right):
    global comparisons, movements

    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i] <= right[j]:
            result.append(left[i])
            movements += 1
            i += 1
        else:
            result.append(right[j])
            movements += 1
            j += 1

    while i < len(left):
        result.append(left[i])
        movements += 1
        i += 1

    while j < len(right):
        result.append(right[j])
        movements += 1
        j += 1

    return result


# ============================
# QUICK SORT (MEDIAN OF THREE)
# ============================

def median_of_three(lst, low, high):
    global movements

    mid = (low + high) // 2

    if lst[low] > lst[mid]:
        lst[low], lst[mid] = lst[mid], lst[low]
        movements += 3

    if lst[low] > lst[high]:
        lst[low], lst[high] = lst[high], lst[low]
        movements += 3

    if lst[mid] > lst[high]:
        lst[mid], lst[high] = lst[high], lst[mid]
        movements += 3

    lst[mid], lst[high - 1] = lst[high - 1], lst[mid]
    movements += 3

    return lst[high - 1]


def insertion_sort_subarray(lst, low, high):
    global comparisons, movements

    for i in range(low + 1, high + 1):
        key = lst[i]
        movements += 1
        j = i - 1

        while j >= low and lst[j] > key:
            comparisons += 1
            lst[j + 1] = lst[j]
            movements += 1
            j -= 1

        lst[j + 1] = key
        movements += 1


def partition(lst, low, high):
    global comparisons, movements

    pivot = median_of_three(lst, low, high)

    i = low
    j = high - 1

    while True:
        i += 1
        while lst[i] < pivot:
            comparisons += 1
            i += 1

        j -= 1
        while lst[j] > pivot:
            comparisons += 1
            j -= 1

        if i >= j:
            break

        lst[i], lst[j] = lst[j], lst[i]
        movements += 3

    lst[i], lst[high - 1] = lst[high - 1], lst[i]
    movements += 3

    return i


def quick_sort(lst, low, high):
    if low + 10 <= high:
        pi = partition(lst, low, high)
        quick_sort(lst, low, pi - 1)
        quick_sort(lst, pi + 1, high)
    else:
        insertion_sort_subarray(lst, low, high)

    return lst


# ============================
# TEST LIST GENERATOR
# ============================

def generate_lists(n):
    lists = {}

    lists['in_order'] = list(range(1, n + 1))
    lists['reverse_order'] = list(range(n, 0, -1))

    lists['almost_order'] = list(range(1, n + 1))
    if n > 2:
        lists['almost_order'][2], lists['almost_order'][-1] = \
            lists['almost_order'][-1], lists['almost_order'][2]

    lists['random_order'] = list(range(1, n + 1))
    random.shuffle(lists['random_order'])

    return lists


def reset_counters():
    global comparisons, movements
    comparisons = 0
    movements = 0


def test_algorithm(sort_func, lst, is_quick=False):
    reset_counters()

    test_list = lst.copy()

    start = time.perf_counter()

    if is_quick:
        sort_func(test_list, 0, len(test_list) - 1)
    else:
        sort_func(test_list)

    end = time.perf_counter()

    return comparisons, movements, end - start


# ============================
# MAIN DRIVER
# ============================

def main():

    sizes = [10, 100, 1000, 10000]

    algorithms = [
        ("Selection Sort", selection_sort, False),
        ("Insertion Sort", insertion_sort, False),
        ("Bubble Sort", bubble_sort, False),
        ("Merge Sort", merge_sort, False),
        ("Quick Sort", quick_sort, True),
    ]

    for n in sizes:
        print(f"\n===== LIST SIZE: {n} =====")

        test_lists = generate_lists(n)

        for list_type, lst in test_lists.items():
            print(f"\n--- Input Type: {list_type} ---")

            for name, func, is_qs in algorithms:
                comps, moves, t = test_algorithm(func, lst, is_qs)
                print(f"{name:15} | Comparisons: {comps:12,} | "
                      f"Movements: {moves:12,} | Time: {t:.6f}s")


if __name__ == "__main__":
    main()
