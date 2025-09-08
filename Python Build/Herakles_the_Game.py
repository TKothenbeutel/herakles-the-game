import tkinter as tk
import time
import random
import turtle

class FightLevel:
    def __init__(self, level_num:int, level:str, fight:list, items:list, specials:list, hp:list):
        self.level = level
        self.levelnum = level_num
        self.fightchoice = fight
        self.availitems = items
        self.availspecials = specials
        self.special_goal = False
        self.turn_num = 0
        self.herakles_start_hp = hp[1]
        self.enemy_start_hp = hp[0]
        self.enemy_attk = 0
        self.enemy_total_attk = 0
        self.herakles_attk = 0
        self.herakles_total_attk = 0        
        self.main_options(True, None) #Calls main_options
    
    def win_or_defeat(self):
        
        #Win!
        if self.herakles_total_attk == self.enemy_start_hp:
            self.imageframe.destroy()
            self.choiceframe.forget()
            self.top_screen()
            self.choiceframe.pack(fill='both', expand=True)
            self.textframe = tk.Frame(self.imageframe, borderwidth=5, relief='sunken')
            self.norun = tk.Label(self.textframe, text= 'You defeated '+self.level+'!').pack(side='bottom', fill='both')
            self.textframe.pack(fill='x', side='bottom')
            self.imageframe.update()
            time.sleep(2.4)
            self.master.destroy()
            if self.levelnum != 6:
                dialogue(self.levelnum + 0.5, True)
            else:
                win(self.levelnum)
        
        #Fully Win
        if self.turn_num == 666:
            self.imageframe.destroy()
            self.choiceframe.forget()
            self.top_screen()
            self.choiceframe.pack(fill='both', expand=True)
            self.textframe = tk.Frame(self.imageframe, borderwidth=5, relief='sunken')
            self.norun = tk.Label(self.textframe, text= 'You tamed Kerebos of the Underworld!').pack(side='bottom', fill='both')
            self.textframe.pack(fill='x', side='bottom')
            self.imageframe.update()
            time.sleep(2.4)
            self.master.destroy()
            fullywin(5, "Congratulations, You've completed all 12 labors!")
        
        #Dead :/
        if self.enemy_total_attk == self.herakles_start_hp:
            for widget in self.master.winfo_children():
                widget.destroy()
            loserframe = tk.Frame(self.master, bg="black")
            defeat = tk.PhotoImage(file='Defeat upper.png')
            tk.Label(loserframe, image=defeat,borderwidth=0).pack()
            tk.Label(loserframe, text=level_and_messages[self.level], bg="black", fg="white", font=('Palatino',20), wraplength=650, justify='center').pack()
            tk.Label(loserframe, text="Click to Retry", bg="black", fg="white").pack(padx=30,side='right')
            loserframe.pack(fill='both', expand=True)
            self.master.bind('<Button-1>',lambda x:[self.master.destroy(), dialogue(self.levelnum, False)])
            self.master.mainloop()

    def top_screen(self):
        '''Creates the upper portion of fight screens'''
        self.imageframe = tk.Frame(self.master, bg= '#001489')
        #Herakles' HP
        tk.Label(self.imageframe, width=25, height=3).place(x=25, y=100) #Herakles BG
        tk.Label(self.imageframe, text= 'Herakles').place(x=25, y=100) #Herakles name
        tk.Label(self.imageframe, width=150, bg='gray', font=('Palatino',1)).place(x=30, y=120) #Herakles HP BG
        herakles_bar = 150 - int(self.enemy_total_attk * (150 / self.herakles_start_hp))
        tk.Label(self.imageframe, width=herakles_bar, bg='green', font=('Palatino',1)).place(x=30, y=120) #Herakles HP
        tk.Label(self.imageframe, text= str(self.herakles_start_hp - self.enemy_total_attk)+'/'+str(self.herakles_start_hp)).place(x=35, y=130) #Herakles HP Num
        #Enemy's HP
        tk.Label(self.imageframe, width=25, height=3).place(x=500, y=25) #Enemy BG
        tk.Label(self.imageframe, text= self.level).place(x=500, y=25) #Enemy name
        tk.Label(self.imageframe, width=150, bg='gray', font=('Palatino',1)).place(x=505, y=45) #Enemy HP BG
        enemy_bar = 150 - int(self.herakles_total_attk * (150 / self.enemy_start_hp))
        tk.Label(self.imageframe, width=enemy_bar, bg='green', font=('Palatino',1)).place(x=505, y=45) #Enemy HP
        tk.Label(self.imageframe, text= str(self.enemy_start_hp - self.herakles_total_attk)+'/'+str(self.enemy_start_hp)).place(x=505, y=55) #Enemy HP Num
        #Display frame
        self.imageframe.pack(side='top', fill='both', expand=True)

    def main_options(self, isfirst, choice):
        """Main page of the screen. Shows the first options the user has, and calls functions to process what they choose"""
        if not isfirst:
            self.master.destroy() # close the current window
        self.master = tk.Tk() # create another Tk instance
        self.master.title(self.level)
        self.master.resizable(False, False)
        self.master.geometry("700x400+100+100")
        self.choiceframe = tk.Frame(self.master)
        self.choiceframe.grid_columnconfigure([0,1], uniform='equal', weight= 1)
        self.choiceframe.grid_rowconfigure([0,1], uniform='equal', weight= 1)
        self.top_screen()
        #Option Buttons
        tk.Button(self.choiceframe, text= 'Fight', bg= '#ff9999', borderwidth=5, command=lambda: self.next_options(self.fightchoice, '#ff9999')).grid(row= 0,column=0,sticky='nesw')
        tk.Button(self.choiceframe, text= 'Item', bg='#fff799', borderwidth=5, command=lambda: self.next_options(self.availitems, '#fff799')).grid(row=1, column=0, sticky='nesw')
        tk.Button(self.choiceframe, text= 'Special', bg='#99ff99', borderwidth=5, command=lambda: self.next_options(self.availspecials, '#99ff99')).grid(row=0, column=1, sticky='nesw')
        tk.Button(self.choiceframe, text= 'Flee', bg='#9999ff', borderwidth=5, command=lambda: self.battle_text(["That's not very heroic of you."])).grid(row=1, column=1, sticky='nesw')
        self.choiceframe.pack(fill='both', expand=True)
        #Call reaction function if it recieves something in the choice parameter
        if choice != None:
            self.reaction(choice)
        self.master.mainloop()
    
    def battle_text(self, result_text: list):
        """Displays text needed to show from the battle"""
        something_dead = False
        for i in range(len(result_text)):
            if result_text[0] != "That's not very heroic of you.":
                if i == 0:
                    self.herakles_total_attk += self.herakles_attk
                    #Don't let the total attack exceed the hp amounts
                    if self.herakles_total_attk >= self.enemy_start_hp:
                        self.herakles_total_attk = self.enemy_start_hp
                        something_dead = True
                    elif self.herakles_total_attk < 0:
                        self.enemy_start_hp += (self.herakles_total_attk * -1)
                        self.herakles_total_attk = 0
                elif result_text[i] == result_text[-1]:
                    self.enemy_total_attk += self.enemy_attk
                    #Don't let the total attack exceed the hp amounts
                    if self.enemy_total_attk >= self.herakles_start_hp:
                        self.enemy_total_attk = self.herakles_start_hp
                        something_dead = True
            self.imageframe.destroy()
            self.choiceframe.forget()
            self.top_screen()
            self.choiceframe.pack(fill='both', expand=True)
            self.textframe = tk.Frame(self.imageframe, borderwidth=5, relief='sunken')
            self.norun = tk.Label(self.textframe, text= result_text[i]).pack(side='bottom', fill='both')
            self.textframe.pack(fill='x', side='bottom')
            self.imageframe.update()
            if self.turn_num == 666:
                something_dead = True
            if result_text[i] == result_text[-1] and not something_dead:
                time.sleep(0.5)
                self.master.bind('<Button-1>',lambda x:self.destroy_text_frame())
            else:
                time.sleep(1.7)
                self.destroy_text_frame()
            if something_dead:
                self.win_or_defeat()
                break    
        
    def destroy_text_frame(self) -> None:
        '''Destroys the text from battle_text function, cause god forbid it could do this in the same function'''
        self.textframe.destroy()
        self.master.unbind('<Button-1>')
        self.master.update()

    def damage(self, enemy_range: list, weapon_range: list) -> None:
        """Calculates how much damage the enemy/herakles hits"""
        #If lion is shleeping, it cannot attack
        if self.special_goal and self.level == "The Nemean Lion":
            self.enemy_attk = 0
        else:
            #Picks how much damage enemy hits
            self.enemy_attk = random.randint(enemy_range[0], enemy_range[1])
        #Picks how much damage user hits
        self.herakles_attk = random.randint(weapon_range[0], weapon_range[1])
        
    def reaction(self, choice) -> None:
        """Decides what the outcome of the turn is based off of the level and what the user chose"""
        things_to_say = ['']
        #1. Lion
        if self.level == "The Nemean Lion":
            enemy_attack = [18, 23] #How much damage the lion can do
            if self.special_goal:
                things_to_say.append("The lion is asleep.")
                self.turn_num += 1
                if self.turn_num == 3:
                    self.special_goal = False
                    things_to_say.append("The lion has awoken.")
                    things_to_say.append("The lion used Scratch.")
                    self.turn_num = 0
            else:
                things_to_say.append("The lion used Scratch.")
            #How much damage Herakles can do
            if choice == "Club" and not self.special_goal:
                self.special_goal = True
                self.damage(enemy_attack, [5,10])
                things_to_say[0] = "You knocked the lion out."
                things_to_say[1] = "The lion is asleep."
            elif choice == "Club":
                things_to_say[0] = "The lion is already knocked out."
            elif choice == "Strangle" and self.special_goal:
                self.damage(enemy_attack, [35, 40])
                things_to_say[0] = "You strangled the knocked out lion."
            else:
                self.damage(enemy_attack, [0,0])
                things_to_say[0] = "It had no effect."
            self.battle_text(things_to_say)
            return
        #2. Hydra
        elif self.level == "The Lernaean Hydra":
            enemy_attack = [8,13]
            if type(self.turn_num) is int:
                self.turn_num = []
            if choice == "Sword":
                self.special_goal = True
                self.turn_num.append(0)
                self.damage(enemy_attack, [1,1])
                things_to_say[0] = "You cut one of the Hydra's head off."
            elif choice == "Torch" and self.special_goal:
                self.damage(enemy_attack, [0,0])
                if len(self.turn_num) == 1:
                    self.special_goal = False
                    things_to_say[0] = "You cauterized the Hydra's wound."
                else:
                    things_to_say[0] = "You cauterized one of the Hydra's wounds."
                del self.turn_num[0]
            else:
                self.damage(enemy_attack, [0,0])
                things_to_say[0] = "It had no effect."
            if self.special_goal:
                for i in range(len(self.turn_num)):
                    self.turn_num[i] += 1
                if self.turn_num[0] == 2:
                    if len(self.turn_num) == 1:
                        self.special_goal = False
                    del self.turn_num[0]
                    self.herakles_total_attk -= 2
                    things_to_say.append("The Hydra grew back two more heads.")
            things_to_say.append("The Hydra used Bite.")
            self.battle_text(things_to_say)
            return
        #9. Amazon Queen
        elif self.level == "The Belt of the Amazon Queen":
            enemy_attack = [20,25]
            if choice == "Sword":
                self.damage(enemy_attack, [35,40])
                things_to_say[0] = "You slashed the Amazon Queen with your sword."
            elif choice == "Bow":
                self.damage(enemy_attack, [30, 35])
                things_to_say[0] = "You shot the Amazon Queen with your bow."
            elif choice == "Strangle":
                self.damage(enemy_attack, [20,25])
                things_to_say[0] = "You attempted to strangle the Amazon Queen."
            else:
                self.damage(enemy_attack, [5,10])
                things_to_say[0] = "It's not very effective."
            things_to_say.append("The Amazon Queen used Quick Axe.")
            self.battle_text(things_to_say)
            return
        #10. Geryon
        elif self.level == "The 3-Bodied Geryon":
            enemy_attack = [30,35]
            if choice == "Sword":
                self.damage(enemy_attack, [30,35])
                things_to_say[0] = "You slashed Geryon with your sword."
            elif choice == "Bow":
                self.damage(enemy_attack, [35, 40])
                things_to_say[0] = "You shot Geryon with your bow."
            elif choice == "Strangle":
                self.damage(enemy_attack, [10,15])
                things_to_say[0] = "You attempted to strangle Geryon."
            else:
                self.damage(enemy_attack, [5,10])
                things_to_say[0] = "It's not very effective."
            things_to_say.append("Geryon used Triple Spear.")
            self.battle_text(things_to_say)
            return
        #12. Kerberos
        elif self.level == "Kerberos":
            enemy_attack = [150,150]
            if choice == "Cloak Self":
                if not self.special_goal:
                    self.damage([0,0], [0,0])
                    things_to_say[0] = "You lathered your hand with raw beef."
                    self.special_goal = True
                    things_to_say.append("Kerberos started licking your hand!")
                else:
                    self.damage(enemy_attack, [0,0])
                    things_to_say[0] = "You've already used up all the raw beef."
                    self.turn_num = 1
            elif choice == "Chain" and self.special_goal:
                self.damage([0,0], [0,0])
                self.turn_num = 666
                things_to_say[0] = "You wrapped the chain around Kerberos' neck like a leash."
            else:
                if self.special_goal:
                    self.turn_num = 1
                self.damage(enemy_attack, [35,40])
                things_to_say[0] = "It's not very effective."
            if self.turn_num == 1:
                things_to_say.append("Kerberos finished licking your hand.")
                self.special_goal = False
            if not self.special_goal:
                things_to_say.append("Kerberos used Crunch.")
            self.battle_text(things_to_say)
            return
        else:
            print('uhhhh error')
            print(self.levelnum)
            return None

    def next_options(self, choices, color):
        """Displays a new window with options directed from the main_options window"""
        #Create window
        self.master.destroy() # close the current window
        self.master = tk.Tk() # create another Tk instance
        self.master.resizable(False, False)
        self.master.title(self.level)
        self.master.geometry("700x400+100+100") #Sets window size
        self.top_screen() #Runs tops window
        #Create frame
        self.choiceframe = tk.Frame(self.master)
        self.choiceframe.grid_columnconfigure([0,1], uniform='equal', weight= 1) #Allows the buttons to expand
        self.choiceframe.grid_rowconfigure([0,1], uniform='equal', weight= 1)
        #Button choices
        for i in range(len(choices)):
            newbut = tk.Button(self.choiceframe, text = choices[i], borderwidth=5, bg=color)
            #Sets the parameter of command fucntion called to None if the button is empty
            if choices[i] != '':
                newbut['command'] = lambda i=i: self.main_options(False, choices[i])
            else:
                newbut['borderwidth'] = 0
                #newbut['command'] = lambda: self.main_options(False, None)
                newbut['command'] = lambda: self.win_or_defeat()
            #No easier way I know of :/
            if i == 0:
                newbut.grid(row=0, column=0, sticky='nesw')
            elif i == 1:
                newbut.grid(row=0, column=1, sticky='nesw')
            elif i == 2:
                newbut.grid(row=1, column=0, sticky='nesw')
            else:
                newbut.grid(row=1, column=1, sticky='nesw')
        self.choiceframe.pack(fill='both', expand=True)
        #Back Button
        tk.Button(self.master, text= 'Back',height= 2, command= lambda: self.main_options(False, None)).pack(fill='both')

class ChaseLevel:
    def __init__(self, level: int, cpuspeed: int) -> None:
        self.level_num = level
        self.screen = turtle.Screen()
        self.screen.setup(width=700, height=400, startx=100, starty=100)
        self.num_defeated = 0
        self.herakles = turtle.Turtle()
        self.cpu = turtle.Turtle()
        #Set up turtles
        self.herakles.speed(0)
        self.herakles.penup()
        self.herakles.goto(-300,100) #-300 100
        self.herakles.shape("circle")
        self.herakles.color('orange')
        self.cpu.speed(0)
        self.cpu.penup()
        self.cpu_speed = cpuspeed
        self.cpu.shape("turtle")
        self.cpu.color('blue')
        #Info storage
        
        self.main()

    def move(self):
        """Moves both herakles and the computer and controls the speed of the game"""
        self.herakles.forward(5)
        if self.cpu.distance(self.herakles) <= 150:
            if random.randint(1,8) == 8:
                self.cpu.left(random.randint(5,40))
            if random.randint(1,8) == 8:
                self.cpu.right(random.randint(5,40))
            self.cpu.forward(self.cpu_speed + 3)
        else:
            if random.randint(1,4) == 4:
                self.cpu.left(random.randint(5,40))
            self.cpu.forward(self.cpu_speed)
        self.screen.ontimer(self.collision, 100)

    def collision(self):
        heraklesX = self.herakles.xcor()
        heraklesY = self.herakles.ycor()
        cpuX = self.cpu.xcor()
        cpuY = self.cpu.ycor()
        #Check herakles hits a wall
        if heraklesY >= 185: #Up
            self.herakles.goto(heraklesX, 185)
        elif heraklesX <= -335: #Left
            self.herakles.goto(-335, heraklesY)
        elif heraklesX >= 327: #Right
            self.herakles.goto(327, heraklesY)
        elif heraklesY <= -175: #Down
            self.herakles.goto(heraklesX, -175)
        #Check if computer hits walls
        if cpuY >= 185: #Up
            self.cpu.goto(cpuX, 185)
            self.cpu.setheading(270)
        elif cpuX <= -335: #Left
            self.cpu.goto(-335, cpuY)
            self.cpu.setheading(0)
        elif cpuX >= 327: #Right
            self.cpu.goto(327, cpuY)
            self.cpu.setheading(180)
        elif cpuY <= -175: #Down
            self.cpu.goto(cpuX, -175)
            self.cpu.setheading(90)
        #Check if they are touching
        if heraklesX >= cpuX-15 and heraklesX <= cpuX+15 and heraklesY >= cpuY-15 and heraklesY <= cpuY+15:
            self.num_defeated += 1
            self.caught()
        else:
            self.move()  

    def main(self):
        self.screen.onkey(lambda: self.herakles.setheading(90), 'Up')
        self.screen.onkey(lambda: self.herakles.setheading(180), 'Left')
        self.screen.onkey(lambda: self.herakles.setheading(0), 'Right')
        self.screen.onkey(lambda: self.herakles.setheading(270), 'Down')
        self.screen.listen()
        self.move()
        self.screen.mainloop()

    def caught(self):
        if self.level_num == 2 and self.num_defeated == 1:
            self.cpu.hideturtle()
            self.cpu.goto (self.herakles.xcor() * -1, self.herakles.ycor() * -1)
            self.cpu_speed = 6
            self.cpu.color('red')
            self.cpu.showturtle()
            self.main()
        else:
            self.screen.bye()
            win(self.level_num)

def multipleChoice(level_num: int, level: str, correct_answer: int, question: str, answers: list):
    """Displays multiple choice question"""
    master = tk.Tk() # create another Tk instance
    master.title(level)
    master.resizable(False, False)
    master.geometry("700x400+100+100")
    questionframe = tk.Frame(master, bg= '#224f22')
    tk.Label(questionframe, bg= '#224f22', fg= 'white', font=('Palatino', 30), text=question, wraplength=650, justify='center').place(relx=0.5, rely=0.5, anchor='center')
    choiceframe = tk.Frame(master)
    choiceframe.grid_columnconfigure([0,1], uniform='equal', weight= 1)
    choiceframe.grid_rowconfigure([0,1], uniform='equal', weight= 1)
    #Option Buttons
    for i in range(4):
        newbut = tk.Button(choiceframe,font=('Palatino', 15), wraplength=300, justify='center', borderwidth=5, text=answers[i], command=lambda i=i: checkAnswer(level_num, i, correct_answer, master))
        #No easier way I know of :/
        if i == 0:
            newbut.grid(row=0, column=0, sticky='nesw')
        elif i == 1:
            newbut.grid(row=0, column=1, sticky='nesw')
        elif i == 2:
            newbut.grid(row=1, column=0, sticky='nesw')
        else:
            newbut.grid(row=1, column=1, sticky='nesw')
    questionframe.pack(side='top', fill='both', expand=True)
    choiceframe.pack(fill='both', expand=True)

def checkAnswer(level_num, choice: int, answer: int, window):
    """Checks if multiple choice question"""
    if choice == answer:
        window.destroy()
        return win(level_num)
    else:
        for widget in window.winfo_children():
            widget.destroy()
        loserframe = tk.Frame(window, bg="black")
        defeat = tk.PhotoImage(file='Defeat upper.png')
        tk.Label(loserframe, image=defeat,borderwidth=0).pack()
        tk.Label(loserframe, text="Click to Retry", bg="black", fg="white").pack(padx=30,side='right')
        loserframe.pack(fill='both', expand=True)
        window.bind('<Button-1>',lambda x: [window.destroy(), dialogue(level_num, False)])
        window.mainloop()
    
def selection_screen():
    master = tk.Tk()
    master.geometry("700x400+100+100")
    master.resizable(False, False)
    master.grid_columnconfigure([0,1,2], uniform='equal', weight=1)
    master.grid_rowconfigure([0,1,2,3], uniform='equal', weight=1)
    master['bg'] = '#001489'
    tk.Label(master, text="Select Level", anchor='center', font=('Palatino', 30)).grid(row=0, columnspan=4)
    for i in range(9):
        level_butt = tk.Button(master, text=i+1, font=('Palatino', 20), borderwidth=5, command=lambda i=i: [master.destroy(), dialogue(i, False)])
        if i < 3:
            level_butt.grid(row=1, column=i, sticky='nesw', padx=15, pady=15)
        elif i < 6:
            level_butt.grid(row=2, column=(i-3), sticky='nesw', padx=15, pady=15)
        else:
            level_butt.grid(row=3, column=(i - 6), sticky='nesw', padx=15, pady=15)
    master.mainloop()

def levels(num, win):
    #deletes past tkinter window
    if win != None:
        win.destroy()
    level_decompiled = level_compiled[num]
    if num <= 1 or num >= 6:
        FightLevel(num, level_decompiled[0],level_decompiled[1],level_decompiled[2],level_decompiled[3],level_decompiled[4])
    elif num == 2 or num == 5:
        ChaseLevel(num, level_decompiled[1])
    elif num == 3 or num == 4:
        multipleChoice(num, level_decompiled[0],level_decompiled[1],level_decompiled[2],level_decompiled[3])

def dialogue(level_num: int, completed: bool):
    """Displays the text before and after each challenge"""
    master = tk.Tk()
    master.title('Epilogue')
    master.resizable(False, False)
    master.geometry("700x440+100+100")
    master['bg'] = 'white'
    tk.Label(master, bg= '#001489', fg= 'white', font=('Palatino', 16), text=story_text[level_num],
    wraplength=650, justify='center').place(relx=0.5, rely=0.5, anchor='center')
    master.bind('<Button-1>',lambda x: master.destroy())
    master.mainloop()
    #Decides what to do next
    if level_num == 0 or level_num == 2 or level_num == 6 or level_num == 8: #Two parter intros
        return dialogue(level_num + 0.25, False)
    if completed: #For those that appear after challenge is completed (all have 0.5)
        return win(level_num - 0.5) #Go to win screen!
    elif level_num == 0.25 or level_num == 2.25 or level_num == 6.25 or level_num == 8.25: #Outlier two parters
        return levels(level_num - 0.25, None)
    else: #Rest are level starter stuff, and will go to the level function
        return levels(level_num, None)

def win(level_num: int):
    """Displays the win screen"""
    win_screen = tk.Tk()
    win_screen.title('Win!')
    win_screen.resizable(False, False)
    win_screen.geometry("700x440+100+100")
    win_screen['bg'] = '#ff7d3c'
    confetimg = tk.PhotoImage(file='Win Screen.png')
    tk.Label(win_screen,image=confetimg).pack()
    tk.Button(win_screen, text='Advance to next level',borderwidth= 5, command=lambda: [win_screen.destroy(), dialogue(level_num + 1, False)]).pack(side='right', padx= 10)
    tk.Button(win_screen, text='Retry level',borderwidth= 5, command=lambda: [win_screen.destroy(), dialogue(level_num, False)]).pack(side='left', padx=40)
    tk.Button(win_screen, text='Level selection',borderwidth= 5, command=lambda:[win_screen.destroy(),selection_screen()]).pack()
    win_screen.mainloop()

def fullywin(stopper: int, message: str):
    """Displays the epilogue and the epic win screen B)"""
    epilogue = tk.Tk()
    epilogue.title('Epilogue')
    epilogue.resizable(False, False)
    epilogue.geometry("700x440+100+100")
    epilogue['bg'] = 'white'
    tk.Label(epilogue, bg= '#001489', fg= 'white', font=('Palatino', 20),
    text='After completing the twelve labors, Herakles ends up winning a wife, losing said wife for being a family killer, murdering Iphitos, becoming a slave for three years, and marrying Deianeira. Things went South when he killed the ferryman who tried to pull a fast one with his wife, for the ferryman, a centaur, told Deianeira to make a garment for Herakles using his blood to make him love her. Later on, she makes a golden robe for him, not knowing that the blood was laced with the poison Herakles acquired from the hydra and used with his arrows. This caused him to slowly die, and at last, he threw himself on a funeral pyre, leaving his mortal self for hades and his divine self for Olympus.',
    wraplength=650, justify='center').place(relx=0.5, rely=0.5, anchor='center')
    epilogue.bind('<Button-1>',lambda x: epilogue.destroy())
    epilogue.mainloop()
    winwin = tk.Tk()
    frame_count = 59
    frames = [tk.PhotoImage(file='confetti-59.gif', format= 'gif -index %i' %(i)) for i in range(frame_count)]
    framee = tk.Frame(winwin)
    tk.Label(framee, image=frames[0]).pack()
    tk.Label(framee, text=message, font=('Arial',10)).pack()
    framee.pack()
    index = 0
    while stopper > 0:
        index += 1
        if index == frame_count:
            index = 0
            stopper -= 1
        framee.forget()
        framee = tk.Frame(winwin)
        tk.Label(framee, image=frames[index]).pack()
        tk.Label(framee, text=message, font=('Arial',10)).pack(anchor='center')
        framee.pack()
        winwin.after(70, winwin.update())
    winwin.mainloop()

#Fight options
fight_choices = ['Bow', 'Strangle', 'Sword', 'Club']
item_choices_empty = ['', '', '', '']
item_choices_kerberos = ['Chain', '', '', '']
special_choices_empty = ['', '', '', '']
special_choices_hydra = ['Torch', '', '', '']
special_choices_kerberos = ['Torch', 'Cloak Self', '', '']
hps = [[40,60],[3,80],'','','','',[120,100],[150,120],[1000,150]]
speed_and_answers = [0,0,4,1,3,7]
questions = ['','','',"The Augean Stables has never been cleaned before!\nWhat will you do?","How will you scare the birds?"]
choices = ['','','',["Clean the stables","Reroute the nearby rivers","Kill all the cows","Refuse"],["Shake the tree","Yell at them","Use your club","Use bronze castanets"]]
#Levels
game_levels = ["The Nemean Lion", "The Lernaean Hydra", "Ceryneian Hind and Erymanthian Boar", 'The Augean Stables', 'The Stymphalian Birds', 'The Cretan Bull', "The Belt of the Amazon Queen", "The 3-Bodied Geryon", "Kerberos"]
defeat_messages = ["Tip: The Lion's hide is said to be ipenetrable. Maybe don't use moves that penetrate enemies",
"Tip: The Hydra grows two heads every time a head is cut off. Maybe there's a way to prevent the wound from regenerating","","","","","","","Kerberos seems too powerful to be killed, maybe there's another way to win."]
level_and_messages = {}
#Match the game levels with the death messages
for i in range(len(game_levels)):
    level_and_messages[game_levels[i]] = defeat_messages[i]
#Compile all varaibles regarding levels into dictionary (minus defeat message)
level_compiled = {}
for i in range(len(game_levels)):
    together = []
    together.append(game_levels[i])
    #Fight levels only
    if i <= 1 or i >= 6:
        together.append(fight_choices)
        if i == 8:
            together.append(item_choices_kerberos)
        else:
            together.append(item_choices_empty)
        if i == 8:
            together.append(special_choices_kerberos)
        elif i >= 1:
            together.append(special_choices_hydra)
        else:
            together.append(special_choices_empty)
        together.append(hps[i])
    #Chase levels
    if i >= 2 and i <= 5:
        together.append(speed_and_answers[i])
        if i == 3 or i == 4:
            together.append(questions[i])
            together.append(choices[i])
    level_compiled[i] = together

#All dialogue text
"""
0: intro,0.25:lion, 0.5: lion(completed) 1: hydra, 1.5: hydra(completed) 2:deer,2.25:boar, 3: stables, 4: birds,
5: bull, 6: mares,6.25: amazon queen, 7: geryon, 7.5: geryon(completed) 8:apples,8.25:Kerberos
"""
story_text = {
    0: "Herakles grew up as a man of great strength. He first became known to others when he killed his lyre teacher, Linos, because he is hot-tempered. His parents then sent him to live on a cattle ranch to avoid another incident. He became even more known after he volunteered to kill a lion terrorizing the cattle every night. From the lion, he skinned it and used the pelt and head as a cloak and helmet, giving him a beastly appearance from afar. His next act was helping Thebes with a war over cattle. For aiding their cause, Kreon gave Herakles Megara, his daughter. They then had three children together and lived a happy life, but not for long. Hera, taking revenge on Zeus for sleeping with Herakles' mother (which produced Herakles), put Herakles under a fit of madness and caused him to burn his wife, children, and his brother and his children. He went into exile voluntarily, until he made it to Delphi, where an oracle told him to complete twelve years of labor, led by Eurystheus, to become immortal.",
    0.25 : "Your first task is to kill another lion, this time terrorizing Nemea, an area of northern Peloponnese. It is said to have an impenetrable hide.",
    0.5: "After defeating the lion, you proceed to use its claws to skin it and wear it as a new cloak.",
    1 : "Your second task is to kill the Hydra that had claimed a swamp. Normally the Hydra has nine heads, but when you arrived it fortunately only had three, saving you time. You also have your nephew, Iolaos, with you, meaning you now know the move Torch (which can be found in the Special tab).",
    1.5: "After defeating the Hydra and giant crab sent by Hera, you place the last Hydra head under a large and heavy rock, as to keep the immortal head from regenerating. You also dipped some of your arrows in its blood, which would be used after the labors.",
    2 : "Your third and fourth task is to capture two wild animals. The first of the two is the Ceryneian deer, the goddess Artemis' animal of choice that draws her chariot. One of them fled the chariot one way or another and needs to be retrieved.",
    2.25: "The second animal is the Erymanthian boar, an enormous boar living near Mt. Erymanthos. Don't ask why they're shaped like turtles. Use the arrow keys to move yourself (the orange ball of power)!",
    3 : "Your fifth labor requires, well, labor. Your task is to clean Augeas' cow barn. This barn, housed in Elis (West of the Peloponnese) houses a thousand cattle, and not once had anybody ever cleaned it.",
    4 : "You're halfway through your task! This sixth one involves birds, hundreds of them. You must find a way to shoo off the birds found at the lake of Stmphalia. Be careful though, as there are rumors that these birds can shoot their feathers at others like arrows.",
    5 : "Since you completed all known dangers in the Peloponnese region, you must travel to Crete for this task, and capture the bull that Minos saved after substituting it for a smaller sacrifice. Be careful for this one is faster than the other two animals you've caught (though still turtle shaped).",
    6: "Your eighth task is to squelch the mares of the Thracian king, who had a habit of eating people. To complete this task, you fed the king to the mares, making them quite satisfied with their meal. Then, you released them to the foothills near Mycenae, where they were slain by predators.",
    6.25 : "Your ninth labor involves the royal belt of Hippolyte. This belt is cherished by the Amazon tribe, as it was a gift from the god Ares. Nevertheless, the Amazon Queen agreed to lend the belt to you, until Hera interfered. Hera created a rumor that you and Theseus were there to abduct the queen, and now your only option left is to kill the Amazon Queen.",
    7 : "Your tenth task is to take Geryon's deep red cattle. For this task, you traveled to Erytheia, crossing the ocean with the golden goblet the Sun uses to float back East after the day. Upon arrival, you are faced with three enemies. First, Geryon's dog, Orthos, who has two heads. Next, is Geryon's herdsman, Eurytion, who looks quite like a regular person. The final obstacle is Geryon himself, who has three bodies united at the waist. After defeating Orthos and Eurytion, you are left with only Geryon...",
    7.5: "After defeating Geryon, you herd the cattle onto the golden goblet and sail back to the mainland. You also set up a pillar before leaving to commemorate the farthest a mortal has ever traveled.",
    8: "Your eleventh labor is a long one, so I'll save you the trouble by summarizing it. Your task was to collect the Golden Apples of Hesperides, which was a wedding gift from Earth to Hera. After wrestling the Old Man of the Sea, Nereus, you traveled to Hyperboreans, which was beyond the North Winds. Along the way, you defeated the tyrant of Libya, Antaeus, in a wrestling match. Next, you avoided being sacrificed in Egypt by using the lion pelt's claws to break free from the ropes they bound you up with. Later, you made it to the Caucasus and freed Prometheus from his punishment. He told you to ask his brother Atlas for his help to retrieve the apples, for a dragon-snake guarded them and was much fiercer than anything you've encountered. Once you made it to Hyperborean, asked Atlas to help you out. He was delighted to help, for that meant he got a break from holding the Earth on his shoulders. After retrieving the apples, Atlas pleaded to explore more, but you tricked him to get back into holding the Earth as you didn't trust his word to return.",
    8.25 : "Finally, your twelfth and final labor! This task requires you to travel to Hell and retrieve Kerberos, a fearsome dog with three heads. This giant dog keeps the dead from leaving the Underworld. It would be futile to try and fight it, so maybe there's another way to retrieve it. Here is a chain (found in the Items tab), and a new move, allowing you to cloak yourself (found in the Special tab). Good luck."
}

def title_screen():
    title_screen = tk.Tk()
    title_screen.title('Title Screen')
    title_screen.resizable(False, False)
    title_screen.geometry("700x400+100+100")
    backg = tk.PhotoImage(file='Title Screen.png')
    img = tk.Label(title_screen, image=backg).pack()
    title_screen.bind('<Button-1>',lambda x: [title_screen.destroy(), selection_screen()])
    title_screen.mainloop()


#Start up the bad boy
title_screen()
