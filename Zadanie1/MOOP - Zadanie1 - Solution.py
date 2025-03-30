from Common.moop_gui import *

def calculate(value_getters):
  print(f'S1_H: {value_getters["S1_H"]()}')
  print(f'S2_H: {value_getters["S2_H"]()}')
  print(f'S1_C: {value_getters["S1_C"]()}')
  print(f'S2_C: {value_getters["S2_C"]()}')
  print(f'S1_Zysk: {value_getters["S1_Zysk"]()}')
  print(f'S2_Zysk: {value_getters["S2_Zysk"]()}')


initialize_app(
  title="Zadanie 1 (zad6)",
  inputs = [
    TaskInput('S1_H', InputType.INT, -2),
    TaskInput('S2_H', InputType.INT, 1),
    TaskInput('S1_C', InputType.INT, 1),
    TaskInput('S2_C', InputType.INT, 2),
    TaskInput('S1_Zysk', InputType.INT, 3),
    TaskInput('S2_Zysk', InputType.INT, 2),
  ],
  apply=calculate
)

