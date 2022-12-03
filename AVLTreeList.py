#username - complete info
#id1      - complete info
#name1    - complete info
#id2      - complete info
#name2    - complete info  



"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 

	@type value: str
	@param value: data of your node
	"""


	def __init__(self, value, isReal=True):
		self.value = value
		self.left = AVLNode(None, False)
		self.right = AVLNode(None, False)
		self.parent = AVLNode(None, False)
		self.height = -1 # Balance factor
		self.size = 0
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
		self.min = None


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

		if 0 > i or i > n:
			return 0

		new_node = AVLNode(val)
		if i == n:
			node_max = self.get_max()
			node_max.setRight(new_node)
			new_node.setParent(node_max)
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
		return -1


	"""returns the value of the first item in the list

	@rtype: str
	@returns: the value of the first item, None if the list is empty
	"""
	def first(self):
		return None

	"""returns the value of the last item in the list

	@rtype: str
	@returns: the value of the last item, None if the list is empty
	"""
	def last(self):
		return None

	"""returns an array representing list 

	@rtype: list
	@returns: a list of strings representing the data structure
	"""
	def listToArray(self):
		return None

	"""returns the size of the list 

	@rtype: int
	@returns: the size of the list
	"""
	def length(self):
		return None

	"""sort the info values of the list

	@rtype: list
	@returns: an AVLTreeList where the values are sorted by the info of the original list.
	"""
	def sort(self):
		return None

	"""permute the info values of the list 

	@rtype: list
	@returns: an AVLTreeList where the values are permuted randomly by the info of the original list. ##Use Randomness
	"""
	def permutation(self):
		return None

	"""concatenates lst to self

	@type lst: AVLTreeList
	@param lst: a list to be concatenated after self
	@rtype: int
	@returns: the absolute value of the difference between the height of the AVL trees joined
	"""
	def concat(self, lst):
		return None

	"""searches for a *value* in the list

	@type val: str
	@param val: a value to be searched
	@rtype: int
	@returns: the first index that contains val, -1 if not found.
	"""
	def search(self, val):
		return None



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

	def predecessor(self, node):
		if node.getLeft().isReal():
			return self.get_max(node.getLeft())
		par = node.getParent()
		while(par.isReal() and node == par.getLeft()):
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
			elif abs(BF) and prev_height != y.getHeight():
				y = y.getParent()
				continue
			else:
				self.check_and_rotate(y)
				cnt_rotations += 1

		return cnt_rotations