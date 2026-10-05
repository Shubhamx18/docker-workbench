def read_servers_file():
    """
    Reads 'servers.txt' and prints server names/IPs line by line.
    """

    try:
        with open('servers.txt', 'r') as file:
            print("📄 Reading servers from servers.txt...\n")

            for line_number, line in enumerate(file, start=1):
                cleaned_line = line.strip()

                # Skip empty lines
                if not cleaned_line:
                    continue

                print(f"{line_number}. {cleaned_line}")

    except FileNotFoundError:
        print("❌ Error: 'servers.txt' file not found.")

    except PermissionError:
        print("❌ Error: Permission denied for 'servers.txt'.")

    except Exception as e:
        print(f"⚠️ Unexpected error: {e} ({type(e)})")

    else:
        print("\n✅ File processed successfully.")

    finally:
        print("🔚 Program execution completed.")


# 🔹 Run directly
if __name__ == "__main__":
    read_servers_file()