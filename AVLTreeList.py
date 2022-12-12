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

	def __init__(self, value, isReal=True, height = 0, size = 1):
		self.value = value
		if(isReal):
			self.left = AVLNode(None, False, -1, 0)
			self.right = AVLNode(None, False, -1, 0)
			self.parent = AVLNode(None, False, -1, 0)
		else:
			self.left = None
			self.right = None
			self.parent = None
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

	def getSize(self):
		if self.is_real:
			return self.size
		return 0
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

	def setSize(self, s):
		self.size = s
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
		self.firstItem = None
		self.lastItem = None


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
			return self.Tree_select(i + 1).getValue()
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
		if 0 > i or i > n:
			return 0
		new_node = AVLNode(val)
		# if tree is empty
		if n == 0:
			return self.insert_first_node(new_node)
		# if insert first
		if i == 0:
			node_first = self.firstItem
			node_first.setLeft(new_node)
			new_node.setParent(node_first)
			self.firstItem = new_node
		# if insert last
		elif i == n:
			node_last = self.lastItem
			node_last.setRight(new_node)
			new_node.setParent(node_last)
			self.lastItem = new_node
		else:
			node_successor = self.Tree_select(i + 1)
			if not node_successor.getLeft().isRealNode():
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

	def insert_first_node(self, node):
		self.root = node
		self.firstItem = node
		self.lastItem = node
		self.size = 1
		return 0
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
			self.firstItem = self.successor(node)
		if i == n - 1:
			self.lastItem = self.predecessor(node)

		# if node is a leaf
		if not node.getLeft().isRealNode() and not node.getRight().isRealNode():
			return self.delete_leaf(node)
		# if node has one right child
		elif not node.getLeft().isRealNode():
			return self.delete_node_with_right_child(node)
		# if node has one left child
		elif not node.getRight().isRealNode():
			return self.delete_node_with_left_child(node)
		# if node has two children
		else:
			return self.delete_node_with_two_children(node, i)

	def delete_leaf(self, node):
		isRoot = (node == self.root)
		node_parent = node.getParent()
		if node_parent.getLeft() == node:
			node_parent.setLeft(AVLNode(None, False, -1, 0))
		else:
			node_parent.setRight(AVLNode(None, False, -1, 0))
		node.setParent(None)
		if isRoot:
			self.root = None
			self.lastItem = None
			self.firstItem = None
			self.size -= 1
			return 0
		self.size -= 1
		self.update_fields_till_root(node_parent)
		cnt_rotations = self.delete_fix_tree(node_parent)

		return cnt_rotations

	def delete_node_with_right_child(self, node):
		isRoot = (node == self.root)
		child = node.getRight()
		node_parent = node.getParent()
		child.setParent(node_parent)
		if node_parent.getLeft() == node:
			node_parent.setLeft(child)
		else:
			node_parent.setRight(child)
		node.setParent(None)
		node.setRight(None)
		if isRoot:
			self.root = child
			self.lastItem = child
			self.firstItem = child
			self.size -= 1
			self.update_fields(child)
			return 0
		self.size -= 1
		self.update_fields_till_root(node_parent)
		cnt_rotations = self.delete_fix_tree(node_parent)

		return cnt_rotations

	def delete_node_with_left_child(self, node):
		isRoot = (node == self.root)
		child = node.getLeft()
		node_parent = node.getParent()
		child.setParent(node_parent)
		if node_parent.getLeft() == node:
			node_parent.setLeft(child)
		else:
			node_parent.setRight(child)
		node.setParent(None)
		node.setLeft(None)
		if isRoot:
			self.root = child
			self.lastItem = child
			self.firstItem = child
			self.size -= 1
			self.update_fields(child)
			return 0
		self.size -= 1
		self.update_fields_till_root(node_parent)
		cnt_rotations = self.delete_fix_tree(node_parent)

		return cnt_rotations

	def delete_node_with_two_children(self, node, index):
		node_successor = self.successor(node)
		cnt_rotations = self.delete(index + 1)
		node_lchild = node.getLeft()
		node_rchild = node.getRight()
		node_parent = node.getParent()
		if node_parent.getLeft() == node:
			node_parent.setLeft(node_successor)
		else:
			node_parent.setRight(node_successor)

		node_lchild.setParent(node_successor)
		node_rchild.setParent(node_successor)
		node_successor.setRight(node_rchild)
		node_successor.setLeft(node_lchild)
		node_successor.setParent(node_parent)

		self.update_fields(node_successor)
		self.update_root(self.firstItem)

		return cnt_rotations


	def update_root(self, node):
		while(node.getParent().isRealNode()):
			node = node.getParent()
		self.root = node

	"""returns the value of the first item in the list

	@rtype: str
	@returns: the value of the first item, None if the list is empty
	"""
	def first(self):
		if self.firstItem is None:
			return None
		return self.firstItem.getValue()

	"""returns the value of the last item in the list

	@rtype: str
	@returns: the value of the last item, None if the list is empty
	"""
	def last(self):
		if self.lastItem is None:
			return None
		return self.lastItem.getValue()

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
		if self.size == 0:
			if lst.size == 0:
				return 0
			self = lst
			return lst.root.height
		if lst.size == 0:
			return self.root.height
		if self.root.height > lst.root.height:
			self.right_concat(lst)
		elif self.root.height < lst.root.height:
			self.left_concat(lst)
		else:
			self.same_height_concat(lst)
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
		if self.root is None:
			return None
		return self.root



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
		while(node.getRight().isRealNode()):
			node = node.getRight()
		return node

	def get_min(self, node):
		while(node.getLeft().isRealNode()):
			node = node.getLeft()
		return node

	def predecessor(self, node):
		if node.getLeft().isRealNode():
			return self.get_max(node.getLeft())
		par = node.getParent()
		while(par.isRealNode() and node == par.getLeft()):
			node = par
			par = node.getParent()
		return par

	def successor(self, node):
		if node.getRight().isRealNode():
			return self.get_min(node.getRight())
		par = node.getParent()
		while(par.isRealNode() and node == par.getRight()):
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
		node_parent = node.getParent()
		rl_node = r_node.getLeft()
		if node_parent.getLeft() == node:
			node_parent.setLeft(r_node)
		else:
			node_parent.setRight(r_node)
		r_node.setParent(node_parent)
		node.setParent(r_node)
		node.setRight(rl_node)
		rl_node.setParent(node)
		r_node.setLeft(node)
		if node == self.root:
			self.root = r_node

		self.update_fields(node)
		self.update_fields(r_node)

	def LR_rotation(self, node):
		l_node = node.getLeft()
		self.L_rotation(l_node)
		self.R_rotation(node)

	def R_rotation(self, node):
		l_node = node.getLeft()
		node_parent = node.getParent()
		lr_node = l_node.getRight()
		if node_parent.getLeft() == node:
			node_parent.setLeft(l_node)
		else:
			node_parent.setRight(l_node)
		l_node.setParent(node_parent)
		node.setParent(l_node)
		node.setLeft(lr_node)
		lr_node.setParent(node)
		l_node.setRight(node)
		if node == self.root:
			self.root = l_node

		self.update_fields(node)
		self.update_fields(l_node)

	def RL_rotation(self, node):
		r_node = node.getRight()
		self.R_rotation(r_node)
		self.L_rotation(node)

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
		while(y.isRealNode()):
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
		while(node.isRealNode()):
			self.update_size(node)
			node = node.getParent()

	# return the number of rotations
	def delete_fix_tree(self, node):
		cnt_rotations = 0
		y = node
		while(y.isRealNode()):
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
				y = y.getParent()

		return cnt_rotations

	def in_order(self, list):
		self.in_order_rec(list, self.root)

	def in_order_rec(self, list, node):
		if node.isRealNode():
			self.in_order_rec(list, node.getLeft())
			list.append(node.getValue())
			self.in_order_rec(list, node.getRight())

	def create_tree_from_sorted_array(self, arr):
		root = self.create_tree_from_sorted_array_rec(arr)
		tree = AVLTreeList()
		tree.root = root
		tree.size = len(arr)
		tree.firstItem = tree.get_min(tree.root)
		tree.lastItem = tree.get_max(tree.root)
		return tree

	def create_tree_from_sorted_array_rec(self, arr):
		if len(arr) == 0:
			return AVLNode(None, False, -1, 0)
		if len(arr) == 1:
			return AVLNode(arr[0], True, 0, 1)
		mid = int((len(arr))/2)
		node_parent = AVLNode(arr[mid])
		left = arr[:mid]
		right = arr[mid + 1:]
		l_child = self.create_tree_from_sorted_array_rec(left)
		r_child = self.create_tree_from_sorted_array_rec(right)
		node_parent.setRight(r_child)
		node_parent.setLeft(l_child)
		l_child.setParent(node_parent)
		r_child.setParent(node_parent)
		self.update_fields(node_parent)
		return node_parent

	def left_concat(self, lst):
		h1 = self.root.getHeight()
		r_node = lst.root
		while(r_node.getHeight() > h1):
			r_node = r_node.getLeft()
		l_node = self.root
		x = AVLNode(None)
		x_index = self.size
		self.join(l_node, x, r_node, "left")
		self.root = lst.root
		self.size += lst.size
		self.lastItem = lst.lastItem
		self.delete(x_index)

	def right_concat(self, lst):
		h2 = lst.root.getHeight()
		l_node = self.root
		while (l_node.getHeight() > h2):
			l_node = l_node.getRight()
		r_node = lst.root
		x = AVLNode(None)
		x_index = self.size
		self.join(l_node, x, r_node, "right")
		self.size += lst.size
		self.firstItem = lst.firstItem
		self.delete(x_index)

	def same_height_concat(self, lst):
		x = AVLNode(0)
		x_index = self.size
		a = self.root
		b = lst.root
		x.setLeft(a)
		x.setRight(b)
		a.setParent(x)
		b.setParent(x)
		self.root = x
		self.lastItem = lst.lastItem
		self.size += lst.size
		self.update_fields(x)
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





	""""""""""""""""""""""""""""""""""""""

	def printt(self):
		out = ""
		for row in self.printree(self.root):  # need printree.py file
			out = out + row + "\n"
		print(out)

	def printree(self, t, bykey=True):
		# for row in trepr(t, bykey):
		#        print(row)
		return self.trepr(t, False)

	def trepr(self, t, bykey=False):
		if t == None:
			return ["#"]

		thistr = str(t.key) if bykey else str(t.getValue())

		return self.conc(self.trepr(t.left, bykey), thistr, self.trepr(t.right, bykey))

	def conc(self, left, root, right):

		lwid = len(left[-1])
		rwid = len(right[-1])
		rootwid = len(root)

		result = [(lwid + 1) * " " + root + (rwid + 1) * " "]

		ls = self.leftspace(left[0])
		rs = self.rightspace(right[0])
		result.append(ls * " " + (lwid - ls) * "_" + "/" + rootwid *
					  " " + "\\" + rs * "_" + (rwid - rs) * " ")

		for i in range(max(len(left), len(right))):
			row = ""
			if i < len(left):
				row += left[i]
			else:
				row += lwid * " "

			row += (rootwid + 2) * " "

			if i < len(right):
				row += right[i]
			else:
				row += rwid * " "

			result.append(row)

		return result

	def leftspace(self, row):
		# row is the first row of a left node
		# returns the index of where the second whitespace starts
		i = len(row) - 1
		while row[i] == " ":
			i -= 1
		return i + 1

	def rightspace(self, row):
		# row is the first row of a right node
		# returns the index of where the first whitespace ends
		i = 0
		while row[i] == " ":
			i += 1
		return i

	def append(self, val):
		self.insert(self.length(), val)


T = AVLTreeList()
for i in range(100):
	T.append(i)
T.printt()
for i in range(99):
	if i % 5 == 0:
		print(0)
		T.delete(0)
	elif i % 5 == 1:
		print(T.length()-1 , T.size)
		T.delete(T.length()-1)
	elif i % 5 == 2:
		print((T.length()-1)//2)
		T.delete((T.length()-1)//2)
	elif i % 5 == 3:
		print((T.length()-1)//3)

		T.delete((T.length()-1)//3)
	else:
		print((T.length()-1)//7)

		T.delete((T.length()-1)//7)
	T.printt()
	print("root BF " + str(T.get_BF(T.root)))

