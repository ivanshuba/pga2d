import csv
from sympy import symbols


def read_cayley_table(csv_path):
    """
    Read a CSV file containing a Cayley table for geometric algebra.

    Args:
        csv_path (str): Path to the CSV file

    Returns:
        tuple: (basis_symbols, cayley_lookup)
            - basis_symbols: dict mapping index to SymPy symbol
            - cayley_lookup: dict with keys (i,j) and values (factor, basis_index)
    """
    basis_symbols = {}
    cayley_lookup = {}

    # Try different delimiters
    delimiters = [',', '\t', ' ']

    with open(csv_path, 'r') as file:
        # Read all lines
        lines = file.readlines()

        # Clean up lines (remove leading/trailing whitespace)
        lines = [line.strip() for line in lines if line.strip()]

        if not lines:
            raise ValueError("Empty CSV file")

        # Determine the delimiter by trying to parse the first line
        first_line = lines[0]
        delimiter = None

        for delim in delimiters:
            if delim in first_line:
                # Split and filter out empty strings
                test_split = [item.strip() for item in first_line.split(delim) if item.strip()]
                if len(test_split) > 1:
                    delimiter = delim
                    break

        if delimiter is None:
            # If no delimiter found, assume space-separated and split on whitespace
            delimiter = None  # This will make split() split on any whitespace

        # Parse the first row to get basis elements
        if delimiter:
            basis_elements = [item.strip() for item in lines[0].split(delimiter) if item.strip()]
        else:
            basis_elements = lines[0].split()

        # Create basis_symbols dictionary
        for i, element in enumerate(basis_elements):
            basis_symbols[i] = symbols(element)

        # Create a reverse mapping for lookup
        element_to_index = {element: i for i, element in enumerate(basis_elements)}

        # Parse ALL rows including the first one to build the full 8x8 Cayley table
        for row_idx, line in enumerate(lines):  # Include ALL lines
            if delimiter:
                row_elements = [item.strip() for item in line.split(delimiter) if item.strip()]
            else:
                row_elements = line.split()

            # Process ALL elements in each row
            for col_idx, value in enumerate(row_elements):
                # Determine the multiplication factor and basis element
                factor = 0
                basis_index = None

                if value == '0':
                    factor = 0
                    basis_index = 0  # We'll use 0 as a placeholder for zero
                else:
                    # Check if the value has a minus sign
                    if value.startswith('-'):
                        factor = -1
                        element_name = value[1:]  # Remove the minus sign
                    else:
                        factor = 1
                        element_name = value

                    # Find the index of this element in the basis
                    if element_name in element_to_index:
                        basis_index = element_to_index[element_name]
                    else:
                        raise ValueError(f"Unknown basis element: {element_name}")

                # Store in the lookup table
                cayley_lookup[(row_idx, col_idx)] = (factor, basis_index)

    return basis_symbols, cayley_lookup


def print_cayley_table(cayley_lookup, num_elements):
    """
    Print the Cayley lookup table in a compact row-by-row format.

    Args:
        cayley_lookup (dict): The Cayley lookup table
        num_elements (int): Number of basis elements (should be 8)
    """
    print("Cayley lookup table:")
    for row in range(num_elements):
        row_str = ""
        for col in range(num_elements):
            if (row, col) in cayley_lookup:
                factor, basis_idx = cayley_lookup[(row, col)]
                row_str += f"({row}, {col}): ({factor}, {basis_idx}),    "
            else:
                row_str += f"({row}, {col}): NOT_FOUND,    "
        print(f" {row_str}")


# Example usage:
if __name__ == "__main__":
    # Test with your CSV file
    try:
        basis_symbols, cayley_lookup = read_cayley_table("PGA2D-Caley.csv")

        print("Basis symbols:")
        for i, symbol in basis_symbols.items():
            print(f"  {i}: {symbol}")

        print(f"\nTotal basis elements: {len(basis_symbols)}")
        print(f"Total lookup entries: {len(cayley_lookup)}")
        print(
            f"Expected entries: {len(basis_symbols)} x {len(basis_symbols)} = {len(basis_symbols) * len(basis_symbols)}")

        print_cayley_table(cayley_lookup, len(basis_symbols))

    except FileNotFoundError:
        print("CSV file not found. Please make sure the file path is correct.")
    except Exception as e:
        print(f"Error: {e}")