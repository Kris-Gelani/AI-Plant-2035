import random
import time

while True:

    temperature = round(random.uniform(150,250),2)
    pressure = round(random.uniform(8,20),2)
    vibration = round(random.uniform(0.5,6),2)

    print("="*60)
    print("EMERGENCY SHUTDOWN SYSTEM")
    print("="*60)

    print("Temperature :", temperature)
    print("Pressure    :", pressure)
    print("Vibration   :", vibration)

    print()

    trip = False

    # ESD CONDITIONS

    if temperature > 230:

        print("CRITICAL TRIP")
        print("-> REACTOR OVERHEATING")

        trip = True

    if pressure > 18:

        print("CRITICAL TRIP")
        print("-> OVER PRESSURE")

        trip = True

    if vibration > 5:

        print("CRITICAL TRIP")
        print("-> EQUIPMENT FAILURE RISK")

        trip = True

    print()

    if trip:

        print("EMERGENCY SHUTDOWN ACTIVATED")
        print("AI ACTIONS:")

        print("-> Close Feed Valve")
        print("-> Stop Reactor")
        print("-> Open Relief System")
        print("-> Notify Operator")

    else:

        print("Plant Running Safely")

    print()

    time.sleep(5)