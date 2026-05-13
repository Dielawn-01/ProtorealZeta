import math
from .ring import ProtorealElement

def protoreal_sinh(u):
    """
    Formal Protoreal Sinh (mesh_sinh)
    a_new = sinh(a)
    b_new = sinh(a+b) - sinh(a)
    m_new = cosh(a) * m
    e_new = cosh(a) * e
    l_new = cosh(a) * l
    """
    if not isinstance(u, ProtorealElement): u = ProtorealElement(a=u)
    
    a, b, m, e, l = u.a, u.b, u.c, u.e, u.l
    
    new_a = math.sinh(a)
    new_b = math.sinh(a + b) - math.sinh(a)
    new_m = math.cosh(a) * m
    new_e = math.cosh(a) * e
    new_l = math.cosh(a) * l
    
    return ProtorealElement(new_a, new_b, new_m, new_e, new_l)

def protoreal_cosh(u):
    """
    Formal Protoreal Cosh (mesh_cosh)
    a_new = cosh(a)
    b_new = cosh(a+b) - cosh(a)
    m_new = sinh(a) * m
    e_new = sinh(a) * e
    l_new = sinh(a) * l
    """
    if not isinstance(u, ProtorealElement): u = ProtorealElement(a=u)
    
    a, b, m, e, l = u.a, u.b, u.c, u.e, u.l
    
    new_a = math.cosh(a)
    new_b = math.cosh(a + b) - math.cosh(a)
    new_m = math.sinh(a) * m
    new_e = math.sinh(a) * e
    new_l = math.sinh(a) * l
    
    return ProtorealElement(new_a, new_b, new_m, new_e, new_l)

def protoreal_tanh(u):
    """
    Formal Protoreal Tanh (sinh/cosh)
    Provides a bounded gradient for axiomatic descent.
    """
    s = protoreal_sinh(u)
    c = protoreal_cosh(u)
    # Using the non-commutative ring division (if implemented) or component-wise
    # For descent, we primarily care about the real and noise components
    return s.a / c.a if c.a != 0 else 0
