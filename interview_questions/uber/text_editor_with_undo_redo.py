# text Editor Undo and Redo
# We can use the command pattern
# inovker -> invokes the command
# reciever -> recieves the command
# For text Editor application, editor is the invoker , it will have separate stack for undo and Redo
# in command pattern the execute and undo doesn't have parameter, all the required things should have present
# either during initialization of command or it should be able to get the required things from the avilable information

from __future__ import annotations
from abc import ABC, abstractmethod
from threading import Lock

class SingletonMeta(type):
    _lock=Lock()
    _instances:dict[type,object]=dict()
    def __call__(cls,*args,**kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance=super().__call__(*args,**kwargs)
                    cls._instances[cls]=instance
        return cls._instances[cls]



# receiver
class TextBuffer(metaclass=SingletonMeta):
    def __init__(self):
        self.text=""

    def _valid_position(self,pos):
        return pos>=0 and pos<=len(self.text)

    def insert(self,insert_pos,string_to_insert):
        # insert pos is the position from which we started adding the text
        if(not self._valid_position(insert_pos)):
            print("Invalid insert position\n");
            return
        left_str=self.text[:insert_pos]
        right_str=self.text[insert_pos:]
        self.text=left_str+string_to_insert+right_str

    def delete(self,delete_pos,char_count_to_delete)->str:
        if(not self._valid_position(delete_pos)):
            print("Invalid delete_pos\n")
            return ""

        left_str=self.text[:delete_pos]
        deleted_str=self.text[delete_pos:delete_pos+char_count_to_delete]
        right_str=self.text[delete_pos+char_count_to_delete:]
        self.text=left_str+right_str
        return deleted_str

    def get_text(self):
        return self.text

class Command(ABC):

    @abstractmethod
    def execute(self):
        raise NotImplementedError("Subclasses must implment this")

    @abstractmethod
    def undo(self):
        raise NotImplementedError("Subcalsses must impolment this")

# concrete commands
class InsertCommand(Command):
    # for insertion we should have the instance of the text editor and the place where we want to insert and the string we want to insert
    def __init__(self,text_buffer,insert_pos,string_to_insert):
        self.text_buffer=text_buffer
        self.insert_pos=insert_pos
        self.string_to_insert=string_to_insert

    def execute(self):
        self.text_buffer.insert(self.insert_pos,self.string_to_insert)

    def undo(self):
        self.text_buffer.delete(self.insert_pos,len(self.string_to_insert))

class DeleteCommand(Command):
    def __init__(self,text_buffer,delete_pos,char_count_to_delete):
        self.text_buffer=text_buffer
        self.delete_pos=delete_pos
        self.char_count_to_delete=char_count_to_delete
        self.deleted_str=None

    def execute(self):
        self.deleted_str=self.text_buffer.delete(self.delete_pos,self.char_count_to_delete)

    def undo(self):
        if self.deleted_str is None:
            print("first execute the delete command to undo this\n")
            return

        self.text_buffer.insert(self.delete_pos,self.deleted_str)

# invoker (TextEditor)
class TextEditor(metaclass=SingletonMeta):
    def __init__(self):
        self.buffer=TextBuffer()
        self.undo_commands:list[Command]=[]
        self.redo_commands:list[Command]=[]

    def execute(self, command:Command):
        command.execute()
        self.undo_commands.append(command)
        self.redo_commands.clear()

    def undo(self):
        if not self.undo_commands:
            print("there is no command to undo\n")
            return
        last_command=self.undo_commands[-1]
        self.undo_commands.pop()
        last_command.undo()

        # add to the redo commands
        self.redo_commands.append(last_command)

    def redo(self):
        if not self.redo_commands:
            print("there is no commands to redo\n")
            return

        last_redo_command=self.redo_commands[-1]
        self.redo_commands.pop()
        last_redo_command.execute()

        # add to the undo commands
        self.undo_commands.append(last_redo_command)

    def get_text(self):
        return self.buffer.get_text()

class CommandFactory(ABC):
    @abstractmethod
    def create(self,*args,**kwargs):
        raise NotImplementedError("Subclasses must implement this method")

class InsertCommandFactory(CommandFactory):
    def __init__(self):
        self.buffer=TextBuffer()
    def create(self,insert_pos,str_to_insert):
        return InsertCommand(self.buffer,insert_pos,str_to_insert)
class DeleteCommandFactory(CommandFactory):
    def __init__(self):
        self.buffer=TextBuffer()

    def create(self,delete_pos,char_count_to_delete):
        return DeleteCommand(self.buffer,delete_pos,char_count_to_delete)

if __name__=="__main__":
    insert_factory=InsertCommandFactory()
    delete_factory=DeleteCommandFactory()
    text_editor=TextEditor()

    cmd1=insert_factory.create(0,"hello")
    cmd2=insert_factory.create(5," world")
    cmd3=delete_factory.create(0,6)
    cmd4=delete_factory.create(0,5)

    print(text_editor.get_text(),"\n")
    text_editor.execute(cmd1)
    print(text_editor.get_text(),"\n")
    text_editor.execute(cmd2)
    print(text_editor.get_text(),"\n")

    text_editor.undo()
    print(text_editor.get_text(),"\n")

    text_editor.redo()
    print(text_editor.get_text(),"\n")

    text_editor.execute(cmd3)
    print(text_editor.get_text(),"\n")

    text_editor.execute(cmd4)
    print(text_editor.get_text(),"\n")





















        