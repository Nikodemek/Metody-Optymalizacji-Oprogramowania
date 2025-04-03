import tkinter as tk
from tkinter import ttk
from enum import Enum
from typing import Dict, Callable


class InputType(Enum):
  STRING = 0,
  INT = 1,
  FLOAT = 2,

type InputTypes = int | float | str

class ValidatedEntry(tk.Entry):
  def __init__(
      self,
      master=None,
      input_type: InputType=InputType.STRING,
      value: InputTypes | None = 0,
      **kwargs,
  ):
    self.default_value = value
    self.variable = tk.StringVar(value=str(self.default_value))
    self.input_type = input_type

    tk.Entry.__init__(
      self,
      master=master,
      textvariable=self.variable,
      validate='focus',
      validatecommand=self.check,
      **kwargs,
    )

  def check(self, *args) -> bool:
    val = self.get()
    match self.input_type:
      case InputType.INT:
        is_valid = str(val).isdigit()
      case InputType.FLOAT:
        is_valid = str(val).isdecimal()
      case InputType.STRING:
        is_valid = True
      case _:
        raise ValueError('Invalid input')

    if not is_valid:
      self.set(str(self.default_value))

    return is_valid

  def get(self) -> InputTypes:
    match self.input_type:
      case InputType.INT:
        return int(self.variable.get())
      case InputType.FLOAT:
        return float(self.variable.get())
      case InputType.STRING:
        return str(self.variable.get())
      case _:
        raise ValueError('Invalid input')

  def set(self, value: InputTypes):
    return self.variable.set(str(value))


class TaskInput:
  def __init__(
      self,
      identifier: str,
      label: str,
      input_type: InputType,
      default_value
  ):
    self.identifier = identifier
    self.label = label
    self.input_type = input_type
    self.default_value = default_value


def initialize_app(
    title: str,
    inputs: list[TaskInput],
    apply: Callable[[Dict[str, Callable[[], float]]], None]
):
  window = tk.Tk()
  window.title("Metody Optymalizacji Oprogramowania")
  window.geometry("500x500")

  title_label = ttk.Label(
    master=window,
    text=f'Metody Optymalizacji\n{title}',
    justify=tk.CENTER,
    font=("Arial", 20, "bold"),
    padding=10,
  )
  title_label.pack()

  input_frame = ttk.Frame(master=window)

  value_getters: Dict[str, Callable[[], float]] = {}

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

    value_getters.update({input.identifier: input_entry.get})

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