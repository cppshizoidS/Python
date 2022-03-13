# sorting algorithms of array
def bubblesort(arr):
    # Swap the elements
    for iter_num in range(len(arr) - 1, 0, -1):
        for idx in range(iter_num):
            if arr[idx] > arr[idx + 1]:
                temp = arr[idx]
                arr[idx] = arr[idx + 1]
                arr[idx + 1] = temp


arr = [20, 2, 37, 45, 6, 11, 219, 27]
bubblesort(arr)
print(arr)
