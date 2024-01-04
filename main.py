from tkinter import filedialog
import os
from tqdm import tqdm


# Deixa o código colorido no terminal
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
PURPLE = '\033[35m'
CYAN = '\033[36m'
CLEAR_COLOR = '\033[m'

R = {"$zero": "00000", "$at": "00001", "$v0": "00010", "$v1": "00011",
     "$a0": "00100", "$a1": "00101", "$a2": "00110", "$a3": "00111",
     "$t0": "01000", "$t1": "01001", "$t2": "01010", "$t3": "01011",
     "$t4": "01100", "$t5": "01101", "$t6": "01110", "$t7": "01111",
     "$s0": "10000", "$s1": "10001", "$s2": "10010", "$s3": "10011",
     "$s4": "10100", "$s5": "10101", "$s6": "10110", "$s7": "10111",
     "$t8": "11000", "$t9": "11001", "$k0": "11010", "$k1": "11011",
     "$gp": "11100", "$sp": "11101", "$fp": "11110", "$ra": "11111",
     "$f0": "00000", "$f1": "00001", "$f2": "00010", "$f3": "00011",
     "$f4": "00100", "$f5": "00101", "$f6": "00110", "$f7": "00111",
     "$f8": "01000", "$f9": "01001", "$f10": "01010", "$f11": "01011",
     "$f12": "01100", "$f13": "01101", "$f14": "01110", "$f15": "01111",
     "$f16": "10000", "$f17": "10001", "$f18": "10010", "$f19": "10011",
     "$f20": "10100", "$f21": "10101", "$f22": "10110", "$f23": "10111",
     "$f24": "11000", "$f25": "11001", "$f26": "11010", "$f27": "11011",
     "$f28": "11100", "$f29": "11101", "$f30": "11110", "$f31": "11111",
     "$0": "00000", "$1": "00001", "$2": "00010", "$3": "00011",
     "$4": "00100", "$5": "00101", "$6": "00110", "$7": "00111",
     "$8": "01000", "$9": "01001", "$10": "01010", "$11": "01011",
     "$12": "01100", "$13": "01101", "$14": "01110", "$15": "01111",
     "$16": "10000", "$17": "10001", "$18": "10010", "$19": "10011",
     "$20": "10100", "$21": "10101", "$22": "10110", "$23": "10111",
     "$24": "11000", "$25": "11001", "$26": "11010", "$27": "11011",
     "$28": "11100", "$29": "11101", "$30": "11110", "$31": "11111"
    }


hex_3r = {"add":   lambda rd, rs, rt: hex(int(f'000000{R[rs]}{R[rt]}{R[rd]}00000100000', 2))[2:].zfill(8),
          "addu":  lambda rd, rs, rt: hex(int(f'000000{R[rs]}{R[rt]}{R[rd]}00000100001', 2))[2:].zfill(8),
          "and":   lambda rd, rs, rt: hex(int(f'000000{R[rs]}{R[rt]}{R[rd]}00000100100', 2))[2:].zfill(8),
          "movn":  lambda rd, rs, rt: hex(int(f'000000{R[rs]}{R[rt]}{R[rd]}00000001011', 2))[2:].zfill(8),
          "mul":   lambda rd, rs, rt: hex(int(f'011100{R[rs]}{R[rt]}{R[rd]}00000000010', 2))[2:].zfill(8),
          "nor":   lambda rd, rs, rt: hex(int(f'000000{R[rs]}{R[rt]}{R[rd]}00000100111', 2))[2:].zfill(8),
          "or":    lambda rd, rs, rt: hex(int(f'000000{R[rs]}{R[rt]}{R[rd]}00000100101', 2))[2:].zfill(8),
          "sltu":  lambda rd, rs, rt: hex(int(f'000000{R[rs]}{R[rt]}{R[rd]}00000101011', 2))[2:].zfill(8),
          "srav":  lambda rd, rt, rs: hex(int(f'000000{R[rs]}{R[rt]}{R[rd]}00000000111', 2))[2:].zfill(8),
          "srlv":  lambda rd, rt, rs: hex(int(f'000000{R[rs]}{R[rt]}{R[rd]}00000000110', 2))[2:].zfill(8),
          "sub":   lambda rd, rs, rt: hex(int(f'000000{R[rs]}{R[rt]}{R[rd]}00000100010', 2))[2:].zfill(8),
          "subu":  lambda rd, rs, rt: hex(int(f'000000{R[rs]}{R[rt]}{R[rd]}00000100011', 2))[2:].zfill(8),
          "xor":   lambda rd, rs, rt: hex(int(f'000000{R[rs]}{R[rt]}{R[rd]}00000100110', 2))[2:].zfill(8)}

hex_2r = {"clo":   lambda rd, rs: hex(int(f'011100{R[rs]}00000{R[rd]}00000100001', 2))[2:].zfill(8),
          "div":   lambda rs, rt: hex(int(f'000000{R[rs]}{R[rt]}0000000000011010', 2))[2:].zfill(8),
          "mult":  lambda rs, rt: hex(int(f'000000{R[rs]}{R[rt]}0000000000011000', 2))[2:].zfill(8)}

hex_1r = {"jr":    lambda rs: hex(int(f'000000{R[rs]}000000000000000001000', 2))[2:].zfill(8),
          "mfhi":  lambda rd: hex(int(f'0000000000000000{R[rd]}00000010000', 2))[2:].zfill(8),
          "mflo":  lambda rd: hex(int(f'0000000000000000{R[rd]}00000010010', 2))[2:].zfill(8)}

hex_3i = {"addi":  lambda rt, rs, imm: hex(int(f'001000{R[rs]}{R[rt]}{imm}', 2))[2:].zfill(8),
          "addiu": lambda rt, rs, imm: hex(int(f'001001{R[rs]}{R[rt]}{imm}', 2))[2:].zfill(8),
          "andi":  lambda rt, rs, imm: hex(int(f'001100{R[rs]}{R[rt]}{imm}', 2))[2:].zfill(8),
          "ori":   lambda rt, rs, imm: hex(int(f'001101{R[rs]}{R[rt]}{imm}', 2))[2:].zfill(8),
          "slti":  lambda rt, rs, imm: hex(int(f'001010{R[rs]}{R[rt]}{imm}', 2))[2:].zfill(8),
          "sltiu": lambda rt, rs, imm: hex(int(f'001011{R[rs]}{R[rt]}{imm}', 2))[2:].zfill(8),
          "xori":  lambda rt, rs, imm: hex(int(f'001110{R[rs]}{R[rt]}{imm}', 2))[2:].zfill(8)}

hex_2i = {"lui":   lambda rt, imm: hex(int(f'00111100000{R[rt]}{imm}', 2))[2:].zfill(8)}

hex_3b = {"beq":   lambda rs, rt, imm: hex(int(f'000100{R[rs]}{R[rt]}{imm}', 2))[2:].zfill(8),
          "bne":   lambda rs, rt, imm: hex(int(f'000101{R[rs]}{R[rt]}{imm}', 2))[2:].zfill(8)}

hex_2b = {"bgez":  lambda rs, imm: hex(int(f'000001{R[rs]}00001{imm}', 2))[2:].zfill(8),
          "bgezal":lambda rs, imm: hex(int(f'000001{R[rs]}10001{imm}', 2))[2:].zfill(8),
          "blez":  lambda rs, imm: hex(int(f'000110{R[rs]}00000{imm}', 2))[2:].zfill(8)}

hex_j =  {"j":     lambda target: hex(int(f'000010{target}', 2))[2:].zfill(8),
          "jal":   lambda target: hex(int(f'000011{target}', 2))[2:].zfill(8)}

hex_m =  {"lb":    lambda rt, offset, base: hex(int(f'100000{R[base]}{R[rt]}{offset}', 2))[2:].zfill(8),
          "lbu":   lambda rt, offset, base: hex(int(f'100100{R[base]}{R[rt]}{offset}', 2))[2:].zfill(8),
          "lw":    lambda rt, offset, base: hex(int(f'100011{R[base]}{R[rt]}{offset}', 2))[2:].zfill(8),
          "sb":    lambda rt, offset, base: hex(int(f'101000{R[base]}{R[rt]}{offset}', 2))[2:].zfill(8),
          "sw":    lambda rt, offset, base: hex(int(f'101011{R[base]}{R[rt]}{offset}', 2))[2:].zfill(8)}

hex_s =  {"sll":   lambda rd, rt, sa: hex(int(f'00000000000{R[rt]}{R[rd]}{sa}000000', 2))[2:].zfill(8),
          "sra":   lambda rd, rt, sa: hex(int(f'00000000000{R[rt]}{R[rd]}{sa}000011', 2))[2:].zfill(8),
          "srl":   lambda rd, rt, sa: hex(int(f'00000000000{R[rt]}{R[rd]}{sa}000010', 2))[2:].zfill(8)}


def print_header(msg: str):
    print()
    print(f"{YELLOW}{'='*50}{CLEAR_COLOR}")
    print(f"|{f' {msg} ':-^48}|")
    print(f"{YELLOW}{'='*50}{CLEAR_COLOR}")
    print()


def get_filepath() -> str:
    # retorna uma string com o path do arquivo
    return filedialog.askopenfilename()


def get_file_lines(filepath: str) -> list:
    # Cada elemento da lista retornada é uma linha do arquivo
    with open(filepath, 'r') as file:
        return file.readlines()


def get_instructions(filepath: str) -> tuple[list, list]:
    label = ''
    is_data_I = False
    data_I, text_I, all_I = [], [], tqdm(get_file_lines(filepath))
    all_I.set_description("> Formating ")
    all_I.bar_format = '{l_bar}{bar}| {n_fmt}/{total_fmt}'
    all_I.ncols = 50
    all_I.colour = 'yellow'

    for line in all_I:
        line = line.replace("\t", " ").replace(",", " ").strip().split()

        if line == []:
            continue
        if '' in line:
            line.remove('')
        if (':' in line[0]) and (len(line) == 1):
            label = line[0]
            continue
        if label != '':
            line.insert(0, label)
            label = ''

        line = " ".join(line)
        
        if line == ".data":
            is_data_I = True
            continue
        if line == ".text":
            is_data_I = False
            continue
        
        if is_data_I:
            data_I.append(line)
        else:
            text_I.append(line)
    #print(f"{CLEAR_COLOR}", end='')
    if data_I != []:
        print("> Found .data section.")
    if text_I != []:
        print("> Found .text section.")
    return (data_I, text_I)


def update_choice(user_input: str, choice: int, options: list) -> int:
    if user_input == "":
        if choice < len(options):
            choice += 1
        else:
            choice = 1
    elif user_input == " ":
        if choice > 1:
            choice -= 1
        else:
            choice = len(options)
    elif user_input.isnumeric():
        choice = int(user_input)
    return choice


def selection_menu(options: list) -> str:
    choice = 1
    while True:
        os.system('cls')
        print_header('Assembler MIPS')

        for i, option in enumerate(options):
            print(f"* {CYAN}[{i+1}] {option}{CLEAR_COLOR}" if i+1 == choice else f"* [{i+1}] {option}")
        
        print(f"\n| {YELLOW}[Enter]{CLEAR_COLOR} desce | {YELLOW}[Espaço]{CLEAR_COLOR} sobe | {YELLOW}[S]{CLEAR_COLOR} seleciona  |")

        j = input(f'\n{YELLOW}< {CLEAR_COLOR}')

        if j.strip() == "S" or j.strip() == "s":
            break

        choice = update_choice(j, choice, options)
    
    os.system('cls')
    return options[choice-1]


def select_file() -> str:
    print_header("Select file")
    while True:
        filepath = get_filepath()

        if filepath != "":
            if filepath[-4:] == ".asm":
                break
            else:
                print(f"{RED}> {CLEAR_COLOR}Selecione um arquivo no formato .asm!")
        else:
            print(f"{RED}> {CLEAR_COLOR}Selecione um arquivo!")

    print(f"{GREEN}> {CLEAR_COLOR}Arquivo selecionado com sucesso!")
    input(f"{YELLOW}< {CLEAR_COLOR}")
    os.system('cls')
    return filepath


def assemble_data(instructions: list) -> list:
    print()
    assembled_data = []
    all_I = tqdm(instructions)
    all_I.set_description("> Assembling .data ")
    all_I.bar_format = '{l_bar}{bar}| {n_fmt}/{total_fmt}'
    all_I.ncols = 50
    all_I.colour = 'yellow'


    for line in all_I:
        line = line.split()[2:]
        for n in line:
            if "x" in n:
                assembled_data.append(n[2:].zfill(8))
            else:
                if int(n) < 0:
                    assembled_data.append(hex(int(''.join(['0' if d == '1' else '1' for d in bin(abs(int(n))).zfill(32)]), 2) + 1)[2:])
                else:
                    assembled_data.append(hex(int(n))[2:].zfill(8))

    return assembled_data


def assemble_text(instructions: list) -> list:
    print()
    assembled_text = []
    all_I = tqdm(instructions)
    all_I.set_description("> Assembling .text ")
    all_I.bar_format = '{l_bar}{bar}| {n_fmt}/{total_fmt}'
    all_I.ncols = 50
    all_I.colour = 'yellow'

    for _idx, instruction in enumerate(all_I):
        t = instruction.split()
        if ":" in t[0]:
            I = t[1:]
        else:
            I = t[:]

        if I[0] in hex_3r:
            a_I = hex_3r[I[0]](I[1], I[2], I[3])
            assembled_text.append(a_I)

        elif I[0] in hex_2r:
            a_I = hex_2r[I[0]](I[1], I[2])
            assembled_text.append(a_I)

        elif I[0] in hex_1r:
            a_I = hex_1r[I[0]](I[1])
            assembled_text.append(a_I)

        elif I[0] in hex_3i:
            imm = int(I[3], 16) if 'x' in I[3].lower() else int(I[3])
            if imm < 0:
                imm = int('0xffff', 16) + imm + 1
            imm = bin(imm)[2:].zfill(16)

            a_I = hex_3i[I[0]](I[1], I[2], imm)
            assembled_text.append(a_I)

        elif I[0] in hex_2i:
            imm = int(I[2], 16) if 'x' in I[2].lower() else int(I[2])
            if imm < 0:
                imm = int('0xffff', 16) + imm + 1
            imm = bin(imm)[2:].zfill(16)

            a_I = hex_2i[I[0]](I[1], imm)
            assembled_text.append(a_I)

        elif I[0] in hex_j:
            addr = None
            for idx, i in enumerate(instructions):
                if i.split()[0][:-1] == I[1]:
                    addr = idx
            addr = bin(addr)[2:].zfill(26)

            a_I = hex_j[I[0]](addr)
            assembled_text.append(a_I)

        elif I[0] in hex_m:
            base = I[2].split("(")[1][:-1]
            offset = bin(int(I[2].split("(")[0]))[2:].zfill(16)

            a_I = hex_m[I[0]](I[1], offset, base)
            assembled_text.append(a_I)

        elif I[0] in hex_3b:
            addr = None
            for idx, i in enumerate(instructions):
                if i.split()[0][:-1] == I[3]:
                    addr = idx
            addr -= _idx
            if addr < 0:
                addr = int('0xffff', 16) + addr
            addr = bin(addr)[2:].zfill(16)

            a_I = hex_3b[I[0]](I[1], I[2], addr)
            assembled_text.append(a_I)

        elif I[0] in hex_2b:
            addr = None
            for idx, i in enumerate(instructions):
                if i.split()[0][:-1] == I[2]:
                    addr = idx
            addr -= _idx
            if addr < 0:
                addr = int('0xffff', 16) + addr
            addr = bin(addr)[2:].zfill(16)

            a_I = hex_2b[I[0]](I[1], addr)
            assembled_text.append(a_I)

        elif I[0] in hex_s:
            imm = bin(int(I[3], 16)) if 'x' in I[3].lower() else bin(int(I[3]))
            if "-" in imm:
                imm = imm[3:].zfill(5)
            else:
                imm = imm[2:].zfill(5)

            a_I = hex_s[I[0]](I[1], I[2], imm)
            assembled_text.append(a_I)

    return assembled_text


def assemble(filepath: str) -> tuple[list]:
    print_header("Assembling")
    data_I, text_I = get_instructions(filepath)
    a_text = assemble_text(text_I)
    a_data = assemble_data(data_I)

    input(f"{YELLOW}< {CLEAR_COLOR}")
    return (a_text, a_data)


def save(filepath: str, assembled_text: list, assembled_data: list):
    print_header("Saving")
    c = 0

    if assembled_text != []:
        with open(f'{filepath[:-4]}_text.mif', 'w') as mif_text_file:
            mif_text_file.write("DEPTH = 16384;\nWIDTH = 32;\nADDRESS_RADIX = HEX;\nDATA_RADIX = HEX;\nCONTENT\nBEGIN\n\n")
            for i, code in enumerate(assembled_text):
                mif_text_file.write(f'{hex(i*4)[2:].zfill(8)} : {code};\n')
            mif_text_file.write('\nEND')
        c+=1

    if assembled_data != []:
        with open(f'{filepath[:-4]}_data.mif', 'w') as mif_data_file:
            mif_data_file.write("DEPTH = 16384;\nWIDTH = 32;\nADDRESS_RADIX = HEX;\nDATA_RADIX = HEX;\nCONTENT\nBEGIN\n\n")
            for i, code in enumerate(assembled_data):
                mif_data_file.write(f'{hex(i*4)[2:].zfill(8)} : {code};\n')
            mif_data_file.write('\nEND')
        c+=1

    if c == 0:
        print(f"{RED}> {CLEAR_COLOR}O Arquivo compilado está vazio!")
    if c == 1:
        print(f"{GREEN}> {CLEAR_COLOR}Arquivo salvo com sucesso!")
    if c == 2:
        print(f"{GREEN}> {CLEAR_COLOR}Arquivos salvos com sucesso!")
    
    input(f"{YELLOW}< {CLEAR_COLOR}")
    os.system('cls')


options = ["Assemble", "Save assembled file", "Exit"]
filepath = ""
assembled_text = []
assembled_data = []

while True:
    choice = selection_menu(options).lower()

    if choice == "assemble":
        filepath = select_file()
        assembled_text, assembled_data = assemble(filepath)

    elif choice == "save assembled file":
        if filepath != '':
            save(filepath, assembled_text, assembled_data)

    elif choice == "exit":
        break
