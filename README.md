# alu-sparse-matrix-implementation
Sparse Matrix Implementation
This is a Python implementation of a sparse matrix data structure for the Data Structures and Algorithms for Engineers Programming Assignment 2.
Project Structure
/dsa
  /sparse_matrix
    /code
      /src
        sparse_matrix.py       - Main implementation of the SparseMatrix class
        test_sparse_matrix.py  - Unit tests for the SparseMatrix class
        create_sample_matrices.py - Utility to create sample matrix files
    /sample_inputs             - Directory containing sample matrix files
    README.md                  - This file
Features

Efficient sparse matrix representation using a dictionary-based data structure
Support for matrix operations: addition, subtraction, and multiplication
File I/O for loading and saving matrices
Proper error handling for invalid input formats
Optimized algorithms for matrix operations

Usage
Running the Program
To run the program:
bashcd dsa/sparse_matrix/code/src
python sparse_matrix.py
The program will prompt you for:

The operation to perform (addition, subtraction, or multiplication)
The file paths of the two input matrices
The file path for the output matrix

Creating Sample Matrices
To create sample matrices for testing:
bashcd dsa/sparse_matrix/code/src
python create_sample_matrices.py
This will create various sample matrix files in the /dsa/sparse_matrix/sample_inputs directory.
Running Tests
To run the unit tests:
bashcd dsa/sparse_matrix/code/src
python test_sparse_matrix.py
Implementation Details
SparseMatrix Class
The SparseMatrix class represents a sparse matrix efficiently by only storing non-zero elements in a dictionary with (row, col) tuples as keys.
Core Methods:

__init__(param): Initialize a sparse matrix either from a file path or with given dimensions.
get_element(row, col): Get the value at a specific position in the matrix.
set_element(row, col, value): Set the value at a specific position in the matrix.
add(other): Add another sparse matrix to this one.
subtract(other): Subtract another sparse matrix from this one.
multiply(other): Multiply this matrix by another sparse matrix.
save_to_file(file_path): Save the sparse matrix to a file.

Design Considerations

Memory Efficiency: Only non-zero elements are stored, making it efficient for sparse matrices where most elements are zero.
Time Complexity:

Get/Set operations: O(1)
Addition/Subtraction: O(n₁ + n₂) where n₁ and n₂ are the number of non-zero elements
Multiplication: O(n₁ × n₂) in the worst case, but typically much better for sparse matrices


Error Handling:

Robust parsing of input files
Validation of matrix dimensions for operations
Proper exception handling with meaningful error messages



Input File Format
The input file format follows the assignment specification:
rows=<number_of_rows>
cols=<number_of_columns>
(<row>, <col>, <value>)
(<row>, <col>, <value>)
...
Where:

The first line specifies the number of rows
The second line specifies the number of columns
Subsequent lines specify the non-zero elements with row, column, and value

Error Handling
The implementation handles various error conditions:

Invalid file formats
Missing files
Matrix dimension mismatches
Out-of-bounds indices

Performance Considerations
The implementation is optimized for sparse matrices by:

Using a dictionary to store only non-zero elements
Grouping elements by row and column for efficient multiplication
Avoiding unnecessary operations on zero elements
