import math
from .ring import ProtorealElement

def protoreal_sin(u):
    """
    Formal Protoreal Sine (mesh_sin)
    a_new = sin(a)
    b_new = sin(a+b) - sin(a)
    m_new = cos(a) * m
    e_new = cos(a) * e
    l_new = cos(a) * l
    """
    if not isinstance(u, ProtorealElement): u = ProtorealElement(a=u)
    
    a, b, m, e, l = u.a, u.b, u.c, u.e, u.l
    
    new_a = math.sin(a)
    new_b = math.sin(a + b) - math.sin(a)
    new_m = math.cos(a) * m
    new_e = math.cos(a) * e
    new_l = math.cos(a) * l
    
    return ProtorealElement(new_a, new_b, new_m, new_e, new_l)

def protoreal_cos(u):
    """
    Formal Protoreal Cosine (mesh_cos)
    a_new = cos(a)
    b_new = cos(a+b) - cos(a)
    m_new = -sin(a) * m
    e_new = -sin(a) * e
    l_new = -sin(a) * l
    """
    if not isinstance(u, ProtorealElement): u = ProtorealElement(a=u)
    
    a, b, m, e, l = u.a, u.b, u.c, u.e, u.l
    
    new_a = math.cos(a)
    new_b = math.cos(a + b) - math.cos(a)
    new_m = -math.sin(a) * m
    new_e = -math.sin(a) * e
    new_l = -math.sin(a) * l
    
    return ProtorealElement(new_a, new_b, new_m, new_e, new_l)
