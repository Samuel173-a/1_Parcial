import sympy as sp


q1, q2, q3 = sp.symbols('q1 q2 q3')
pi = sp.pi


def dh_matrix(theta, d, a, alpha):
    return sp.Matrix([
        [sp.cos(theta), -sp.sin(theta)*sp.cos(alpha),  sp.sin(theta)*sp.sin(alpha), a*sp.cos(theta)],
        [sp.sin(theta),  sp.cos(theta)*sp.cos(alpha), -sp.cos(theta)*sp.sin(alpha), a*sp.sin(theta)],
        [0,              sp.sin(alpha),               sp.cos(alpha),              d],
        [0,              0,                           0,                          1]
    ])


A1 = dh_matrix(q1, 1, 0, -pi/2)


A2 = dh_matrix(q2, 0, 0.5, 0)


A3 = dh_matrix(q3, 0, 0.3, 0)


T = sp.simplify(A1 * A2 * A3)

print("\n" + "-" * 30)
print("ECUACIONES DE POSICIÓN (x, y, z)")
print("-" * 30)
# La última columna de la matriz T nos da la posición del efector final
print(f"Px = {T[0,3]}")
print(f"Py = {T[1,3]}")
print(f"Pz = {T[2,3]}")