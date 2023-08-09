from tkinter import *

#info variable setup:
#   index 0 - object
#   index 1-4: scaling dots
#   index 5-8: Anchor dots
#   index 9-end: arrow connections


#width x height of all objects
DIAMOND_SIZE = [300,200]

CIRCLE_SIZE = [300,200]

RECTANGLE_SIZE = [300,200]

PARALLELOGRAM_SIZE = [300,200]
PARALLELOGRAM_ANGLE = 45

ARROW_SIZE = 300
ARROW_WIDTH = 30

DOT_SIZE = 10

COLOR = "#666666"
BASE_COLOR = "#663300"

last_clicked = None
show_anchors = False

first_anchor = None
first_coords = None
first_anchor_coords = None
first_anchor_orient = None
first_object_hitbox = None
first_object_info = None

second_anchor = None
second_coords = None
second_anchor_coords = None
second_anchor_orient = None
second_object_hitbox = None
second_object_info = None

#instating the window
window = Tk()
window.title("Flowchart Maker")
#window.attributes("-fullscreen",True)
#instating the canvas that fills the whole window even when expanded
canvas = Canvas(window,bg="#000000")
canvas.pack(fill="both", expand=True)

def anchor_mode():
    global show_anchors
    if show_anchors:
        show_anchors = False
        canvas.itemconfig("anchor",state="hidden")
        anchor_button.config(text="Arrow Mode: OFF")
    else:
        show_anchors = True
        canvas.itemconfig("anchor",state="normal")
        anchor_button.config(text="Arrow Mode: ON")

anchor_button = Button(canvas,highlightbackground="#CCCCAA",text="Arrow Mode: OFF",font=("Noteworthy",25),command=anchor_mode,fg=BASE_COLOR,padx=5,pady=5,relief=GROOVE,bd=4)
anchor_button.pack(side=BOTTOM)


#CREATION OF CLASSES

#click function: this basically just finds the place that the user clicked inside the object
#without this the program wouldn't be able to find the distance between point A and B

#drag function: this finds where the cursor is now and subtracts the distance between where the cursor is to where it was
#Then the program uses canvas.move() to move the object however many units and then sets the last click position to where the cursor is now for future calls

#__init__ function: each time an object is created, it gets the width x height constants and is created at a specific location
#it looks like a lot of math, but in reality it is the size of every object above itself + 20 for spacing between each object

class Icon:
    
    def click(self, event):
        #coordinates of the place we click the label at (Point A)
        self.click_x = event.x
        self.click_y = event.y
        print("Click:",self.click_x,self.click_y)
        
        global last_clicked
        
        try:
            canvas.itemconfig(self.info[4], state="normal")  
            canvas.itemconfig(last_clicked.info[1], state="hidden")
            canvas.itemconfig(last_clicked.info[2], state="hidden")
            canvas.itemconfig(last_clicked.info[3], state="hidden")
            canvas.itemconfig(last_clicked.info[4], state="hidden")
        except AttributeError:
            pass
        finally:
            last_clicked = self
            
            canvas.itemconfig(self.info[1], state="normal")
            canvas.itemconfig(self.info[2], state="normal")
            canvas.itemconfig(self.info[3], state="normal")
    
    def drag(self, event, obj_type):
        #coordinates of the place we are dragging the widget to (Point B)
        pointer_x=event.x
        pointer_y=event.y
        print("Pointer:",pointer_x,pointer_y)
        
        #distance between Point A and Point B for x and y
        x = pointer_x - self.click_x
        y = pointer_y - self.click_y
        
        canvas.move(self.info[0], x, y)
        canvas.move(self.info[1], x, y)
        canvas.move(self.info[2], x, y)
        canvas.move(self.info[3], x, y)
        canvas.move(self.info[4], x, y)
        
        canvas.move(self.info[5], x, y)
        canvas.move(self.info[6], x, y)
        canvas.move(self.info[7], x, y)
        canvas.move(self.info[8], x, y)
        
        self.click_x = pointer_x
        self.click_y = pointer_y
        
        self.coords = canvas.coords(self.info[0])
        
        if obj_type == "circle":
            self.hitbox = [self.coords[0],self.coords[1],
                            self.coords[2],self.coords[3]]
        elif obj_type == "rectangle":
            self.hitbox = [self.coords[0], self.coords[1],
                            self.coords[4], self.coords[5]]
        elif obj_type == "diamond":
            self.hitbox = [self.coords[2], self.coords[1],
                            self.coords[6], self.coords[5]]
        elif obj_type == "parallelogram":
            self.hitbox = [self.coords[2], self.coords[1],
                            self.coords[6], self.coords[5]]
        
        print("Hitbox:",self.hitbox)
    
    def scale(self, event, obj_type, dot):
        coords = canvas.coords(self.info[0])
        if obj_type == "circle":
            if dot == 1:
                canvas.coords(self.info[0], [event.x,event.y,coords[2],coords[3]])
            elif dot == 2:
                canvas.coords(self.info[0], [event.x,coords[1],coords[2],event.y])
            elif dot == 3:
                canvas.coords(self.info[0], [coords[0],coords[1],event.x,event.y])
            elif dot == 4:
                canvas.coords(self.info[0], [coords[0],event.y,event.x,coords[3]])
            
            coords = canvas.coords(self.info[0])
            
            canvas.coords(self.info[1], [coords[0]-DOT_SIZE, coords[1]-DOT_SIZE, coords[0]+DOT_SIZE, coords[1]+DOT_SIZE])    
            canvas.coords(self.info[2], [coords[0]-DOT_SIZE, coords[3]-DOT_SIZE, coords[0]+DOT_SIZE, coords[3]+DOT_SIZE])
            canvas.coords(self.info[3], [coords[2]-DOT_SIZE, coords[3]-DOT_SIZE, coords[2]+DOT_SIZE, coords[3]+DOT_SIZE])
            canvas.coords(self.info[4], [coords[2]-DOT_SIZE, coords[1]-DOT_SIZE, coords[2]+DOT_SIZE, coords[1]+DOT_SIZE])
            
            canvas.coords(self.info[5], [coords[0] + ((coords[2]-coords[0])/2) -DOT_SIZE, coords[1]-DOT_SIZE, coords[0] + ((coords[2]-coords[0])/2) +DOT_SIZE, coords[1]+DOT_SIZE])    
            canvas.coords(self.info[6], [coords[0] -DOT_SIZE, coords[1] + ((coords[3]-coords[1])/2) -DOT_SIZE, coords[0] +DOT_SIZE, coords[1] + ((coords[3]-coords[1])/2) + DOT_SIZE])
            canvas.coords(self.info[7], [coords[0] + ((coords[2]-coords[0])/2) -DOT_SIZE, coords[3] -DOT_SIZE, coords[0] + ((coords[2]-coords[0])/2) +DOT_SIZE, coords[3] + DOT_SIZE])
            canvas.coords(self.info[8], [coords[2] -DOT_SIZE, coords[1] + ((coords[3]-coords[1])/2) -DOT_SIZE, coords[2] +DOT_SIZE, coords[1] + ((coords[3]-coords[1])/2) + DOT_SIZE])
        
        elif obj_type == "rectangle": 
            if dot == 1:
                canvas.coords(self.info[0], [event.x, event.y, event.x, coords[3], coords[4], coords[5], coords[6], event.y])
            elif dot == 2:
                canvas.coords(self.info[0], [event.x, coords[1], event.x, event.y, coords[4], event.y, coords[6], coords[7]])
            elif dot == 3:
                canvas.coords(self.info[0], [coords[0], coords[1], coords[2], event.y, event.x, event.y, event.x, coords[7]])
            elif dot == 4:
                canvas.coords(self.info[0], [coords[0], event.y, coords[2], coords[3], event.x, coords[5], event.x, event.y])
            
            coords = canvas.coords(self.info[0])
            
            canvas.coords(self.info[1], [coords[0]-DOT_SIZE, coords[1]-DOT_SIZE, coords[0]+DOT_SIZE, coords[1]+DOT_SIZE])    
            canvas.coords(self.info[2], [coords[2]-DOT_SIZE, coords[3]-DOT_SIZE, coords[2]+DOT_SIZE, coords[3]+DOT_SIZE])
            canvas.coords(self.info[3], [coords[4]-DOT_SIZE, coords[5]-DOT_SIZE, coords[4]+DOT_SIZE, coords[5]+DOT_SIZE])
            canvas.coords(self.info[4], [coords[6]-DOT_SIZE, coords[7]-DOT_SIZE, coords[6]+DOT_SIZE, coords[7]+DOT_SIZE])
            
            canvas.coords(self.info[5], [coords[0] + ((coords[6]-coords[0])/2) -DOT_SIZE, coords[1]-DOT_SIZE, coords[0] + ((coords[6]-coords[0])/2) +DOT_SIZE, coords[1]+DOT_SIZE])    
            canvas.coords(self.info[6], [coords[2] + ((coords[0]-coords[2])/2) -DOT_SIZE, coords[1] + ((coords[3]-coords[1])/2) -DOT_SIZE, coords[2] + ((coords[0]-coords[2])/2) +DOT_SIZE, coords[1] + ((coords[3]-coords[1])/2) + DOT_SIZE])
            canvas.coords(self.info[7], [coords[2] + ((coords[4]-coords[2])/2) -DOT_SIZE, coords[3] -DOT_SIZE, coords[2] + ((coords[4]-coords[2])/2) +DOT_SIZE, coords[3] + DOT_SIZE])
            canvas.coords(self.info[8], [coords[4] + ((coords[6]-coords[4])/2) -DOT_SIZE, coords[7] + ((coords[5]-coords[7])/2) -DOT_SIZE, coords[4] + ((coords[6]-coords[4])/2) +DOT_SIZE, coords[7] + ((coords[5]-coords[7])/2) + DOT_SIZE])
            
        elif obj_type == "diamond":
            if dot == 1:
                canvas.coords(self.info[0], [event.x + ((coords[6]-coords[2])/2), event.y, 
                                            event.x, event.y + ((coords[5]-coords[1])/2),
                                            event.x + ((coords[6]-coords[2])/2), coords[5],
                                            coords[6], event.y + ((coords[5]-coords[1])/2)])
            elif dot == 2:
                canvas.coords(self.info[0], [event.x + ((coords[6]-coords[2])/2), coords[1],
                                            event.x, event.y - ((coords[5]-coords[1])/2),
                                            event.x + ((coords[6]-coords[2])/2), event.y,
                                            coords[6], event.y - ((coords[5]-coords[1])/2)])
            elif dot == 3:
                canvas.coords(self.info[0], [event.x - ((coords[6]-coords[2])/2), coords[1],
                                            coords[2], event.y - ((coords[5]-coords[1])/2),
                                            event.x - ((coords[6]-coords[2])/2), event.y,
                                            event.x, event.y - ((coords[5]-coords[1])/2)])
            elif dot == 4:
                canvas.coords(self.info[0], [event.x - ((coords[6]-coords[2])/2), event.y,
                                            coords[2], event.y + ((coords[5] - coords[1])/2),
                                            event.x - ((coords[6]-coords[2])/2), coords[5],
                                            event.x, event.y + ((coords[5] - coords[1])/2)])
            
            coords = canvas.coords(self.info[0])
            
            canvas.coords(self.info[1], [coords[2]-DOT_SIZE, coords[1]-DOT_SIZE, coords[2]+DOT_SIZE, coords[1]+DOT_SIZE])    
            canvas.coords(self.info[2], [coords[2]-DOT_SIZE, coords[5]-DOT_SIZE, coords[2]+DOT_SIZE, coords[5]+DOT_SIZE])
            canvas.coords(self.info[3], [coords[6]-DOT_SIZE, coords[5]-DOT_SIZE, coords[6]+DOT_SIZE, coords[5]+DOT_SIZE])
            canvas.coords(self.info[4], [coords[6]-DOT_SIZE, coords[1]-DOT_SIZE, coords[6]+DOT_SIZE, coords[1]+DOT_SIZE])
            
            canvas.coords(self.info[5], [coords[0]-DOT_SIZE, coords[1]-DOT_SIZE, coords[0]+DOT_SIZE, coords[1]+DOT_SIZE])    
            canvas.coords(self.info[6], [coords[2]-DOT_SIZE, coords[3]-DOT_SIZE, coords[2]+DOT_SIZE, coords[3]+DOT_SIZE])
            canvas.coords(self.info[7], [coords[4]-DOT_SIZE, coords[5]-DOT_SIZE, coords[4]+DOT_SIZE, coords[5]+DOT_SIZE])
            canvas.coords(self.info[8], [coords[6]-DOT_SIZE, coords[7]-DOT_SIZE, coords[6]+DOT_SIZE, coords[7]+DOT_SIZE])
        
        elif obj_type == "parallelogram":
            if dot == 1:
                canvas.coords(self.info[0], [event.x + PARALLELOGRAM_ANGLE, event.y, 
                                            event.x, coords[3],
                                            coords[4], coords[5],
                                            coords[6], event.y])
            elif dot == 2:
                canvas.coords(self.info[0], [event.x + 45, coords[1], 
                                            event.x, event.y,
                                            coords[4], event.y,
                                            coords[6], coords[7]])
            elif dot == 3:
                canvas.coords(self.info[0], [coords[0], coords[1], 
                                            coords[2], event.y,
                                            event.x - PARALLELOGRAM_ANGLE, event.y,
                                            event.x, coords[7]])
            elif dot == 4:
                canvas.coords(self.info[0], [coords[0], event.y, 
                                            coords[2], coords[3],
                                            event.x - PARALLELOGRAM_ANGLE, coords[5],
                                            event.x, event.y])
            
            coords = canvas.coords(self.info[0])
            
            canvas.coords(self.info[1], [coords[2]-DOT_SIZE, coords[1]-DOT_SIZE, coords[2]+DOT_SIZE, coords[1]+DOT_SIZE])    
            canvas.coords(self.info[2], [coords[2]-DOT_SIZE, coords[3]-DOT_SIZE, coords[2]+DOT_SIZE, coords[3]+DOT_SIZE])
            canvas.coords(self.info[3], [coords[6]-DOT_SIZE, coords[5]-DOT_SIZE, coords[6]+DOT_SIZE, coords[5]+DOT_SIZE])
            canvas.coords(self.info[4], [coords[6]-DOT_SIZE, coords[7]-DOT_SIZE, coords[6]+DOT_SIZE, coords[7]+DOT_SIZE])
            
            canvas.coords(self.info[5], [coords[0] + ((coords[6]-coords[0])/2) -DOT_SIZE, coords[1]-DOT_SIZE, coords[0] + ((coords[6]-coords[0])/2) +DOT_SIZE, coords[1]+DOT_SIZE])    
            canvas.coords(self.info[6], [coords[2] + ((coords[0]-coords[2])/2) -DOT_SIZE, coords[1] + ((coords[3]-coords[1])/2) -DOT_SIZE, coords[2] + ((coords[0]-coords[2])/2) +DOT_SIZE, coords[1] + ((coords[3]-coords[1])/2) + DOT_SIZE])
            canvas.coords(self.info[7], [coords[2] + ((coords[4]-coords[2])/2) -DOT_SIZE, coords[3] -DOT_SIZE, coords[2] + ((coords[4]-coords[2])/2) +DOT_SIZE, coords[3] + DOT_SIZE])
            canvas.coords(self.info[8], [coords[4] + ((coords[6]-coords[4])/2) -DOT_SIZE, coords[7] + ((coords[5]-coords[7])/2) -DOT_SIZE, coords[4] + ((coords[6]-coords[4])/2) +DOT_SIZE, coords[7] + ((coords[5]-coords[7])/2) + DOT_SIZE])
            
    def connect(self, event, anchor):
        def check_for_orient(info, anchor):
            if info[5] == anchor:
                return "top"
            elif info[6] == anchor:
                return "left"
            elif info[7] == anchor:
                return "bottom"
            elif info[8] == anchor:
                return "right"
            else:
                return None

        global first_anchor, second_anchor, first_coords, second_coords, first_anchor_coords, second_anchor_coords, first_anchor_orient, second_anchor_orient, first_object_hitbox, second_object_hitbox, first_object_info, second_object_info
        if first_anchor == None:
            
            first_anchor = anchor
            first_object_info = self.info
            first_anchor_orient = check_for_orient(first_object_info, anchor)
            
            first_anchor_coords = canvas.coords(first_anchor)
            first_anchor_coords = [first_anchor_coords[0]+DOT_SIZE, first_anchor_coords[1]+DOT_SIZE]
            print("first anchor clicked: ",first_anchor_coords)
            
            first_object_hitbox = self.hitbox
            
        elif second_anchor != first_anchor:
            
            second_anchor = anchor
            second_object_info = self.info
            second_anchor_orient = check_for_orient(self.info, anchor)
            
            second_anchor_coords = canvas.coords(second_anchor)
            second_anchor_coords = [second_anchor_coords[0]+DOT_SIZE, second_anchor_coords[1]+DOT_SIZE]
            print("second anchor clicked: ",second_anchor_coords)
            
            second_object_hitbox = self.hitbox
            
            line_coords = []
            line_coords.append(first_anchor_coords)
            
            #Code goes here! Thank you for any help!
            
            line_coords.append(second_anchor_coords)
            

            first_anchor = None
            second_anchor = None
            
                
            line = Arrow("#AA66AA", line_coords)
            
            line.info.append(first_object_info[0])
            line.info.append(second_object_info[0])
            
            first_object_info.append(line)
            second_object_info.append(line)
            
            

    
           

class Circle(Icon):
    def __init__(self, color):
        self.info =[]
        
        self.info.append(canvas.create_oval(10,10,10+CIRCLE_SIZE[0],10+CIRCLE_SIZE[1], fill=color,width=4,outline="black"))
        self.coords = canvas.coords(self.info[0])
        print(self.coords)
        
        self.info.append(canvas.create_oval(((self.coords[0])-DOT_SIZE,self.coords[1]-DOT_SIZE),
                                              ((self.coords[0])+DOT_SIZE,self.coords[1]+DOT_SIZE),
                                              fill="white", outline="black", width=3, state="hidden", tag="dot"))
        self.info.append(canvas.create_oval((self.coords[0]-DOT_SIZE,(self.coords[3])-DOT_SIZE),
                                              (self.coords[0]+DOT_SIZE,(self.coords[3])+DOT_SIZE),
                                              fill="white", outline="black", width=3, state="hidden", tag="dot"))
        self.info.append(canvas.create_oval((self.coords[2]-DOT_SIZE,(self.coords[3])-DOT_SIZE),
                                              (self.coords[2]+DOT_SIZE,(self.coords[3])+DOT_SIZE),
                                              fill="white", outline="black", width=3, state="hidden", tag="dot"))
        self.info.append(canvas.create_oval(((self.coords[2])-DOT_SIZE,self.coords[1]-DOT_SIZE),
                                              ((self.coords[2])+DOT_SIZE,self.coords[1]+DOT_SIZE),
                                              fill="white", outline="black", width=3, state="hidden", tag="dot"))
        
        self.info.append(canvas.create_oval((self.coords[0] + ((self.coords[2]-self.coords[0])/2) -DOT_SIZE, self.coords[1]-DOT_SIZE),
                                              (self.coords[0] + ((self.coords[2]-self.coords[0])/2) +DOT_SIZE, self.coords[1]+DOT_SIZE),
                                              fill="#999900", outline="black", width=3, state="hidden", tag="anchor"))
        self.info.append(canvas.create_oval((self.coords[0] -DOT_SIZE, self.coords[1] + ((self.coords[3]-self.coords[1])/2) -DOT_SIZE),
                                              (self.coords[0] +DOT_SIZE, self.coords[1] + ((self.coords[3]-self.coords[1])/2) + DOT_SIZE),
                                              fill="#999900", outline="black", width=3, state="hidden", tag="anchor"))
        self.info.append(canvas.create_oval((self.coords[0] + ((self.coords[2]-self.coords[0])/2) -DOT_SIZE, self.coords[3] -DOT_SIZE),
                                              (self.coords[0] + ((self.coords[2]-self.coords[0])/2) +DOT_SIZE, self.coords[3] +DOT_SIZE),
                                              fill="#999900", outline="black", width=3, state="hidden", tag="anchor"))
        self.info.append(canvas.create_oval((self.coords[2] -DOT_SIZE, self.coords[1] + ((self.coords[3]-self.coords[1])/2) -DOT_SIZE),
                                              (self.coords[2] +DOT_SIZE, self.coords[1] + ((self.coords[3]-self.coords[1])/2) + DOT_SIZE),
                                              fill="#999900", outline="black", width=3, state="hidden", tag="anchor"))
        
        self.hitbox = [self.coords[0],self.coords[1],
                       self.coords[2],self.coords[3]]
        
        canvas.tag_bind(self.info[0],"<Button-1>",self.click)
        canvas.tag_bind(self.info[0],"<B1-Motion>",lambda event: self.drag(event, "circle"))
        
        canvas.tag_bind(self.info[1], "<B1-Motion>", lambda event: self.scale(event, "circle", 1))
        canvas.tag_bind(self.info[2], "<B1-Motion>", lambda event: self.scale(event, "circle", 2))
        canvas.tag_bind(self.info[3], "<B1-Motion>", lambda event: self.scale(event, "circle", 3))
        canvas.tag_bind(self.info[4], "<B1-Motion>", lambda event: self.scale(event, "circle", 4))
        
        canvas.tag_bind(self.info[5], "<Button-1>", lambda event: self.connect(event, self.info[5]))
        canvas.tag_bind(self.info[6], "<Button-1>", lambda event: self.connect(event, self.info[6]))
        canvas.tag_bind(self.info[7], "<Button-1>", lambda event: self.connect(event, self.info[7]))
        canvas.tag_bind(self.info[8], "<Button-1>", lambda event: self.connect(event, self.info[8]))  

class Rectangle(Icon):
    def __init__(self, color):
        self.info =[]
        
        self.info.append(canvas.create_polygon(10, CIRCLE_SIZE[1]+20,
                                            10, CIRCLE_SIZE[1]+20+RECTANGLE_SIZE[1],
                                            10+RECTANGLE_SIZE[0], CIRCLE_SIZE[1]+20+RECTANGLE_SIZE[1],
                                            10+RECTANGLE_SIZE[0], CIRCLE_SIZE[1]+20,
                                            fill=color,width=4,outline="black"))
        self.coords = canvas.coords(self.info[0])
        
        self.info.append(canvas.create_oval((self.coords[0]-DOT_SIZE,self.coords[1]-DOT_SIZE),
                                              (self.coords[0]+DOT_SIZE,self.coords[1]+DOT_SIZE),
                                              fill="white",outline="black",width=3,state="hidden"))
        self.info.append(canvas.create_oval((self.coords[2]-DOT_SIZE,self.coords[3]-DOT_SIZE),
                                              (self.coords[2]+DOT_SIZE,self.coords[3]+DOT_SIZE),
                                              fill="white",outline="black",width=3,state="hidden"))
        self.info.append(canvas.create_oval((self.coords[4]-DOT_SIZE,self.coords[5]-DOT_SIZE),
                                              (self.coords[4]+DOT_SIZE,self.coords[5]+DOT_SIZE),
                                              fill="white",outline="black",width=3,state="hidden"))
        self.info.append(canvas.create_oval((self.coords[6]-DOT_SIZE,self.coords[7]-DOT_SIZE),
                                              (self.coords[6]+DOT_SIZE,self.coords[7]+DOT_SIZE),
                                              fill="white",outline="black",width=3,state="hidden"))
        
        self.info.append(canvas.create_oval((self.coords[0] + ((self.coords[6]-self.coords[0])/2) -DOT_SIZE, self.coords[1]-DOT_SIZE),
                                              (self.coords[0] + ((self.coords[6]-self.coords[0])/2) +DOT_SIZE, self.coords[1]+DOT_SIZE),
                                              fill="#999900", outline="black", width=3, state="hidden", tag="anchor"))
        self.info.append(canvas.create_oval((self.coords[2] + ((self.coords[0]-self.coords[2])/2) -DOT_SIZE, self.coords[1] + ((self.coords[3]-self.coords[1])/2) -DOT_SIZE),
                                              (self.coords[2] + ((self.coords[0]-self.coords[2])/2) +DOT_SIZE, self.coords[1] + ((self.coords[3]-self.coords[1])/2) + DOT_SIZE),
                                              fill="#999900", outline="black", width=3, state="hidden", tag="anchor"))
        self.info.append(canvas.create_oval((self.coords[2] + ((self.coords[4]-self.coords[2])/2) -DOT_SIZE, self.coords[3] -DOT_SIZE),
                                              (self.coords[2] + ((self.coords[4]-self.coords[2])/2) +DOT_SIZE, self.coords[3] + DOT_SIZE),
                                              fill="#999900", outline="black", width=3, state="hidden", tag="anchor"))
        self.info.append(canvas.create_oval((self.coords[4] + ((self.coords[6]-self.coords[4])/2) -DOT_SIZE, self.coords[7] + ((self.coords[5]-self.coords[7])/2) -DOT_SIZE),
                                              (self.coords[4] + ((self.coords[6]-self.coords[4])/2) +DOT_SIZE, self.coords[7] + ((self.coords[5]-self.coords[7])/2) + DOT_SIZE),
                                              fill="#999900", outline="black", width=3, state="hidden", tag="anchor"))
        
        self.hitbox = [self.coords[0], self.coords[1],
                       self.coords[4], self.coords[5]]
        
        canvas.tag_bind(self.info[0],"<Button-1>",self.click)
        canvas.tag_bind(self.info[0],"<B1-Motion>",lambda event: self.drag(event, "rectangle"))
        
        canvas.tag_bind(self.info[1], "<B1-Motion>", lambda event: self.scale(event, "rectangle", 1))
        canvas.tag_bind(self.info[2], "<B1-Motion>", lambda event: self.scale(event, "rectangle", 2))
        canvas.tag_bind(self.info[3], "<B1-Motion>", lambda event: self.scale(event, "rectangle", 3))
        canvas.tag_bind(self.info[4], "<B1-Motion>", lambda event: self.scale(event, "rectangle", 4))
        
        canvas.tag_bind(self.info[5], "<Button-1>", lambda event: self.connect(event, self.info[5]))
        canvas.tag_bind(self.info[6], "<Button-1>", lambda event: self.connect(event, self.info[6]))
        canvas.tag_bind(self.info[7], "<Button-1>", lambda event: self.connect(event, self.info[7]))
        canvas.tag_bind(self.info[8], "<Button-1>", lambda event: self.connect(event, self.info[8]))  

class Diamond(Icon):
    def __init__(self, color):
        self.info =[]
        
        self.info.append(canvas.create_polygon((10+ (DIAMOND_SIZE[0] / 2), (RECTANGLE_SIZE[1]+20+CIRCLE_SIZE[1]+20)),
                                             (10, (RECTANGLE_SIZE[1]+20+CIRCLE_SIZE[1]+20) + (DIAMOND_SIZE[1] / 2)),
                                             (10+ (DIAMOND_SIZE[0] / 2), (RECTANGLE_SIZE[1]+20+CIRCLE_SIZE[1]+20)  + DIAMOND_SIZE[1]),
                                             (10+ DIAMOND_SIZE[0], (RECTANGLE_SIZE[1]+20+CIRCLE_SIZE[1]+20) + (DIAMOND_SIZE[1] / 2)),
                                             fill=color,width=4,outline="black"))
        self.coords = canvas.coords(self.info[0])
        
        self.info.append(canvas.create_oval((self.coords[2]-DOT_SIZE,self.coords[1]-DOT_SIZE),
                                              (self.coords[2]+DOT_SIZE,self.coords[1]+DOT_SIZE),
                                              fill="white", outline="black", width=3, state="hidden"))
        self.info.append(canvas.create_oval((self.coords[2]-DOT_SIZE,self.coords[5]-DOT_SIZE),
                                              (self.coords[2]+DOT_SIZE,self.coords[5]+DOT_SIZE),
                                              fill="white", outline="black", width=3, state="hidden"))
        self.info.append(canvas.create_oval((self.coords[6]-DOT_SIZE,self.coords[5]-DOT_SIZE),
                                              (self.coords[6]+DOT_SIZE,self.coords[5]+DOT_SIZE),
                                              fill="white", outline="black", width=3, state="hidden"))
        self.info.append(canvas.create_oval((self.coords[6]-DOT_SIZE,self.coords[1]-DOT_SIZE),
                                              (self.coords[6]+DOT_SIZE,self.coords[1]+DOT_SIZE),
                                              fill="white", outline="black", width=3, state="hidden"))
        
        self.info.append(canvas.create_oval((self.coords[0] -DOT_SIZE, self.coords[1]-DOT_SIZE),
                                              (self.coords[0] +DOT_SIZE, self.coords[1]+DOT_SIZE),
                                              fill="#999900", outline="black", width=3, state="hidden", tag="anchor"))
        self.info.append(canvas.create_oval((self.coords[2] -DOT_SIZE, self.coords[3] -DOT_SIZE),
                                              (self.coords[2] +DOT_SIZE, self.coords[3] +DOT_SIZE),
                                              fill="#999900", outline="black", width=3, state="hidden", tag="anchor"))
        self.info.append(canvas.create_oval((self.coords[4] -DOT_SIZE, self.coords[5] -DOT_SIZE),
                                              (self.coords[4] +DOT_SIZE, self.coords[5] +DOT_SIZE),
                                              fill="#999900", outline="black", width=3, state="hidden", tag="anchor"))
        self.info.append(canvas.create_oval((self.coords[6] -DOT_SIZE, self.coords[7] -DOT_SIZE),
                                              (self.coords[6] +DOT_SIZE, self.coords[7] +DOT_SIZE),
                                              fill="#999900", outline="black", width=3, state="hidden", tag="anchor"))
        
        self.hitbox = [self.coords[2], self.coords[1],
                       self.coords[6], self.coords[5]]
        
        canvas.tag_bind(self.info[0],"<Button-1>",self.click)
        canvas.tag_bind(self.info[0],"<B1-Motion>",lambda event: self.drag(event, "diamond"))
        
        canvas.tag_bind(self.info[1], "<B1-Motion>", lambda event: self.scale(event, "diamond", 1))
        canvas.tag_bind(self.info[2], "<B1-Motion>", lambda event: self.scale(event, "diamond", 2))
        canvas.tag_bind(self.info[3], "<B1-Motion>", lambda event: self.scale(event, "diamond", 3))
        canvas.tag_bind(self.info[4], "<B1-Motion>", lambda event: self.scale(event, "diamond", 4))
        
        canvas.tag_bind(self.info[5], "<Button-1>", lambda event: self.connect(event, self.info[5]))
        canvas.tag_bind(self.info[6], "<Button-1>", lambda event: self.connect(event, self.info[6]))
        canvas.tag_bind(self.info[7], "<Button-1>", lambda event: self.connect(event, self.info[7]))
        canvas.tag_bind(self.info[8], "<Button-1>", lambda event: self.connect(event, self.info[8]))  

class Parallelogram(Icon):
    def __init__(self, color):
        self.info =[]
        
        self.info.append(canvas.create_polygon((10+PARALLELOGRAM_ANGLE, (RECTANGLE_SIZE[1]+20+CIRCLE_SIZE[1]+20+DIAMOND_SIZE[1]+20)),
                                             (10, (RECTANGLE_SIZE[1]+20+CIRCLE_SIZE[1]+20+DIAMOND_SIZE[1]+20)+PARALLELOGRAM_SIZE[1]),
                                             (10+PARALLELOGRAM_SIZE[0]-PARALLELOGRAM_ANGLE, (RECTANGLE_SIZE[1]+20+CIRCLE_SIZE[1]+20+DIAMOND_SIZE[1]+20)+PARALLELOGRAM_SIZE[1]),
                                             (10+PARALLELOGRAM_SIZE[0], (RECTANGLE_SIZE[1]+20+CIRCLE_SIZE[1]+20+DIAMOND_SIZE[1]+20)),
                                             fill=color,width=4,outline="black"))
        self.coords = canvas.coords(self.info[0])
        
        self.info.append(canvas.create_oval((self.coords[2]-DOT_SIZE,self.coords[1]-DOT_SIZE),
                                              (self.coords[2]+DOT_SIZE,self.coords[1]+DOT_SIZE),
                                              fill="white", outline="black", width=3, state="hidden"))
        self.info.append(canvas.create_oval((self.coords[2]-DOT_SIZE,self.coords[3]-DOT_SIZE),
                                              (self.coords[2]+DOT_SIZE,self.coords[3]+DOT_SIZE),
                                              fill="white", outline="black", width=3, state="hidden"))
        self.info.append(canvas.create_oval((self.coords[6]-DOT_SIZE,self.coords[5]-DOT_SIZE),
                                              (self.coords[6]+DOT_SIZE,self.coords[5]+DOT_SIZE),
                                              fill="white", outline="black", width=3, state="hidden"))
        self.info.append(canvas.create_oval((self.coords[6]-DOT_SIZE,self.coords[7]-DOT_SIZE),
                                              (self.coords[6]+DOT_SIZE,self.coords[7]+DOT_SIZE),
                                              fill="white", outline="black", width=3, state="hidden"))
        
        self.info.append(canvas.create_oval((self.coords[0] + ((self.coords[6]-self.coords[0])/2) -DOT_SIZE, self.coords[1]-DOT_SIZE),
                                              (self.coords[0] + ((self.coords[6]-self.coords[0])/2) +DOT_SIZE, self.coords[1]+DOT_SIZE),
                                              fill="#999900", outline="black", width=3, state="hidden", tag="anchor"))
        self.info.append(canvas.create_oval((self.coords[2] + ((self.coords[0]-self.coords[2])/2) -DOT_SIZE, self.coords[1] + ((self.coords[3]-self.coords[1])/2) -DOT_SIZE),
                                              (self.coords[2] + ((self.coords[0]-self.coords[2])/2) +DOT_SIZE, self.coords[1] + ((self.coords[3]-self.coords[1])/2) + DOT_SIZE),
                                              fill="#999900", outline="black", width=3, state="hidden", tag="anchor"))
        self.info.append(canvas.create_oval((self.coords[2] + ((self.coords[4]-self.coords[2])/2) -DOT_SIZE, self.coords[3] -DOT_SIZE),
                                              (self.coords[2] + ((self.coords[4]-self.coords[2])/2) +DOT_SIZE, self.coords[3] + DOT_SIZE),
                                              fill="#999900", outline="black", width=3, state="hidden", tag="anchor"))
        self.info.append(canvas.create_oval((self.coords[4] + ((self.coords[6]-self.coords[4])/2) -DOT_SIZE, self.coords[7] + ((self.coords[5]-self.coords[7])/2) -DOT_SIZE),
                                              (self.coords[4] + ((self.coords[6]-self.coords[4])/2) +DOT_SIZE, self.coords[7] + ((self.coords[5]-self.coords[7])/2) + DOT_SIZE),
                                              fill="#999900", outline="black", width=3, state="hidden", tag="anchor"))
        
        self.hitbox = [self.coords[2], self.coords[1],
                       self.coords[6], self.coords[5]]
        
        canvas.tag_bind(self.info[0],"<Button-1>",self.click)
        canvas.tag_bind(self.info[0],"<B1-Motion>",lambda event: self.drag(event, "parallelogram"))
        
        canvas.tag_bind(self.info[1], "<B1-Motion>", lambda event: self.scale(event, "parallelogram", 1))
        canvas.tag_bind(self.info[2], "<B1-Motion>", lambda event: self.scale(event, "parallelogram", 2))
        canvas.tag_bind(self.info[3], "<B1-Motion>", lambda event: self.scale(event, "parallelogram", 3))
        canvas.tag_bind(self.info[4], "<B1-Motion>", lambda event: self.scale(event, "parallelogram", 4))
        
        canvas.tag_bind(self.info[5], "<Button-1>", lambda event: self.connect(event, self.info[5]))
        canvas.tag_bind(self.info[6], "<Button-1>", lambda event: self.connect(event, self.info[6]))
        canvas.tag_bind(self.info[7], "<Button-1>", lambda event: self.connect(event, self.info[7]))
        canvas.tag_bind(self.info[8], "<Button-1>", lambda event: self.connect(event, self.info[8]))  

class Arrow(Icon):

    
    def __init__(self, color, coordinates):
        self.info =[]
        
        self.info.append(canvas.create_line((coordinates),
                                             fill=color, width=2, arrow="last", arrowshape=(30,30,9)))
        self.coords = canvas.coords(self.info[0])
        print(self.coords)

#For each object, there is a base object that creates a new canvas item when it is clicked
#The math for where it is placed is the same as the __init__ variables above
#when it is clicked, is creates another circle with the color from the constant at the top

base_oval = canvas.create_oval(10,10,10+CIRCLE_SIZE[0],
                               10+CIRCLE_SIZE[1],
                               fill=BASE_COLOR, width=4, outline="black")
canvas.tag_bind(base_oval,"<Button-1>",lambda self: Circle(COLOR))

base_rectangle = canvas.create_rectangle(10,(CIRCLE_SIZE[1]+20),
                                        10+RECTANGLE_SIZE[0],(CIRCLE_SIZE[1]+20)+RECTANGLE_SIZE[1],
                                        fill=BASE_COLOR, width=4, outline="black")
canvas.tag_bind(base_rectangle,"<Button-1>",lambda self: Rectangle(COLOR))

base_diamond = canvas.create_polygon((10+ (DIAMOND_SIZE[0] / 2), (RECTANGLE_SIZE[1]+20+CIRCLE_SIZE[1]+20)),
                                             (10, (RECTANGLE_SIZE[1]+20+CIRCLE_SIZE[1]+20) + (DIAMOND_SIZE[1] / 2)),
                                             (10+ (DIAMOND_SIZE[0] / 2), (RECTANGLE_SIZE[1]+20+CIRCLE_SIZE[1]+20)  + DIAMOND_SIZE[1]),
                                             (10+ DIAMOND_SIZE[0], (RECTANGLE_SIZE[1]+20+CIRCLE_SIZE[1]+20) + (DIAMOND_SIZE[1] / 2)),
                                             fill=BASE_COLOR, width=4, outline="black")
canvas.tag_bind(base_diamond,"<Button-1>",lambda self: Diamond(COLOR))

base_parallelogram = canvas.create_polygon((10+PARALLELOGRAM_ANGLE, (RECTANGLE_SIZE[1]+20+CIRCLE_SIZE[1]+20+DIAMOND_SIZE[1]+20)),
                                             (10, (RECTANGLE_SIZE[1]+20+CIRCLE_SIZE[1]+20+DIAMOND_SIZE[1]+20)+PARALLELOGRAM_SIZE[1]),
                                             (10+PARALLELOGRAM_SIZE[0]-PARALLELOGRAM_ANGLE, (RECTANGLE_SIZE[1]+20+CIRCLE_SIZE[1]+20+DIAMOND_SIZE[1]+20)+PARALLELOGRAM_SIZE[1]),
                                             (10+PARALLELOGRAM_SIZE[0], (RECTANGLE_SIZE[1]+20+CIRCLE_SIZE[1]+20+DIAMOND_SIZE[1]+20)),
                                             fill=BASE_COLOR, width=4, outline="black")
canvas.tag_bind(base_parallelogram,"<Button-1>",lambda self: Parallelogram(COLOR))


window.mainloop()
