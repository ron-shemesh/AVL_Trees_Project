#Name1: Ron Shemesh
#Name2: Roee Shlain


"""A class represnting a node in an AVL tree"""
import math


class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = self.Virtual_builder(self)     #create virtualNode
		self.right = self.Virtual_builder(self)    #create virtualNode
		self.parent = None
		self.height = 0


	def Virtual_builder(self,AVLNode): #to create a virtualNode, insert "AVLNode" - parent
		virtual_node = AVLVirtualNode(self)
		return virtual_node

	"""returns whether self is not a virtual node 
		complexity: O(1)
		@rtype: bool
		@returns: False if self is a virtual node, True otherwise.
		"""

	def is_real_node(self):
		return True

	"""calculates the balance factor of a node
		complexity : O(1)
		@rtype: int
		@returns: a value for that stands for balance factor
		"""
	def bfac(self):
		return abs(self.right.height - self.left.height)




class AVLVirtualNode(object):
	def __init__(self,parent):
		self.key = None
		self.value = None
		self.left = None
		self.right = None
		self.parent = parent
		self.height = -1
		self.size = 0 # for testing purposes


	def is_real_node(self): #return is adjusted to virtual nodes
		return False




"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.
	"""
	def __init__(self):
		self.root = None
		#self.root.parent = None
		#self.size = 1
		self.max = None

	"""function sets to an existing node a new root for a given node
	complexity: O(log(n))
	"""
	def set_root(self, AVLNode):
		self.root = AVLNode
		while (AVLNode.right.key != None):
			AVLNode = AVLNode.right
		self.max = AVLNode


	""" searches the parent of the desired key location
	
	complexity: O(log(n))
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""

	def search_parent(self, key):
		if (self.get_root() is None):
			return None, -1
		node = self.root
		search_len = 1
		while (node.key != None):
			if (key == node.key):
				return (node.parent, search_len)
			elif (key < node.key):
				node = node.left
				search_len += 1
			elif (key > node.key):
				node = node.right
				search_len += 1
		return node.parent, search_len



	"""searches for a node in the dictionary corresponding to the key (starting at the root)
    complexity: O(log(n))    
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def search(self, key):
		if(self.get_root() is None):
			return None, -1
		if (key == self.root.key):
			return (self.root, 1)
		x,y = self.search_parent(key)
		if x.key == None:
			return None, -1
		else:
			if (x.key < key):
				if (x.right.key != None):
					return (x.right, y+1)
				else:
					return (None, -1)
			else:
				if (x.left.key != None):
					return (x.left, y)
				else:
					return (None, -1)


	"""searches for a node in the dictionary corresponding to the key, starting at the max
    
    complexity: O(log(n))    
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def finger_search(self, key):
		search_len = 1
		if (key == self.get_root().key):
			node = self.max
			while (node.key != self.get_root().key):
				node=node.parent
				search_len += 1
			return (self.get_root(), search_len)
		x,y = self.finger_search_parent(key)
		if (x.key < key):
			if (x.right.key != None):
				return (x.right, y-1)
			else:
				return (None, -1)
		else:
			if (x.left.key != None):
				return (x.left, y+1)
			else:
				return (None, -1)

	"""finger searches the parent of the desired key location

	complexity: O(log(n))
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the max node and ending node+1.
	"""
	def finger_search_parent(self, key):
		node = self.max
		search_len = 1
		if (key > node.key):
			return (node, 1)
		while (node.key != None):
			if (key == node.key):
				return (node.parent, search_len+1)
			elif (key < node.key):				# in case we need to keep going up the tree
				if (node.parent != None):
					node = node.parent
					search_len += 1
				else:	# in case we reach the tree root
					(x, y) = self.search_parent(key)
					if (node.key < key):
						return (x, search_len+y-2)
					else:
						return (x, search_len+y-2)
			else:
				subTree = AVLTree()
				subTree.set_root(node)
				(x, y) = subTree.search_parent(key)
				if (key< self.get_root().key):
					return (x, search_len + y - 1)
				else:
					return (x, search_len + y - 3)
		return None, -1



	"""inserts a new node into the dictionary with corresponding key and value (starting at the root)
	
	complexity: O(log(n))
	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def insert(self, key, val):
		if(self.get_root() == None):
			node = AVLNode(key, val)
			self.set_root(node)
			return node, 1, 0
		node,search_len = self.search_parent(key)
		node_ret, count_ret = self.perform_insert(key, val, node)
		node, search_len = self.search_parent(key)
		return node_ret, search_len, count_ret

	"""performas an insertion for a node in a specific location
	
	complexity: O(log(n))
	@type key: int
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int)"""
	def perform_insert(self, key, val, pointer):
		if (self.root == None):
			self.set_root(AVLNode(key, val))
		node = pointer
		node_to_insert = AVLNode(key, val)
		count = 0;
		self.update_max(node_to_insert)
		if node.key < key:
			node.right = node_to_insert
			node.right.parent = node
		else:
			node.left = node_to_insert
			node.left.parent = node
		while (node != None):
			old_height = node.height
			node.height = max(node.left.height,node.right.height)+1
			if (old_height == node.height):
				break
			else:
				if (node.bfac() < 2):
					count+=1
					node = node.parent
				else:
					self.rebalance(node)
		return node_to_insert, count

	"""performs right rotation
	
	complexity: O(1)
	@type node: AVLNode
	@param: parent of rotation
	@returns: None"""
	def rotate_right(self, node):
		origin_left = node.left
		if (node.parent != None):
			origin_father = node.parent
			origin_left.parent = origin_father
			if(origin_left.key < origin_father.key):
				origin_father.left = origin_left
			else:
				origin_father.right = origin_left
		else:
			self.root = origin_left
			origin_left.parent = None
		node.parent = origin_left
		node.left = origin_left.right
		origin_left.right.parent = node
		origin_left.right = node
		node.height = max(node.left.height, node.right.height) +1
		origin_left.height = max(origin_left.left.height, origin_left.right.height) +1
		return origin_left

	"""performs left rotation
		
		complexity: O(1)
		@type node: AVLNode
		@param: parent of rotation
		@returns: None"""
	def rotate_left(self,node):
		origin_right = node.right
		if (node.parent != None):
			origin_father = node.parent
			origin_right.parent = origin_father
			if (origin_right.key < origin_father.key):
				origin_father.left = origin_right
			else:
				origin_father.right = origin_right
		else:
			self.root = origin_right
			origin_right.parent = None
		node.parent = origin_right
		node.right = origin_right.left
		node.right.parent = node
		origin_right.left = node
		origin_right.left.parent = origin_right
		node.height = max(node.left.height, node.right.height) + 1
		origin_right.height = max(origin_right.left.height, origin_right.right.height) + 1
		return origin_right

	"""inserts a new node into the dictionary with corresponding key and value, starting at the max
	complexity: O(log(n))
	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def finger_insert(self, key, val):
		if(self.get_root() == None):
			node = AVLNode(key, val)
			self.set_root(node)
			return node, 1, 0
		node, search_len = self.finger_search_parent(key)
		node_ret, count_ret = self.perform_insert(key, val, node)
		node, search_len = self.finger_search(key)
		return node_ret, search_len, count_ret

	"""verifies which case of imbalanced vertices, for each case performs the right set of rotations
	complexity: O(1)
	"""
	def rebalance(self, node):
		if (node.left.height > node.right.height):
			if (node.left.left.height >= node.left.right.height):
				node = self.rotate_right(node)
			else:
				self.rotate_left(node.left)
				node = self.rotate_right(node)
		# rotate left node.left.right to node.left and then rotate right like before
		else:
			if (node.right.right.height >= node.right.left.height):
				node = self.rotate_left(node)
			# rotate left node.right to node
			else:
				self.rotate_right(node.right)
				node = self.rotate_left(node)
		# rotate right node.right.left to node.right and then rotate left like before and check if need to break
		return node

	"""deletes node from the dictionary
	
	complexity: O(log(n))
	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node):
		if (node.key == self.max.key):
			if (node.parent != None):
				self.max = node.parent
			else:
				self.max = node.left

		if (node.height == 0):
			if (node.key == self.get_root().key):
				self.root = AVLNode(None,None)
				self.max = None
			else:
				father = node.parent
				if (node.key < father.key):
					father.left = AVLVirtualNode(father)
				else:
					father.right = AVLVirtualNode(father)
			# check heights
		else:
			heir, isPre = self.to_replace(node)
			father = heir.parent
			if (father == node):
				if (node.parent == None):
					if (isPre):
						heir.right = node.right
						node.right.parent = heir
						self.set_root(heir)
						self.max = heir
					else:
						heir.left = node.left
						heir.left.parent = heir
						self.set_root(heir)
				else:
					if(node.key < node.parent.key):
						node.parent.left = heir
						heir.parent = node.parent
						father = heir
					else:
						node.parent.right = heir
						heir.parent = node.parent
						father = heir
					if (isPre):
						heir.right = node.right
						heir.right.parent = heir
					else:
						heir.left = node.left
						heir.left.parent = heir
				heir.height = max(heir.left.height, heir.right.height) + 1
				if (node.parent != None):
					node.parent.height = max(node.parent.right.height, node.parent.left.height)+1
			else:
				if (node.parent == None):
					if (not isPre):
						if (heir.right.key != None):
							father.left = heir.right
							father.left.parent = father
						else:
							father.left = AVLVirtualNode(father)
						father.height = max(father.left.height, father.right.height) + 1
					else:
						if (heir.left.key != None):
							father.right = heir.left
							father.right.parent = father
						else:
							father.right = AVLVirtualNode(father)
						father.height = max(father.right.height, father.left.height) + 1
				node.key = heir.key
				node.value = heir.value
				if (not isPre):
					if (heir.right.key != None):
						father.left = heir.right
						father.left.parent = father
					else:
						father.left = AVLVirtualNode(father)
					father.height = max(father.left.height, father.right.height) +1
				else:
					if (heir.left.key != None):
						father.right = heir.left
						father.right.parent = father
					else:
						father.right = AVLVirtualNode(father)
					father.height = max(father.right.height, father.left.height) + 1
		while (father.parent != None):
			if (father.bfac() == 1):
				return None
			elif (father.bfac() == 0):
				if (father.height > max(father.right.height, father.left.height) + 1):
					father.height -= 1
					father = father.parent
				else:
					return None
			else:
				if (father.right.height > father.left.height):
					if(father.right.bfac() == 0):
						self.rotate_left(father)
						return None
					else:
						if(father.right.right.height > father.right.left.height):
							self.rotate_left(father)
							father = father.parent
						else:
							self.rotate_right(father.right)
							self.rotate_left(father)
							father = father.parent
				else:
					if (father.left.bfac() == 0):
						self.rotate_right(father)
						return None
					else:
						if (father.left.right.height > father.left.left.height):
							self.rotate_left(father)
							father = father.parent
						else:
							self.rotate_right(father)
							father = father.parent
		return None


	"""joins self with item and another AVLTree
	
	complexity: O(log(n))
	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: the key separting self and tree2
	@type val: string
	@param val: the value corresponding to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
	or the opposite way
	"""

	def join(self, tree2, key, val):
		s_tree = self  # smaller keys tree
		b_tree = tree2  # bigger keys tree
		if (self.get_root() == None or tree2.get_root() == None):
			if (tree2.get_root() == None):
				return self
			else:
				self.root = tree2.get_root()
				self.max = tree2.max_node()
				tree2.root = None
				return self
		if (self.max.key < tree2.max.key):
			self.max = tree2.max_node()
		connector_node = AVLNode(key, val)
		if (self.get_root().key > tree2.get_root().key):  # normalize one tree as the smaller keys tree
			s_tree = tree2
			b_tree = self
		if (s_tree.get_root().height == b_tree.get_root().height):
			# case 0 - heights are equal
			connector_node.right = b_tree.get_root()
			b_tree.get_root().parent = connector_node
			connector_node.left = s_tree.get_root()
			s_tree.get_root().parent = connector_node
			connector_node.height = max(connector_node.left.height, connector_node.right.height) + 1
			self.set_root(connector_node)
			return self
		elif (s_tree.get_root().height < b_tree.get_root().height):  # case 1 - smaller tree is also shorter
			running_node = b_tree.get_root()  # this node will match the lower root height
			while (running_node.height > s_tree.get_root().height):  # start going down on bigger tree to find node with matching height
				running_node = running_node.left
			running_parent = running_node.parent
			connector_node.left = s_tree.get_root()
			connector_node.right = running_node
			s_tree.get_root().parent = connector_node
			running_node.parent = connector_node  # now connector is set with valid children
			running_parent.left = connector_node
			connector_node.parent = running_parent  # now connector is set as child of prev running parent
			connector_node.height = max(connector_node.left.height, connector_node.right.height)
		elif (s_tree.get_root().height > b_tree.get_root().height):  # case 2 - smaller tree is higher
			running_node = s_tree.get_root()  # this node will match the lower root height
			while (running_node.height > b_tree.get_root().height):  # start going down on bigger tree to find node with matching height
				running_node = running_node.right
			running_parent = running_node.parent
			connector_node.right = b_tree.get_root()
			connector_node.left = running_node
			b_tree.get_root().parent = connector_node
			running_node.parent = connector_node  # now connector is set with valid children
			running_parent.right = connector_node
			connector_node.parent = running_parent  # now connector is set as child of prev running parent
			connector_node.height = max(connector_node.right.height, connector_node.left.height)+1
			"check running_parent children balance factor and height differences of them with parent, and rebalance/promote accordingly"
		# after both cases now the nodes are set
		while (running_parent.key is not None):
			running_parent.height = max(running_parent.left.height, running_parent.right.height)+1
			old_height = running_parent.height
			if (running_parent.bfac()) > 1:  # Balance factor check
				self.rebalance(running_parent)
			if running_parent.height == old_height:  # Stop if height hasn't changed
				break
			running_parent = running_parent.parent

		while(running_parent.parent is not None):
			running_parent = running_parent.parent
		# Update root reference
		self.set_root(running_parent)
		tree2.set_root(AVLNode(None,None))
		return self


	"""splits the dictionary at a given node
	
	complexity: O(log(n))
	@type node: AVLNode
	@pre: node is in self
	@param node: the node in the dictionary to be used for the split
	@rtype: (AVLTree, AVLTree)
	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node):
		if (node.key == None):
			return self
		if(node == self.root and node.height == 0):
			tree = AVLTree()
			tree2 = AVLTree()
			return tree,tree2
		key = node.key
		smaller = None
		bigger = None
		was_right = False
		was_left = False
		# setting roots if aligning children exist
		if (node.right.key != None):
			bigger = AVLTree()
			bigger.set_root(node.right)
			bigger.root.parent = None
			bigger_start = True
		else:
			bigger_start = False
		if (node.left.key != None):
			smaller = AVLTree()
			smaller.set_root(node.left)
			smaller.root.parent = None
			smaller_start = True
		else:
			smaller_start = False
		# checking weather the splitting node is the root
		if (node.parent == None):
			return (smaller, bigger)
		count = 0
		while node.parent is not None:
			if node.parent.key < node.key:
				was_right = True
			elif node.parent.key > node.key:
				was_left = True
			node = node.parent
			if was_right:
				node.right = AVLVirtualNode(node)
				if not smaller_start:
					if (node.left.is_real_node()):
						smaller = AVLTree()
						smaller.set_root(node.left)
						smaller.get_root().parent = None
						smaller.insert(node.key, node.value)
					else:
						smaller = AVLTree()
						smaller.set_root(AVLNode(node.key, node.value))
					smaller_start = True
				else:
					if (node.left.is_real_node()):
						tmp = AVLTree()
						tmp.set_root(node.left)
						tmp.get_root().parent = None
						smaller.join(tmp, node.key, node.value)
					else:
						smaller.insert(node.key, node.value)
			if was_left:
				node.left = AVLVirtualNode(node)
				if not bigger_start:
					if (node.right.is_real_node()):
						count+=1
						bigger = AVLTree()
						bigger.set_root(node.right)
						bigger.get_root().parent = None
						bigger.insert(node.key, node.value)
					else:
						bigger = AVLTree()
						bigger.set_root(AVLNode(node.key, node.value))
					bigger_start = True
				else:
					if (node.right.is_real_node()):
						count+=1
						tmp = AVLTree()
						tmp.set_root(node.right)
						tmp.get_root().parent = None
						bigger.join(tmp, node.key, node.value)
					else:
						count+=1
						bigger.insert(node.key, node.value)
			was_left = False
			was_right = False
		if (not smaller_start):
			if(not bigger_start):
				return AVLTree(), AVLTree()
			return AVLTree(), bigger
		if(not bigger_start):
			if (not smaller_start):
				return AVLTree(), AVLTree()
			return smaller,AVLTree()
		return smaller, bigger

	"""returns an array representing dictionary 
	
	complexity: O(מ)
	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		def rec_avl_to_array(node):  # recursive entering of keys and values by key in order
			if node.key == None:
				return []
			return rec_avl_to_array(node.left) + [(node.key, node.value)] + rec_avl_to_array(node.right)
		if (self.get_root() == None):
			return []
		node = self.get_root()
		return rec_avl_to_array(node)


	"""returns the node with the maximal key in the dictionary
	
	complexity: O(1)
	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	"""
	def max_node(self):
		return self.max

	"""checks if necessary to update max key node
	complexity: O(1)
	"""

	def update_max(self, node):
		if (self.max.key < node.key):
			self.max = node
		return None


	"""returns the number of items in dictionary 
	complexity: O(1)
	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		size = self.avl_to_array()
		return len(size)


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return self.root

	"""returns the succesor for a given node"""
	def to_replace(self, node):
		if (node.right.key == None):
			return (self.predecessor(node.left),True)
		else:
			return (self.successor(node.right), False)


	"""return min node for a given vertice"""
	def successor(self, node):
		while(node.left.key != None):
			node = node.left
		return node

	"""returns max node for a given vertice"""

	def predecessor(self, node):
		while (node.right.key != None):
			node = node.right
		return node


	def get_height(self, node):
		if not node:
			return 0
		return node.height

	def get_balance(self, node):
		if not node:
			return 0
		return self.get_height(node.left) - self.get_height(node.right)

	"""print - tree function: prints the tree to visualize inputs and outputs 
	**[ONLY HERE FOR TESTERS CONVIENIENCE IN CASE NEEDED]**
	
	
	def print_tree(self):
		if self.root == None:
			print('empty tree')
		# Tree visualization using only print and while
		queue = [(self.get_root(), 0)]  # Queue of (node, level) pairs
		prev_level = -1

		while queue:
			node, level = queue.pop(0)

			# Print level separator if we're on a new level
			if level != prev_level:
				if prev_level != -1:  # Avoid extra newline before the first level
					print()
				prev_level = level

			# Print the current node or "None" if the node is null
			if node:
				print(f"({node.key})", end=" ")
				queue.append((node.left, level + 1))
				queue.append((node.right, level + 1))
			else:
				print("None", end=" ")

		print()  # Final newline for clean output

"""



