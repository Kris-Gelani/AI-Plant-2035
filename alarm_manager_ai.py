import random
import time

while True:

    temperature = round(random.uniform(150,220),2)
    pressure = round(random.uniform(8,18),2)
    tank_level = round(random.uniform(20,100),2)
    vibration = round(random.uniform(0.5,5),2)

    print("="*50)
    print("AI ALARM MANAGEMENT SYSTEM")
    print("="*50)

    print("Temperature :", temperature)
    print("Pressure    :", pressure)
    print("Tank Level  :", tank_level)
    print("Vibration   :", vibration)

    print()

    alarms = []

    if temperature > 200:
        alarms.append("HIGH TEMPERATURE ALARM")

    if pressure > 15:
        alarms.append("HIGH PRESSURE ALARM")

    if tank_level < 30:
        alarms.append("LOW TANK LEVEL ALARM")

    if vibration > 4:
        alarms.append("HIGH VIBRATION ALARM")

    if len(alarms) == 0:
        print("STATUS : NORMAL OPERATION")

    else:
        print("ACTIVE ALARMS:")

        for alarm in alarms:
            print("->", alarm)

    print()

    time.sleep(5)