# sorting algorithms of array
def bubblesort(arr):
        n = len(arr)

        for i in range(n):

            for j in range(0, n - i - 1):

                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]


arr = [20, 2, 37, 45, 6, 11, 219, 27]
bubblesort(arr)
print(arr)
