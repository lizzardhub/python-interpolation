from tkinter import *
from decimal import *
getcontext().prec = 500

#******Polynom******#

def polFunc(polynom, x):
    # assuming deg(f) >= 0 (polynom not empty)
    y = polynom[len(polynom) - 1]
    for i in range(len(polynom) - 1, 0, -1):
        y = y * x + polynom[i - 1]
    return y

def mulPolynom(pol1, pol2):
    # f(x) = a_n * x^n + ... + a_1 * x^1 + a_0 * x^0
    # deg(f) = n = len(coefficient) - 1
    
    deg1 = len(pol1) - 1
    deg2 = len(pol2) - 1
    
    # deg(fg) = deg(f) + deg(g)
    
    mulPol = [0] * (deg1 + deg2 + 1)
    
    for i in range(deg1 + 1):
        for i1 in range(deg2 + 1):
            mulPol[i + i1] += pol1[i] * pol2[i1]
    return mulPol

def constructLagrange(table):
    n = len(table)    
    
    coefficient = [Decimal(0)] * n
    
    for i in range(n):
        # count k and unbracket simultaneously
        k = table[i][1]
        polynom = [Decimal(1)]
        
        for i1 in range(i):
            k /= table[i][0] - table[i1][0]
            polynom = mulPolynom(polynom, [-table[i1][0], Decimal(1)])
        for i1 in range(i + 1, n):
            k /= table[i][0] - table[i1][0]
            polynom = mulPolynom(polynom, [-table[i1][0], Decimal(1)])
        
        for i1 in range(len(polynom)):
            coefficient[i1] += polynom[i1] * k
    
    return coefficient

#************#

def draw_point(coors):
    global graph_global; global point_size
    graph_global.create_rectangle(coors[0] - point_size, coors[1] - point_size, coors[0] + point_size, coors[1] + point_size, fill = "black")

def coor_conv(point):
    global coor_local; global axis_magnify
    return (point[0] * axis_magnify[0] + coor_local[0], coor_local[1] - point[1] * axis_magnify[1])

def graph_move(direction):
    global coor_local
    speed = 100
    if direction == "u":
        coor_local[1] += speed
    elif direction == "r":
        coor_local[0] -= speed
    elif direction == "d":
        coor_local[1] -= speed
    else:
        coor_local[0] += speed
    graph_redraw()

def magnify(boolean, axis_list):
    # axis <iterable> parameter: [0] is x-axis and [1] is y-axis, [0, 1] will apply to both
    global coor_center; global coor_local; global axis_magnify; global coefficient; global f_coefficient
    for axis in axis_list:
        if boolean:
            axis_magnify[axis] *= coefficient
            coor_local[axis] = (coor_local[axis] - coor_center[axis]) * f_coefficient + coor_center[axis]
        else:
            axis_magnify[axis] /= coefficient
            coor_local[axis] = (coor_local[axis] - coor_center[axis]) / f_coefficient + coor_center[axis]
    graph_redraw()

def graph_redraw():
    global window_graph; global graph_global; global edge_x; global edge_y; global coor_local; global table
    graph_global.delete("all")
    
    graph_global.create_line(edge_x[0], coor_local[1], edge_x[1], coor_local[1], arrow = LAST)
    graph_global.create_line(coor_local[0], edge_y[1], coor_local[0], edge_y[0], arrow = LAST)
    
    for point in table:
        draw_point(coor_conv(point))

def graph_interpolate(polynom):
    table = []
    for x in range(-3000, 3000):
        table.append((x, float(polFunc(polynom, x))))
    return table

def graph_plot(table):
    global graph_global; global coor_local; global size_x
    last_point = coor_conv(table[0])
    for cur_point in table[1:]:
        cur_point = coor_conv(cur_point)
        graph_global.create_line(last_point, cur_point)
        last_point = cur_point
        
#******************************************************************************#

# Read points and construct the polynom
table = []
init_magnify = 50
inf = open("input.txt", "r")
s = inf.readline()
while s:
    x, y = map(int, s.split())
    table.append((x * init_magnify, y * init_magnify))
    s = inf.readline()

table_decimal = []
for pair in table:
    table_decimal.append(list(map(Decimal, pair)))
polynom = constructLagrange(table_decimal)

# Construct the application and initiate graph vars
application = Tk()

size_x = 550; size_y = 360
edge_x = [0, size_x * 2]; edge_y = [0, size_y * 2]
coor_center = [size_x, size_y]; coor_local = coor_center[:]

point_size = 5
point_size /= 2
coefficient = 3
f_coefficient = float(coefficient)
axis_magnify = [1, 1]

window_graph = Frame()
graph_global = Canvas(window_graph, width = sum(map(abs, edge_x)), height = sum(map(abs, edge_y)), bg = "white")
graph_redraw()

window_button = Frame()
images = [PhotoImage(file = "arrow_up.gif"), PhotoImage(file = "arrow_right.gif"), 
          PhotoImage(file = "arrow_down.gif"), PhotoImage(file = "arrow_left.gif"), 
          PhotoImage(file = "zoom_in.gif"), PhotoImage(file = "zoom_out.gif"), 
          PhotoImage(file = "x_stretch.gif"), PhotoImage(file = "x_shrink.gif"),
          PhotoImage(file = "y_stretch.gif"), PhotoImage(file = "y_shrink.gif"),
          PhotoImage(file = "plot.gif")]

# Button init
b_u = Button(window_button, image = images[0], command = lambda: graph_move("u"))
b_r = Button(window_button, image = images[1], command = lambda: graph_move("r"))
b_d = Button(window_button, image = images[2], command = lambda: graph_move("d"))
b_l = Button(window_button, image = images[3], command = lambda: graph_move("l"))
b_zoomin_prop = Button(window_button, image = images[4], command = lambda: magnify(True, [0, 1]))
b_zoomout_prop = Button(window_button, image = images[5], command = lambda: magnify(False, [0, 1]))
b_zoomin_x = Button(window_button, image = images[6], command = lambda: magnify(True, [0]))
b_zoomout_x = Button(window_button, image = images[7], command = lambda: magnify(False, [0]))
b_zoomin_y = Button(window_button, image = images[8], command = lambda: magnify(True, [1]))
b_zoomout_y = Button(window_button, image = images[9], command = lambda: magnify(False, [1]))
b_plot = Button(window_button, image = images[10], command = lambda: graph_plot(graph_interpolate(polynom)))



b_u.grid(row = 0, column = 1)
b_r.grid(row = 1, column = 2)
b_d.grid(row = 2, column = 1)
b_l.grid(row = 1, column = 0)
b_zoomin_prop.grid(row = 3, column = 1)
b_zoomout_prop.grid(row = 3, column = 2)
b_zoomin_x.grid(row = 0, column = 0)
b_zoomout_x.grid(row = 2, column = 0)
b_zoomin_y.grid(row = 0, column = 2)
b_zoomout_y.grid(row = 2, column = 2)
b_plot.grid(row = 3, column = 0)
window_button.grid(row = 0, column = 0)

graph_global.pack()
window_graph.grid(row = 0, column = 1)
application.mainloop()
