import unittest
import os
import tempfile
from sparse_matrix import SparseMatrix

class TestSparseMatrix(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        
        self.sample_file_1 = os.path.join(self.test_dir, "matrix1.txt")
        with open(self.sample_file_1, 'w') as f:
            f.write("rows=3\n")
            f.write("cols=3\n")
            f.write("(0, 0, 5)\n")
            f.write("(0, 2, 8)\n")
            f.write("(1, 1, 3)\n")
            f.write("(2, 0, 6)\n")
        
        self.sample_file_2 = os.path.join(self.test_dir, "matrix2.txt")
        with open(self.sample_file_2, 'w') as f:
            f.write("rows=3\n")
            f.write("cols=3\n")
            f.write("(0, 0, 2)\n")
            f.write("(1, 0, 4)\n")
            f.write("(1, 1, 1)\n")
            f.write("(2, 2, 7)\n")
        
        self.sample_file_error = os.path.join(self.test_dir, "matrix_error.txt")
        with open(self.sample_file_error, 'w') as f:
            f.write("rows=3\n")
            f.write("cols=3\n")
            f.write("(0, 0, 5)\n")
            f.write("(0, 2, 8.5)\n")
        
        self.sample_file_whitespace = os.path.join(self.test_dir, "matrix_whitespace.txt")
        with open(self.sample_file_whitespace, 'w') as f:
            f.write("rows=3\n")
            f.write("cols=3\n")
            f.write("(0, 0, 5)\n")
            f.write("  \n")
            f.write("(0, 2, 8)\n")
            f.write("    (1, 1, 3)    \n")
        
        self.output_file = os.path.join(self.test_dir, "output.txt")
    
    def tearDown(self):
        if os.path.exists(self.sample_file_1):
            os.remove(self.sample_file_1)
        if os.path.exists(self.sample_file_2):
            os.remove(self.sample_file_2)
        if os.path.exists(self.sample_file_error):
            os.remove(self.sample_file_error)
        if os.path.exists(self.sample_file_whitespace):
            os.remove(self.sample_file_whitespace)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        
        os.rmdir(self.test_dir)
    
    def test_load_from_file(self):
        matrix = SparseMatrix(self.sample_file_1)
        
        self.assertEqual(matrix.num_rows, 3)
        self.assertEqual(matrix.num_cols, 3)
        self.assertEqual(matrix.get_element(0, 0), 5)
        self.assertEqual(matrix.get_element(0, 2), 8)
        self.assertEqual(matrix.get_element(1, 1), 3)
        self.assertEqual(matrix.get_element(2, 0), 6)
        self.assertEqual(matrix.get_element(0, 1), 0)

    def test_create_with_dimensions(self):
        matrix = SparseMatrix((4, 5))
        
        self.assertEqual(matrix.num_rows, 4)
        self.assertEqual(matrix.num_cols, 5)
        self.assertEqual(len(matrix.elements), 0)
    
    def test_set_and_get_element(self):
        matrix = SparseMatrix((3, 3))
        
        matrix.set_element(0, 0, 5)
        matrix.set_element(1, 2, 7)
        
        self.assertEqual(matrix.get_element(0, 0), 5)
        self.assertEqual(matrix.get_element(1, 2), 7)
        self.assertEqual(matrix.get_element(2, 2), 0)
        
        matrix.set_element(0, 0, 0)
        self.assertEqual(matrix.get_element(0, 0), 0)
        self.assertNotIn((0, 0), matrix.elements)
    
    def test_addition(self):
        matrix1 = SparseMatrix(self.sample_file_1)
        matrix2 = SparseMatrix(self.sample_file_2)
        
        result = matrix1.add(matrix2)
        
        self.assertEqual(result.get_element(0, 0), 7)
        self.assertEqual(result.get_element(0, 2), 8)
        self.assertEqual(result.get_element(1, 0), 4)
        self.assertEqual(result.get_element(1, 1), 4)
        self.assertEqual(result.get_element(2, 0), 6)
        self.assertEqual(result.get_element(2, 2), 7)
    
    def test_subtraction(self):
        matrix1 = SparseMatrix(self.sample_file_1)
        matrix2 = SparseMatrix(self.sample_file_2)
        
        result = matrix1.subtract(matrix2)
        
        self.assertEqual(result.get_element(0, 0), 3)
        self.assertEqual(result.get_element(0, 2), 8)
        self.assertEqual(result.get_element(1, 0), -4)
        self.assertEqual(result.get_element(1, 1), 2)
        self.assertEqual(result.get_element(2, 0), 6)
        self.assertEqual(result.get_element(2, 2), -7)
    
    def test_multiplication(self):
        matrix1 = SparseMatrix(self.sample_file_1)
        matrix2 = SparseMatrix(self.sample_file_2)
        
        result = matrix1.multiply(matrix2)
        
        self.assertEqual(result.get_element(0, 0), 10)
        self.assertEqual(result.get_element(0, 1), 0)
        self.assertEqual(result.get_element(0, 2), 0)
        self.assertEqual(result.get_element(1, 0), 12)
        self.assertEqual(result.get_element(1, 1), 3)
        self.assertEqual(result.get_element(1, 2), 0)
        self.assertEqual(result.get_element(2, 0), 12)
        self.assertEqual(result.get_element(2, 1), 0)
        self.assertEqual(result.get_element(2, 2), 0)
    
    def test_save_to_file(self):
        matrix = SparseMatrix(self.sample_file_1)
        matrix.save_to_file(self.output_file)
        
        loaded_matrix = SparseMatrix(self.output_file)
        
        self.assertEqual(loaded_matrix.num_rows, matrix.num_rows)
        self.assertEqual(loaded_matrix.num_cols, matrix.num_cols)
        
        for (row, col), value in matrix.elements.items():
            self.assertEqual(loaded_matrix.get_element(row, col), value)
    
    def test_error_handling(self):
        with self.assertRaises(ValueError):
            SparseMatrix(self.sample_file_error)
    
    def test_whitespace_handling(self):
        matrix = SparseMatrix(self.sample_file_whitespace)
        
        self.assertEqual(matrix.num_rows, 3)
        self.assertEqual(matrix.num_cols, 3)
        self.assertEqual(matrix.get_element(0, 0), 5)
        self.assertEqual(matrix.get_element(0, 2), 8)
        self.assertEqual(matrix.get_element(1, 1), 3)
    
    def test_dimension_mismatch(self):
        matrix1 = SparseMatrix((3, 3))
        matrix2 = SparseMatrix((3, 4))
        matrix3 = SparseMatrix((4, 3))
        
        with self.assertRaises(ValueError):
            matrix1.add(matrix3)
        
        with self.assertRaises(ValueError):
            matrix1.subtract(matrix3)
        
        with self.assertRaises(ValueError):
            matrix1.multiply(matrix2)
        
        result = matrix1.multiply(matrix2)
        self.assertEqual(result.num_rows, 3)
        self.assertEqual(result.num_cols, 4)


if __name__ == "__main__":
    unittest.main()
