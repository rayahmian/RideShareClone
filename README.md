# Ride-Share Clone

This is a ride-share simulation (similar to Uber or Lyft).
To simulate a night of rider-driver activities, you can run simulation.py using events.txt. You can
also run RideShareTest.py which is a unittest created to test the simulation.

## Objects

- **Riders**: request rides from their current location to their destination
- **Drivers**: drive to the pick-up location and then drop-off riders at their destination
- **The Dispatcher**: receives requests from riders for drivers and satisfies requests with drivers for riders
- **The Monitor**: keeps track of activities in the simulation and generates a report when prompted

## The Simulation

- The activities of the ride-share simulation take place on a simplified city grid.
- Locations of the riders and drivers are the intersection they are closest to.
    - An intersection is a tuple of positive integers that represent a North/South street 
      and an East/West street, respectively.
    - For instance, `(1, 2)` represents Street 1 N/S & Street 2 E/W.
- When a rider requests a driver, the dispatcher attempts to assign a driver to the rider. 
  If there is no driver, the dispatcher keeps the rider on hold until a driver becomes available.
    - A rider will cancel if they have to wait too long.
- When a driver requests a rider, the dispatcher assigns a waiting rider if one is available. 
  If this is the driver's first request, the dispatcher registers the driver into its fleet. 
  Once registered, a driver never unregisters.
- There is an apparent relationship between how long riders are waiting to be picked up and 
  how many drivers are available, waiting to be assigned to riders.
    - This simulation can measure how this relationship affects rider wait times and driver earnings.
- This simulation measures the following events: 
    - Riders requesting rides
    - Drivers picking up riders 
        - Or riders cancelling trips first
    - Drivers dropping off riders
    - Drivers requesting to be assigned to riders
