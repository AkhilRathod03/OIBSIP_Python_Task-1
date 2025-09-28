from bmi_logic import calculate_bmi, classify_bmi

def run_cli():
    """Runs the command-line interface for the BMI calculator."""
    print("--- BMI Calculator (CLI Mode) ---")
    while True:
        try:
            weight_str = input("Enter your weight in kilograms (kg): ")
            weight = float(weight_str)
            if not 0 < weight < 500:
                print("Error: Please enter a realistic weight.")
                continue

            height_str = input("Enter your height in meters (m): ")
            height = float(height_str)
            if not 0 < height < 3:
                print("Error: Please enter a realistic height.")
                continue

            bmi = calculate_bmi(weight, height)
            category = classify_bmi(bmi)

            print("\n--- Your BMI Result ---")
            print(f"BMI: {bmi}")
            print(f"Category: {category}")
            print("-----------------------\n")
            break

        except ValueError:
            print("Invalid input. Please enter numbers only.")
        except KeyboardInterrupt:
            print("\nCalculation cancelled.")
            break

def main():
    """Main function to select the application mode."""
    print("Welcome to the BMI Calculator!")
    while True:
        mode = input("Choose your mode (1 for CLI, 2 for GUI): ").strip()
        if mode == '1':
            run_cli()
            break
        elif mode == '2':
            try:
                from gui import run_gui
                print("Launching GUI mode...")
                run_gui()
            except ImportError as e:
                print(f"Error: Could not launch GUI. Please ensure all dependencies are installed: {e}")
                print("You can install them using: pip install -r requirements.txt")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
