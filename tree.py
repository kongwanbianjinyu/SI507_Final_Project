class Node:
    def __init__(self, name,data,left= None,right = None):
        self.name = name
        self.data = data
        self.left = left
        self.right = right


def sortedArrayToBST(name_list, data_list):
    if not data_list:
        return None

    # find middle
    mid = (len(data_list)) // 2

    # make the middle element the root
    root = Node(name_list[mid],data_list[mid])

    # left subtree of root has all
    # values <arr[mid]
    root.left = sortedArrayToBST(name_list[:mid],data_list[:mid])

    # right subtree of root has all
    # values >arr[mid]
    root.right = sortedArrayToBST(name_list[mid + 1:],data_list[mid + 1:])

    return root


# A utility function to print the preorder traversal of the BST
def preOrder(node):
    if not node:
        return []

    result = [node.name] + preOrder(node.left) + preOrder(node.right)
    return result

def midOrder(node):
    if not node:
        return []

    result = midOrder(node.left) + [node.name] + midOrder(node.right)
    return result

def postOrder(node):
    if not node:
        return []

    result = postOrder(node.left) + postOrder(node.right) + [node.name]
    return result



def printTree(node, level=0):
    if not node:
        return ""

    result = printTree(node.left, level + 1) +"\n"+ ' ' * 40 * level + '-->'+ node.name + printTree(node.right, level + 1)

    return result

def saveTree(tree, treeFile):
    if isLeaf(tree):
        print("Leaf\n"+ tree.name, file = treeFile)
    else:
        print("Internal node\n" + tree.name , file = treeFile)
        if tree.left is not None:
            saveTree(tree.left, treeFile)
        if tree.right is not None:
            saveTree(tree.right, treeFile)



def isLeaf(tree):
    return tree.left is None and tree.right is None

if __name__ == '__main__':
    data_list= [1, 2, 3, 4, 5]
    name_list = ["c1","c2","c3","c4","c5"]
    root = sortedArrayToBST(name_list, data_list)
    print("PreOrder Traversal of constructed BST ")
    print(preOrder(root))

    print("MidOrder Traversal of constructed BST ")
    print(midOrder(root))

    print("PostOrder Traversal of constructed BST ")
    print(postOrder(root))

    print(printTree(root))

    treeFile = open('tree.json', "w")
    saveTree(root, treeFile)
    treeFile.close()




