'''
Jared Bawden
Project - Balanced Binary Search Tree
'''

from recursioncounter import RecursionCounter

class Node:
    ''' node class '''

    def __init__(self, data, left_child=None, right_child=None):
        ''' contructor for node class '''
        self.data = data
        self.left_child = left_child
        self.right_child = right_child
        self.height = 0

    def is_leaf(self):
        ''' return if the node is a leaf '''
        if self.left_child is None and self.right_child is None:
            return True
        return False

    def update_height(self):
        ''' update height of node '''
        if self.left_child is None:
            left = -1
        else:
            left = self.left_child.height
        if self.right_child is None:
            right = -1
        else:
            right = self.right_child.height
        self.height = max(left, right) + 1

    def __str__(self):
        ''' string method for node class '''
        if self.is_leaf():
            return f'{self.data} (0) [leaf]'
        return f'{self.data} ({self.height})'

class BinarySearchTree:
    ''' binary search tree class '''

    def __init__(self):
        ''' constructor '''
        self.root = None

    def is_empty(self):
        ''' return True if empty, False otherwise '''
        if self.root is None:
            return True
        return False

    def add(self, data):
        ''' adds a node with value data to the tree '''
        def add_helper(cursor, data):
            RecursionCounter()
            if cursor is None:
                return Node(data)
            if data < cursor.data:
                cursor.left_child = add_helper(cursor.left_child, data)
            else:
                cursor.right_child = add_helper(cursor.right_child, data)
            cursor.update_height()
            return cursor
        self.root = add_helper(self.root, data)

    def find(self, data):
        ''' return the matched item. If item is not in tree, return None '''
        def find_helper(cursor, data):
            RecursionCounter()
            if cursor is None:
                return None
            if cursor.data == data:
                return cursor
            left = find_helper(cursor.left_child, data)
            right = find_helper(cursor.right_child, data)
            if left is not None:
                return left
            if right is not None:
                return right
            return None
        return find_helper(self.root, data)

    def remove(self, data):
        ''' remove an item from tree'''
        def remove_helper(cursor, data):
            RecursionCounter()
            while cursor is not None:
                if cursor.data == data:
                    if cursor.is_leaf() is False:
                        if cursor.left_child is None:
                            return cursor.right_child
                        if cursor.right_child is None:
                            return cursor.left_child
                        successor = cursor.right_child
                        while successor.left_child is not None:
                            successor = successor.left_child
                        successor_data = successor.data
                        remove_helper(cursor, successor_data)
                        cursor.data = successor_data
                        cursor.update_height()
                        return cursor
                    return None
                cursor.left_child = remove_helper(cursor.left_child, data)
                cursor.right_child = remove_helper(cursor.right_child, data)
                cursor.update_height()
                return cursor
            return None
        self.root = remove_helper(self.root, data)

    def preorder(self):
        ''' return a list containing the tree's data in pre-order '''
        def preorder_helper(cursor, lyst):
            RecursionCounter()
            if cursor is None:
                return
            lyst.append(cursor.data)
            preorder_helper(cursor.left_child, lyst)
            preorder_helper(cursor.right_child, lyst)
        lyst = []
        preorder_helper(self.root, lyst)
        return lyst

    def height(self):
        ''' return the height of the tree '''
        if self.root is None:
            return -1
        return self.root.height

    def __str__(self):
        ''' string method for binarysearchtree class '''
        def print_helper(cursor, offset):
            RecursionCounter()
            if cursor is None:
                return f'{offset}[Empty]'
            if cursor.is_leaf():
                return f'{offset}{cursor}'
            return f"{offset}{cursor}\n{print_helper(cursor.left_child, offset+'   ')}\n{print_helper(cursor.right_child, offset+'   ')}"
        return print_helper(self.root, '')

    def __len__(self):
        ''' return the number of items in the tree'''
        def length_helper(cursor):
            RecursionCounter()
            if cursor is None:
                return 0
            while not cursor.is_leaf():
                return 1 + length_helper(cursor.right_child) + length_helper(cursor.left_child)
            return 1
        if self.root is not None:
            return length_helper(self.root)
        return 0

    def inorder(self):
        ''' inorder function '''
        def inorder_helper(cursor):
            if cursor is None:
                return
            yield from inorder_helper(cursor.left_child)
            yield cursor.data
            yield from inorder_helper(cursor.right_child)

        yield from inorder_helper(self.root)

    def rebalance_tree(self):
        ''' rebalance binary tree '''
        inorder = list(self.inorder())
        self.root = self.rebalance_tree_helper(inorder, 0, len(inorder)-1)

    def rebalance_tree_helper(self, data, low, high):
        ''' rebalance helper '''
        if low > high:
            return None 
        mid = (low + high)//2
        cursor = Node(data[mid])
        cursor.left_child = self.rebalance_tree_helper(data, low, mid-1)
        cursor.right_child = self.rebalance_tree_helper(data, mid+1, high)
        cursor.update_height()
        return cursor
