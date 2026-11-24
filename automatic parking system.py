import datetime
import config
import csv

#All the available spots in car parking are imported from config.py

parking_slots = {}

for floor in config.parking_structure["floors"]:
    parking_slots[floor] = {}

    for section in config.parking_structure["floors"][floor]:
        parking_slots[floor][section] = {}

        for vehicle, capacity in config.parking_structure["floors"][floor][section].items():
            parking_slots[floor][section][vehicle] = {}

            for slot in range(1, capacity + 1):
                parking_slots[floor][section][vehicle][slot] = None

parking_details = {}
parking_parked_time = {}

def main_menu():
    choice = input("Type 'park' if you want to park the vehicle or type 'exit' if you want to exit : ").strip().lower()
    return choice

def save_parking():
    with open("parking.csv", "w", newline = "") as file:
        writer = csv.writer(file)

        for parking_key, details in parking_details.items():
            floor, section, vehicle, slot = parking_key
            brand, model, licence_plate = details

            parked_time_str = parking_parked_time[parking_key].strftime("%Y-%m-%d %H:%M:%S")

            writer.writerow([
                floor, section, vehicle, slot,
                brand, model, licence_plate, parked_time_str
            ])

def load_parking():
    try:
        with open("parking.csv", "r", newline = "") as file:
            reader = csv.reader(file)

            for row in reader:
                floor = row[0]
                section = row[1]
                vehicle = row[2]
                slot = int(row[3])
                brand = row[4]
                model = row[5]
                licence_plate = row[6]

                parked_time = datetime.datetime.strptime(
                    row[7], "%Y-%m-%d %H:%M:%S"
                )

                parking_key = (floor, section, vehicle, slot)

                parking_slots[floor][section][vehicle][slot] = "occupied"

                parking_details[parking_key] = (
                    brand, model, licence_plate
                )

                parking_parked_time[parking_key] = parked_time

    except FileNotFoundError:
        pass

def park_vehicle():
    vehicle_type = input("Enter the type of vehicle you want to park (car/bike): ").strip().lower()

    if vehicle_type not in ["car", "bike"]:
        print("Invalid input")
        return

    free_floor = None
    free_section = None
    free_vehicle = None
    free_slot = None

    # Search for an available parking slot
    for floor in parking_slots:
        for section in parking_slots[floor]:
            for vehicle in parking_slots[floor][section]:

                if vehicle == vehicle_type:
                    for slot in parking_slots[floor][section][vehicle]:

                        if parking_slots[floor][section][vehicle][slot] is None:
                            free_floor = floor
                            free_section = section
                            free_vehicle = vehicle
                            free_slot = slot
                            break

                    if free_slot is not None:
                        break

            if free_slot is not None:
                break

        if free_slot is not None:
            break

    # Check parking availability
    if free_slot is not None:

        brand = input("Enter vehicle brand: ")
        model = input("Enter vehicle model: ")
        licence_plate = input("Enter vehicle licence plate number: ").strip().upper()

        parking_key = (free_floor, free_section, free_vehicle, free_slot)

        parking_details[parking_key] = (brand, model, licence_plate)

        parking_slots[free_floor][free_section][free_vehicle][free_slot] = "occupied"

        parking_parked_time[parking_key] = datetime.datetime.now()

        save_parking()

        # Generate parking ticket
        print("\n========== PARKING TICKET ==========")
        print(f"Vehicle Type : {free_vehicle}")
        print(f"Floor        : {free_floor}")
        print(f"Section      : {free_section}")
        print(f"Slot Number  : {free_slot}")
        print(f"Brand        : {brand}")
        print(f"Model        : {model}")
        print(f"Licence Plate: {licence_plate}")
        print("====================================")
        print("Vehicle parked successfully!")

    else:
        print("Parking full")

def exit_vehicle():
    vehicle_type = input("Enter the type vehicle you want to exit (car/bike) : ").strip().lower()

    if vehicle_type not in ["car", "bike"]:
        print("Invalid vehicle type")
        return

    exit_plate = input("Enter vehicle licence plate number: ").strip().upper()

    found_key = None


    #Search for the vehicle
    for parking_key, details in parking_details.items():

        if parking_key[2] == vehicle_type and details[2] == exit_plate:
            found_key = parking_key
            break


    #Check whether vehicle was found
    if found_key is None:
        print("No vehicle with this licence plate was found")
        return


    #Get parking information

    floor, section, vehicle, slot = found_key

    brand, model, licence_plate = parking_details[found_key]


    parked_time = parking_parked_time[found_key]
    exit_time = datetime.datetime.now()

    elapsed_seconds = (exit_time - parked_time).total_seconds()
    elapsed_hours = elapsed_seconds / 3600

    if elapsed_hours <= 1:
        amount = config.first_hour_rate
    else:
        extra_hours = int(elapsed_hours - 1) + 1
        amount = config.first_hour_rate + extra_hours * config.per_hour_rate


    print("\n========== EXIT BILL ==========")
    print(f"Vehicle Type : {vehicle}")
    print(f"Floor        : {floor}")
    print(f"Section      : {section}")
    print(f"Slot Number  : {slot}")
    print(f"Licence Plate: {licence_plate}")
    print(f"Parking Fee  : {amount}")
    print("===============================")

    with open("report.csv", "a", newline = "") as file:
        writer = csv.writer(file)
        writer.writerow([
            vehicle, floor, section, slot,
            brand, model, licence_plate,
            parked_time.strftime("%Y-%m-%d %H:%M:%S"),
            exit_time.strftime("%Y-%m-%d %H:%M:%S"),
            amount
        ])

    #Free the parking slot
    parking_slots[floor][section][vehicle][slot] = None

    del parking_details[found_key]
    del parking_parked_time[found_key]

    save_parking()

    print("Thank you for using our parking!")

load_parking()

while True:
    choice = main_menu()
    if choice == 'park':
        park_vehicle()
    elif choice == 'exit':
        exit_vehicle()
    else:
        print("Invalid input, try again")


