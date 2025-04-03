from __future__ import annotations
import math

from common.axis import Axis

class LinearFunction:
  def __init__(self, slope_a: float, slope_b: float, gen_a: float, gen_b: float, gen_c: float):
    self.slope_a = slope_a
    self.slope_b = slope_b
    self.gen_a = gen_a
    self.gen_b = gen_b
    self.gen_c = gen_c

  def calculate_value(self, x):
    return self.slope_a * x + self.slope_b

  def find_intersection(self, other: LinearFunction):
    if self.slope_a == other.slope_a:
      if self.slope_b != other.slope_b:
        return None
      else:
        return 0

    a_diff = self.slope_a - other.slope_a
    intersection = (other.slope_b - self.slope_b) / a_diff

    return intersection

  def find_intersection_with_axis(self, axis: Axis):
    match axis:
      case Axis.X:
        return self.gen_c / self.gen_a
      case Axis.Y:
        return 0

  def is_rising(self) -> bool:
    return self.slope_a > 0

  @classmethod
  def from_slope(cls, a: float, b: float):
    if a == 0:
      raise ValueError("Slope A must not be 0!")

    gen_a = -a
    gen_b = 1
    gen_c = b

    func = cls(a, b, gen_a, gen_b, gen_c)
    return func

  @classmethod
  def from_general(cls, gen_a: float, gen_b: float, gen_c: float):
    if gen_b == 0:
      raise ValueError("Constant b can not be 0!")

    a = -gen_a / gen_b
    b = gen_c / gen_b

    func = cls(a, b, gen_a, gen_b, gen_c)
    return func

  def to_slope_string(self):
    sign = '+' if self.slope_b >= 0 else '-'
    return f'y = {self.slope_a}x {sign} {math.fabs(self.slope_b)}'

  def to_general_string(self):
    sign = '+' if self.gen_b >= 0 else '-'
    return f'{self.gen_a}x {sign} {math.fabs(self.gen_b)}y = {self.gen_c}'