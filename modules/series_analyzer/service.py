import numpy as np
from fastapi import HTTPException

def is_arithmetic(seq):
    diffs = np.diff(seq)
    return np.allclose(diffs, diffs[0]), diffs[0]

def is_geometric(seq):
    try:
        ratios = [seq[i+1]/seq[i] for i in range(len(seq)-1) if seq[i] != 0]
        return np.allclose(ratios, ratios[0]), ratios[0]
    except ZeroDivisionError:
        return False, None

def is_fibonacci(seq):
    if len(seq) < 3:
        return False
    for i in range(2, len(seq)):
        if seq[i] != seq[i-1] + seq[i-2]:
            return False
    return True

def is_square(seq):
    roots = [np.sqrt(x) for x in seq]
    return all(float(r).is_integer() for r in roots)

def is_cube(seq):
    roots = [round(x ** (1/3)) for x in seq]
    return all(abs(r**3 - s) < 1e-6 for r, s in zip(roots, seq))

def polynomial_fit_predict(seq, degree=2):
    """Try to fit polynomial of given degree."""
    x = np.arange(len(seq))
    coeffs = np.polyfit(x, seq, degree)
    poly = np.poly1d(coeffs)
    next_term = round(poly(len(seq)))
    return next_term, coeffs.tolist()

def predict_next_term(seq):
    if len(seq) < 2:
        raise HTTPException(status_code=400, detail="Provide at least two numbers in the series")

    seq = list(map(float, seq))
    next_term = None
    pattern = "Unknown"

    # 1️⃣ Arithmetic
    arith, diff = is_arithmetic(seq)
    if arith:
        next_term = seq[-1] + diff
        pattern = f"Arithmetic progression (d = {diff})"
    # 2️⃣ Geometric
    elif (geo := is_geometric(seq))[0]:
        next_term = seq[-1] * geo[1]
        pattern = f"Geometric progression (r = {round(geo[1],3)})"
    # 3️⃣ Fibonacci
    elif is_fibonacci(seq):
        next_term = seq[-1] + seq[-2]
        pattern = "Fibonacci sequence"
    # 4️⃣ Square
    elif is_square(seq):
        root = int(np.sqrt(seq[-1]))
        next_term = (root + 1)**2
        pattern = "Square numbers"
    # 5️⃣ Cube
    elif is_cube(seq):
        root = round(seq[-1] ** (1/3))
        next_term = (root + 1)**3
        pattern = "Cubic numbers"
    # 6️⃣ Polynomial Fit (Complex)
    else:
        try:
            next_term, coeffs = polynomial_fit_predict(seq)
            pattern = f"Polynomial fit (degree 2): coeffs={coeffs}"
        except Exception:
            raise HTTPException(status_code=400, detail="Could not determine the next term pattern")

    return {
        "input_sequence": seq,
        "pattern_detected": pattern,
        "predicted_next_term": round(next_term, 3)
    }
