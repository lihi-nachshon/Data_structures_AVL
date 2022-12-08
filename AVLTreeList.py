#username - complete info
#id1      - complete info
#name1    - complete info
#id2      - complete info
#name2    - complete info  
import random


"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 

	@type value: str
	@param value: data of your node
	"""


	def __init__(self, value, isReal=True, height = -1, size = 1):
		self.value = value
		self.left = AVLNode(None, False)
		self.right = AVLNode(None, False)
		self.parent = AVLNode(None, False)
		self.height = height # Balance factor
		self.size = size
		self.is_real = isReal

	"""returns the left child
	@rtype: AVLNode
	@returns: the left child of self, None if there is no left child
	"""
	def getLeft(self):
		if self.is_real:
			return self.left
		return None


	"""returns the right child

	@rtype: AVLNode
	@returns: the right child of self, None if there is no right child
	"""
	def getRight(self):
		if self.is_real:
			return self.right
		return None

	"""returns the parent 

	@rtype: AVLNode
	@returns: the parent of self, None if there is no parent
	"""
	def getParent(self):
		return self.parent


	"""return the value

	@rtype: str
	@returns: the value of self, None if the node is virtual
	"""
	def getValue(self):
		if self.is_real:
			return self.value
		return None

	"""returns the height

	@rtype: int
	@returns: the height of self, -1 if the node is virtual
	"""
	def getHeight(self):
		if self.is_real:
			return self.height
		return -1


	"""sets left child

	@type node: AVLNode
	@param node: a node
	"""
	def setLeft(self, node):
		self.left = node

	"""sets right child

	@type node: AVLNode
	@param node: a node
	"""
	def setRight(self, node):
		self.right = node

	"""sets parent

	@type node: AVLNode
	@param node: a node
	"""
	def setParent(self, node):
		self.parent = node

	"""sets value

	@type value: str
	@param value: data
	"""
	def setValue(self, value):
		self.value = value

	"""sets the balance factor of the node

	@type h: int
	@param h: the height
	"""
	def setHeight(self, h):
		self.height = h

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def isRealNode(self):
		return self.is_real



"""
A class implementing the ADT list, using an AVL tree.
"""

class AVLTreeList(object):

	"""
	Constructor, you are allowed to add more fields.  

	"""
	def __init__(self):
		self.size = 0
		self.root = None
		self.first = None
		self.last = None


	"""returns whether the list is empty

	@rtype: bool
	@returns: True if the list is empty, False otherwise
	"""
	def empty(self):
		return self.size == 0


	"""retrieves the value of the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: index in the list
	@rtype: str
	@returns: the the value of the i'th item in the list
	"""
	def retrieve(self, i):
		if 0 <= i <= self.size:
			return self.Tree_select(i + 1)
		return None


	"""inserts val at position i in the list

	@type i: int
	@pre: 0 <= i <= self.length()
	@param i: The intended index in the list to which we insert val
	@type val: str
	@param val: the value we inserts
	@rtype: list
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def insert(self, i, val):
		n = self.size

		if 0 > i or i >= n:
			return 0

		new_node = AVLNode(val)
		if i == 0:
			self.first = new_node
		if i == n - 1:
			node_max = self.last
			node_max.setRight(new_node)
			new_node.setParent(node_max)
			self.last = new_node
		else:
			node_successor = self.Tree_select(i + 1)
			if not node_successor.getLeft().isReal():
				node_successor.setLeft(new_node)
				new_node.setParent(node_successor)
			else:
				node_predecessor = self.predecessor(node_successor)
				node_predecessor.setRight(new_node)
				new_node.setParent(node_predecessor)

		self.size += 1
		self.update_fields_till_root(new_node)
		cnt_rotations = self.insert_fix_tree(new_node)

		return cnt_rotations


	"""deletes the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: The intended index in the list to be deleted
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, i):
		n = self.size

		if 0 > i or i >= n:
			return -1

		node = self.Tree_select(i + 1)

		if i == 0:
			self.first = node.getParent()
		if i == n-1:
			self.last = self.predecessor(node)

		parent_of_deleted = node.getParent()
		# if node is a leaf
		if node.getLeft().isReal() == False and node.getRight().isReal() == False:
			parent = node.getParent()
			if parent.getLeft() == node:
				parent.setLeft(AVLNode(None, False))
			else:
				parent.setRight(AVLNode(None, False))
			node.setParent(None)
		# if node has one child
		elif node.getLeft().isReal() == False:
			child = node.getRight()
			parent = node.getParent()
			child.setParent(parent)
			if parent.getLeft() == node:
				parent.setLeft(child)
			else:
				parent.setRight(child)
			node.setParent(None)
			node.setRight(None)

		elif node.getRight().isReal() == False:
			child = node.getLeft()
			parent = node.getParent()
			child.setParent(parent)
			if parent.getLeft() == node:
				parent.setLeft(child)
			else:
				parent.setRight(child)
			node.setParent(None)
			node.setLeft(None)
		# if node has two children
		else:
			node_successor = self.successor(node)
			parent_of_deleted = node_successor.getParent()
			child = node_successor.getRight()
			parent = node_successor.getParent()
			child.setParent(parent)
			if parent.getLeft() == node_successor:
				parent.setLeft(child)
			else:
				parent.setRight(child)

			node_successor.setRight(node.getRight())
			node_successor.setLeft(node.getLeft())
			node_successor.setParent(node.getParent())
			node.setParent(None)
			node.setLeft(None)
			node.setRight(None)

		self.size -= 1
		self.update_fields_till_root(parent_of_deleted)
		cnt_rotations = self.delete_fix_tree(parent_of_deleted)

		return cnt_rotations

	"""returns the value of the first item in the list

	@rtype: str
	@returns: the value of the first item, None if the list is empty
	"""
	def first(self):
		if self.size == 0:
			return None
		return self.first

	"""returns the value of the last item in the list

	@rtype: str
	@returns: the value of the last item, None if the list is empty
	"""
	def last(self):
		if self.size == 0:
			return None
		return self.last

	"""returns an array representing list 

	@rtype: list
	@returns: a list of strings representing the data structure
	"""
	def listToArray(self):
		list = []
		if self.size > 0:
			self.in_order(list)
		return list

	"""returns the size of the list 

	@rtype: int
	@returns: the size of the list
	"""
	def length(self):
		return self.size

	"""sort the info values of the list

	@rtype: list
	@returns: an AVLTreeList where the values are sorted by the info of the original list.
	"""
	def sort(self):
		arr = self.listToArray()
		arr.sort()
		return self.create_tree_from_sorted_array(arr)

	"""permute the info values of the list 

	@rtype: list
	@returns: an AVLTreeList where the values are permuted randomly by the info of the original list. ##Use Randomness
	"""
	def permutation(self):
		arr = self.listToArray()
		random.shuffle(arr)
		return self.create_tree_from_sorted_array(arr)

	"""concatenates lst to self

	@type lst: AVLTreeList
	@param lst: a list to be concatenated after self
	@rtype: int
	@returns: the absolute value of the difference between the height of the AVL trees joined
	"""
	def concat(self, lst):
		if self.root.height >= lst.root.height:
			self.right_concat(lst)
		else:
			self.left_concat(lst)
		return abs(self.root.height - lst.root.height)

	"""searches for a *value* in the list

	@type val: str
	@param val: a value to be searched
	@rtype: int
	@returns: the first index that contains val, -1 if not found.
	"""
	def search(self, val):
		arr = self.listToArray()
		return arr.index(val)



	"""returns the root of the tree representing the list

	@rtype: AVLNode
	@returns: the root, None if the list is empty
	"""
	def getRoot(self):
		return None


	#auxiliary functions

	#returns the K-th item
	def Tree_select(self, k):
		return self.Tree_select_rec(self.root, k)

	def Tree_select_rec(self, node, k):
		curr_rank = node.getLeft().getSize() + 1
		if k == curr_rank:
			return node
		elif k < curr_rank:
			return self.Tree_select_rec(node.getLeft(), k)
		else:
			return self.Tree_select_rec(node.getRight(), k - curr_rank)

	def get_max(self, node):
		while(node.getRight().isReal()):
			node = node.getRight()
		return node

	def get_min(self, node):
		while(node.getLeft().isReal()):
			node = node.getLeft()
		return node

	def predecessor(self, node):
		if node.getLeft().isReal():
			return self.get_max(node.getLeft())
		par = node.getParent()
		while(par.isReal() and node == par.getLeft()):
			node = par
			par = node.getParent()
		return par

	def successor(self, node):
		if node.getRight().isReal():
			return self.get_min(node.getRight())
		par = node.getParent()
		while(par.isReal() and node == par.getRight()):
			node = par
			par = node.getParent()
		return par

	def update_size(self, node):
		node.setSize(node.getLeft().getSize() + node.getRight().getSize() + 1)

	def update_height(self, node):
		node.setHeight(max(node.getLeft().getHeight(), node.getRight().getHeight()) + 1)

	def update_fields(self, node):
		self.update_height(node)
		self.update_size(node)

	def get_BF(self, node):
		return node.getLeft().getHeight() - node.getRight().getHeight()

	def L_rotation(self, node):
		r_node = node.getRight()
		r_node.setParent(node.getParent())
		node.setParent(r_node)
		node.setRight(r_node.getLeft())
		r_node.setLeft(node)

		self.update_fields(node)
		self.update_fields(r_node)

	def LR_rotation(self, node):
		l_node = node.getLeft()
		rl_node = l_node.getRight()
		self.L_rotation(l_node)
		self.R_rotation(rl_node)

	def R_rotation(self, node):
		l_node = node.getLeft()
		l_node.setParent(node.getParent())
		node.setParent(l_node)
		node.setLeft(l_node.getRight())
		l_node.setRight(node)

		self.update_fields(node)
		self.update_fields(l_node)

	def RL_rotation(self, node):
		r_node = node.getRight()
		lr_node = r_node.getLeft()
		self.R_rotation(r_node)
		self.L_rotation(lr_node)

	def check_and_rotate(self, node):
		BF = self.get_BF(node)
		if BF == -2:
			BF_r = self.get_BF(node.getRight())
			if BF_r == -1 or BF_r == 0:
				self.L_rotation(node)
			if BF_r == 1:
				self.RL_rotation(node)
		if BF == 2:
			BF_l = self.get_BF(node.getLeft())
			if BF_l == -1:
				self.LR_rotation(node)
			if BF_l == 1 or BF_l == 0:
				self.R_rotation(node)

	# return the number of rotations
	def insert_fix_tree(self, node):
		cnt_rotations = 0
		y = node.getParent()
		while (y.isReal()):
			prev_height = y.getHeight()
			self.update_fields(y)
			BF = self.get_BF(y)
			if abs(BF) < 2 and prev_height == y.getHeight():
				break
			elif abs(BF) < 2 and prev_height != y.getHeight():
				y = y.getParent()
				continue
			else:
				self.check_and_rotate(y)
				cnt_rotations += 1
				break

		return cnt_rotations

	def update_fields_till_root(self, node):
		while(node.isReal()):
			self.update_fields(node)
			node = node.getParent()

	# return the number of rotations
	def delete_fix_tree(self, node):
		cnt_rotations = 0
		y = node
		while (y.isReal()):
			prev_height = y.getHeight()
			self.update_fields(y)
			BF = self.get_BF(y)
			if abs(BF) < 2 and prev_height == y.getHeight():
				break
			elif abs(BF) < 2 and prev_height != y.getHeight():
				y = y.getParent()
				continue
			else:
				self.check_and_rotate(y)
				cnt_rotations += 1

		return cnt_rotations

	def in_order(self, list):
		self.in_order_rec(list, self.root)

	def in_order_rec(self, list, node):
		if node.isReal():
			self.in_order_rec(list, node.getLeft())
			list.append(node.getValue())
			self.in_order_rec(list, node.getRight())

	def create_tree_from_sorted_array(self, arr):
		root = self.create_tree_from_sorted_array_rec(arr)
		tree = AVLTreeList()
		tree.root = root
		tree.size = len(arr)
		tree.first = tree.get_min()
		tree.last = tree.get_max()
		return tree

	def create_tree_from_sorted_array_rec(self, arr):
		if len(arr) == 0:
			return AVLNode(None, False)
		if len(arr) == 1:
			return AVLNode(arr[0], True, 0, 1)
		mid = int((len(arr))/2)
		parent = AVLNode(arr[mid])
		left = arr[:mid]
		right = arr[mid + 1:]
		l_child = self.create_tree_from_sorted_array_rec(left)
		r_child = self.create_tree_from_sorted_array_rec(right)
		parent.setRight(r_child)
		parent.setLeft(l_child)
		l_child.setParent(parent)
		r_child.setParent(parent)
		self.update_fields(parent)
		return parent

	def left_concat(self, lst):
		h1 = self.root.getHeight()
		r_node = lst.root
		while(r_node.getHeight() > h1):
			r_node = r_node.getLeft()
		l_node = self.root
		x = AVLNode(None)
		x_index = self.size + 1
		self.join(l_node, x, r_node, "left")
		self.root = lst.root
		self.size = lst.size
		self.last = lst.last
		self.delete(x_index)

	def right_concat(self, lst):
		h2 = lst.root.getHeight()
		l_node = self.root
		while (l_node.getHeight() > h2):
			l_node = l_node.getRight()
		r_node = lst.root
		x = AVLNode(None)
		x_index = self.size + 1
		self.join(r_node, x, l_node, "right")
		self.first = lst.first
		self.delete(x_index)

	def join(self, a, x, b, dir):
		x.setLeft(a)
		x.setRight(b)
		c = b.getParent()
		a.setParent(x)
		b.setParent(x)
		x.setParent(c)
		if dir == "left":
			c.setLeft(x)
		else:
			c.setRight(x)
		self.update_fields_till_root(x)
		self.insert_fix_tree(c)
