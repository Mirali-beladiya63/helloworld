import mysql.connector
import time

username = 'root'
password = ''
host = 'localhost'
database = 'lift'

cnx = mysql.connector.connect(
    user=username,
    password=password,
    host=host,
    database=database
)

cursor = cnx.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS LIFT (              

      LIFT_NUMBER_OF_PERSON INT,
      LIFT_FROM_FLOOR INT,
      LIFT_TO_FLOOR INT
    );
""")

class lift:
    def __init__(self, current_floor=0):
         self.lift_number_of_person = 0
         self.current_floor = current_floor
         self.direction = "direction"
         self.requested_floors = []

    def move(self, floor):
        if floor > self.current_floor:
            self.direction = "up"
            while self.current_floor < floor: 
                self.current_floor += 1
                time.sleep(1)
                print("Moving up to floor", self.current_floor)
                self.connection(self.lift_number_of_person, self.current_floor + 1, self.current_floor) 
        elif floor < self.current_floor:
            self.direction = "down"
            while self.current_floor > floor:
                self.current_floor -= 1
                time.sleep(1)
                print("Moving down to floor", self.current_floor)
                self.connection(self.lift_number_of_person, self.current_floor - 1, self.current_floor)  
        else:
            print("Already on floor", self.current_floor)

        self.direction = "direction"

    def request_floor(self, floor):
        self.requested_floors.append(floor)
        self.process_requests()
        time.sleep(1)

    def process_requests(self):
        while self.requested_floors:
            next_floor = self.requested_floors.pop(0)
            self.move(next_floor)
            time.sleep(1) 

    def connection(self, num_of_person, from_floor, to_floor):
        query = "INSERT INTO LIFT (LIFT_NUMBER_OF_PERSON, LIFT_FROM_FLOOR, LIFT_TO_FLOOR) VALUES (%s, %s, %s)"
        cursor.execute(query, (num_of_person, from_floor, to_floor))
        cnx.commit()  

    def add_person(self, num_of_person):
        self.lift_number_of_person = num_of_person

if __name__ == "__main__":
    elevator = lift()
    while True:
            num_of_person = int(input("Enter the number of persons (1-10): "))
            if 1 <= num_of_person <= 10:
                elevator.add_person(num_of_person)
            else:
                print("invalid  input")
            floor = int(input("Enter the floor number (0-10): "))
            if  floor <= 10:
               elevator.request_floor(floor)
            else:
               print("Invalid floor number")