from classes import Simulation, State, Sensor



def main():

    while True:
        
        print("Load previous simulation?")
        print("1. Yes")
        print("2. No")
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                sim = Simulation.load("simulation.json")
                break
            elif choice == 2:

                floors = int(input("Enter number of floors: "))
                rooms = int(input("Enter number of rooms: "))

                if floors <= 0 or rooms <= 0:
                    raise ValueError
                
                sim = Simulation(rooms, floors)
                break
            else:
                raise ValueError
        except ValueError:
            #clear screen
            print("\033[H\033[J")
            print("Invalid choice")

    #clear screen
    print("\033[H\033[J")
    while True:
        print("1. Add zombies")
        print("2. Block room")
        print("3. Print state")
        print("4. Update sensors")
        print("5. Reset sensor")
        print("6. Update simulation")
        print("7. Save")
        print("8. Exit")
        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                x = int(input("Enter Room number: "))
                y = int(input("Enter Floor number: "))
                sim.add_zombies(x, y)
                print("\033[H\033[J")
                print("Zombies added")

            elif choice == 2:
                x = int(input("Enter Room number: "))
                y = int(input("Enter Floor number: "))
                sim.block_room(x, y)
                print("\033[H\033[J")
                print("Room blocked")

            elif choice == 3:
                sim.print_state()

            elif choice == 4:
                print("\033[H\033[J")
                print("Sensors updated")
                sim.update_sensors()

            elif choice == 5:
                x = int(input("Enter Room number: "))
                y = int(input("Enter Floor number: "))
                sim.reset_sensor(x,y)
            elif choice == 6:
                sim.update()
                print("\033[H\033[J")
                print("Simulation updated")  

            elif choice == 7:
                sim.save("simulation.json")
                print("\033[H\033[J")
                print("Simulation saved")

            elif choice == 8:
                break

            else:
                raise ValueError
            
        except ValueError:
            #clear screen
            print("\033[H\033[J")
            print("Invalid choice")

main()
