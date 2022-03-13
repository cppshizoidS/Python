def swap(self, left, right, array):
        array[left], array[right] = array[right], array[left]

def quickSort(self, start, end, array):
    if start > end:
        return

    pivot = start
    left = pivot + 1
    right = end
    while left <= right:
        if array[left] > array[pivot] and array[right] <= array[pivot]:
            self.swap(left, right, array)
        if array[left] <= array[pivot]:
            left += 1
        if array[right] > array[pivot]:
            right -= 1
    self.swap(pivot, right, array)

    leftArrayIsSmall = right - 1 - start < end - right + 1

    if leftArrayIsSmall:
        self.quickSort(start, right - 1, array)
        self.quickSort(right + 1, end, array)
    else:
            self.quickSort(right + 1, end, array)
            self.quickSort(start, right - 1, array)

def sortArray(self, nums: list[int]) -> list[int]:

    if not nums:
        return
    self.quickSort(0, len(nums) - 1, nums)
    return nums

