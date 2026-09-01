import numpy as np

print('=====  Question 1: 2x2 @ 2x2 =====')
A1 = np.array([[2, 3], [1, 4]])
B1 = np.array([[5, 1], [0, 2]])
C1 = A1 @ B1
print(f'A:\n{A1}')
print(f'B:\n{B1}')
print(f'A @ B:\n{C1}')
expected1 = np.array([[10, 8], [5, 9]])
print(f'Expected:\n{expected1}')
print(f'Match: {np.array_equal(C1, expected1)}')
print()

print('=====  Question 2: 3x3 @ 3x3 =====')
A2 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
B2 = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]])
C2 = A2 @ B2
print(f'A:\n{A2}')
print(f'B:\n{B2}')
print(f'A @ B:\n{C2}')
expected2 = np.array([[30, 24, 18], [84, 69, 54], [138, 114, 90]])
print(f'Expected:\n{expected2}')
print(f'Match: {np.array_equal(C2, expected2)}')
print()

print('=====  Question 3: 2x3 @ 3x2 =====')
A3 = np.array([[1, 0, 2], [-1, 3, 1]])
B3 = np.array([[3, 1], [2, 1], [1, 0]])
C3 = A3 @ B3
print(f'A:\n{A3}')
print(f'B:\n{B3}')
print(f'A @ B:\n{C3}')
expected3 = np.array([[5, 1], [4, 2]])
print(f'Expected:\n{expected3}')
print(f'Match: {np.array_equal(C3, expected3)}')
print()

if all([
    np.array_equal(C1, expected1),
    np.array_equal(C2, expected2),
    np.array_equal(C3, expected3),
]):
    print('All 3 questions: CORRECT!')
else:
    print('Some mismatches found!')
