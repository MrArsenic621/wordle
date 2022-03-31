from tkinter import *
from tkinter import messagebox
from dictionary import Word

colors = {
    'red':'#ff4f5f',
    'green': '#6aaa64',
    'darkendGreen': '#538d4e',# correct
    'yellow': '#c9b458',
    'darkendYellow': '#b59f3b',#wrong place word
    'lightGray': '#d8d8d8',
    'gray': '#86888a',#unknown state word
    'darkGray': '#939598',
    'white': '#fff',#text color
    'shadowblack': '#212121',#wrong word
    'orange': '#f5793a',
    'blue': '#85c0f9',
    'black': "#000"
}

class UI(Tk):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_window()
        self.create_container()
        self.create_board(6,5)
        self.statusbar(False)
        self.new_random_word()
        self.create_keyboard()
        self.game_state = 'Playing'

    def config_window(self):
        self.title('Wordle')
        self.geometry("900x700")
        self.resizable(width=True, height=True)
        self.configure(bg=colors['black'])

    def create_container(self):
        # header
        self.header = Frame(self, width=400, height=50, bg=colors['black'])
        self.header.pack(side=TOP)
        self.header.pack_propagate(0)
        # main frames
        self.frames =[
            Frame(self, width=350, height=50, bg=colors['black']),
            Frame(self, width=350, height=50, bg=colors['black']),
            Frame(self, width=350, height=50, bg=colors['black']),
            Frame(self, width=350, height=50, bg=colors['black']),
            Frame(self, width=350, height=50, bg=colors['black']),
            Frame(self, width=350, height=50, bg=colors['black']),
            Frame(self, width=350, height=100, bg=colors['black']),
            Frame(self, width=700, height=50, bg=colors['black']),
            Frame(self, width=630, height=50, bg=colors['black']),
            Frame(self, width=700, height=50, bg=colors['black']),
        ]
        for frame in self.frames:
            frame.pack(side=TOP)
            frame.pack_propagate(0)
        
        self.status = [
                Label(self.frames[6], text='', bg=colors['white'], font=('Times New Roman', 20)),
                Button(self.frames[6], text="Play Again!", width=10,
                    command=self.restart_game)
            ]

    def create_board(self,row_count,char_count):
        self.row_count = row_count
        self.char_count = char_count
        self.rows = []
        for i in range(row_count):
            row = []
            for _ in range(char_count):
                row.append(
                            Button(  
                                    self.frames[i], text="", width=2,
                                    highlightbackground=colors['black'],
                                    disabledforeground=colors['white'],
                                    bg=colors['black'], state=DISABLED,
                                    borderwidth=3, font=('Times New Roman', 20)
                                  )
                          )
                    
            self.rows.append(row)
        for row in self.rows:
            for button in row:
                button.pack(side=LEFT, padx=5, pady=5)

    def statusbar(self,show_statusbar,msg='',color=colors['white']):
        
        if show_statusbar:
            self.status = [
                Label(self.frames[6], text=msg, bg=color, font=('Times New Roman', 20)),
                Button(self.frames[6], text="Play Again!", width=10,
                    command=self.restart_game)
            ]
            self.status[0].pack(side=LEFT, padx=5, pady=5)
            self.status[1].pack(side=RIGHT, padx=5, pady=5)
        else:
            self.status[0].pack_forget()
            self.status[1].pack_forget()

    def restart_game(self):
        self.new_random_word()
        self.clear_screen()
        self.statusbar(show_statusbar=False)
        self.game_state = 'Playing'

    def new_random_word(self):
        self.word = Word.random_word()

    def create_keyboard(self):
     
        self.position = {
            'row' : 1,
            'item' : 1,
        }
        self.state_colors={
            'T':colors['darkendGreen'],
            'P':colors['darkendYellow'],
            'F':colors['shadowblack'],
            'U':colors['gray'],
        }

        # keyboard layout
        keyboard_layout = [
            'Q,W,E,R,T,Y,U,I,O,P'.split(','),
            'A,S,D,F,G,H,J,K,L'.split(','),
            'Enter,Z,X,C,V,B,N,M,Back'.split(',')
        ]

        self.keyboard = {}
        for i,row in enumerate(keyboard_layout):
            for key in row:
                self.keyboard[key] = Button(
                                self.frames[7+i], text=key,borderwidth=3,
                                width=2 if key not in ['Enter','Back'] else 5,
                                font=('Times New Roman',20), bg=colors['gray'], fg=colors['white'],
                                activebackground=colors['gray'], activeforeground=colors['white'],
                                command=lambda pressed_key=key :self.keyboard_action(pressed_key))
        for key in self.keyboard:
            self.keyboard[key].pack(side=LEFT, padx=5, pady=5)

    def game_over(self):
        if self.game_state == 'Win':
            self.statusbar(show_statusbar=True,msg='You Win!',color=colors['green'])
        elif self.game_state == 'Lose':
            self.statusbar(show_statusbar=True,msg=f'The word was:{self.word}',color=colors['red'])
            
    def get_row_text(self):
        guess = ''
        for btn in self.rows[self.position['row'] - 1]:
            guess +=btn['text']
        return guess

    def clear_row(self,msg_type=None,msg=None):
        
        if msg_type and msg:
            msg_types = {
                'error': messagebox.showerror,
                'info': messagebox.showinfo,
                'warning': messagebox.showwarning,
            }
            msg_types[msg_type](msg_type,msg)
            self.clear_row()

        else:
            for btn in self.rows[self.position['row']-1]:
                btn['text'] = ''
            self.position['item'] = 1

    def clear_board(self):
        for i in range(self.row_count):
            for btn in self.rows[i]:
                btn['text'] = ''
                btn['bg']= colors['black']
    
    def clear_keyboard(self):
        for key in self.keyboard:
            self.keyboard[key]['bg']=self.state_colors['U']
    
    def clear_positions(self):
        self.position = {
            'row' : 1,
            'item' : 1,
        }

    def clear_screen(self):
        self.clear_board()
        self.clear_keyboard()
        self.clear_positions()

    def update_board_colors(self, result):
        for i,c in enumerate(result):
            self.rows[self.position['row']-1][i]['bg'] = self.state_colors[c]
            self.position['item'] = 1
        self.position['row'] +=1

    def update_keyboard_colors(self, guess, result):
        for i in range(5):
            current_key_color = self.keyboard[guess[i]]['bg']

            if current_key_color == self.state_colors['F'] or current_key_color == self.state_colors['U']:
                self.keyboard[guess[i]]['bg'] = self.state_colors[result[i]]
            elif current_key_color == self.state_colors['P']:
                if result[i] != 'F':
                    self.keyboard[guess[i]]['bg'] = self.state_colors[result[i]]

    def keyboard_action(self,key):
        if self.position['row'] <= self.row_count and self.game_state == 'Playing':
            if key == 'Enter':
                if self.position['item'] == self.char_count + 1:
                    guess = self.get_row_text()               
                    result = Word.check_compatibility(guess.lower(), self.word)
                    if result:
                        self.update_board_colors(result)
                        self.update_keyboard_colors(guess, result)
                    else:
                        self.clear_row('error', 'not a real word')
                    if result == 'TTTTT':
                        self.game_state = 'Win'
                        self.game_over()
                    if self.position['row'] > self.row_count and self.game_state != 'Win':
                        self.game_state = 'Lose'
                        self.game_over()


                    
                        
                else:
                    messagebox.showerror('error',"not a valid word")
            elif key == 'Back':
                if self.position['item'] > 1:
                    self.position['item'] -= 1
                    self.rows[self.position['row']-1][self.position['item']-1]['text'] = ''                    
            else:
                if self.position['item']<=self.char_count:
                    self.rows[self.position['row']-1][self.position['item']-1]['text'] = key
                    self.position['item']+=1
        

        


class Wordle():
    def __init__(self,user_interface):
        self.user_interface = user_interface
        self.user_interface.mainloop()
    


    
   
    


if __name__ == '__main__':
    ui = UI()
    app = Wordle(ui)
    