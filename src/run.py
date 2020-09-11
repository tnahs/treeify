from treeify import Treeify

string = """
root
    node
        node
            node
                node
                    node
                    node
                node
            node
                node
                    node
                    node
                node
        node
            node
        node
    node
"""

if __name__ == "__main__":

    tree = Treeify(string=string)
    tree.inspect_nodes()
    tree.render()
