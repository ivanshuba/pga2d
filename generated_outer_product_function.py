import csv
from sympy import symbols
from cayley_table_reader import read_cayley_table


def generate_outer_product_function_detailed(csv_path):
    """
    Generate an outer product multiplication function with detailed analysis.
    """
    # Read the Cayley table
    basis_symbols, cayley_lookup = read_cayley_table(csv_path)

    num_basis = len(basis_symbols)

    # Create basis symbol names for display
    basis_names = []
    for i in range(num_basis):
        symbol_str = str(basis_symbols[i])
        basis_names.append(symbol_str)

    print("Basis elements:")
    for i, name in enumerate(basis_names):
        print(f"  {i}: {name}")
    print()

    # Initialize result components
    result_terms = [[] for _ in range(num_basis)]

    # Generate detailed analysis for each row of the first multivector
    for i in range(num_basis):
        print(f"=" * 80)
        print(f"Row {i}: Outer product of basis element '{basis_names[i]}' from multivector a")
        print(f"=" * 80)

        # Stage 1: Raw symbolic form
        print(f"\n1. RAW SYMBOLIC FORM:")
        print(f"   a[{i}] * {basis_names[i]} ^ (entire b multivector) =")
        raw_terms = []
        for j in range(num_basis):
            raw_term = f"a[{i}]{basis_names[i]} ^ b[{j}]{basis_names[j]}"
            raw_terms.append(raw_term)
        print(f"   " + " ^ ".join(raw_terms))

        # Stage 2: Converted form (apply Cayley table)
        print(f"\n2. CONVERTED FORM (after applying outer product Cayley table):")
        converted_terms = []
        conversion_details = []

        for j in range(num_basis):
            if (i, j) in cayley_lookup:
                factor, result_basis_idx = cayley_lookup[(i, j)]

                if factor == 0:
                    converted_term = "0"
                    detail = f"{basis_names[i]}^{basis_names[j]} = 0"
                elif factor == 1:
                    if result_basis_idx < len(basis_names):
                        result_basis = basis_names[result_basis_idx]
                        converted_term = f"(+1) * a[{i}]b[{j}]{result_basis}"
                        detail = f"{basis_names[i]}^{basis_names[j]} = +{result_basis}"
                    else:
                        converted_term = f"(+1) * a[{i}]b[{j}]"
                        detail = f"{basis_names[i]}^{basis_names[j]} = +1"
                elif factor == -1:
                    if result_basis_idx < len(basis_names):
                        result_basis = basis_names[result_basis_idx]
                        converted_term = f"(-1) * a[{i}]b[{j}]{result_basis}"
                        detail = f"{basis_names[i]}^{basis_names[j]} = -{result_basis}"
                    else:
                        converted_term = f"(-1) * a[{i}]b[{j}]"
                        detail = f"{basis_names[i]}^{basis_names[j]} = -1"
                else:
                    converted_term = f"({factor}) * a[{i}]b[{j}]"
                    detail = f"{basis_names[i]}^{basis_names[j]} = {factor}"

                converted_terms.append(converted_term)
                conversion_details.append(detail)
            else:
                converted_terms.append("UNKNOWN")
                conversion_details.append(f"{basis_names[i]}^{basis_names[j]} = UNKNOWN")

        print("   " + " + ".join(converted_terms))
        print("\n   Basis outer product details:")
        for detail in conversion_details:
            print(f"     {detail}")

        # Stage 3: Final simplified form and grouping
        print(f"\n3. FINAL SIMPLIFIED FORM (grouped by result basis):")

        # Group terms by their result basis
        basis_groups = {}
        for j in range(num_basis):
            if (i, j) in cayley_lookup:
                factor, result_basis_idx = cayley_lookup[(i, j)]

                if factor != 0:  # Skip zero terms
                    if result_basis_idx not in basis_groups:
                        basis_groups[result_basis_idx] = []

                    # Create the coefficient term
                    if factor == 1:
                        term = f"a[{i}]*b[{j}]"
                    elif factor == -1:
                        term = f"-a[{i}]*b[{j}]"
                    else:
                        term = f"{factor}*a[{i}]*b[{j}]"

                    basis_groups[result_basis_idx].append(term)
                    result_terms[result_basis_idx].append(term)

        # Display the grouped terms
        for basis_idx in sorted(basis_groups.keys()):
            basis_name = basis_names[basis_idx] if basis_idx < len(basis_names) else f"basis_{basis_idx}"
            terms = basis_groups[basis_idx]
            terms_str = " + ".join(terms).replace("+ -", "- ")
            print(f"   r[{basis_idx}] ({basis_name}): {terms_str}")

        print()

    # Generate the final function
    print("=" * 80)
    print("FINAL GENERATED OUTER PRODUCT FUNCTION")
    print("=" * 80)

    function_code = """def outer_product(a, b):
    \"\"\"
    Compute the outer product of two PGA2D multivectors.

    Args:
        a: List/array of 8 coefficients for multivector a
        b: List/array of 8 coefficients for multivector b

    Returns:
        List of 8 coefficients representing the result multivector
    \"\"\"
    r = [0] * 8
"""

    # Generate each result component
    for basis_idx in range(num_basis):
        terms = result_terms[basis_idx]
        if terms:
            # Join all terms for this basis element
            expression = terms[0]
            for term in terms[1:]:
                if term.startswith('-'):
                    expression += term
                else:
                    expression += '+' + term

            basis_name = basis_names[basis_idx] if basis_idx < len(basis_names) else f"basis_{basis_idx}"
            function_code += f"    r[{basis_idx}] = {expression}  # {basis_name}\n"
        else:
            basis_name = basis_names[basis_idx] if basis_idx < len(basis_names) else f"basis_{basis_idx}"
            function_code += f"    r[{basis_idx}] = 0  # {basis_name} - no terms\n"

    function_code += "\n    return r\n"

    return function_code, basis_symbols, result_terms


if __name__ == "__main__":
    try:
        function_code, basis_symbols, result_terms = generate_outer_product_function_detailed(
            "PGA2D-Outer-Product-Caley.csv")

        print(function_code)

        # Save to file
        with open("generated_outer_product.py", "w") as f:
            f.write("# Auto-generated outer product function for PGA2D\n")
            f.write("# Generated with detailed analysis\n\n")
            f.write(function_code)

        print(f"\nFunction saved to 'generated_outer_product.py'")

    except FileNotFoundError:
        print("CSV file not found. Please make sure 'PGA2D-Outer-Product-Caley.csv' exists.")
    except Exception as e:
        print(f"Error: {e}")