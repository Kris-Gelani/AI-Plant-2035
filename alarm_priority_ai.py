import random
import time

while True:

    temperature = round(random.uniform(150,220),2)
    pressure = round(random.uniform(8,18),2)
    tank_level = round(random.uniform(20,100),2)
    vibration = round(random.uniform(0.5,5),2)

    print("="*60)
    print("AI INTELLIGENT ALARM SYSTEM")
    print("="*60)

    print("Temperature :", temperature)
    print("Pressure    :", pressure)
    print("Tank Level  :", tank_level)
    print("Vibration   :", vibration)

    print()

    # HIGH TEMPERATURE

    if temperature > 200:

        print("CRITICAL ALARM")
        print("-> HIGH TEMPERATURE")

        print("AI ACTION:")
        print("-> Reduce Reactor Feed")
        print("-> Start Cooling System")

        print()

    # HIGH PRESSURE

    if pressure > 15:

        print("CRITICAL ALARM")
        print("-> HIGH PRESSURE")

        print("AI ACTION:")
        print("-> Open Relief Valve")
        print("-> Reduce Feed Flow")

        print()

    # LOW LEVEL

    if tank_level < 30:

        print("WARNING")
        print("-> LOW TANK LEVEL")

        print("AI ACTION:")
        print("-> Start Feed Pump")

        print()

    # HIGH VIBRATION

    if vibration > 4:

        print("WARNING")
        print("-> HIGH VIBRATION")

        print("AI ACTION:")
        print("-> Inspect Equipment")
        print("-> Schedule Maintenance")

        print()

    if (
        temperature <= 200 and
        pressure <= 15 and
        tank_level >= 30 and
        vibration <= 4
    ):
        print("STATUS : NORMAL OPERATION")

    print()

    time.sleep(5)