 Sparse Matrix Implementation

A Python implementation of a sparse matrix data structure for Data Structures and Algorithms for Engineers (Programming Assignment 2).


/dsa
  /sparse_matrix
    /code
      /src
        sparse_matrix.py   
        - Main SparseMatrix class implementation
        test_sparse_matrix.py
        - Unit tests
        create_sample_matrices.py 
        - Utility to create sample files
    /sample_inputs        
    - Sample matrix files




- Dictionary-based sparse matrix representation (stores only non-zero elements)
- Supports matrix operations: addition, subtraction, multiplication
- File I/O for loading and saving matrices
- Error handling for invalid inputs



Run the program:
bash
cd dsa/sparse_matrix/code/src
python sparse_matrix.py


Create sample matrices:
bash
python create_sample_matrices.py


Run tests:
bash
python test_sparse_matrix.py


 Input File Format


rows=<number_of_rows>

cols=<number_of_columns>

(row, col, value)
(row, col, value)
...








