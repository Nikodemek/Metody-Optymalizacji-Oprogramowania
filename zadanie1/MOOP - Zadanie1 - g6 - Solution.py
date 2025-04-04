from __future__ import annotations

from typing import Dict, Callable
import matplotlib.pyplot as plt

from common.linearfunction import LinearFunction
from common.moop_gui import initialize_app, TaskInput, InputType
from common.points2d import Point2d
from common.axis import Axis
from common.limitation import Limitation

def find_all_notable_points(funcs: list[LinearFunction]) -> list[Point2d]:
  points: list[Point2d] = []

  for i, func in enumerate(funcs):
    for axis in Axis:
      intersection_with_axis = func.find_intersection_with_axis(axis)
      points.append(Point2d(intersection_with_axis, func.calculate_value(intersection_with_axis)))

    if i < len(funcs) - 1:
      for other_func in funcs[(i+1):]:
        intersection_with_func = func.find_intersection(other_func)
        points.append(Point2d(intersection_with_func, func.calculate_value(intersection_with_func)))

  return points

def filter_invalid_points(
    points: list[Point2d],
    funcs_with_limitations: list[(LinearFunction, Limitation)]
) -> list[Point2d]:
  valid_points: list[Point2d] = []

  for point in points:
    is_valid = False

    for func, limitation in funcs_with_limitations:
      is_valid = True
      value_in_point = func.calculate_value(point.x)

      match limitation:
        case limitation.LESS_OR_EQUAL:
          is_valid = point.y <= value_in_point
        case limitation.GREATER_OR_EQUAL:
          is_valid = point.y >= value_in_point
        case limitation.EQUAL:
          is_valid = point.y == value_in_point
      if not is_valid:
        break

    if is_valid:
      valid_points.append(point)

  return valid_points

def get_range_to_display(notable_points: list[Point2d], extra: float = 0.5) -> tuple[float, float]:
  if len(notable_points) == 0:
    return -5, 5

  min_x = max_x = notable_points[0].x

  for point in notable_points[1:]:
    if point.x < min_x:
      min_x = point.x
    if point.x > max_x:
      max_x = point.x

  diff = max_x - min_x
  additional = diff * extra

  return min_x - additional, max_x + additional

def plot_func(func: LinearFunction, display_range: tuple[float, float], color):
  X = [display_range[0], display_range[1]]
  Y = [func.calculate_value(x) for x in X]
  plt.plot(X, Y, label=func.to_slope_string(), color=color, linewidth=2)

  fill_min, fill_max = [0, display_range[1]]
  intersection_with_x = func.find_intersection_with_axis(Axis.X)

  intersection_or_0 = max(intersection_with_x, 0)
  if func.is_rising():
    fill_min = intersection_or_0
  else:
    fill_max = intersection_or_0
    if intersection_with_x < 0:
      return

  fill_X = [fill_min, fill_max]
  fill_Y = [func.calculate_value(x) for x in fill_X]
  plt.fill_between(fill_X, fill_Y, [0, 0], color=color, alpha=0.2)

def find_optimal(notable_points: list[Point2d], utility_func: Callable[[float, float], float]) -> list[Point2d]:
  if len(notable_points) == 0:
    return []

  best_points: list[(Point2d, float)] = []

  for point in notable_points:
    value = utility_func(point.x, point.y)

    if len(best_points) == 0:
      best_points.append((point, value))

    current_best = best_points[0][1]
    if value >= current_best:
      if value > current_best:
        best_points.clear()
      best_points.append((point, value))

  return [best[0] for best in best_points]


def calculate(value_getters: Dict[str, Callable[[], float]]):
  vg = value_getters
  func_h = LinearFunction.from_general(gen_a=vg['S1_H'](), gen_b=vg['S2_H'](), gen_c=vg['H_max']())
  func_c = LinearFunction.from_general(gen_a=vg['S1_C'](), gen_b=vg['S2_C'](), gen_c=vg['C_max']())
  utility_func = lambda x1, x2: (vg['S1_zysk']() * x1) + (vg['S2_zysk']() * x2)

  points = find_all_notable_points([func_h, func_c])
  valid_points = filter_invalid_points(points, [
    (func_h, Limitation.LESS_OR_EQUAL),
    (func_c, Limitation.LESS_OR_EQUAL),
  ])
  optimal_points = find_optimal(valid_points, utility_func)

  plt.figure(figsize=(8, 6))

  display_range = get_range_to_display(points, 0.3)
  plot_func(func_h, display_range, 'purple')
  plot_func(func_c, display_range, 'green')

  plt.scatter(
    x=[point.x for point in optimal_points],
    y=[point.y for point in optimal_points],
    color='red',
    linewidths=3,
    label=f'Optimum',
  )
  for point in optimal_points:
    plt.text(point.x, point.y + 0.7, str(point), size=12, color='red')

  plt.xlabel('x1')
  plt.ylabel('x2')
  plt.axhline(0, color='black')
  plt.axvline(0, color='black')
  plt.legend()
  plt.grid()

  print(
    f'Punkty, w których rozwiązanie jest optymalne: {optimal_points}, '
    f'ponieważ zysk w tych punktach wynosi kolejno {[utility_func(point.x, point.y) for point in optimal_points]}'
  )

  plt.show()


initialize_app(
  title="Zadanie 1 (zad6)",
  inputs = [
    TaskInput('S1_H', 'Wykorzystanie H przy S1', InputType.FLOAT, -2),
    TaskInput('S2_H', 'Wykorzystanie H przy S2', InputType.FLOAT, 1),
    TaskInput('S1_C', 'Wykorzystanie C przy S1', InputType.FLOAT, 1),
    TaskInput('S2_C', 'Wykorzystanie C przy S2', InputType.FLOAT, 2),
    TaskInput('S1_zysk', 'Zysk z S1', InputType.FLOAT, 3),
    TaskInput('S2_zysk', 'Zysk z S2', InputType.FLOAT, 2),
    TaskInput('H_max', 'Max zużycie H', InputType.FLOAT, 2),
    TaskInput('C_max', 'Max zużycie C', InputType.FLOAT, 8),
  ],
  apply=calculate,
)

