import random
import tkinter as tk
from tkinter import messagebox
import pygame


pygame.mixer.init()
pygame.mixer.music.load("jungles.ogg")
pygame.mixer.music.play(-1)  

class TreasureHunt:
    def __init__(self, master):
        self.master = master
        self.master.title("Игра 'Охота за сокровищами'")
        
        self.grid_size = 5
        self.max_attempts = 10
        self.hidden_treasure = (0, 0)
        self.attempts = 0
        self.won = False
        
        self.initialize_game()
        
    def initialize_game(self):
        self.hidden_treasure = (random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1))
        self.attempts = 0
        
        self.label = tk.Label(self.master, text="Введите координаты сокровища (x, y) от 0 до 4:")
        self.label.pack()

        self.entry_x = tk.Entry(self.master)
        self.entry_x.pack()
        self.entry_x.insert(0, "x")

        self.entry_y = tk.Entry(self.master)
        self.entry_y.pack()
        self.entry_y.insert(0, "y")

        self.guess_button = tk.Button(self.master, text="Попробовать", command=self.check_guess)
        self.guess_button.pack()

        self.reset_button = tk.Button(self.master, text="Сбросить", command=self.reset_game)
        self.reset_button.pack()
        
        self.hint_label = tk.Label(self.master, text="")
        self.hint_label.pack()

    def check_guess(self):
        if self.won:
            messagebox.showinfo("Игра окончена", "Вы уже нашли сокровище! Сбросьте игру, чтобы попробовать снова.")
            return
        
        try:
            x_guess = int(self.entry_x.get())
            y_guess = int(self.entry_y.get())
            
            if not (0 <= x_guess < self.grid_size and 0 <= y_guess < self.grid_size):
                raise ValueError("Координаты вне диапазона.")
            
            self.attempts += 1
            
            if (x_guess, y_guess) == self.hidden_treasure:
                self.won = True
                messagebox.showinfo("Поздравляем!", f"Вы нашли сокровище за {self.attempts} попыток!")
            else:
                distance = abs(x_guess - self.hidden_treasure[0]) + abs(y_guess - self.hidden_treasure[1])
                
                if distance == 1:
                    hint = "Горячо! Вы очень близко."
                else:
                    hint = "Холодно... попробуйте снова."
                
                self.hint_label.config(text=hint)
                
                if self.attempts >= self.max_attempts:
                    messagebox.showinfo("Конец игры", f"Вы исчерпали все попытки! Сокровище было в ({self.hidden_treasure[0]}, {self.hidden_treasure[1]}).")
                    self.won = True
        
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Пожалуйста, введите корректные координаты.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def reset_game(self):
        self.won = False
        self.hint_label.config(text="")
        self.initialize_game()


if __name__ == "__main__":
    root = tk.Tk()
    game = TreasureHunt(root)
    root.mainloop()