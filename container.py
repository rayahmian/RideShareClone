class Container:
    """A container that holds objects.

    This is an abstract class. Only child classes should be instantiated.
    """

    def add(self, item):
        """Add <item> to this Container.

        @type self: Container
        @type item: Object
        @rtype: None
        """
        raise NotImplementedError("Implemented in a subclass")

    def remove(self):
        """Remove and return a single item from this Container.

        @type self: Container
        @rtype: Object
        """
        raise NotImplementedError("Implemented in a subclass")

    def is_empty(self):
        """Return True iff this container is empty.

        @type self: Container
        @rtype: bool
        """
        raise NotImplementedError("Implemented in a subclass")


class PriorityQueue(Container):
    """A queue of items that operates in priority order.

    Items are removed from the queue according to priority; the item with the
    highest priority is removed first. Ties are resolved in FIFO order,
    meaning the item that was inserted *earlier* is the first one to be removed.

    Priority is defined by the rich comparison of methods for the objects in the
    container (__lt__, __le__, __gt__, __ge__).

    If x < y, then x has a *HIGHER* priority than y.

    All objects in the container must be of the same type.
    """

    # === Private Attributes ===
    # @type _items: list
    #   The items stored in the priority queue.
    #
    # === Representation Invariants ===
    # _items is a sorted list, where the first item in the queue is the
    # item with the highest priority.

    def __init__(self):
        """Initialize an empty PriorityQueue.

        @type self: PriorityQueue
        @rtype: None
        """
        self._items = []

    def __str__(self):
        """Return a str representation of the PriorityQueue.

        @type self: PriorityQueue
        @rtype: str
        """
        return str(self._items)

    def remove(self):
        """Remove and return the next item from this PriorityQueue.

        Precondition: <self> should not be empty.

        @type self: PriorityQueue
        @rtype: object

        >>> pq = PriorityQueue()
        >>> pq.add("red")
        >>> pq.add("blue")
        >>> pq.add("yellow")
        >>> pq.add("green")
        >>> pq.remove()
        'blue'
        >>> pq.remove()
        'green'
        >>> pq.remove()
        'red'
        >>> pq.remove()
        'yellow'
        """
        return self._items.pop(0)

    def is_empty(self):
        """
        Return true iff this PriorityQueue is empty.

        @type self: PriorityQueue
        @rtype: bool

        >>> pq = PriorityQueue()
        >>> pq.is_empty()
        True
        >>> pq.add("thing")
        >>> pq.is_empty()
        False
        """
        return len(self._items) == 0

    def add(self, item):
        """Add <item> to this PriorityQueue

        @type self: PriorityQueue
        @type item: object
        @rtype: None

        >>> pq = PriorityQueue()
        >>> pq.add("yellow")
        >>> pq.add("blue")
        >>> pq.add("red")
        >>> pq.add("green")
        >>> pq._items
        ['blue', 'green', 'red', 'yellow']
        """
        i = 0
        for items in self._items:
            if item > items:
                self._items.insert(i, item)
            else:
                i += 1


class Queue(Container):
    """First-in, First-out (FIFO) Queue."""

    def __init__(self):
        """Initialize a new queue.

        @type self: Queue
        """
        self._queue = []

    def add(self, item):
        """Add <item> to the top of Queue self.

        @type self: Queue
        @type item: Object
        @rtype: None
        """
        self._queue.append(item)

    def __str__(self):
        """Return a str representation of the Queue.
        @type self: Queue
        @rtype: str

        >>> s = Queue()
        >>> s.add(3)
        >>> s.add(2)
        >>> print(s)
        [3, 2]
        """
        return str(self._queue)

    def __eq__(self, other):
        """Return whether Queue self is equivalent to other.

        @type self: Queue
        @type other: Queue | Any
        @rtype: bool

        >>> q1 = Queue()
        >>> q1.add(3)
        >>> q2 = Queue()
        >>> q2.add(3)
        >>> q1 == q2
        True
        """
        return (type(self) == type(other) and
                self._queue == other._queue)

    def remove(self):
        """Remove and return top item of Queue self.

        Assume Queue self is not empty.

        @type self: Queue
        @rtype: Object

        >>> s = Queue()
        >>> s.add(5)
        >>> s.add(7)
        >>> s.remove()
        7
        """
        return self._queue.pop(0)

    def is_empty(self):
        """Return whether Queue is empty.

        @type self: Queue
        @rtype: bool

        >>> s = Queue()
        >>> s.is_empty()
        True
        """
        return len(self._queue) == 0
