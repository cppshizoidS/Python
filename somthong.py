import time
import random
import pygame
import math


def draw(values, index, is_current_rendering=False):
    pygame.draw.line(window, (0, 0, 0), [index, HEIGHT], [index, 0], 1)

    if is_current_rendering:
        pygame.draw.line(window, (255, 0, 0), [index, HEIGHT], [index, HEIGHT - values[index]], 1)
        pygame.display.update()

    pygame.draw.line(window, (values[index] // (HEIGHT / 256), 255 - values[index] // (HEIGHT / 256), 128),
                     [index, HEIGHT], [index, HEIGHT - values[index]], 1)

    if not is_current_rendering:
        pygame.display.update()


def bubble_sort(values, n):
	for i in range(n - 1):
		for j in range(n - i - 1):
			if values[j] > values[j + 1]:
				values[j], values[j + 1] = values[j + 1], values[j]
				draw(values, j, True)
				draw(values, j + 1, True)


def quick_sort(values, upper, lower=0):
	if lower >= upper:
		return

	pivot = values[(lower + upper) // 2]
	l, u = lower, upper

	while l <= u:
		while values[l] < pivot:
			l += 1
		while values[u] > pivot:
			u -= 1

		if l <= u:
			values[l], values[u] = values[u], values[l]

			draw(values, l, True)
			draw(values, u, True)

			l += 1
			u -= 1

	quick_sort(values, u, lower)
	quick_sort(values, upper, l)


def heapify(values, n, index):
	root = index

	first = 2 * index + 1
	second = 2 * index + 2

	if first < n and values[root] < values[first]:
		root = first

	if second < n and values[root] < values[second]:
		root = second

	if root != index:
		values[index], values[root] = values[root], values[index]
		draw(values, index, True)
		draw(values, root, True)

		heapify(values, n, root)


def heap_sort(values, n):
	for i in range(n // 2 - 1, -1, -1):
		heapify(values, n, i)

	for i in range(n - 1, 0, -1):
		values[0], values[i] = values[i], values[0]
		draw(values, 0, True)
		draw(values, i, True)

		heapify(values, i, 0)


def merge_sort(values, end, start=0):
	if end - start > 1:
		mid = (start + end) // 2

		merge_sort(values, mid, start)
		merge_sort(values, end, mid)

		merge(values, start, mid, end)


def merge(values, start, mid, end):
	left = values[start:mid]
	right = values[mid:end]
	left_index = 0
	right_index = 0
	index = start

	while start + left_index < mid and mid + right_index < end:
		if left[left_index] <= right[right_index]:
			values[index] = left[left_index]
			left_index += 1
		else:
			values[index] = right[right_index]
			right_index += 1

		draw(values, index, True)
		index += 1

	if start + left_index < mid:
		while index < end:
			values[index] = left[left_index]
			draw(values, index, True)
			left_index += 1
			index += 1
	else:
		while index < end:
			values[index] = right[right_index]
			draw(values, index, True)
			right_index += 1
			index += 1


def shell(values, n):
    step = n // 2
    while step > 0:
        for i in range(step, n - 1):
            j = i
            delta = j - step

            while delta >= 0 and values[delta] > values[j]:
                values[delta], values[j] = values[j], values[delta]
                draw(values, j, True)
                draw(values, delta, True)

                j = delta
                delta = j - step

        step //= 2


def shake(values, n):
    left = 0
    right = n - 1

    while left <= right:
        for i in range(left, right):
            if values[i] > values[i + 1]:
                values[i], values[i + 1] = values[i + 1], values[i]

                draw(values, i, True)
                draw(values, i + 1, True)

        right -= 1

        for i in range(right, left, -1):
            if values[i - 1] > values[i]:
                values[i], values[i - 1] = values[i - 1], values[i]

                draw(values, i, True)
                draw(values, i - 1, True)

        left += 1


def counting_sort(values, n):
    c = [0] * (HEIGHT + 1)

    for i in range(n):
        c[values[i]] += 1

    c[0] -= 1

    for i in range(1, HEIGHT + 1):
        c[i] += c[i - 1]

    result = [None] * n

    for x in reversed(values):
        result[c[x]] = x
        draw(result, c[x], True)
        c[x] -= 1


HEIGHT = 600
WIDTH = 1200

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Visualization")

sorts =  quick_sort, counting_sort, heap_sort, merge_sort, shell, shake, bubble_sort
data = []

for i in range(WIDTH):
    data.append(i % HEIGHT)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()

    window.fill((0, 0, 0))

    for i in range(len(sorts)):
        time.sleep(1)
        random.shuffle(data)

        for j in range(len(data)):
            draw(data, j)

        time.sleep(1)

        if not i:
            sorts[i](data, len(data) - 1)
            continue

        sorts[i](data, len(data))


