# -*- coding: utf-8 -*-
"""
Author:                 Ian Sinclair
Date Created:           1/10/2022
Functionality:          Program to construct polygons and then test to
                        determine if points are in the polygon.
                        Added functionality to upload polygon data,
                        and interactively add multiple query points
                        and polygons.
"""

import tkinter as tk 
from tkinter import *
from tkinter import filedialog




class point() :
    def __init__( self, x: int, y: int) :
        self.x = x
        self.y = y
    
    def isEqual( self, p ) :
        if self.x == p.x and self.y == p.y :
            return True
        return False
    
    def draw_point( self, color : str ) :
        point_rad = 3
        x2, y2 = cast_To_Pixel( self.x, self.y )
        
        canvas.create_oval(x2-point_rad, y2-point_rad, x2+point_rad, y2+point_rad, fill = color)
    
    def toString( self ) :
        return "( " + str( self.x ) + " " + str( self.y ) + " )"

class vertex() :
    def __init__( self, x : int, y : int ) :
        self.x = x
        self.y = y
    
    #  Returns true if self is equivalent to vertex 'v'.
    def isEqual( self, v ) :
        if self.x == v.x and self.y == v.y :
            return True
        return False
    def distance( self, v ) :
        return ((self.x-v.x)^2 + (self.y - v.y)**2)**(1/2)

class polygon() :
    def __init__( self, list_of_verices = None ) :
        self.vertex_List = []
        self.closingEdge = canvas.create_line(0,0,0,0, fill = color)
        if list_of_verices != None :
            for v in list_of_verices :
                self.add_vertex( vertex( v[0], v[1] ) )
    
    def add_vertex( self, v : vertex ) :
        self.draw_edge( v )
        self.vertex_List.append( v )
    
    def empty( self ) :
        self.vertex_List = []
    
    def draw_edge( self, v : vertex) :
        point_rad = 3
        x2, y2 = cast_To_Pixel( v.x, v.y )
        
        canvas.create_oval(x2-point_rad, y2-point_rad, x2+point_rad, y2+point_rad, fill = color)
        if len( self.vertex_List ) > 0 :
            x1, y1 = cast_To_Pixel( self.vertex_List[-1].x, self.vertex_List[-1].y )
            canvas.create_line(x1, 
                               y1, 
                               x2,
                               y2,
                               fill = color )
            x0, y0 = cast_To_Pixel( self.vertex_List[0].x, self.vertex_List[0].y )
            canvas.coords(self.closingEdge, x0, y0, x2, y2)

    
    
    def toString( self ) :
        output = str( len(self.vertex_List) ) + '\n'
        for v in self.vertex_List :
            output += str(v.x) + ' ' + str(v.y) + '\n'
        
        return output
    
    def length( self ) :
        return len(self.vertex_List)
            


class objects() :
    def __init__( self ) :
        self.objects_List = []
        global color
        color = 'red'
    
    def add_polygon( self, poly = None ) :
        self.objects_List += [ polygon() ]
        if poly != None :
            for v in poly.vertex_List :
                self.new_vertex( v )
    
    def isClosed( self, v : vertex) :
        for j in self.objects_List[-1].vertex_List :
            if j.isEqual( v ) :
                return True
        return False
    
    def new_vertex( self, v : vertex) :
        if len( self.objects_List) == 0 :
            self.add_polygon()
            
        if self.isClosed( v ) :
            self.objects_List[-1].add_vertex( v )
            self.add_polygon()
        
        else :
            self.objects_List[-1].add_vertex( v )
        
    def empty( self ) :
        for j in self.objects_List :
            j.empty()
        self.objects_List = []
    
    
    def test_in_polygon( self, q : point) :
        for p in self.objects_List :
            if InPolygon( p, q ) == 1 :
                color = 'green'
                break
            elif InPolygon( p, q ) == -1 :
                color = 'red'
            elif InPolygon( p, q ) == 0 :
                color = 'blue'
                break
        q.draw_point(color)
        color = 'red'

    
    def toFile( self ) :
        files = [('Text Document', '*.txt')]
        filename = filedialog.asksaveasfilename(filetypes = files, defaultextension = files, initialdir = '/', title = 'Save Polygon')
        
        
        output = ''
        for q in self.objects_List :
            output += q.toString()
        
        try:
            outputFile = open(filename, "w+")
            outputFile.write( output )
            outputFile.close()
    
        except: 
            print("Unable to print file: see 'toFile' method in Objects class")
    
    



"""
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

            HOMEWORK 1
            
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& 
       
----------------------------------
    In-Polygon Problem Solution
----------------------------------
"""


def cross( A : vertex, B : vertex, q : point ) :
    """
    Parameters
    ----------
    q : Point
        Query point
    A : vertex
    B : vertex

    Returns
    -------
    Cross product between 2D vectors (B-A) and (q-B).
    """
    return ( (B.y - A.y) * (q.x - B.x) ) - ( (B.x - A.x) * (q.y - B.y) )

def Orient(A : vertex, B : vertex, q : point ) :
    """
    Parameters
    ----------
    q : Point
        Query point
    A : vertex
    B : vertex

    Returns
    0 --> A, B and q are collinear
    1 --> Clockwise
    -1 --> Counterclockwise
    """
    Cross_product = cross( A, B, q ) 
    if Cross_product != 0 :
        return Cross_product / abs( Cross_product )  #Directed normal
    return 0;


def onEdge( q : point, v1 : vertex, v2 : vertex ) :
    """
    Parameters
    ----------
    q : point
    v1 : vertex
    v2 : vertex
    Assume q, v1, v2 are colinear
    Returns
    -------
    bool
        True --> q is on line segment v1v2
        False --> q is not on line segment v1v2.

    """
    if (v1.y >= q.y >= v2.y) or (v2.y >= q.y >= v1.y) :
        if (v1.x >= q.x >= v2.x) or (v2.x >= q.x >= v1.x) :
            return True
    return False
    
def intersect( A1 : point, A2 : point, B1 : vertex, B2: vertex ) :
    """
    Parameters
    ----------
    A1 : point
    A2 : point
    B1 : vertex
    B2 : vertex
    
    Line segment A1 --> A2 and B1 --> B2

    Returns
    -------
    INT
        0 --> if A1 is on line segment of B1 --> B2
        1 --> if line segment A1 --> A2 intersects B1 --> B2
        -1 --> if no intersection.

    """
    #  Orientation of every combination of connecting vectors between
    #   line segments.
    O1 = Orient(A1, A2, B1)
    O2 = Orient(A1, A2, B2)
    O3 = Orient(B1, B2, A1)
    O4 = Orient(B1, B2, A2)
    
    if (O3 == 0) : #  A1 is colinear with B1,B2
        if onEdge( A1, B1, B2 ) : #  A1 is on line segment B1 --> B2
            return 0
        return -1  #  A1 is colinear with B1,B2 but not on line segment. (intersection is impossible.)
    
    if (O1 == 0) and (O2 == 0) :  #  B1 and B2 are colinear with A1 and A2.
        if onEdge( A1, B1, B2 ) : #  A1 is on boundary of B1 -- B2
            return 0
        return -1
    
    
    #  Picks the upper endpoint in y of segment B1 -- B2
    #  This is so vertex intersections are not double counted between tests.
    if (B1.y > B2.y) :
        Upper_Bound = point( B1.x, B1.y )
    elif (B2.y > B1.y) :
        Upper_Bound = point( B2.x, B2.y )
    
    if Orient(A1, A2, Upper_Bound) == 0 :
        if onEdge( Upper_Bound, A1, A2 ) :
            return 1
    
    #  General case, if both line segments intersect but none are colinear.
    if ( O1 != 0 and O2 != 0 and O3 != 0 and O4 != 0 ) :
        if (O1 != O2) and (O3 != O4) :
            return 1    
    return -1

def InPolygon(P : polygon, q : point) :
    """
    Parameters
    ----------
    P : polygon
        Simple closed polygon
    q : point
        Query point

    Returns
    -------
    INT
        0 --> q is on the boundary of P.
        1 --> q is with the boundary of P.
        -1 --> q is not in P.
    """
    
    inside = -1
    j = P.length() - 1
    
    #  casts horizontal ray from query point
    #  Note: screen max is 100 in both x,y, so rayEnd.x = 1000
    #  must be past the x coordinate boundary of any vertex.
    rayEnd = point( 1000, q.y )
    
    for i in range( 0, P.length() ) :
        if (P.vertex_List[i].y <= q.y <= P.vertex_List[j].y or P.vertex_List[j].y <= q.y <= P.vertex_List[i].y) :
            if intersect( q, rayEnd, P.vertex_List[i], P.vertex_List[j] ) == 0 :
                return 0
            if intersect( q, rayEnd, P.vertex_List[i], P.vertex_List[j] ) == 1 :
                inside *= -1      
        j = i
    return inside
    
    


"""
----------------------------------
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& 
"""
    

def load_polygon_data() :
    view_List.add_polygon()

    # show the open file dialog
    filename = filedialog.askopenfilename(initialdir = '/')
    
    try:
        with open(filename, 'r') as file:
            for line in file :
                coords = line.split()
                if len(coords) == 2 :
                    view_List.new_vertex( vertex( int(coords[0]), int(coords[1]) ) )
    except : 
        print("Unable to open file")

    
def list_to_polygon(P : list) :
    """
    Parameters
    ----------
    P : list
        List of vertex coordinates in the form [ [x1,y1], [x2,y2], ... ]

    Returns
    -------
    polygon object.
        Adds polygon to view_list.
    """
    
    poly = polygon( P )
    view_List.add_polygon( poly )    
    view_List.add_polygon()
    return poly

def cast_To_Grid(x , y) :
    canvas.update()
    return int( (x/canvas.winfo_width())*100 ), int(100 - (y/canvas.winfo_height()*100))

def cast_To_Pixel( x, y ) :
    canvas.update()
    return (x/100)*canvas.winfo_width(), ((y-100)/-100)*canvas.winfo_height()


def canvas_click_event( event ) :
    x,y = cast_To_Grid( event.x, event.y )
    if ShapeToggle.config('relief')[-1] == 'raised':
        view_List.new_vertex( vertex( x, y ) )
        
    else:
        view_List.test_in_polygon( point(x,y) ) 
        
def ClearScreen() :
    canvas.delete("all")
    view_List.empty()

def new_Shape() :
    view_List.add_polygon()

def toggle() :
    if ShapeToggle.config('relief')[-1] == 'sunken':
        ShapeToggle.config(relief="raised", text = "Add Query Point", bg = 'light blue')
        
    else:
        ShapeToggle.config(relief="sunken", text = "Add Vertex", bg = '#A877BA')
        view_List.add_polygon()



def init_GUI () :
    global canvas
    global root
    global ShapeToggle
    global color
    global view_List
    view_List = objects()
    
    root = tk.Tk()
    root.title("COMP 3705 HW 0 Ian Sinclair")
    root.geometry('800x400')
    
    printButton = Button(root, text = 'Print To File', bd = '5',
                              command = view_List.toFile)
    printButton.pack(side = 'top')
    
    ClearButton = Button(root, text = 'Clear', bd = '5',
                          command = ClearScreen)
    ClearButton.pack(side = 'top')
    
    NewShapeButton = Button(root, text = 'New Polygon', bd = '5',
                          command = new_Shape)
    NewShapeButton.pack(side = 'top')
    
    ShapeToggle = tk.Button(text="Add Query Point", width=12, relief="raised", command = toggle, bg = 'light blue')
    ShapeToggle.pack(side = 'top')
    
    UploadPolygon = tk.Button(text="Upload Polygon", width=12, command = load_polygon_data, bg = 'green')
    UploadPolygon.pack(side = 'left')
    
    canvas = Canvas(root, width = 100, height = 100, bg = "black")
    canvas.pack(expand = YES, fill = BOTH)
    
    canvas.bind( "<Button-1>", canvas_click_event )

    message = Label( root, text = "Click to add a new vertex" )
    message.pack( side = BOTTOM )


"""
        MAIN
"""
def main() :    
    pass

def Driver_to_load_polygon() :
    load_polygon_data()

def test1() :
    polygon = [ [70,70], [30,30], [90,50] ]
    
    Query_points = [ point(65,70), 
              point(70,70),
              point(75,70),
              point(25,30),
              point(30,30),
              point(35,30),
              point(85,50),
              point(90,50),
              point(95,50),
              point(35,40),
              point(40,40),
              point(45,40),
              point(45,35),
              point(43,35),
              point(47,35),
              ]
    
    poly = list_to_polygon( polygon )
    
    for q in Query_points :
        view_List.test_in_polygon( q )
        print( InPolygon( poly, q ) )
def test2() :
    polygon = [ [70,70], [60,70], [40,40], [30, 30], [30,20], [50,10], [70,40] ]
    
    Query_points = [ point(50,50), 
              point(20,20),
              point(20,50),
              point(60,40),
              point(90,40),
              point(30,30),
              point(40,40),
              point(60,60),
              point(35,35)
              ]
    
    poly = list_to_polygon( polygon )
    
    for q in Query_points :
        view_List.test_in_polygon( q )
        print( InPolygon( poly, q ) )
    
def test3() :
    polygon = [ [70,60], [60,70], [55,65], [45, 30], [20,25], [50,10] ]
    
    points = [ point(10,10), point(20,20), point(30,30),point(40,40),point(60,60) ]
    
    poly = list_to_polygon( polygon )
    
    for q in points :
        view_List.test_in_polygon( q )
        print( InPolygon( poly, q ) )
    
def test4() :
    pass
    
"""
    MAIN CALL
"""
if __name__ == "__main__" :
    init_GUI()
    
    main()
    
    #Driver_to_load_polygon()
    #test1()
    #test2()
    #test3()
    #test4()
        
    root.mainloop()
    
    
    
    