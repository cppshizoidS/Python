# sorting algorithms of array
def bubblesort(arr):
        n = len(arr)

        for i in range(n):

            for j in range(0, n - i - 1):

                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]

def countingSort(arr, min, max):
    # initialize 0 array for keeping count of each key
    count = [0] * (max + 1 - min)

    # count the occurances of each number
    for i in arr:
        count[i - min] += 1

    z = 0
	# insert each element as many times onto the output array as they appear in count
    for i in range(min, max + 1):
        while (count[i - min] > 0):
            print(i)
            arr[z] = i
            z += 1
            count[i - min] -= 1

    return arr

def insertionSort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while (j >= 0 and arr[j] > key):
            arr[j + 1] = arr[j]
            j = j - 1

        arr[j + 1] = key

def mergeSort(arr):


arr = [20, 2, 37, 45, 6, 11, 219, 27]
bubblesort(arr)
print(arr)
