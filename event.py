"""Simulation Events

This file should contain all of the classes necessary to model the different
kinds of events in the simulation
"""
from rider import Rider, CANCELLED, SATISFIED
from dispatcher import Dispatcher
from driver import Driver
from location import deserialize_location
from monitor import Monitor, RIDER, DRIVER, REQUEST, CANCEL, PICKUP, DROPOFF


class Event:
    """An event.

    Events have an ordering that is based on the event timestamp. Events with
    older timestamps are less than those with newer timestamps.

    This class is abstract; subclasses must implement do().

    You may, if you wish, change the API of this class to add
    extra public methods or attributes. Make sure that anything
    you add makes sense for ALL events, and not just a particular
    event type.

    Document any such changes carefully!

    === Attributes ===
    @type timestamp: int
        A timestamp for this event
    """

    def __init__(self, timestamp):
        """Initialize an Event with a given timestamp.

        @type self: Event
        @type timestamp: int
            A timestamp for this event.
            Precondition: must be a non-negative integer.
        @rtype: None

        >>> Event(7).timestamp
        7
        """
        self.timestamp = timestamp

    # The following six 'magic methods' are overridden to allow for easy
    # comparison of Event instances. All comparisons simply perform the
    # same comparison on the 'timestamp' attribute of the two events.
    def __eq__(self, other):
        """Return True iff this Event is equal to <other>.

        Two events are equal iff they have the same timestamp.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first == second
        False
        >>> second.timestamp = first.timestamp
        >>> first == second
        True
        """
        return self.timestamp == other.timestamp

    def __ne__(self, other):
        """Return True iff this Event is not equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first != second
        True
        >>> second.timestamp = first.timestamp
        >>> first != second
        False
        """
        return not self == other

    def __lt__(self, other):
        """Return True iff this Event is less than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first < second
        True
        >>> second < first
        False
        """
        return self.timestamp < other.timestamp

    def __le__(self, other):
        """Return True iff this Event is less than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first <= first
        True
        >>> first <= second
        True
        >>> second <= first
        False
        """
        return self. timestamp <= other.timestamp

    def __gt__(self, other):
        """Return True iff this Event is greater than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first > second
        False
        >>> second > first
        True
        """
        return not self <= other

    def __ge__(self, other):
        """Return True iff this Event is greater than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first >= first
        True
        >>> first >= second
        False
        >>> second >= first
        True
        """
        return not self < other

    def __str__(self):
        """Return a string representation of this event.

        @type self: Event
        @rtype: str
        """
        raise NotImplementedError("Implemented in a subclass")

    def do(self, dispatcher, monitor):
        """Do this Event.

        Update the state of the simulation, using the dispatcher, and
        any attributes according to the meaning of the event.

        Notify the monitor of any activities that have occurred during the
        event.

        Return a list of new events spawned by this event (making sure the
        timestamps are correct).

        Note: the "business logic" of what actually happens should not be
        handled in any Event classes.

        @type self: Event
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        raise NotImplementedError("Implemented in a subclass")


class RiderRequest(Event):
    """A rider requests a driver.

    === Attributes ===
    @type rider: Rider
        The rider.
    """

    def __init__(self, timestamp, rider):
        """Initialize a RiderRequest event.

        @type self: RiderRequest
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher, monitor):
        """"Assign the rider to a driver or add the rider to a waiting list.
        If the rider is assigned to a driver, the driver starts driving to
        the rider.

        Return a Cancellation event. If the rider is assigned to a driver,
        also return a Pickup event.

        @type self: RiderRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        events = []
        monitor.notify(self.timestamp, RIDER, REQUEST, self.rider.identifier,
                       self.rider.origin)
        driver = dispatcher.request_driver(self.rider)
        if driver is not None:
            travel_time = driver.start_drive(self.rider.origin)
            events.append(Pickup(self.timestamp + travel_time, self.rider, driver))
            if travel_time > self.rider.patience:
                events.append(Cancellation(self.timestamp + self.rider.patience, self.rider))
        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: RiderRequest
        @rtype: str
        """
        return "{} -- {}: Request a driver".format(self.timestamp, self.rider)


class DriverRequest(Event):
    """A driver requests a rider.

    === Attributes ===
    @type driver: Driver
        The driver.
    """

    def __init__(self, timestamp, driver):
        """Initialize a DriverRequest event.

        @type self: DriverRequest
        @type driver: Driver
        @rtype: None
        """
        super().__init__(timestamp)
        self.driver = driver

    def do(self, dispatcher, monitor):
        """Register the driver if this is the first request and
        assign driver to a rider if one is available.

        If a rider is available, return a Pickup event.

        @type self: DriverRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        events = []
        monitor.notify(self.timestamp, DRIVER, REQUEST,
                       self.driver.identifier, self.driver.location)
        rider = dispatcher.request_rider(self.driver)
        if rider is not None:
            travel_time = self.driver.start_drive(rider.origin)
            events.append(Pickup(self.timestamp + travel_time, rider,
                                 self.driver))
        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: DriverRequest
        @rtype: str
        """
        return "{} -- {}: Request a rider".format(self.timestamp, self.driver)


class Cancellation(Event):
    """A cancellation event.

    === Attributes ===
    @type rider: Rider
        The rider.
    """

    def __init__(self, timestamp, rider):
        """Initialize a Cancellation event.

        @type self: Cancellation
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher, monitor):
        """Cancel the ride and delete it from the wait list.

        Update the status of the ride.

        @type self: Cancellation
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        events = []
        monitor.notify(self.timestamp, RIDER, CANCEL,
                       self.rider.identifier, self.rider.origin)
        dispatcher.cancel_ride(self.rider)
        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: Cancellation
        @rtype: str
        """
        return "{} -- {}: Cancelled ride".format(self.timestamp,
                                                 self.rider)


class Pickup(Event):
    """A Pickup Event.

    === Attributes ===
    @type rider: Rider
        The rider
    @type driver: Driver
        The driver.
    """

    def __init__(self, timestamp, rider, driver):
        """Initialize a Pickup Event.

        @type self: Pickup
        @type rider: Rider
        @type driver: Driver
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider
        self.driver = driver

    def do(self, dispatcher, monitor):
        """Set driver's location as the rider's location.

        Dropoff Event is scheduled for the time they will arrive at the
        rider's destination. If the rider cancelled, a new event for the
        driver requesting a rider is scheduled.

        @type self: Pickup
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        events = []
        self.driver.start_drive(self.rider.origin)
        if self.rider.get_status() == CANCELLED:
            self.driver.end_drive()
            events.append(DriverRequest(self.timestamp, self.driver))
        else:
            monitor.notify(self.timestamp, RIDER, PICKUP,
                           self.rider.identifier, self.rider.origin)
            monitor.notify(self.timestamp, DRIVER, PICKUP,
                           self.driver.identifier, self.driver.location)
            travel_time = self.driver.get_travel_time(self.driver.destination)
            events.append(Dropoff(self.timestamp + travel_time, self.rider,
                                  self.driver))
        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: Pickup
        @rtype: str
        """
        return "{} -- {} -- {}: Driver picks up rider".format(self.timestamp,
                                                              self.rider,
                                                              self.driver)


class Dropoff(Event):
    """A Dropoff Event.

    === Attributes ===
    @type rider: Rider
        The rider.
    @type driver: Driver
        The driver.
    """

    def __init__(self, timestamp, rider, driver):
        """Initialize a Dropoff Event

        @type self: Dropoff
        @type timestamp: int
        @type rider: Rider
        @type driver: Driver
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider
        self.driver = driver

    def do(self, dispatcher, monitor):
        """Sets the driver's location to the rider's destination, then leaves
        the rider satisfied.

        A new event for the driver requesting a rider is scheduled to take
        place immediately, and the driver has no destination.

        @type self: Dropoff
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        events = []
        self.driver.end_drive()
        monitor.notify(self.timestamp, RIDER, DROPOFF,
                       self.rider.identifier, self.rider.destination)
        monitor.notify(self.timestamp, DRIVER, DROPOFF,
                       self.driver.identifier, self.driver.location)
        self.rider.status = SATISFIED
        events.append(DriverRequest(self.timestamp, self.driver))
        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: Dropoff
        @rtype: str
        """
        return "{} -- {} -- {}: Driver drops off rider".format(self.timestamp,
                                                               self.rider,
                                                               self.driver)


def create_event_list(filename):
    """Return a list of Events based on raw list of events in <filename>.
    
    Precondition: the file stored at <filename> is in a specified format.
    
    @type filename: str
        The name of a file that contains the list of events.
    @rtype: list[Event]
    """
    events = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            tokens = line.split()
            timestamp = int(tokens[0])
            event_type = tokens[1]
            identifier = tokens[2]
            if event_type == "DriverRequest":
                location = deserialize_location(tokens[3])
                speed = int(tokens[4])
                driver = Driver(identifier, location, speed)
                event = DriverRequest(timestamp, driver)
            elif event_type == "RiderRequest":
                origin = deserialize_location(tokens[3])
                destination = deserialize_location(tokens[4])
                patience = int(tokens[5])
                rider = Rider(identifier, origin, destination, patience)
                event = RiderRequest(timestamp, rider)
            events.append(event)
    return events
