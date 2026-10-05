# save_and_view.py

print("👋 Welcome to the Data Saver Program!")

filename = "data.txt"

# Step 1: Take user input
user_input = input("Enter some text to save: ")

# Step 2: Save input to file
with open(filename, "a") as file:
    file.write(user_input + "\n")

print("✅ Your input has been saved!")

# Step 3: Ask if user wants to view all data
choice = input("Do you want to see all saved data? (y/n): ").lower()

if choice == "y":
    print("\n--- Saved Data ---")
    try:
        with open(filename, "r") as file:
            content = file.read()
            if content.strip() == "":
                print("(No data yet)")
            else:
                print(content)
    except FileNotFoundError:
        print("(No file found yet)")
else:
    print("Okay, exiting the program 👋")
