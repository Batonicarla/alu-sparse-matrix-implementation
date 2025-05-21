import os
import sys
import time
from sparse_matrix import SparseMatrix

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print("=" * 60)
    print("               SPARSE MATRIX OPERATIONS")
    print("=" * 60)
    print("Data Structures and Algorithms for Engineers - Assignment 2")
    print("-" * 60)

def get_operation():
    print("\nAvailable Operations:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. View Matrix Details")
    print("5. Exit")

    while True:
        try:
            choice = int(input("\nEnter your choice (1-5): "))
            if 1 <= choice <= 5:
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_file_path(prompt):
    while True:
        file_path = input(prompt)
        if os.path.isfile(file_path):
            return file_path
        else:
            print(f"Error: File '{file_path}' not found. Please try again.")

def get_output_file_path():
    while True:
        file_path = input("Enter output file path: ")

        # Check if file exists and confirm overwrite
        if os.path.exists(file_path):
            confirm = input(f"File '{file_path}' already exists. Overwrite? (y/n): ")
            if confirm.lower() == 'y':
                return file_path
        else:
            # Check if directory exists
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                except OSError:
                    print(f"Error: Cannot create directory '{directory}'.")
                    continue
            return file_path

def view_matrix_details():
    try:
        file_path = get_file_path("Enter matrix file path: ")
        start_time = time.time()
        matrix = SparseMatrix(file_path)
        load_time = time.time() - start_time

        print("\nMatrix Details:")
        print(f"Dimensions: {matrix.num_rows} x {matrix.num_cols}")
        print(f"Non-zero elements: {len(matrix.elements)}")
        print(f"Sparsity: {1 - len(matrix.elements) / (matrix.num_rows * matrix.num_cols):.4f} " +
              f"({len(matrix.elements)} / {matrix.num_rows * matrix.num_cols})")
        print(f"Load time: {load_time:.4f} seconds")

        # Print a sample of the matrix if it's not too large
        if matrix.num_rows <= 10 and matrix.num_cols <= 10:
            print("\nMatrix content:")
            for i in range(matrix.num_rows):
                row = []
                for j in range(matrix.num_cols):
                    row.append(str(matrix.get_element(i, j)))
                print(" ".join(row))
        else:
            # For larger matrices, print first few non-zero elements
            print("\nSample of non-zero elements:")
            count = 0
            for (row, col), value in sorted(matrix.elements.items()):
                print(f"({row}, {col}) = {value}")
                count += 1
                if count >= 10:
                    print("...")
                    break

    except Exception as e:
        print(f"Error: {e}")

    input("\nPress Enter to continue...")

def perform_operation(operation):
    try:
        # Get input files
        file1 = get_file_path("Enter first matrix file path: ")
        file2 = get_file_path("Enter second matrix file path: ")

        # Load matrices
        print("\nLoading matrices...")
        start_time = time.time()
        matrix1 = SparseMatrix(file1)
        matrix2 = SparseMatrix(file2)
        load_time = time.time() - start_time
        print(f"Matrices loaded in {load_time:.4f} seconds")

        # Perform operation
        print(f"\nPerforming {'addition' if operation == 1 else 'subtraction' if operation == 2 else 'multiplication'}...")
        start_time = time.time()

        if operation == 1:  # Addition
            result = matrix1.add(matrix2)
        elif operation == 2:  # Subtraction
            result = matrix1.subtract(matrix2)
        else:  # Multiplication
            result = matrix1.multiply(matrix2)

        operation_time = time.time() - start_time
        print(f"Operation completed in {operation_time:.4f} seconds")

        # Get output file and save result
        output_file = get_output_file_path()
        result.save_to_file(output_file)
        print(f"\nResult saved to '{output_file}'")
        print(f"Result dimensions: {result.num_rows} x {result.num_cols}")
        print(f"Non-zero elements in result: {len(result.elements)}")

    except Exception as e:
        print(f"\nError: {e}")

    input("\nPress Enter to continue...")

def main():
    while True:
        clear_screen()
        print_banner()

        choice = get_operation()

        if choice == 5:  # Exit
            print("\nExiting program. Goodbye!")
            sys.exit(0)
        elif choice == 4:  # View Matrix Details
            view_matrix_details()
        else:  # Matrix operations (1-3)
            perform_operation(choice)

if __name__ == "__main__":
    main()
