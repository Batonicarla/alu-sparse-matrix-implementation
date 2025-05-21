"""
Utility script to create sample matrix files for testing the SparseMatrix implementation.
This will create sample matrices in the 'sample_inputs' directory.
"""

import os
import random
import shutil

def create_sample_directory():
    """Create the sample_inputs directory if it doesn't exist."""
    directory = os.path.join('dsa', 'sparse_matrix', 'sample_inputs')
    os.makedirs(directory, exist_ok=True)
    return directory

def generate_sparse_matrix(rows, cols, density=0.01, value_range=(-1000, 1000)):
    """
    Generate a sparse matrix with the given dimensions and density.
    
    Args:
        rows: Number of rows
        cols: Number of columns
        density: Fraction of non-zero elements (between 0 and 1)
        value_range: Range of values (min, max)
    
    Returns:
        Dictionary mapping (row, col) to values
    """
    num_elements = int(rows * cols * density)
    elements = {}
    
    # Generate unique random positions
    positions = set()
    while len(positions) < num_elements:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        positions.add((row, col))
    
    # Assign random values to the positions
    for row, col in positions:
        value = random.randint(value_range[0], value_range[1])
        # Ensure value is not 0
        while value == 0:
            value = random.randint(value_range[0], value_range[1])
        elements[(row, col)] = value
    
    return elements

def write_matrix_to_file(file_path, rows, cols, elements):
    """
    Write a sparse matrix to a file.
    
    Args:
        file_path: Path to write the file
        rows: Number of rows
        cols: Number of columns
        elements: Dictionary mapping (row, col) to values
    """
    with open(file_path, 'w') as file:
        file.write(f"rows={rows}\n")
        file.write(f"cols={cols}\n")
        
        # Sort elements by row and column for better readability
        sorted_elements = sorted(elements.items(), key=lambda x: (x[0][0], x[0][1]))
        
        for (row, col), value in sorted_elements:
            file.write(f"({row}, {col}, {value})\n")

def main():
    """Generate sample matrices."""
    directory = create_sample_directory()
    
    # Generate sample matrices for addition/subtraction
    matrix_sizes = [
        (10, 10),      # Small matrix
        (100, 100),    # Medium matrix
        (1000, 100),   # Tall matrix
        (100, 1000),   # Wide matrix
        (5000, 5000)   # Large matrix (for performance testing)
    ]
    
    for i, (rows, cols) in enumerate(matrix_sizes):
        # Create two matrices of the same size for addition/subtraction
        elements1 = generate_sparse_matrix(rows, cols)
        elements2 = generate_sparse_matrix(rows, cols)
        
        file_path1 = os.path.join(directory, f"matrix_add_sub_{i}_a.txt")
        file_path2 = os.path.join(directory, f"matrix_add_sub_{i}_b.txt")
        
        write_matrix_to_file(file_path1, rows, cols, elements1)
        write_matrix_to_file(file_path2, rows, cols, elements2)
        
        print(f"Created addition/subtraction matrices: {file_path1}, {file_path2}")
    
    # Generate sample matrices for multiplication
    matrix_pairs = [
        ((10, 15), (15, 10)),    # Small square result
        ((30, 20), (20, 40)),    # Medium rectangular result
        ((100, 50), (50, 100)),  # Large square result
        ((500, 30), (30, 70)),   # Very large rectangular result
    ]
    
    for i, ((rows1, cols1), (rows2, cols2)) in enumerate(matrix_pairs):
        # Create matrices where cols1 = rows2 for multiplication
        elements1 = generate_sparse_matrix(rows1, cols1)
        elements2 = generate_sparse_matrix(rows2, cols2)
        
        file_path1 = os.path.join(directory, f"matrix_mult_{i}_a.txt")
        file_path2 = os.path.join(directory, f"matrix_mult_{i}_b.txt")
        
        write_matrix_to_file(file_path1, rows1, cols1, elements1)
        write_matrix_to_file(file_path2, rows2, cols2, elements2)
        
        print(f"Created multiplication matrices: {file_path1}, {file_path2}")
    
    # Create a special case matrix with an incorrect format
    error_file = os.path.join(directory, "matrix_error.txt")
    with open(error_file, 'w') as file:
        file.write(f"rows=5\n")
        file.write(f"cols=5\n")
        file.write(f"(0, 0, 5)\n")
        file.write(f"(1, 1, 3.5)\n")  # Floating point value (error)
    
    print(f"Created matrix with incorrect format: {error_file}")

if __name__ == "__main__":
    main()