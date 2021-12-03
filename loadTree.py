def loadTree(treeFile):
    while True:
        line = treeFile.readline().strip()
        if line == '':
            break
        elif line == "Leaf":
            leaf = treeFile.readline().strip()
            return (leaf, None, None)
        else:
            question = treeFile.readline().strip()
            return (question,loadTree(treeFile),loadTree(treeFile))

if __name__ == '__main__':
    treeFile = 'tree.json'
    treeFile = open(treeFile, "r")
    tree = loadTree(treeFile)
    print(tree)
    treeFile.close()