from enum import Enum

def generateHeapSize(n: int, l: int=0) -> int:
    """
    Generate a heap size that is wholly complete (a full pyramid with no holes) that
    will fit n-nodes. Given n may be smaller than the returned heap size.

    [1, 3, 7, 15, 31, ..., 2^(j+1)-1] where j is the number of layers in the heap.

    **Parameters**
    - *n: int*
    > Size of the given dataset. 
    - *l: int*
    > Number of layers to go beyond what would've normally been returned.

    > generateHeapSize(n=14, l=0) --> 15

    > generateHeapSize(n=14, l=1) --> 31

    > generateHeapSize(n=7, l=0) --> 7

    > generateHeapSize(n=7, l=1) --> 15
    """

    k = 1
    increment = 1

    while(k < n):
        increment *= 2
        k += increment

    while(l > 0):
        increment *= 2
        k += increment
        l -= 1

    return k

class HeapType(Enum):
    MINIMUM = "minimum"
    MAXIMUM = "maximum"

class Heap:

    #-------------[ CONSTRUCTOR(S) ]-------------#

    def __init__(self, *args, capacity: int=None, heaptype: HeapType=HeapType.MINIMUM):
        
        self._capacity = (capacity if capacity is not None else None)
        self._heaptype = heaptype or HeapType.MINIMUM
            # Strictly enforcing the default heaptype.
            # Heap breaks if not strictly enforced.
            # Example Break Case: User passes in heaptype=None.
        self._array = []
        self.insert(*args)

    #-------------[ OBJECT DESCRIPTOR(S) ]-------------#

    def __len__(self) -> int:
        return len(self._array)

    def __getitem__(self, i: int):
        return self._array[i]

    def __str__(self) -> str:
        return str(self._array) 
    
    @property
    def n(self) -> int:
        return len(self) - 1
    
    @property
    def top(self):
        return self[0]
    
    @property
    def bottom(self):
        return self[self.n]
    
    @property
    def minimum(self):
        minimum = self[0]
        if(len(self) > 1 and self._heaptype is HeapType.MAXIMUM):
            for i in range(1, len(self)):
                if(minimum > self[i]):
                    minimum = self[i]
        return minimum
    
    @property
    def maximum(self):
        maximum = self[0]
        if(len(self) > 1 and self._heaptype is HeapType.MINIMUM):
            for i in range(1, len(self)):
                if(maximum < self[i]):
                    maximum = self[i]
        return maximum
    
    @property
    def empty(self) -> bool:
        return len(self) == 0
    
    @property
    def capacity(self) -> int|None:
        return self._capacity
    
    @capacity.setter
    def capacity(self, value: int) -> None:
        self._capacity = value
    
    @capacity.deleter
    def capacity(self) -> None:
        self._capacity = None

    @property
    def full(self) -> bool:
        """
        Always returns False if no capacity has been set.
        """
        if(self._capacity is None):
            return False
        return len(self) >= self._capacity
    
    #-------------[ INDEX GENERATOR(S) ]-------------#

    def parent(self, i: int) -> int:
        return i // 2
    
    def left(self, i: int) -> int:
        return i * 2
    
    def right(self, i: int) -> int:
        return i * 2 + 1
    
    @property
    def lastParent(self) -> int:
        return self.parent(self.n)
    
    @property
    def leaves(self) -> list[int]:
        return [i for i in range(self.lastParent + 1, len(self))]
    
    def __extremaIndexHelper(self, value, i: int=0) -> int|None:
        """
        This greedy algorithm attempts to ensure that only the absolute 
        minimums/maximums of the data set being inserted are stored 
        in this heap. There is room for error, but overall, this 
        does this functionality without looping over all leaf nodes.
        The only other solution that unfortunately results in O(n/2) 
        run time. This reduces that down to a spectacular O(log(n)) 
        as we are essentially doing a sift down to find the extrema 
        in opposite to the heap type.

        The roughness can be avoided by simply maintaining a larger
        heap than what is wanted i.e. for maintaining k-smallest
        elements in a min-heap, maintain a heap that is size k+m
        where m is some arbitrary number set by the user. Using
        the generateHeapSize() function defined in this module is
        recommended for this.
        """

        if(self.isLeaf(i)):
            if(
                (self._heaptype is HeapType.MINIMUM and self[i] < value)
                or
                (self._heaptype is HeapType.MAXIMUM and self[i] > value)
            ):
                return None
            return i

        l = self.left(i)
        r = self.right(i)

        if(r > self.n):
            return self.__extremaIndexHelper(value, l)
            # Left is guaranteed to exist as insertions are made left to right and
            # that we already checked if this node is a parent earlier i.e. it is
            # not a leaf node. So all we need to do is check if right exists. If
            # right does not exist, it also implies the left node is a leaf node.
            # We can just return it immediately then once we've verified value is
            # lt/gt (in accordance with heaptype) than self[l].

        if(
            (self._heaptype is HeapType.MINIMUM and self[l] > self[r])
            or
            (self._heaptype is HeapType.MAXIMUM and self[l] < self[r])
        ):
            return self.__extremaIndexHelper(value, l)
        else:
            return self.__extremaIndexHelper(value, r)
            # We default to bubbling down the right side as it is more likely
            # that the maximum/minimum leaf is on the left due to insertion 
            # being left to right.
    
    #-------------[ CLASS FUNCTION(S) ]-------------#

    def __setitem__(self, i: int, value) -> None:
        self._array[i] = value

    def append(self, *args) -> None:
        for value in args:
            if(self.full):
                raise IndexError("Appending past this heap's capacity.")
            self._array.append(value)

    def __iter__(self):
        for i in range(0, len(self)):
            yield(self[i])
    
    def isLeaf(self, index: int) -> bool:
        return index > (self.lastParent) and index <= self.n
    
    def swap(self, i: int, j: int) -> None:
        self[i], self[j] = self[j], self[i]

    def heapify(self, i: int, heaptype: HeapType=None) -> None:
        heaptype = heaptype or self._heaptype

        if(heaptype is not self._heaptype):
            self._heaptype = heaptype
            for j in range(self.lastParent, -1, -1):
                self.heapify(j)
            # HeapType was changed, so now the 
            # entire heap must be re-heapified.
        if(self.isLeaf(i)):
            return
        
        extreme = i
        l = self.left(i)
        r = self.right(i)
        
        if(heaptype is HeapType.MINIMUM):
            if(l <= self.n and self[i] > self[l]):
                extreme = l
            if(r <= self.n and self[extreme] > self[r]):
                extreme = r
        elif(heaptype is HeapType.MAXIMUM):
            if(l <= self.n and self[i] < self[l]):
                extreme = l
            if(r <= self.n and self[extreme] < self[r]):
                extreme = r

        if(extreme != i):
            self.swap(i, extreme)
            self.heapify(extreme, heaptype=heaptype)

    def insert(self, *args) -> None:

        for arg in args:
            
            i = 0

            if(self.full):
                i = self.__extremaIndexHelper(arg, i)
                if(i is not None):
                    self[i] = arg
                else:
                    continue
            else:
                self.append(arg)
                i = self.n
            
            while(
                (self._heaptype is HeapType.MINIMUM and self[i] < self[self.parent(i)])
                or
                (self._heaptype is HeapType.MAXIMUM and self[i] > self[self.parent(i)])
            ):
                self.swap(i, self.parent(i))
                i = self.parent(i)

    def pop(self):
        popped = self[0]
        self[0] = self[self.n]
            # By sending the last element to the
            # top, the entire heap is forced to
            # adjust as a result thus removing
            # any issues that break the heap.
        self._array.pop()
            # Removes the last element to ensure 
            # there are no duplicate values as a 
            # result of the previous line.
        self.heapify(0)

        return popped
