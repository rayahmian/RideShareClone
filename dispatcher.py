from driver import Driver
from rider import Rider, CANCELLED
from container import Queue


class Dispatcher:
    """A dispatcher fulfills requests from riders and drivers for a
    ride-sharing service.

    When a rider requests a driver, the dispatcher assigns a driver to the
    rider. If no driver is available, the rider is placed on a waiting
    list for the next available driver. A rider that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a rider, the dispatcher assigns a rider from
    the waiting list to the driver. If there is no rider on the waiting list,
    the dispatcher does nothing. Once a driver requests a rider, the driver
    is registered with the dispatcher, and will be used to fulfill future
    rider requests.
    """

    def __init__(self):
        """Initialize a Dispatcher.

        @type self: Dispatcher
        @rtype: None
        """
        self.wait_list = Queue()
        self.driver_fleet = []

    def __str__(self):
        """Return a string representation.

        @type self: Dispatcher
        @rtype: str
        """
        s = "Riders' Wait List: {}, Driver Fleet: {}".format(self.wait_list,
                                                             self.driver_fleet)
        return s

    def request_driver(self, rider):
        """Return a driver for the rider, or None if no driver is available.

        Add the rider to the waiting list if there is no available driver.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: Driver | None
        """
        req_driver = None
        for driver in self.driver_fleet:
            if driver.is_idle():
                req_driver = driver
                break
        if req_driver is None:
            self.wait_list.add(rider)
        return req_driver

    def request_rider(self, driver):
        """Return a rider for the driver, or None if no rider is available.

        If this is a new driver, register the driver for future rider requests.

        @type self: Dispatcher
        @type driver: Driver
        @rtype: Rider | None
        """
        if driver not in self.driver_fleet:
            self.driver_fleet.append(driver)
        if self.wait_list.is_empty():
            return None
        else:
            return self.wait_list.remove()

    def cancel_ride(self, rider):
        """Cancel the ride request for rider.

        Precondition: A ride request exists for the rider.
        Precondition: The rider is next on the wait list.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: None
        """
        if rider == self.wait_list.remove():
            rider.status = CANCELLED
