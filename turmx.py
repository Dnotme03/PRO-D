# turmx.py

from interface import loading_animation, hacking_theme, show_title, show_menu
from time import sleep

def crack_pin():
    print("\n[INFO] Connect victim phone via USB cable to proceed... (Simulated)")
    sleep(2)
    print("[OK] Phone connected successfully! (Simulated)")
    print("[INFO] Starting brute-force simulation...\n")
    
    for pin in range(10000):
        print(f"Trying PIN: {str(pin).zfill(4)}", end="\r")
        sleep(0.005)  # Faster animation

    print("\n[✓] Brute force simulation complete! This is for educational purposes only.\n")

def main():
    loading_animation()
    hacking_theme()
    show_title()
    show_menu()

    choice = input("\nEnter your choice: ")
    if choice == "1":
        crack_pin()
    elif choice == "0":
        print("Exiting...")
    else:
        print("Invalid input!")

if __name__ == "__main__":
    main()
