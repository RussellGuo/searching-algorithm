from fractions import Fraction


def tan_of_add(tan_a: Fraction, tan_b: Fraction) -> Fraction:
    result = (tan_a + tan_b) / (1 - tan_a * tan_b)
    return result


def tan_of_neg(tan_a: Fraction) -> Fraction:
    return -tan_a


def tan_of_double(tan_a: Fraction) -> Fraction:
    return tan_of_add(tan_a, tan_a)


def tan_of_sub(tan_a: Fraction, tan_b: Fraction) -> Fraction:
    tan_neg_b = tan_of_neg(tan_b)
    return tan_of_add(tan_a, tan_neg_b)


def tan_of_complementary(tan_a: Fraction):
    return Fraction(1) / tan_a
