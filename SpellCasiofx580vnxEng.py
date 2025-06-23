print("Program spell for Casio fx580vnx. Version 3.0.1")
print("This program isn't supported special characters like ! , . ; > < v.v (Basically, I'm just too scared to do it)")
print("The hex splitting might be buggy, I'm so sorry ! However you can spell by Inject method.")
import string
import random

def parse_line(raw_line):
    label, data = raw_line.split('=')
    parts = data.strip().split()
    return label.strip(), parts

def process_template(label, parts):
    reversed_parts = list(reversed(parts))
    actions = []
    count = 0
    post_20_count = 0
    post_20_mode = False

    for part in reversed_parts:
        if part == 'x10':
            continue

        if part == '20':
            if count > 0:
                actions.append(f"[<] x{count} [DEL]")
            elif post_20_count > 0:
                actions.append(f"[<] x{post_20_count} [DEL]")
            count = 0
            post_20_mode = True
            post_20_count = 0
            continue

        if part == '1.':
            if post_20_mode and post_20_count > 0:
                actions.append(f"[<] x{post_20_count} [DEL] x2")
            elif not post_20_mode and count > 0:
                actions.append(f"[<] x{count} [DEL] x2")
            count = 0
            post_20_mode = False
            post_20_count = 0
            continue

        elif part == '1.0000':
            if post_20_mode and post_20_count > 0:
                actions.append(f"[<] x{post_20_count}")
            elif not post_20_mode and count > 0:
                actions.append(f"[<] x{count}")
            count = 0
            post_20_mode = False
            post_20_count = 0
            continue

        if len(part) == 2:
            if post_20_mode:
                post_20_count += 1
            else:
                count += 1

    return label, list((actions))

def is_valid_for_slot(slot, byte):
    if '!' in slot:
        return all(c.isdigit() for c in byte)
    return True

def fill_template(template, hex_list, hex_index):
    filled = []
    i = hex_index
    byte_count = 0

    for part in template:
        if part == '__' or any(s in part for s in ['_!', '!_', '!!']):
            if i >= len(hex_list):
                filled.append('3C 23')
                byte_count += 2
                return filled, i, True, byte_count
            
            byte = hex_list[i]
            i += 1
            
            if ('!' in part and not byte.isdigit() and not byte[-1].isdigit()):
                filled.append('20')
            else:
                filled.append(byte)
            byte_count += 1

        elif not part.startswith('x'):
            filled.append(part)
            if len(part) == 2 and part != '1.' and not part.startswith('1.'):
                byte_count += 1

    return filled, i, False, byte_count

def count_segments_around_20(template_result):
    reversed_parts = list(reversed(template_result))
    after_20 = 0
    before_20 = 0
    found_20 = False

    for part in reversed_parts:
        if part == 'x10':
            continue
        if part.startswith('1.'):
            break
        if not found_20:
            if part == '20':
                found_20 = True
                continue
            elif len(part) == 2:
                after_20 += 1
        else:
            if part == '20': #Dòng này đẹp nè, có lẽ không ai để ý đâu hehe (ý là số á)
                break
            if len(part) == 2:
                before_20 += 1

    if found_20:
        return after_20, before_20
    else:
        total = after_20
        return total, None

def spell_var (line):
    char_list = []
    charst = ['a','b','c','d','e','f','g','j','k','L','M','N','O','T','U','V','W','X','Y','Z']
    char1=[]
    ds=list(line)
    hex_list=[]
    found_keys={}
    if len(line) > 17:
        print("That line was over 17 char (1 line) ! ")
    else:
        print("Ok")
        print("Chars needed: ")
        for i in line:
            if i == " ":
                print("    Space", end=' ')
            else:
                print(f"    {i}", end=' ')
        j=list(string.ascii_letters)
        j.append("!")
        j.append('"')
        j.append('#')
        print("\nChars can't write by keyboard: ")
        for a in line:
            if a in charst:
                print(f"        {a}", end='')
                char_list.append(a)
            if a not in j:
                print(f"        {a}", end='')
                char_list.append(a)

        with open("chars.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            
            # Phần đầu - lấy hex_list
            for char in char_list:
                found = False
                for line in lines:
                    line = line.strip()
                    if line.endswith(f": {char}"):
                        hex_code = line.split(" : ")[0]
                        print(f"\n{char} = {hex_code}")
                        found = True
                        hex_list.append(hex_code)
                        break
                if not found:
                    print(f"{char} : Can't found in file. Hmm just pretend nothing happened, hehe :)")
            
            # Phần hai - lấy found_keys
            for line in lines:
                line = line.strip()
                if " : " in line:
                    parts = line.split(" : ")
                    if len(parts) == 3:
                        hex_code, char, button = parts
                        if char in ds:
                            found_keys[char] = button
        c=len(ds)
        space =17-c
        if space % 2 == 0:
            a = space // 2
            ds=[' ' for _ in range(a)] + ds
            ds=ds + [' ' for _ in range(a)]
        elif space % 2 == 1:
            a = (space-1) // 2
            b = a + 1
            ds=[' ' for _ in range(b)] + ds
            ds=ds+[' ' for _ in range(a)]
        str_spell="".join(ds)
        print(str_spell)
        s=0
        for b in hex_list:
            for ch in b:
                if ch.isalpha():
                    char1.append(ch)
        char1.append('C')
        print("[v] means press down button\n[<] means press left button\n[>] means press right button\n[^] means press up button")
        print('Step 1: Reset: \n [shift] [9] [3] [=] [=]')
        print('Step 2: Go to LineI/O: \n [shift] [menu] [1] [3]')
        print('Step 3: Basic Overflow: \n [x] [alpha] [CALC] [shift] [x] [x] [shift] [)] [9] [shift] [)] [9] [9] [9] [CALC] {[=] [AC]}-> nhấn nhanh [<] [del] [del] [CALC] [=] [<] [shift] [.]')
        print('Step 4: Take needed Hex chars: \n ' + "".join(char1))
        with open('takechars.txt','r') as s:
            lines=s.readlines()
        for char in char1:
            found=False
            for line in lines:
                line=line.strip()
                if line.startswith(f'{char} :'):
                    value=line.split(':')[1].strip()
                    print(value)
                    found = True
                    break
        print('([<] [9] [DEL])×', len(char1), '[DEL]×10', "[alpha] [∫]\nAfter that, how do I make the Casio screen display like this:")
        template_A = ['1.0000', '__', '__', '__', '_!', '!_', '×10', '!!']
        template_B = ['1.', '__', '__', '__', '__', '__', '_!', '!_', '×10', '!!']
        template_C = ['1.', '__', '__', '__', '__', '__', '_!', '!_', '×10', '!!']

        filled_outputs = []
        hex_index = 0

        print("x:")
        for label, template in zip(['A', 'B', 'C'], [template_A, template_B, template_C]):
            result, hex_index, done, byte_count = fill_template(template, hex_list, hex_index)
            filled_outputs.append(f"{label} = {' '.join(result)}")
            if done: #Số đẹp hẹ hẹ
                break
        for line in filled_outputs:
            print(line + ':')
            variables_printed = set()

            for line in filled_outputs:
                if '=' in line:
                    var_name = line.split('=')[0].strip()
                    variables_printed.add(var_name)

        print(f'[CALC] ([=])×{len(variables_printed)+1} times')
        print('Step 5: Take "an":\n[x] [alpha] [CALC] [shift] [x] [x] [shift] [)] [9] [shift] [)] [9] [CALC] [=] [<] [shift] [.] [shift] [.] [<] [<] [DEL] [v] [shift] [8] [v] [2] [6] [<] [<] [>] [9] [DEL] [<] [)] [+] [100 số bất kì]\n[CALC] [=]')
        print('Step 6: Take "@":\n[x] [alpha] [CALC] [shift] [x] [x] [shift] [)] [9] [shift] [)] [9] [CALC] [=] [<] [shift] [.]', end='')
        if len(variables_printed) == 1:
            print('[shift] [7] [4] [8]', end=' ')
            print('([<] [9] [DEL])×1\n[DEL]×10',end='')
            print('[<] [9 số bất kì] [>] [alpha] [∫] [>] [alpha] [CALC] [alpha] [(-)]\n[CALC] ([=])×2 [^]')
        elif len(variables_printed) == 2:
            print('[shift] [7] [4] [8] [shift] [7] [4] [9]', end=' ')
            print('([<] [9] [DEL])×2\n[DEL]×10',end='')
            print('[<] [9 số bất kì] [>] [alpha] [∫] [>] [alpha] [CALC] [alpha] [(-)] [alpha] [∫] [>] [alpha] [CALC] [alpha] [□ \' "]\n[CALC] ([=])×3 [^]')
        elif len(variables_printed) == 3:
            print('[shift] [7] [4] [8] [shift] [7] [4] [9] [shift] [7] [1] [4]', end=' ')
            print('([<] [9] [DEL])×3\n[DEL]×10',end='')
            print('[<] [9 số bất kì] [>] [alpha] [∫] [>] [alpha] [CALC] [alpha] [(-)] [alpha] [∫] [>] [alpha] [CALC] [alpha] [□ \' "] [alpha] [∫] [>] [alpha] [CALC] [alpha] [x^-1]\n[CALC] ([=])×4 [^]')
        print('Step 7: Delete not needed bytes:')
        results = []
        for raw in filled_outputs:
            label, parts = parse_line(raw)
            label, actions = process_template(label, parts)
            results.append((label, actions))

        for label, actions in reversed(results[:3]):
            for action in actions:
                print(f"  {action}", end='')
        p=0
        print('\nStep 8: Do like this: ')
        for char in ds:
            if char in found_keys:
                print(f"{found_keys[char]}", end=' ')
            else:
                if char == " ":
                    print("[shift] [8] [3] [4]", end=' ')  # Thay thế cho dấu cách
                    p+=1
                else:
                    print(f"[>]", end=' ')
        print(f'[{17-p} optional numbers] [shift] [(] [>] [2] [x]')
        print('Final step: [CALC] [=]')
        file.close()
        print("Dev: AxesMC")
def spell_inj_4_ol(b):
    for i in range(b):
        a = input(f"Enter the sentence you want to spell on line {i+1} on the Casio (supports both Vietnamese and English). Some special characters such as , : > < = ? are also supported.\n")
        g=list(a)
        if len(g)>17:
            raise Exception("That line was over 17 chars ~ 1 line !")
        space=17-len(g)
        if space % 2==0:
            c=space//2
            g=[' ' for _ in range(c)] + g + [' ' for _ in range(c)]
        elif space%2==1:
            c=(space-1)//2
            d=c+1
            g=[' ' for _ in range(c)] + g + [' ' for _ in range(d)]
        char_list = g
        hex_list = []
        with open("chars.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            for char in char_list:
                found = False
                for line in lines:
                    line = line.strip()
                    parts = line.split(" : ")
                    if len(parts) >= 2 and parts[1] == char:
                        hex_code = parts[0]
                        hex_list.append(hex_code)
                        found = True
                        break
                if not found:
                    if char == " ":
                        hex_list.append("20")
                    else:
                        print(f"Oops! Can't find {char} in chars.txt \n Submit it on GitHub and I'll add it—just make sure it's a valid Casio character!")
        true_byte = []
        for item in hex_list:
            true_byte.extend(item.strip().split()) #Đẩy mấy phần tử 2 byte ra khỏi nhau (chia tay hehe)
        # Đảm bảo đủ 48 byte đầu tiên (3 dòng đầu × 16 bytes)
        while len(true_byte) < 48:
            true_byte.append("00")
        with open("output.txt", "a", encoding="utf-8") as f:
            for i in range(0, 48, 16):
                group = true_byte[i:i+16]
                f.write(' '.join(group) + '\n')
            f.write('[menu] [3]\n')
            for i in range(48, len(true_byte), 16):
                group = true_byte[i:i+16]
                f.write(' '.join(group) + '\n')
    with open("output.txt", "r", encoding="utf-8") as f:
        print("Inject these code to started addr is EA30 (how to inject : go to QuickCPY++, at version 3.0.2 I'll tutorial :) wait for me)\n")
        print(''.join(f.readlines()))
        for i in range(4-e):
            print("20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20\n20 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")
            print("[menu] [3]")
def spell_inj_8_ol(b):
    all_hex = []
    m=list(string.ascii_letters)
    m.append(" ")
    m.append(",")
    m.append("0")
    m.append("1")
    m.append("2")
    m.append("3")
    m.append("4")
    m.append("5")
    m.append("6")
    m.append("7")
    m.append("8")
    m.append("9")
    m.append("'")
    m.append('"')
    for i in range(b):
        a = input(f"Enter the sentence you want to spell at line {i+1} on the Casio (only supported English). Some special characters such as , : > < = ? are also supported. \n")
        for z in a:
            if z not in m:
                raise Exception("The line you entered contains special characters!")
        if len(a)>32:
            raise Exception("The line you entered was over 32 char ~ 1 small line !")
        char_list = list(a)
        space = 32 - len(char_list)
        if space % 2 == 0:
            c = space // 2
            char_list = [' ' for _ in range(c)] + char_list + [' ' for _ in range(c)]
        else:
            c = (space - 1) // 2
            d = c + 1
            char_list = [' ' for _ in range(c)] + char_list + [' ' for _ in range(d)]

        with open("chars.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            for char in char_list:
                found = False
                for line in lines:
                    line = line.strip()
                    parts = line.split(" : ")
                    if len(parts) >= 2 and parts[1] == char:
                        hex_code = parts[0]
                        all_hex.append(hex_code)
                        found = True
                        break
                if not found:
                    if char == " ":
                        all_hex.append("20")
                    else:
                        print(f"Oops! Can't find {char} in chars.txt \n Submit it on GitHub and I'll add it—just make sure it's a valid Casio character!")
    for z in range(8-e):
        for a in range(32):
            all_hex.append("20")
    with open("output.txt", "a", encoding="utf-8") as f:
        f.write("34 7b 31 30 08 01 a0 ea cc 3d 32 30 7e 94 30 30\n")
        f.write("34 7b 31 30 08 09 c0 ea cc 3d 32 30 7e 94 30 30\n")
        f.write("34 7b 31 30 08 11 e0 ea cc 3d 32 30 7e 94 30 30\n")
        f.write("34 7b 31 30 08 19 00 eb cc 3d 32 30 7e 94 30 30\n")
        f.write("34 7b 31 30 08 21 20 eb cc 3d 32 30 7e 94 30 30\n")
        f.write("34 7b 31 30 08 29 40 eb cc 3d 32 30 7e 94 30 30\n")
        f.write("[menu] [3]\n")
        f.write("34 7b 31 30 08 31 60 eb cc 3d 32 30 7e 94 30 30\n")
        f.write("34 7b 31 30 08 39 80 eb cc 3d 32 30 7e 94 30 30\n")
        f.write("34 7b 31 30 0a f0 73 00 d2 03 32 30 34 7b 31 30\n")
        f.write("10 f0 00 00 d2 03 32 30 34 7b 31 30 30 d6 84 d1\n")
        f.write("c8 03 32 30 78 5c 31 30 2e d6 60 0d 32 30 00 00\n")
        f.write("00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n")
        f.write("[menu] [3]\n")
        i = 0
        while i < len(all_hex):
            group_of_96 = all_hex[i:i + 96]
            while len(group_of_96) < 96:
                group_of_96.append("00")
            for j in range(0, 96, 16):
                line = group_of_96[j:j + 16]
                f.write(' '.join(line) + '\n')
            f.write('[menu] [3]\n')
            i += 96
    with open("output.txt", "r", encoding="utf-8") as f:
        print("Inject these code to started addr is EA30 (how to inject : go to QuickCPYMax, at version 3.0.2 I'll tutorial :) wait for me)")
        print(f.read())

a = input("Choose your spelling method for Casio fx-580VN X: \n Type 'var' to use variables A, B, C \nType 'inj' to inject (for advanced users with QuickCPYMax or QuickCPY++ skills)\n")

if a == 'var':
    b=input("Enter the sentence you want to spell (English or France supported): ")
    spell_var(b)
if a == 'inj':
    with open("output.txt", "w", encoding='utf-8') as e:
        pass
    e=int(input("How many lines do you want to spell on the Casio fx-580VN X using the Inject method?\n"))
    if e<=4:
        spell_inj_4_ol(e)
        print("Launcher ? At version 3.0.2 I'll tutorial !")
    elif e<=8 and e>4:
        spell_inj_8_ol(e)
        print("Launcher ? At version 3.0.2 I'll tutorial !")
    elif e>8:
        print("That's more than the Casio can handle! :v")
if random.randint(1,80) == 1:
    print("Good luck spelling!")
