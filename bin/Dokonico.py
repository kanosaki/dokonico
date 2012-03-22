
import tkinter as tk
import os

MAIN_SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), "main.py"))

class ExecContext:
	def sync(self):
		os.system("python {} --from-gui sync".format(MAIN_SCRIPT))
		
	def show(self):
		os.system("python {} --from-gui show".format(MAIN_SCRIPT))
	
contex = ExecContext()

class Frame(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master, width=400, height=300)
		self.master.title('Dokonico')

		commands = [ ("Sync", contex.sync), ("Show", contex.show) ]
		for (tex, com) in commands:
			btn = tk.Button(self, text=tex, command=com, width=10)
			btn.pack(side=tk.LEFT)

if __name__ == '__main__':
    f = Frame()
    f.pack()
    f.mainloop()

