from enum import Enum

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
        self._minLeafIndex = 0
        self._maxLeafIndex = 0
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
            for j in range(self.lastParent, 0, -1):
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
            
            i = self.n

            if(self._heaptype is HeapType.MINIMUM):
                if(self.full):
                    i = self._maxLeafIndex
                    if(self[i] > arg):
                        self[i] = arg
                else:
                    self.append(arg)
                    i = self.n

                while(self[i] < self[self.parent(i)]):
                    self.swap(i, self.parent(i))
                    i = self.parent(i)

            elif(self._heaptype is HeapType.MAXIMUM):
                if(self.full):
                    i = self._minLeafIndex
                    if(self[i] < arg):
                        self[i] = arg
                else:
                    self.append(arg)
                    i = self.n

                while(self[i] > self[self.parent(i)]):
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
