import gdb
import tempfile
import os

def execute_and_capture(command):
    with open("/tmp/gdb_stderr_capture.txt", "w+") as temp_file:
        gdb.execute("call (void) freopen(\"/tmp/gdb_stderr_capture.txt\", \"w\", stderr)")
        gdb.execute(command)
        gdb.execute("call (void) freopen(\"/dev/tty\", \"w\", stderr)")
        temp_file.seek(0)
        captured_output = temp_file.read()
        return captured_output


class LLVMTypePrinter:
    """Pretty printer for llvm::Type objects."""
    def __init__(self, val):
        self.val = val

    def to_string(self):
        try:
            dump_output = execute_and_capture(f'call ((llvm::Type*){self.val})->dump()')
            return dump_output.strip() or "<empty output>"
        except gdb.error as e:
            return f'<error: {e}>'


class LLVMValuePrinter:
    """Pretty printer for llvm::Value objects."""
    def __init__(self, val):
        self.val = val

    def to_string(self):
        try:
            dump_output = execute_and_capture(f'call ((llvm::Value*){self.val})->dump()')
            return dump_output.strip() or "<empty output>"
        except gdb.error as e:
            return f'<error: {e}>'


def check_inheritance(valtype, base_name):
    """Check if a given type inherits from a specified base class."""
    if valtype.tag == base_name:
        return True
    
    for f in valtype.fields():
        if f.is_base_class:
            if f.name == base_name:
                return True
            else:
                return check_inheritance(f.type, base_name)
    return False


def is_address_valid(address):
    """Check if a memory address is valid."""
    if address == 0:
        return False

    try:
        gdb.selected_inferior().read_memory(address, 1)
        return True
    except:
        return False


def llvm_pretty_printer(val):
    if not is_address_valid(val.address):
        return None

    basic_type = gdb.types.get_basic_type(val.type)

    if basic_type.code == gdb.TYPE_CODE_PTR:
        return None

    if basic_type.code != gdb.TYPE_CODE_STRUCT:
        return None

    if check_inheritance(basic_type, "llvm::Value"):
        return LLVMValuePrinter(val.address)
    
    if check_inheritance(basic_type, "llvm::Type"):
        return LLVMTypePrinter(val.address)

    return None


def register_pretty_printers(obj):
    if obj is None:
        obj = gdb

    gdb.printing.register_pretty_printer(obj, llvm_pretty_printer)

register_pretty_printers(gdb.current_objfile())
