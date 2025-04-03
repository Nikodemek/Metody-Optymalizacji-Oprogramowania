from __future__ import annotations

class Point2d:
  def __init__(self, x: float, y: float):
    self.x = x
    self.y = y

  def magnitude_from(self, other: Point2d):
    return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

  def distance_from(self, other: Point2d):
    return math.sqrt(self.magnitude_from(other))

  def __repr__(self):
    return f"[{self.x:.3g}, {self.y:.3g}]"