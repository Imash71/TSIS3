import tkinter as tk
import random
import json
import os
WIDTH = 500
HEIGHT = 700
root = tk.Tk()
root.title("TSIS 3 Racer Game")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="gray")
canvas.pack()
# ---------------- GAME STATE ----------------
player_x = WIDTH // 2
player_y = HEIGHT - 100
score = 0
distance = 0
coins = []
obstacles = []
game_over = False

# ---------------- SETTINGS ----------------
settings = {
   "difficulty": "normal"
}
if os.path.exists("settings.json"):
   with open("settings.json", "r") as f:
       settings = json.load(f)

# ---------------- DRAW ROAD ----------------
road_offset = 0
def draw_road():
   global road_offset
   canvas.create_rectangle(150, 0, 350, HEIGHT, fill="black")
   for i in range(0, HEIGHT, 40):
       y = (i + road_offset) % HEIGHT
       canvas.create_line(250, y, 250, y + 20, fill="white", width=2)
   road_offset += 10

# ---------------- DRAW PLAYER (CAR) ----------------
def draw_player():
   x = player_x
   y = player_y
   # body
   canvas.create_rectangle(x - 18, y - 30, x + 18, y + 30, fill="blue", outline="black")
   # window
   canvas.create_rectangle(x - 12, y - 20, x + 12, y - 5, fill="lightblue")
   # wheels
   canvas.create_oval(x - 22, y + 20, x - 12, y + 30, fill="black")
   canvas.create_oval(x + 12, y + 20, x + 22, y + 30, fill="black")

# ---------------- SPAWN ----------------
def spawn_coin():
   x = random.randint(180, 320)
   coins.append([x, 0])

def spawn_obstacle():
   x = random.randint(180, 320)
   obstacles.append([x, 0])

# ---------------- SAVE LEADERBOARD ----------------
def save_score():
   name = input("Enter name: ")
   data = []
   if os.path.exists("leaderboard.json"):
       with open("leaderboard.json", "r") as f:
           data = json.load(f)
   data.append({
       "name": name,
       "score": score,
       "distance": distance
   })
   data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]
   with open("leaderboard.json", "w") as f:
       json.dump(data, f)

# ---------------- UPDATE GAME ----------------
def update():
   global player_x, score, distance, game_over
   if game_over:
       return
   canvas.delete("all")
   draw_road()
   # spawn logic
   if random.randint(1, 35) == 1:
       spawn_coin()
   if random.randint(1, 50) == 1:
       spawn_obstacle()
   # coins
   for c in coins[:]:
       c[1] += 6
       canvas.create_oval(c[0], c[1], c[0]+15, c[1]+15, fill="gold")
       # collision
       if abs(c[0] - player_x) < 20 and abs(c[1] - player_y) < 20:
           score += 10
           coins.remove(c)
   # obstacles
   for o in obstacles[:]:
       o[1] += 7
       canvas.create_rectangle(o[0], o[1], o[0]+20, o[1]+20, fill="red")
       # collision
       if abs(o[0] - player_x) < 20 and abs(o[1] - player_y) < 20:
           game_over = True
           save_score()
           canvas.create_text(250, 350, text="GAME OVER", fill="white", font=("Arial", 30))
           return
   # cleanup
   coins[:] = [c for c in coins if c[1] < HEIGHT]
   obstacles[:] = [o for o in obstacles if o[1] < HEIGHT]
   draw_player()
   distance += 1
   # UI
   canvas.create_text(80, 20, text=f"Score: {score}", fill="white", font=("Arial", 16))
   canvas.create_text(380, 20, text=f"Distance: {distance}", fill="white", font=("Arial", 16))
   root.after(50, update)

# ---------------- CONTROLS ----------------
def left(event):
   global player_x
   if player_x > 180:
       player_x -= 20

def right(event):
   global player_x
   if player_x < 320:
       player_x += 20

root.bind("<Left>", left)
root.bind("<Right>", right)
update()
root.mainloop()