from location import Location

"""
The rider module contains the Rider class. It also contains
constants that represent the status of the rider. 

=== Constants === 
@type WAITING: str
    A constant used for the waiting rider status. 
@type CANCELLED: str 
    A constant used for the cancelled rider status.
@type SATISFIED: str 
    A constant used for the satisfied rider status. 
"""

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"


class Rider:
    """A rider for a ride-sharing service

    === Attributes ===
    @param str identifier:
        A unique identifier for the rider.
    @param Location origin:
        Pick-up location for Rider.
    @param Location destination:
        Drop-off location for Rider
    @param int patience:
        The number of time units that the rider will wait.
    """

    def __init__(self, identifier, origin, destination, patience):
        """Initialize a rider.

        @type identifier: str
            The rider's identifier.
        @type origin: Location
            The original location of the rider.
        @type destination: Location
            The destination location for the rider.
        @type patience: int
            The amount of time that the rider can wait.
        @type status: WAITING | CANCELLED | SATISFIED
            The status of the rider.
        # TODO: fix status param
        @rtype: None
        """
        self.identifier = identifier
        self.origin = origin
        self.destination = destination
        self.patience = patience
        self.status = WAITING

    def __str__(self):
        """Return a string representation of the Rider.

        @type self: Rider
        @rtype: str
        """
        s = "Identifier {}, Origin: {}, Destination: {}, Patience: {}, "\
            "Status: {}".format(self.identifier, self.origin, self.destination,
                                self.patience, self.status)
        return s

    def __eq__(self, other):
        """Return whether self and other are equal to each other.

        @type self: Rider
        @type other: Any | Rider
        @rtype: bool
        """
        return (type(self) == type(other) and
                self.identifier == other.identifier and
                self.origin == other.origin and
                self.destination == other.destination and
                self. patience == other.patience and
                self.status == other.status)

    def get_status(self):
        """Return the status of the rider.

        @type self: Rider
        @rtype: str
        """
        return self.status
