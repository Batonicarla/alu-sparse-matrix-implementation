class SparseMatrix:
    def __init__(self, param=None):
        self.elements = {}
        if isinstance(param, str):
            self._load_from_file(param)
        elif isinstance(param, tuple) and len(param) == 2:
            self.num_rows, self.num_cols = param
        else:
            raise ValueError("Invalid parameter. Expected file path or (rows, cols) tuple.")

    def _load_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                lines = [line.strip() for line in file.readlines() if line.strip()]
                if not lines[0].startswith("rows="):
                    raise ValueError("Input file has wrong format")
                if not lines[1].startswith("cols="):
                    raise ValueError("Input file has wrong format")
                try:
                    self.num_rows = int(lines[0].split('=')[1])
                    self.num_cols = int(lines[1].split('=')[1])
                except (ValueError, IndexError):
                    raise ValueError("Input file has wrong format")
                for i in range(2, len(lines)):
                    line = lines[i].strip()
                    if not (line.startswith('(') and line.endswith(')')):
                        raise ValueError("Input file has wrong format")
                    content = line[1:-1].strip()
                    try:
                        values = [int(val.strip()) for val in content.split(',')]
                        if len(values) != 3:
                            raise ValueError("Input file has wrong format")
                        row, col, value = values
                        if row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols:
                            raise ValueError(f"Matrix indices out of bounds: ({row}, {col})")
                        if value != 0:
                            self.elements[(row, col)] = value
                    except ValueError:
                        raise ValueError("Input file has wrong format")
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")

    def get_element(self, row, col):
        if row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols:
            raise IndexError(f"Matrix indices out of bounds: ({row}, {col})")
        return self.elements.get((row, col), 0)

    def set_element(self, row, col, value):
        if row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols:
            raise IndexError(f"Matrix indices out of bounds: ({row}, {col})")
        if value == 0:
            self.elements.pop((row, col), None)
        else:
            self.elements[(row, col)] = value

    def add(self, other):
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrix dimensions do not match for addition")
        result = SparseMatrix((self.num_rows, self.num_cols))
        for (row, col), value in self.elements.items():
            result.set_element(row, col, value)
        for (row, col), value in other.elements.items():
            current_value = result.get_element(row, col)
            result.set_element(row, col, current_value + value)
        return result

    def subtract(self, other):
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrix dimensions do not match for subtraction")
        result = SparseMatrix((self.num_rows, self.num_cols))
        for (row, col), value in self.elements.items():
            result.set_element(row, col, value)
        for (row, col), value in other.elements.items():
            current_value = result.get_element(row, col)
            result.set_element(row, col, current_value - value)
        return result

    def multiply(self, other):
        if self.num_cols != other.num_rows:
            raise ValueError("Matrix dimensions do not match for multiplication")
        result = SparseMatrix((self.num_rows, other.num_cols))
        self_rows = {}
        for (row, col), value in self.elements.items():
            if row not in self_rows:
                self_rows[row] = {}
            self_rows[row][col] = value
        other_cols = {}
        for (row, col), value in other.elements.items():
            if col not in other_cols:
                other_cols[col] = {}
            other_cols[col][row] = value
        for row in self_rows:
            for col in other_cols:
                total = 0
                for k in self_rows[row]:
                    if k in other_cols[col]:
                        total += self_rows[row][k] * other_cols[col][k]
                if total != 0:
                    result.set_element(row, col, total)
        return result

    def save_to_file(self, file_path):
        with open(file_path, 'w') as file:
            file.write(f"rows={self.num_rows}\n")
            file.write(f"cols={self.num_cols}\n")
            sorted_elements = sorted(self.elements.items(), key=lambda x: (x[0][0], x[0][1]))
            for (row, col), value in sorted_elements:
                file.write(f"({row}, {col}, {value})\n")

    def __str__(self):
        s = f"SparseMatrix: {self.num_rows}x{self.num_cols}, {len(self.elements)} non-zero elements\n"
        if self.num_rows <= 10 and self.num_cols <= 10:
            for i in range(self.num_rows):
                row = []
                for j in range(self.num_cols):
                    row.append(str(self.get_element(i, j)))
                s += " ".join(row) + "\n"
        else:
            sorted_elements = sorted(self.elements.items(), key=lambda x: (x[0][0], x[0][1]))
            for (row, col), value in sorted_elements:
                s += f"({row}, {col}): {value}\n"
                if len(sorted_elements) > 10 and sorted_elements.index(((row, col))) == 9:
                    s += "...\n"
                    break
        return s


def main():
    print("Sparse Matrix Operations")
    print("========================")
    print("Select operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    try:
        operation = int(input("Enter option (1-3): "))
        if operation not in [1, 2, 3]:
            raise ValueError("Invalid operation selection")
        matrix1_file = input("Enter file path for first matrix: ")
        matrix2_file = input("Enter file path for second matrix: ")
        output_file = input("Enter output file path: ")
        print("Loading matrices...")
        matrix1 = SparseMatrix(matrix1_file)
        matrix2 = SparseMatrix(matrix2_file)
        if operation == 1:
            print("Performing addition...")
            result = matrix1.add(matrix2)
        elif operation == 2:
            print("Performing subtraction...")
            result = matrix1.subtract(matrix2)
        else:
            print("Performing multiplication...")
            result = matrix1.multiply(matrix2)
        result.save_to_file(output_file)
        print(f"Result saved to {output_file}")
    except ValueError as e:
        print(f"Error: {e}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
  
      
     
     
        
     
     
     
        
  
    
      
    
  
  
