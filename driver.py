from location import Location, manhattan_distance


class Driver:
    """A driver for a ride-sharing service.

    === Attributes ===
    :param str identifier:
        A unique identifier for the driver
    :param Location location:
        The current location of the driver.
    :param bool is_idle:
        A property that is True if the driver is idle and False otherwise.
    """

    def __init__(self, identifier, location, speed):
        """ Initialize a Driver.

        @type self: Driver
        @type identifier: str
        @type location: Location
        @type speed: int
        @rtype: None
        """
        self.identifier = identifier
        self.location = location
        self.speed = speed
        self.is_idle = True
        self.destination = None

    def __str__(self):
        """Return a string representation.

        @type self: Driver
        @rtype: str
        """
        s = "Identifier: {}, Location: {}, Speed: {}".format(self.identifier,
                                                             self.location,
                                                             self.speed)
        if self.is_idle is False:
            s += ", Destination: {}".format(self.destination)
        return s

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @type self: Driver
        @type other: Driver | Any
        @rtype: bool
        """
        return (type(self) == type(other) and
                self.identifier == other.identifier and
                self.location == other.location and
                self.speed == other.speed and
                self.is_idle == other.is_idle and
                self.destination == other.destination)

    def get_travel_time(self, destination):
        """Return the time it will take to arrive at the destination,
        rounded to the nearest integer.

        @type self: Driver
        @type destination: Location
        @rtype: int
        """
        time = manhattan_distance(self.location, destination) / self.speed
        return int(time)

    def start_drive(self, location):
        """Start driving to the location and return the required travel time
        to location.

        @type self: Driver
        @type location: Location
        @rtype: int
        """
        self.is_idle = False
        self.destination = location
        return self.get_travel_time(location)

    def end_drive(self):
        """End the drive and arrive at the destination.

        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None
        """
        self.is_idle = True
        self.location = self.destination
        self.destination = None

    def end_shift(self):
        """Driver has finished his job for the day and is no longer taking riders.

        @type self: Driver
        @rtype: None
        """
        self.is_idle = False
