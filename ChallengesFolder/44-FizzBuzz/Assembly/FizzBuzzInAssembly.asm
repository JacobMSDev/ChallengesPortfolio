
Started: 1/1/2022

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
    Fizz db "Fizz", 0xa     ; Store byte array to Fizz, 0xa is newline
    FizzLen equ $-Fizz      ; Store length of fizz into FizzLen
    Buzz db "Buzz", 0xa
    BuzzLen equ $-Buzz
    FizzBuzz db "FizzBuzz", 0xa
    FizzBuzzLen equ $-FizzBuzz

section .bss:
    num db 1

section .text:
_start:

    mov ecx, 5              ; How many times loop is to be run
    mov eax, '1'
    
  loopTop:
    mov [num], eax
  
    push ecx                ; Free ecx register
    
    mov eax, 0x4            ; Use the write syscall
    mov ebx, 1              ; Use stdout
    mov ecx, Fizz           ; Use Fizz as the buffer
    mov edx, FizzLen        ; Supply the buffer length
    int 0x80                ; Invoke the syscall 
    
    mov eax, 0x4            ; Use the write syscall
    mov ebx, 1              ; Use stdout
    mov ecx, Buzz           ; Use Buzz as the buffer
    mov edx, BuzzLen        ; Supply the buffer length
    int 0x80                ; Invoke the syscall 
    
    mov eax, 0x4            ; Use the write syscall
    mov ebx, 1              ; Use stdout
    mov ecx, FizzBuzz       ; Use FizzBuzz as the buffer
    mov edx, FizzBuzzLen    ; Supply the buffer length
    int 0x80                ; Invoke the syscall 
    
    pop ecx                 ; Return loop counter to ecx
  loop loopTop              ; Loop if ecx > 0 after decrement
  
    ; Close the program
    mov eax, 0x1            ; Use the exit syscall
    mov ebx, 0
    int 0x80                ; Invoke the syscall

==========================================================================================================

section .data:
    Fizz db "Fizz", 0xa     ; Store byte array to Fizz, 0xa is newline
    FizzLen equ $-Fizz      ; Store length of fizz into FizzLen
    Buzz db "Buzz", 0xa
    BuzzLen equ $-Buzz
    FizzBuzz db "FizzBuzz", 0xa
    FizzBuzzLen equ $-FizzBuzz
    
    num db '#', 0x0a, 0x00

;section .bss:
    ;num db '1', 0xa
    ;num resb 0
    ;num dw '12'

section .text:
    global _start

_start:

    mov ecx, 0             ; How many times loop is to be run
    ;inc byte[num]
    ;mov byte[num], 0xa
    
  loopTop:
    cmp ecx, 5
    je loopComplete
  
    inc ecx
  
    ;add cl, 1
  
    push ecx                ; Free ecx register
    
    mov eax, 0x4            ; Use the write syscall
    mov ebx, 0x1            ; Use stdout
    mov ecx, Fizz           ; Use Fizz as the buffer
    mov edx, FizzLen        ; Supply the buffer length
    int 0x80                ; Invoke the syscall 
    
    mov eax, 0x4            ; Use the write syscall
    mov ebx, 0x1            ; Use stdout
    mov ecx, Buzz           ; Use Buzz as the buffer
    mov edx, BuzzLen        ; Supply the buffer length
    int 0x80                ; Invoke the syscall 
    
    mov eax, 0x4            ; Use the write syscall
    mov ebx, 0x1            ; Use stdout
    mov ecx, FizzBuzz       ; Use FizzBuzz as the buffer
    mov edx, FizzBuzzLen    ; Supply the buffer length
    int 0x80                ; Invoke the syscall
    
    mov eax, 0x4
    mov ebx, 0x1
    mov ecx, num
    mov edx, 2
    int 0x80
    
    pop ecx   ; Return loop counter to ecx
    jmp loopTop
    
  loopComplete:             ; Loop if ecx < 10
    ; Close the program
    mov eax, 0x1            ; Use the exit syscall
    ;mov ebx, 0x0
    int 0x80                ; Invoke the syscall
    
====================================================================================================

section .bss
    num resd 1

section .text
    global _start

_start:

    mov ecx, 0              ; Loop starts at 0
    mov eax, '1'            ; First number is 1

  loopTop:
    inc ecx
    
    cmp ecx, 9              ; How many times loop is to be run
    je loopComplete
    
    mov [num], eax
  
    push ecx                ; Free ecx register
    
    mov eax, 0x4
    mov ebx, 0x1
    mov ecx, num
    mov edx, 1
    int 0x80

    mov eax, [num]
    sub eax, '0'
    inc eax
    add eax, '0'
    
    pop ecx   ; Return loop counter to ecx
    jmp loopTop
  loopComplete:             ; Loop if ecx < 10
    
    ; Close the program
    mov eax, 0x1            ; Use the exit syscall
    int 0x80                ; Invoke the syscall
