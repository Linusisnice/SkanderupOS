[BITS 16]
[ORG 0x7C00]

START:
    ; Print "Hi" message
    mov ah, 0x0E
    mov al, 'H'
    int 0x10
    mov al, 'i'
    int 0x10

    ; Load kernel (assuming it is at the next sector)
    ; Use BIOS interrupt 13h to load the kernel

    mov bx, 0x0000        ; Load segment (0x0000:0x1000)
    mov es, bx
    mov bx, 0x1000        ; Load offset (0x1000)

    mov ah, 0x02          ; BIOS function: Read sectors
    mov al, 1             ; Number of sectors to read
    mov ch, 0             ; Cylinder number
    mov cl, 2             ; Sector number (start at 2nd sector)
    mov dh, 0             ; Head number
    mov dl, 0x80          ; Drive number (0x80 = first hard drive)

    int 0x13              ; Call BIOS to load the sector

    jc LOAD_FAILED        ; Jump if carry flag is set (error)
    
    ; Jump to the loaded kernel (kernel is loaded at 0x0000:0x1000)
    jmp 0x0000:0x1000

LOAD_FAILED:
    hlt                   ; Halt if loading failed

    ; Fill the rest of the boot sector with zeros
    TIMES 510-($-$$) db 0
    DW 0xAA55             ; Boot signature
