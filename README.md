# LLVM GDB Pretty Printers
This project provides GDB pretty printers for LLVM types, specifically for `llvm::Type` and `llvm::Value`. The pretty printers directly use the `dump()` method when inspecting LLVM types within GDB.


![Screenshot from 2024-05-25 01-34-30](https://github.com/bmanga/llvm-ir-pp/assets/13623481/0048ca9c-f7ca-4ff4-a792-080914cd7c8e)

## Installation
1. Clone the repository:
```sh
git clone https://github.com/bmanga/llvm-ir-pp.git
```
2. Load the pretty printers in your GDB session by adding the following to your `.gdbinit` file:
```sh
source /path/to/llvm-ir-pp/llvm-ir-prettyprinter.py
```

## Usage
Once the pretty printers are loaded, GDB will automatically use them to display LLVM types when they are encountered. For example:

```sh
(gdb) p *ST
$1 = store ptr addrspace(1) %data_out_raw, ptr %data, align 4
```
Your IDE may also be able to make use of it (eg. VSCode, see the image above)

## Contributing
Contributions are welcome! Please submit pull requests or open issues to discuss potential changes.
