from container import PriorityQueue
from dispatcher import Dispatcher
from event import create_event_list
from monitor import Monitor


class Simulation:
    """A simulation.

    This is the class which is responsible for setting up and running a
    simulation. This is the entry point into the program.
    """

    # === Private Attributes ===
    # @type _events: PriorityQueue[Event]
    #       A sequence of events arranged in priority determined by the event
    #       sorting order.
    # @type _dispatcher: Dispatcher
    #       The dispatcher associated with the simulation.
    # @type _monitor: Monitor
    #       The monitor associated with the simulation.

    def __init__(self):
        """Initialize a Simulation

        @type self: Simulation
        @rtype: None
        """
        self._events = PriorityQueue()
        self._dispatcher = Dispatcher()
        self._monitor = Monitor()

    def run(self, initial_events):
        """Run the simulation on the list of events in <initial_events>.

        Return a dictionary containing statistics of the simulation.

        @type self: Simulation
        @type initial_events: list[Event]
            An initial list of events.
        @rtype: dict[str, object]
        """
        for event in initial_events:
            self._events.add(events)
        while not self._events.is_empty():
            event = self._events.remove().do(self._dispatcher, self._monitor)
            if event is not None:
                self._events.add(event)
        return self._monitor.report()
        # TODO: fix run event

if __name__ == "__main__":
    events = create_event_list("events.txt")
    sim = Simulation()
    final_stats = sim.run(events)
    print(final_stats)
