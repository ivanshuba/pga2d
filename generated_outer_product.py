# Auto-generated outer product function for PGA2D
# Generated with detailed analysis

def outer_product(a, b):
    """
    Compute the outer product of two PGA2D multivectors.

    Args:
        a: List/array of 8 coefficients for multivector a
        b: List/array of 8 coefficients for multivector b

    Returns:
        List of 8 coefficients representing the result multivector
    """
    r = [0] * 8
    r[0] = a[0]*b[0]  # 1
    r[1] = a[0]*b[1]+a[1]*b[0]  # e0
    r[2] = a[0]*b[2]+a[2]*b[0]  # e1
    r[3] = a[0]*b[3]+a[3]*b[0]  # e2
    r[4] = a[0]*b[4]+a[1]*b[2]-a[2]*b[1]+a[4]*b[0]  # e01
    r[5] = a[0]*b[5]+a[1]*b[3]-a[3]*b[1]+a[5]*b[0]  # e02
    r[6] = a[0]*b[6]+a[2]*b[3]-a[3]*b[2]+a[6]*b[0]  # e12
    r[7] = a[0]*b[7]+a[1]*b[6]-a[2]*b[5]+a[3]*b[4]+a[4]*b[3]-a[5]*b[2]+a[6]*b[1]+a[7]*b[0]  # e012

    return r
