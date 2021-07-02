from location import Location, manhattan_distance

"""
The Monitor module contains the Monitor class, the Activity class,
and a collection of constants. Together the elements of the module
help keep a record of activities that have occurred.

Activities fall into two categories: River activities and Driver
activities. Each activity also has a description, which is one of
request, cancel, pickup or dropoff.

=== Constants === 
@type RIDER: str
    A constant used for the Rider activity category. 
@type DRIVER: str
    A constant used for the Driver activity category.
@type REQUEST: str
    A constant used for the request activity description.
@type CANCEL: str
    A constant used for the cancel activity description.
@type PICKUP: str
    A constant used for the pickup activity description.
@type DROPOFF: str
    A constant used for the dropoff activity description.
"""

RIDER = "rider"
DRIVER = "driver"

REQUEST = "request"
CANCEL = "cancel"
PICKUP = "pickup"
DROPOFF = "dropoff"


class Activity:
    """An activity that occurs in the simulation.

    === Attributes ===
    @type timestamp: int
        The time at which the activity occurred.
    @type description: str
        A description of the activity.
    @type identifier: str
        An identifier for the person doing the activity.
    @type location: Location
        The location at which the activity occurred.
    """

    def __init__(self, timestamp, description, identifier, location):
        """Initialize an Activity

        @type self: Activity
        @type timestamp: int
        @type description: str
        @type identifier: str
        @type location: Location
        @rtype: None
        """
        self.description = description
        self.time = timestamp
        self.identifier = identifier
        self.location = location


class Monitor:
    """A monitor that is notified of activities and keeps a record them.
    When required, it generates a report of the activities that it has recorded.
    """

    # === Private Attributes ===
    # @type _activities: dict[str, dict[str, list[Activity]]]
    #       A dictionary whose key is a category, and value is another
    #       dictionary. The key of the second dictionary is an identifier
    #       and its value is a list of Activities.

    def __init__(self):
        """Initialize a Monitor

        @type self: Monitor
        """
        self._activities = {
            RIDER: {},
            DRIVER: {}
        }
        """@type _activities: dict[str, dict[str, list[Activity]]]"""

    def __str__(self):
        """Return a string representation.

        @type self: Monitor
        @rtype: str
        """
        return "Monitor ({} drivers, {} riders)".format(
            len(self._activities[DRIVER]), len(self._activities[RIDER]))

    def notify(self, timestamp, category, description, identifier, location):
        """Notify the monitory of activity.

        @type self: Monitor
        @type timestamp: int
            The time of the activity.
        @type category: DRIVER | RIDER
            The category of the activity.
        @type description: REQUEST | CANCEL | PICKUP | DROPOFF
            A description of the activity.
        @type identifier: str
            The identifier for the actor.
        @type location: Location
            The location of the activity.
        @rtype: None
        """
        if identifier not in self._activities[category]:
            self._activities[category][identifier] = []
        activity = Activity(timestamp, description, identifier, location)
        self._activities[category][identifier].append(activity)

    def report(self):
        """Return a report of the activities that have occurred

        @type self: Monitor
        @rtype: dict[str, object]
        """
        return {"rider_wait_time": self._average_wait_time(),
                "driver_total_distance": self._average_total_distance(),
                "driver_ride_distance": self._average_ride_distance()}

    def _average_wait_time(self):
        """Return the average wait time of riders that have either been picked
        up or have cancelled their ride.

        @type self: Monitor
        @rtype: float
        """
        wait_time = 0
        count = 0
        for activities in self._activities[RIDER].values():
            # A rider that has less than two activities hasn't finished
            # waiting (they haven't cancelled or been picked up).
            if len(activities) >= 2:
                # The first activity is REQUEST, and the second is PICKUP
                # or CANCEL. The wait time is the difference between between the two.
                wait_time += activities[1].time - activities[0].time
                count += 1
        if count == 0:
            return 0
        return wait_time / count

    def _average_total_distance(self):
        """Return the average distance drivers have driven.

        @type self: Monitor
        @rtype: float
        """
        distance = 0
        drivers = self._activities[DRIVER].values()
        for activities in drivers:
            for i in range(len(activities) - 1):
                if activities[i].description == PICKUP:
                    pickup = activities[i]
                    if activities[i+1].description == DROPOFF:
                        dropoff = activities[i+1]
                        distance += manhattan_distance(pickup.location,
                                                       dropoff.location)
                elif activities[i].description == DROPOFF:
                    dropoff = activities[i]
                    next_activity = activities[i+1].description
                    second_next_activity = activities[i+2].description
                    if (next_activity == PICKUP) and (second_next_activity ==
                                                      DROPOFF):
                        pickup = activities[i+1]
                        distance += manhattan_distance(dropoff.location,
                                                       pickup.location)
        if len(drivers) == 0:
            return 0.0
        return distance / len(drivers)

    def _average_ride_distance(self):
        """Return the average distance drivers have driven on rides.

        @type self: Monitor
        @rtype: float
        """
        distance = 0
        drivers = list(self._activities[DRIVER].values())
        for activities in drivers:
            rides_distance = 0
            ride_count = 0
            for i in range(len(activities) - 1):
                if activities[i].description == PICKUP:
                    pickup = activities[i]
                    if activities[i+1].description == DROPOFF:
                        dropoff = activities[i+1]
                        ride_count += 1
                        rides_distance += manhattan_distance(pickup.location,
                                                             dropoff.location)
            rides_distance = rides_distance / ride_count
            distance += rides_distance
        if len(drivers) == 0:
            return 0
        return distance / len(drivers)
