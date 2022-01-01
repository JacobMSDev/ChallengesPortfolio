global _start         ; Specify entry point

section .data:
  message db "Hello World!", 0xa
  messageLen equ $-message

section .text:
_start:               ; Start program
  mov eax, 0x4        ; Use the write syscall
  mov ebx, 1          ; Use stdout
  mov ecx, message    ; Use the message as the buffer
  mov edx, messageLen ; Supply the buffer length
  int 0x80            ; Invoke the syscall
  
  ; Close the program
  mov eax, 0x1        ; Use the exit syscall
  mov ebx, 0
  int 0x80            ; Invoke the syscall


# ----- # LOOP BIT
(Prints hello world 5 times)

https://www.tutorialspoint.com/compile_asm_online.php

global _start

section .data:
    message db "Hello World!", 0xa
    messageLen equ $-message

section .text:
_start:

    mov ecx, 5          ; How many times loop is run
    
  loopTop:
    push ecx            ; Free ecx register
  
    mov eax, 0x4        ; Use the write syscall
    mov ebx, 1          ; Use stdout
    mov ecx, message    ; Use the message as the buffer
    mov edx, messageLen ; Supply the buffer length
    int 0x80            ; Invoke the syscall 
    
    pop ecx             ; Return loop counter to ecx
    
  loop loopTop
  
    ; Close the program
    mov eax, 0x1        ; Use the exit syscall
    mov ebx, 0
    int 0x80            ; Invoke the syscall
