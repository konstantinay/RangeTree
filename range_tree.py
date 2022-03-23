#diastaseis dentrou
DIMENSIONS = 2

class Node:
	def __init__(self, coords, name=None, left=None, right=None, next_dimension=None):
		self.coords = coords
		self.name = name
		self.left = left
		self.right = right
		self.next_dimension = next_dimension


#eisodos: lista me tis syntetagmenes twn komvwn 
#eksodos: h riza tou dentrou kai mia lista gia ta dentra epomenis diastasis
def create_range_tree(nodes_list, dimension=0):

	if len(nodes_list) == 0 or dimension >= DIMENSIONS:
		return None, []

	#mesaio stoixeio gia riza dentrou
	mid = int(len(nodes_list)/2)
	root = nodes_list[mid]

    #aristero kai deksi ypodentro
	root.left, left_list = create_range_tree(nodes_list[:mid], dimension)
	root.right, right_list = create_range_tree(nodes_list[mid+1:], dimension)
    
    #gia tis epomenes diastaseis 
	merged_list = []

	if dimension + 1 < DIMENSIONS: #sti periptwsi mas tha stamatisei stis 2 diastaseis
		merged_list = merge(root, left_list, right_list, dimension + 1)

    #ftiaxnoume ti nea diastash me ta kainouria sorted nodes    
	root.next_dimension, _ = create_range_tree(merged_list, dimension + 1)

	return root, merged_list


#eisodos: riza kai duo sorted listes
#eksodos: mia sorted lista 
def merge(root, left_list, right_list, dimension=0):
    
    if dimension >= DIMENSIONS:
        return []
    
    final_list = []
    left_index = 0
    right_index = 0
    
    #theloume na enwsoume tis duo listes kratwntas to sort
    #kanoume xeirokinhta to sort twn syntetagmenwn opws me to lambda sto menu
    
    #oso uparxoun kai aristera kai deksia stoixeia
    while left_index < len(left_list) and right_index < len(right_list):
        if left_list[left_index].coords[dimension] < right_list[right_index].coords[dimension]:
            final_list.append(Node(left_list[left_index].coords, left_list[left_index].name))
            left_index = left_index + 1
        else:
            final_list.append(Node(right_list[right_index].coords, right_list[right_index].name))
            right_index = right_index + 1
            
    #an exoume mono aristera kai oxi deksia (mono i sinthiki 1)
    while left_index < len(left_list):
        final_list.append(Node(left_list[left_index].coords, left_list[left_index].name))
        left_index = left_index + 1
        
    #an exoume deksia kai oxi aristera (mono i sinthiki 2)
    while right_index < len(right_list):
    	final_list.append(Node(right_list[right_index].coords, right_list[right_index].name))
    	right_index = right_index + 1
        
    #afou ftiaksoume th lista theloume na vroume th thesh ths rizas
    #eite tha einai kapou mesa sto final list h sto telos
    for i in range(0, len(final_list)):
    	if root.coords[dimension] < final_list[i].coords[dimension]:
			#mesa
    		return final_list[:i] + [Node(root.coords, root.name)] + final_list[i:]
	
	#telos
    return final_list + [Node(root.coords, root.name)]


#eisodos: riza, neos komvos
#eksodos: h riza tou neou dentrou
def insert(root, node, dimension=0):
    #an eimaste se fyllo
	if root is None:
		node.next_dimension = Node(node.coords, node.name)
		return node
    
	#an den eimaste se fyllo
	if node.coords[dimension] <= root.coords[dimension]:
		root.left = insert(root.left, node, dimension)
	else:
		root.right = insert(root.right, node, dimension)
    
    #epomeni diastasi
	if dimension + 1 < DIMENSIONS:
		root.next_dimension = insert(root.next_dimension, Node(node.coords, node.name), dimension + 1)

	return root


#pio aristeros komvos - gia tin delete
#eisodos: komvos
#eksodos: pio aristeros komvos
def leftmost_node(node):
    while node.left is not None:
        node = node.left
    return node


#eisodos: riza, syntetagmenes komvou pros diagrafi
#eksodos: riza neou dentrou
def delete(root, delete_coords, dimension=0):
   
	if root is None:
		return None
    
    #an o komvos pros diagrafi einai mikroteros tis rizas paei sto aristero ypodentro
	if delete_coords[dimension] < root.coords[dimension]:
		root.left = delete(root.left, delete_coords, dimension)
        
    #an o komvos pros diagrafi einai megalyteros tis rizas paei sto deksi ypodentro
	elif delete_coords[dimension] > root.coords[dimension]:
		root.right = delete(root.right, delete_coords, dimension)
    
    #otan oi syntetagmenes aytis tis diastaseis einai ises
	else:
		if root.coords == delete_coords:
            #an den yparxoun paidia
			if root.left is None and root.right is None:
				root = None
				return None
            #an yparxei mono 1 paidi
			if root.left is None or root.right is None:
				temp = root.right if root.right is not None else root.left
				root = None
				return temp             #antikathistoume ti riza me to 1 paidi
            #an yparxoun 2 paidia
			else:
                #vriskoume to pio aristero node tou deksiou upodentrou kai antikathistoume
				temp = leftmost_node(root.right)
				root.coords = temp.coords
				root.name = temp.name
				root.right = delete(root.right, temp.coords, dimension)
				return root

		#duplicates: to iso tha paei aristera
		root.left = delete(root.left, delete_coords, dimension)
	
	if dimension + 1 < DIMENSIONS:
		root.next_dimension = delete(root.next_dimension, delete_coords, dimension + 1)

	return root


#otan theloume na vroume sygkekrimeno komvo
#eisodos: riza, syntetagmenes pou psaxnoume
#eksodos: lista me tous komvous pou exoun autes tis syntetagmenes
def search(root, coords, dimension=0):
    
	if root is None:
		return []
    
    #an oi syntetagmenes einai megalyteres tis rizas psaxnei deksia
	if coords[dimension] > root.coords[dimension]:
		return search(root.right, coords, dimension)
    #an oi syntetagmenes einai mikroteres tis rizas psaxnei aristera
	elif coords[dimension] < root.coords[dimension]:
		return search(root.left, coords, dimension)
    #alliws tha einai i riza - komvos pou psaxnoume
	else:
		nodes_list = []
		if root.coords == coords:
			nodes_list.append(root)
        
		return nodes_list + search(root.left, coords, dimension) #duplicates: to iso tha paei aristera


#vriskoume to split node - gia tin range search
#eisodos: riza, syntetagmenes gia to range
#eksodos: split node
def find_split_node(root, range_coords, dimension=0):    
	if root:
        #an to min megalytero tou root
		if range_coords[dimension][0] > root.coords[dimension]:
			return find_split_node(root.right, range_coords, dimension)
        #an to max mikrotero tou root
		elif range_coords[dimension][1] < root.coords[dimension]:
			return find_split_node(root.left, range_coords, dimension)
		else:
			#split node or None
			return root	
	return None


#an oi syntetagmenes anikoun sto given range - gia tin range search
#eisodos: syntetagmenes, given range
#eksodos: boolean
def is_in_range(coords, range_coords):    
	for d in range(0, DIMENSIONS):
        #mikroteri tou min h megalyterh tou max
		if coords[d] < range_coords[d][0] or coords[d] > range_coords[d][1]:
			return False	
	return True


#eisodos: riza, diastima anazitisis
#eksodos: lista komvwn mesa sto diastima
def range_search(root, range_coords, dimension=0):

	if root is None:
		return []

	#gia tis prwtes d-1 dimensions
	if dimension + 1 < DIMENSIONS:
        #vriskoume to split node - ekei pou xwrizei i anazitisi gia to min, max
		split_node = find_split_node(root, range_coords, dimension)

		if split_node is None:
			return []

		nodes_list = []
        
        #vazoume to split node stin lista
		if is_in_range(split_node.coords, range_coords):
			nodes_list.append(split_node)
        
        #ksekiname tin anazitisi aristera (min)
		left_child = split_node.left
		while left_child:
			if is_in_range(left_child.coords, range_coords):
				nodes_list.append(left_child)
            
            #an to min einai pio aristera
			if range_coords[dimension][0] <= left_child.coords[dimension]:
				#tha prepei na paroume ta deksia paidia tou kai stin epomeni diastasi
				if left_child.right:
					nodes_list += range_search(left_child.right.next_dimension, range_coords, dimension + 1)
                #kai na synexisoume aristera
				left_child = left_child.left
			else:
                #synexizoume deksia
				left_child = left_child.right
        
        #ksekiname tin anazitisi deksia (max)
		right_child = split_node.right
		while right_child:
			if is_in_range(right_child.coords, range_coords):
				nodes_list.append(right_child)
            
            #an to max einai pio deksia
			if right_child.coords[dimension] <= range_coords[dimension][1]:
                #tha prepei na paroume ta aristera paidia tou kai stin epomeni diastasi
				if right_child.left:
					nodes_list += range_search(right_child.left.next_dimension, range_coords, dimension + 1)
                #synexizoume deksia
				right_child = right_child.right
			else:
                #synexizoume aristera
				right_child = right_child.left

		return nodes_list

	#teleutaia diastasi - periorizoume sta katallhla shmeia
	if dimension + 1 == DIMENSIONS:
		if root.coords[dimension] < range_coords[dimension][0]:
			return range_search(root.right, range_coords, dimension)
		elif root.coords[dimension] > range_coords[dimension][1]:
			return range_search(root.left, range_coords, dimension)
		else:
            #diladi range_coords[dimension][0] <= root.coords[dimension] and root.coords[dimension] <= range_coords[dimension][1]:
			nodes_list = [root] + range_search(root.right, range_coords, dimension) + range_search(root.left, range_coords, dimension)
			return nodes_list


#eisodos: riza, syntetagmenes, nees syntetagmenes
#eksodos: riza neou dentrou
def update(root, coords, new_coords):
    
    #elegxos an uparxei o arxikos komvos
	node_to_update = search(root, coords)
	if len(node_to_update) == 0:
		print("Node NOT Found!")
		return root

	new_nodes = []
    #ftiaxnoume to neo node object
	for node in node_to_update:
		new_nodes.append(Node(new_coords, node.name))
    #diagrafoume to yparxon
	for node in node_to_update:
		root = delete(root, coords)
    #kanoume insert to neo
	for node in new_nodes:
	  root = insert(root, node)
	return root
