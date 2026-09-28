import datetime
import config
import csv

#All the available spots in car parking are imported from config.py

car_slots = {}
for i in range(1, config.total_car_slots + 1):
    car_slots[i] = None
car_details = {}
car_parked_time = {}


#All the available spots in bike parking are imported from config.py

bike_slots = {}
for i in range(1, config.total_bike_slots + 1):
    bike_slots[i] = None
bike_details = {}
bike_parked_time = {}

def main_menu():
    choice = input("Type 'park' if you want to park the vehicle or type 'exit' if you want to exit : ")
    return choice

def save_car_parking():
    with open("car_parking.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for slot in car_details:
            brand, model, licence_plate = car_details[slot]
            parked_time_str = car_parked_time[slot].strftime("%Y-%m-%d %H-%M-%S")
            writer.writerow([slot, brand, model, licence_plate, parked_time_str])

def save_bike_parking():
    with open("bike_parking.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for slot in bike_details:
            brand, model, licence_plate = bike_details[slot]
            parked_time_str = bike_parked_time[slot].strftime("%Y-%m-%d %H-%M-%S")
            writer.writerow([slot, brand, model, licence_plate, parked_time_str])

def load_car_parking():
    try:
        with open("car_parking.csv", "r", newline = "") as file:
            reader = csv.reader(file)
            for row in reader:
                slot_number = int(row[0])
                brand = row[1]
                model = row[2]
                licence_plate = row[3]
                parked_time_str = row[4]
                parked_time = datetime.datetime.strptime(parked_time_str, "%Y-%m-%d %H-%M-%S")
                car_slots[slot_number] = "occupied"
                car_details[slot_number] = (brand, model, licence_plate)
                car_parked_time[slot_number] = parked_time
    except FileNotFoundError:
        pass

def load_bike_parking():
    try:
        with open("bike_parking.csv", "r", newline = "") as file:
            reader = csv.reader(file)
            for row in reader:
                slot_number = int(row[0])
                brand = row[1]
                model = row[2]
                licence_plate = row[3]
                parked_time_str = row[4]
                parked_time = datetime.datetime.strptime(parked_time_str, "%Y-%m-%d %H-%M-%S")
                bike_slots[slot_number] = "occupied"
                bike_details[slot_number] = (brand, model, licence_plate)
                bike_parked_time[slot_number] = parked_time
    except FileNotFoundError:
        pass

def park_vehicle():
    vehicle_type = input("Enter the type vehicle you want to park (car/bike) : ")
    if vehicle_type == "car":
        free_slot = None
        for slot in car_slots:
            if car_slots[slot] is None:
                free_slot = slot
                break
        if free_slot is not None:
            brand = input("Enter your car's brand : ")
            model = input("Enter your car's model : ")
            licence_plate = (input("Enter your car's licence plate number : ")).strip().upper()

            car_d_tuple = (brand, model, licence_plate)
            car_details[free_slot] = car_d_tuple

            car_slots[free_slot] = "occupied"

            car_parked_time[free_slot] = datetime.datetime.now()

            print(f"Ticket : Car parked in slot {free_slot}. Brand : {brand}. Model : {model}. Licence plate number : {licence_plate}")
            save_car_parking()

        else:
            print("Parking full")

    elif vehicle_type == "bike":
        free_slot = None
        for slot in bike_slots:
            if bike_slots[slot] is None:
                free_slot = slot
                break
        if free_slot is not None:
            brand = input("Enter your bike's brand : ")
            model = input("Enter your bike's model : ")
            licence_plate = (input("Enter your bike's licence plate number : ")).strip().upper()

            bike_d_tuple = (brand, model, licence_plate)
            bike_details[free_slot] = bike_d_tuple

            bike_slots[free_slot] = "occupied"

            bike_parked_time[free_slot] = datetime.datetime.now()

            print(f"Ticket : Bike parked in slot {free_slot}. Brand : {brand}. Model : {model}. Licence plate number : {licence_plate}")
            save_bike_parking()

        else:
            print("Parking full")
    else:
        print("Invalid input")

def exit_vehicle():
    vehicle_type = input("Enter the type vehicle you want to exit (car/bike) : ")
    if vehicle_type == "car":
        while True:
            exit_plate = input("Enter the car's licence plate number : ").strip().upper()
            slot_number = None
            for slot in car_details:
                if car_details[slot][2] == exit_plate:
                    slot_number = slot
                    break
            if slot_number is not None:
                elapsed_seconds = (datetime.datetime.now() - car_parked_time[slot_number]).total_seconds()
                elapsed_hours = elapsed_seconds / 3600
                if elapsed_hours <= 1:
                    amount = config.first_hour_rate
                    print(f"The amount to be paid is : {amount}")
                else:
                    amount = config.first_hour_rate + int(elapsed_hours - 1) * config.per_hour_rate
                    print(f"The amount to be paid is : {amount}")

                with open("report.csv", "a", newline = "") as file:
                    writer = csv.writer(file)
                    brand, model, licence_plate = car_details[slot_number]
                    writer.writerow(["car", slot_number, brand, model, licence_plate,
                                     car_parked_time[slot_number].strftime("%Y-%m-%d %H-%M-%S"),
                                     datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"), amount])

                car_slots[slot_number] = None
                del car_details[slot_number]
                del car_parked_time[slot_number]
                save_car_parking()
                print("Thank you for using our parking!")
                break
            else:
                print("No car with this licence plate was found")

    elif vehicle_type == "bike":
        while True:
            exit_plate = input("Enter the bike's licence plate number : ").strip().upper()
            slot_number = None
            for slot in bike_details:
                if bike_details[slot][2] == exit_plate:
                    slot_number = slot
                    break
            if slot_number is not None:
                elapsed_seconds = (datetime.datetime.now() - bike_parked_time[slot_number]).total_seconds()
                elapsed_hours = elapsed_seconds / 3600
                if elapsed_hours <= 1:
                    amount = config.first_hour_rate
                    print(f"The amount to be paid is : {amount}")
                else:
                    amount = config.first_hour_rate + int(elapsed_hours - 1) * config.per_hour_rate
                    print(f"The amount to be paid is : {amount}")

                with open("report.csv", "a", newline="") as file:
                    writer = csv.writer(file)
                    brand, model, licence_plate = bike_details[slot_number]
                    writer.writerow(["bike", slot_number, brand, model, licence_plate,
                                     bike_parked_time[slot_number].strftime("%Y-%m-%d %H-%M-%S"),
                                     datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"), amount])

                bike_slots[slot_number] = None
                del bike_details[slot_number]
                del bike_parked_time[slot_number]
                save_bike_parking()
                print("Thank you for using our parking!")
                break
            else:
                print("No bike with this licence plate was found")

    else:
        print("Invalid input")

load_car_parking()
load_bike_parking()

while True:
    choice = main_menu()
    if choice == 'park':
        park_vehicle()
    elif choice == 'exit':
        exit_vehicle()
    else:
        print("Invalid input, try again")


