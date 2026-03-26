# Composite design pattern
from __future__ import annotations
from threading import Lock
class Node:
    def __init__(self,name:str,parent:Node | None):
        self.name=name
        self.parent=parent

# leaf (but for Folder system in pwd, cd and mkdir we don't deal with the leaf, so for now we will keep it optional), if there is need to print some information for each file and folder then we will create the file as well
# Node is Leaf and Directory will act as Composite

class Directory(Node):
    def __init__(self,name:str,parent:Node|None=None):
        super().__init__(name,parent)
        # name to Directory map
        self.children:dict[str,Node]=dict()


    def add_child(self,name:str)->None:
        childNode=Directory(name,self)
        self.children[name]=childNode

    def get_child(self,child_name:str)->Directory|None:
        return self.children.get(child_name)

class FileSystem:
    _instance=None
    _lock=Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance=super().__new__(cls)
                    cls._has_initialized=False
        return cls._instance


    def __init__(self):
        if getattr(self,"_has_initialized"):
            return
        self.root=Directory("/")
        self.cwd=self.root
        self._has_initialized=True



    def cd(self, path:str)->str|None:
        nodes=self._resolve_multiple_directory(path)
        if not nodes:
           print("Path Not Found")
           return

           #  keep the first entry for deterministic
        self.cwd=sorted(nodes,key=lambda x: x.name)[0]
        print(self.cwd.name)


    def mkdir(self,path:str):
        try:
           node_created=self._resolve_single_directory(path,True)
           print(f"path {path} created successfully\n")
        except Exception:
            print("Path Not Created\n")

    def pwd(self)->str:
        curr_node=self.cwd
        res=[]
        while curr_node!=self.root:
            res.append(curr_node.name)
            curr_node=curr_node.parent

        return "/"+"/".join(reversed(res))




    # resolve single (No wildcard matching, used in mkdir)
    def _resolve_single_directory(self,path:str,create_if_not_found=True)->str|None:
        path=path.strip()
        start_from=self.root if path.startswith("/") else self.cwd

        curr_node=start_from
        for part in path.split('/'):
            part=part.strip()
            if part in ["","."]:
                continue
            elif part == "..":
                curr_node=curr_node.parent if curr_node.parent else curr_node
            else:
                if part not in curr_node.children:
                    if not create_if_not_found:
                        raise Exception("Path Not Found")
                    else:
                        curr_node.add_child(part)

            curr_node=curr_node.get_child(part)

        return curr_node

    def _resolve_multiple_directory(self,path:str):
        path=path.strip()
        start_node= self.root if path.startswith('/') else self.cwd

        # create a set of start Node
        current_nodes={start_node}

        for part in path.split('/'):
            part=part.strip()
            if part in ["","."]:
                continue
            next_nodes=set()

            for curr_node in current_nodes:
                if part == "..":
                    parent=curr_node.parent if curr_node.parent else curr_node
                    next_nodes.add(parent)
                elif part == "*":
                    next_nodes.update(curr_node.children.values())
                else:
                    child = curr_node.get_child(part)
                    if child:
                        next_nodes.add(child)
                    # Don't raise error in else part because due to wildcard, even if one matches other might succeed
                    # raise Exception("Path Not Found")

            # swap current_nodes and next_nodes
            current_nodes=next_nodes

        return current_nodes



if __name__=="__main__":
    fs=FileSystem()

    # fs.mkdir("/a")
    # fs.mkdir("/b")

    # fs.cd("/")
    # fs.cd("*")
    # fs.pwd()

    # fs.mkdir("/a/x")
    # fs.mkdir("/b/x")

    # fs.cd("/")
    # fs.cd("*/x")
    # print(fs.pwd())

    # fs.mkdir("/a/x/p")
    # fs.mkdir("/b/y/p")

    # fs.cd("/")
    # fs.cd("*/*/p")
    # print(fs.pwd())


    # fs.mkdir("/a/x/p")
    # fs.mkdir("/b/y/q")

    # fs.cd("/")
    # fs.cd("*/*")
    # print(fs.pwd())

    # fs.mkdir("/a/x")
    # fs.mkdir("/b/x")

    # fs.cd("/a/x")
    # fs.cd("../../*/x")
    # print(fs.pwd())

    # fs.mkdir("/a/x")

    # fs.cd("/")
    # fs.cd("./a/./x")
    # print(fs.pwd())

    # fs.mkdir("/a/x")
    # fs.mkdir("/b/y")

    # fs.cd("/")
    # fs.cd("*/x")
    # print(fs.pwd())

    # fs.cd("/")
    # fs.cd("*")

    fs.mkdir("/a/x/p")
    fs.mkdir("/a/y/p")
    fs.mkdir("/b/z/p")

    fs.cd("/")
    fs.cd("*/ */p")
    print(fs.pwd())


        