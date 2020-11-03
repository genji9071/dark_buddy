class Solution():
    def findMagicIndex(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        left = 0
        right = len(nums) - 1
        try_index = int(right / 2)
        while True:
            if nums[try_index] == try_index:
                return nums[try_index]
            if right - left < 2:
                return -1
            if try_index > nums[try_index] - 1:
                left = try_index
                try_index = int((right - try_index) / 2 + try_index)
            else:
                right = try_index
                try_index = int((try_index - left) / 2)

if __name__ == "__main__":
    solution = Solution()
    print(solution.findMagicIndex([32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32]))