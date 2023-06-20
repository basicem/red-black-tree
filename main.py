class Node():
    def __init__(self, data):
        self.data = data  # holds the key
        self.parent = None #pointer to the parent
        self.left = None # pointer to left child
        self.right = None #pointer to right child
        self.color = 1 # 1 . Red, 0 . Black

class RedBlackTree():
    def __init__(self):
        self.TNULL  =  Node(0)
        self.root = self.TNULL 

    # rotate left at node x
    def left_rotate(self, x):
        y = x.right                 # set y
        x.right = y.left            # turn ys left subtree to xs rigth subtree
        if y.left != self.TNULL:    # parent of ys left subtree to x
            y.left.parent = x

        y.parent = x.parent         # link xs parent to y
        if x.parent == None:
            self.root = y           # if x has no parent y is root
        elif x == x.parent.left:    
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x                  # put x on ys left
        x.parent = y                # y is parent for x

    # rotate right at node x
    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # insert the key to the tree in its appropriate position
    # and fix the tree
    def insert(self, key):
        
        node = Node(key)
        node.parent = None
        node.data = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 1 # new node must be red

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        # y is parent of x
        node.parent = y
        if y == None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        if node.parent == None :                         # Root node is always Black
            node.color = 0
            return

        if node.parent.parent == None :                  # If parent of node is Root Node
            return

        # Fix the tree
        self.__fix_insert(node)

    def  __fix_insert(self, k):
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:   # if parent of k is right child 
                u = k.parent.parent.left            # uncle
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.left_rotate(k.parent.parent)
            else:                                   # parent of k is left child
                u = k.parent.parent.right           # uncle       

                if u.color == 1:                    # if uncle is red only change colors
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent             # k is parent of ks parent
                else:                               # if uncle is black rotation/s is/are needed
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0

    def __rb_transplant(self, u, v):
        if u.parent == self.TNULL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right  = v
        v.parent = u.parent
    
    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    def rb_delete(self, key):
        z = self.root
        while z != self.TNULL:                                  # Search for the node having value/data as parameter
            if z.data == key:
                break

            if z.data <= key :
                z = z.right
            else :
                z = z.left

            if z == self.TNULL :                                # If not present then can not delete
                print ( "Value not present!" )
                return

        y = z                                                   # Store the color of z node                                                       
        y_original_color = y.color                              
        if z.left == self.TNULL:                                # If left child of z is NUll assign right child of z to x
            x = z.right
            self.__rb_transplant(z, z.right)                    # Transplant node to be deleted with x
        elif z.right == self.TNULL:                             # If right child of z is NUll assign left child of z to x
            x = z.left
            self.__rb_transplant(z, z.left)                     # Transplant node to be deleted with x
        else:                                                   # If z has two children find minimum of the right subtree 
            y = self.minimum(z.right)
            y_original_color = y.color                          # store color of y
            x = y.right
            if y.parent == z:                                   # if y is child of z 
                x.parent = y                                    # set parent of x as y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.__rb_transplant(z, y)                          # set ys parent and its child
            y.left = z.left                                     # set left child of z do left child of y
            y.left.parent = y
            y.color = z.color                                   # set the color of z to y
        if y_original_color == 0:                               # if color was black then fixing is needed
            self.rb_delete_fixup(x)

    def rb_delete_fixup(self, x):
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == 1:
                    w.color =  0
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == 0 and w.right.color == 0:
                    w.color = 1
                    x = x.parent
                elif w.right.color == 0:
                    w.left.color = 0
                    w.color = 1
                    self.right_rotate(w)
                    w = x.parent.right
                w.color = x.parent.color
                x.parent.color = 0
                w.right.color = 0
                self.left_rotate(x.parent)
                x = self.root
            else:
                w = x.parent.left                         # Sibling of x
                if w.color == 1 :                         # if sibling is red
                    w.color = 0                           # Set its color to black
                    x.parent.color = 1                    # Make its parent red
                    self.right_rotate(x.parent)                  # Call for right rotate on parent of x
                    w = x.parent.left

                if w.right.color == 0 and w.right.color == 0 :
                    w.color = 1
                    x = x.parent
                else :
                    if w.left.color == 0 :                # If left child of s is black
                        w.right.color = 0                 # set right child of s as black
                        w.color = 1
                        self.left_rotate(w)                     # call left rotation on x
                        w = x.parent.left

                    w.color = x.parent.color
                    x.parent.color = 0
                    w.left.color = 0
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 0

    def inorder(self):
        self.__in_order_helper(self.root)

    def __in_order_helper(self, node):
        if node != self.TNULL:
            self.__in_order_helper(node.left)
            print(node.data)
            self.__in_order_helper(node.right)


if __name__ == "__main__":
    n = None
    bst = RedBlackTree()
    while True:
        print("Za umetanje novog čvora unesite 1")
        print("Za INORDER ispis unesite 2")
        print("Za brisanje čvora unesite 3")
        print("Za izlaz 4")
        print("Izbor:")
        n = input()
        if n == "4":
            break
        elif n == "3":
            print("Vrijednost: ")
            value = input()
            if(value.isnumeric()):
                bst.rb_delete(int(value))
            else:
                bst.rb_delete(value)
        elif n == "1":
            print("Vrijednost: ")
            value = input()
            if(value.isnumeric()):
                bst.insert(int(value))
            else:
                bst.insert(value)
        elif n == "2":
            bst.inorder();
        else:
            print("Unesena upcija nije validna")