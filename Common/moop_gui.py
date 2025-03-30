import tkinter as tk
from tkinter import ttk
from enum import Enum
from typing import Dict, Callable


class InputType(Enum):
  STRING = '',
  INT = 0,
  FLOAT = 0.0,


class ValidatedEntry(tk.Entry):
  def __init__(
      self,
      master=None,
      input_type: InputType=InputType.STRING,
      value: str | int | float | None = 0,
      **kwargs
  ):
    self.default_value = str(input_type.value[0] if value is None else value)

    self.variable = tk.StringVar(value=self.default_value)
    self.get, self.set = self.variable.get, self.variable.set

    self.input_type = input_type
    tk.Entry.__init__(
      self,
      master=master,
      textvariable=self.variable,
      validate='focus',
      validatecommand=self.check,
      **kwargs
    )

  def check(self, *args) -> bool:
    val = self.get()
    is_valid = False
    match self.input_type:
      case InputType.INT:
        is_valid = val.isdigit()
      case InputType.FLOAT:
        is_valid = val.isdecimal()
      case InputType.STRING:
        is_valid = True
      case _:
        raise ValueError('Invalid input')

    return is_valid


class TaskInput:
  def __init__(
      self,
      label: str,
      input_type: InputType,
      default_value
  ):
    self.label = label
    self.input_type = input_type
    self.default_value = default_value


def initialize_app(
    title: str,
    inputs: list[TaskInput],
    apply: Callable[[Dict[str, Callable]], None]):
  window = tk.Tk()
  window.title("Metody Optymalizacji Oprogramowania")
  window.geometry("500x500")

  title_label = ttk.Label(
    master=window,
    text=f'Metody Optymalizacji\n{title}',
    justify=tk.CENTER,
    font=("Arial", 20, "bold"),
    padding=10
  )
  title_label.pack()

  input_frame = ttk.Frame(master=window)

  value_getters = {}

  for input in inputs:
    input_container = ttk.Frame(master=input_frame)

    input_label = ttk.Label(
      master=input_container,
      text=input.label,
      justify=tk.LEFT,
      font=("Arial", 12, "normal"),
    )
    input_entry = ValidatedEntry(
      master=input_container,
      input_type=input.input_type,
      value=str(input.default_value),
      font=("Arial", 12, "normal"),
    )

    value_getters.update({input.label: input_entry.get})

    input_entry.pack(side=tk.RIGHT, padx=5, pady=5)
    input_label.pack(side=tk.LEFT, padx=5, pady=5)

    input_container.pack(side="top", padx=5, pady=5)

  button = ttk.Button(
    master=input_frame,
    text='Oblicz',
    command=lambda: apply(value_getters)
  )
  button.pack(side="bottom", padx=5, pady=5)

  input_frame.pack(side=tk.TOP, padx=10)

  window.mainloop()