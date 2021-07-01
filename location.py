class Location:
    def __init__(self, row, column):
        """Initialize a location

        @type self: Location
        @type row: int
        @type column: int
        @rtype: None
        """
        self._row = row
        self._col = column

    def __str__(self):
        """Return a string representation

        @rtype: str
        """
        return "({}, {})".format(self._row, self._col)

    def __eq__(self, other):
        """Return True iff self equals other, and false otherwise.

        @type self: Location
        @type other: Location | Any
        @rtype: bool

        >>> l1 = Location(1, 2)
        >>> l2 = Location (2, 1)
        >>> l1 == l2
        False
        """
        return (type(self) == type(other) and
                self._row == other._row and
                self._col == other._col)

    def get_row(self):
        """Return the row

        @type self: Location
        @rtype: int

        >>> l1 = Location(1, 2)
        >>> get_row()
        1
        """
        return self._row

    def get_col(self):
        """Return the column

        @type self: Location
        @rtype: int

        >>> l1 = Location(1, 2)
        >>> get_col()
        2
        """
        return self._col


def manhattan_distance(origin, destination):
    """Return the Manhattan distance between the origin and the destination.

    @type origin: Location
    @type destination: Location
    @rtype: int
    """
    distance_x = destination.get_col() - origin.get_col()
    distance_y = destination.get_row() - origin.get_row()
    distance = abs(distance_x) + abs(distance_y)
    return int(distance)


def deserialize_location(location_str):
    """Deserialize a location

    @type location_str: str
        A location in the format 'row,col'
    @rtype: Location
    """
    return Location(location_str[0], location_str[-1])
