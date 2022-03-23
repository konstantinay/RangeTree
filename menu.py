import csv
import random
import string
import range_tree as rt
import hospitals_rt as hos

#### Functions ####

#gia tin print tree: pre-order traversal
def pre_order(root, string=""):
    if root:
        print(string + str(root.coords) + "|Name:" + str(root.name))
        pre_order(root.left, "\t" + string + "-left-")
        pre_order(root.right, "\t" + string + "-right-")

#gia tin range search: print result
def print_nodes(nodes_list):
	for node in nodes_list:
		print(str(node.coords) + "\t|\tName:" + str(node.name))
        
#euclidean distance variation for kNN - xwris riza
def euclidean_dist(pointa, pointb):
    return sum((pointa[i] - pointb[i]) ** 2 for i in range(rt.DIMENSIONS))

#kNN
#geitones (+1 gia ton eauto tou), to node, tou opoiou psaxnw tous geitones
#ti riza tou dentrou
def knn_algorithm(k, point, root):
    
    #tyxaia arxikopoihsh toy [[x_min, x_max],[y_min, y_max]] gia range search
    my_range = [[point.coords[0]-3, point.coords[0]+3],[point.coords[1]-3, point.coords[1]+3]]
    
    #range search sto arxiko diastima gyrw apo to simeio endiaferontos
    temp_nodes = rt.range_search(root, my_range)
    
    #ypologizoume tis apostaseis kathe komvou pou epestrepse to range search
    #apo to simeio endiaferontos kai sortaroume 
    temp_distances = [[euclidean_dist(point.coords, node.coords), node.name, node.coords] for node in temp_nodes]
    temp_distances = sorted(temp_distances)
    
    #prosarmozoume to diastima wste na psaxnoume aristera apo to x_min,y_min
    #kai deksia apo to x_max, y_max kai epanalamvanoume mexri na vroume k geitones
    while len(temp_nodes) < k:
        
        #pairnoume to max giati mporei na exoume vrei mono ton eauto tou
        #opote h apostash tha einai 0 
        my_range[0][1] += max(temp_distances[int(len(temp_distances)/2)][0],1)
        my_range[1][1] += max(temp_distances[int(len(temp_distances)/2)][0],1)
        my_range[0][0] -= max(temp_distances[int(len(temp_distances)/2)][0],1)
        my_range[1][0] -= max(temp_distances[int(len(temp_distances)/2)][0],1)
        
        temp_nodes = rt.range_search(root, my_range)
        temp_distances = [[euclidean_dist(point.coords, node.coords), node.name, node.coords] for node in temp_nodes]
        temp_distances = sorted(temp_distances)

    return temp_distances[0:k]

#### Menu ####

#dialegoume real h simulated data
choose_data = int(input("0 - Real Data\n1 - Simulated Data\n-> "))

my_nodes = []
nodes_counter = 0

if choose_data == 0:
    
    filename = 'data.csv'
    
    #diavazoume to arxeio kai dimiourgoume kateytheian node objects
    with open(filename, mode='r', encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            my_nodes.append(rt.Node([float(row[0].replace(',','.')), float(row[1].replace(',','.'))], row[2]))
            nodes_counter += 1
        print('Number of Nodes: ' + str(nodes_counter))
    
    #gia na mporoume na kanoume search me to name ston knn
    with open(filename, mode='r', encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        hosp = hos.put_into_list(csv_file)
        
else:
    #tyxaia string gia ta onomata twn simulated data
    string_len = 5
    chars = string.ascii_lowercase
    
    for j in range(0,int(input("Give the number of Nodes you want to create: "))):
        coords = []
        name = ''.join((random.sample(chars, string_len)))
        for k in range(0, rt.DIMENSIONS):
            coords.append(random.randint(0,10))
            nodes_counter += 1
    
        my_nodes.append(rt.Node(coords, name))

#sortaroume tis syntetagmenes twn komvwn kai ftiaxnoume to dentro
sorted_nodes = sorted(my_nodes, key=lambda l:(l.coords[0], l.coords[1]))
my_root, _ = rt.create_range_tree(sorted_nodes)

#menu gia tis diadikasies tou dentrou
print("\nMENU")
print("0 - Print Tree")
print("1 - Range Search")
print("2 - Insert Node")
print("3 - Delete Node")
print("4 - Update Node")
print("5 - kNN")
print("-1 - Exit Program\n")

choice = int(input())

while choice != -1:

    # Print Tree
    if choice == 0:
        print('-----------------------')
        pre_order(my_root)
        print('-----------------------')

    # Range Search
    elif choice == 1:
        my_range = []
        
        for d in range(rt.DIMENSIONS):
            d_range = []
            
            print("Give min coordinate for dimension " + str(d))
            d_range.append(float(input()))
            
            print("Give max coordinate for dimension " + str(d))
            d_range.append(float(input()))
            
            my_range.append(d_range)            
        print('-----------------------')
        
        res_list = rt.range_search(my_root, my_range)
        
        if len(res_list) == 0:
            print('-----------------------')
            print("Not Found!")
            print('-----------------------')
            
        else:
            print('-----------------------')
            print('Nodes found (' + str(len(res_list)) + ')')
            print_nodes(res_list)
            print('-----------------------')

    # Insert
    elif choice == 2:
        coords = []
        
        for d in range(rt.DIMENSIONS):
            print("Give coordinate for dimension " + str(d))
            coords.append(float(input()))
        
        name = input("Give your Hospital's name: ")
        print('-----------------------')
        
        my_root = rt.insert(my_root, rt.Node(coords, name))

    # Delete
    elif choice == 3:
        coords = []
        
        for d in range(rt.DIMENSIONS):
            print("Give coordinate for dimension " + str(d))
            coords.append(float(input()))
            
        print('-----------------------')
        
        my_root = rt.delete(my_root, coords)

    # Update
    elif choice == 4:
        coords = []
        new_coords = []
        
        for d in range (rt.DIMENSIONS):
            print("Give old coordinate for dimension " + str(d))
            coords.append(float(input()))
            
        print('-----------------------')
        
        for d in range (rt.DIMENSIONS):
            print("Give new coordinate for dimension " + str(d))
            new_coords.append(float(input()))
            
        print('-----------------------')
        
        my_root = rt.update(my_root, coords, new_coords)
    
    #kNN
    elif choice == 5:
        
        #real data
        if choose_data == 0:
            name = input("Give your Hospital's name: ")
            #k+1 giati perilamvanei kai ton eauto tou, distance = 0
            k = int(input("How many nearby hospitals do you want: ")) + 1
            
            pcoords = [0,0]
            flag = 0
            #elegxoume an uparxei
            for i in range(len(hosp)):
                if hosp[i].gaz_name == name:
                    pcoords[0] = hosp[i].latitude
                    pcoords[1] = hosp[i].longitude
                    flag = 1
                 
            if flag != 1:  
                print("Hospital doesn't exist.")
            
            else:
                #theloume ton komvo pou zitithike san node object
                res = rt.range_search(my_root, [[pcoords[0], pcoords[0]],[pcoords[1], pcoords[1]]])
                print('-----------------------')
                
                neighboring_hosp = knn_algorithm(k, res[0], my_root)
                
                for i in range(len(neighboring_hosp)):
                    print("|Distance:" + str(neighboring_hosp[i][0]) + "\t|\tName:" + str(neighboring_hosp[i][1]) + "\t|\tCoordinates:" + str(neighboring_hosp[i][2]))
                    print("\n")
                    
            print('-----------------------')
            
        else:
            pcoords = []
            
            for d in range(rt.DIMENSIONS):
                print("Give coordinate for dimension " + str(d))
                pcoords.append(int(input()))
            
            k = int(input("How many nearby nodes do you want: ")) + 1   #k+1 giati perilamvanei kai ton eauto tou, distance = 0
            if k > nodes_counter/2:     #node counter += 1 gia kathe coord
                print("Tree nodes = ", int(nodes_counter/2))
                k = int(nodes_counter/2)
                
            #theloume ton komvo pou zitithike san node object            
            res = rt.search(my_root, pcoords)
            print('-----------------------')
            
            k_neighbors = knn_algorithm(k, res[0], my_root)
            
            for i in range(len(k_neighbors)):
                print("|Distance:" + str(k_neighbors[i][0]) + "\t|\tName:" + str(k_neighbors[i][1]) + "\t|\tCoordinates:" + str(k_neighbors[i][2]))
            
            print('-----------------------')

    choice = int(input())