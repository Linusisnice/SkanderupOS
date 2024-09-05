@echo off

REM Assemble the bootloader
nasm -f bin bootloader/boot.asm -o boot.bin

REM Compile the kernel (optional if you have kernel.cpp)
i686-elf-g++ -ffreestanding -c kernel/kernel.cpp -o kernel/kernel.o

REM Link the kernel
i686-elf-ld -o kernel.bin -Ttext 0x1000 --oformat binary kernel/kernel.o -e kernel_main

REM Run the Skanderup++ compiler to generate assembly from Skanderup++ source
python skanderup++/skanderup_compiler.py source/program.skp

REM Assemble the generated assembly code into a binary file
nasm -f bin output.asm -o kernel.bin

REM Combine bootloader and kernel into a single disk image
copy /b boot.bin + kernel.bin disk.img

REM Run the OS in QEMU for testing
qemu-system-x86_64 -drive format=raw,file=disk.img

@echo Build complete.
