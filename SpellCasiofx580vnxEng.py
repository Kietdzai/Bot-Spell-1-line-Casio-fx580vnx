print("Program spell for Casio fx580vnx. Version 3.0")
print("This program isn't supported special characters like ! , . ; > < v.v (Basically, I'm just too scared to do it)")
print("The hex splitting might be buggy, I'm so sorry ! However you can spell by Inject method.")
import string

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
        print("Câu bạn vừa nhập quá 1 dòng (17 kí tự) ! ")
    else:
        print("Ok")
        print("Các kí tự cần: ")
        for i in line:
            if i == " ":
                print("    Space", end=' ')
            else:
                print(f"    {i}", end=' ')

        print("\nCác kí tự không thể viết trên bàn phím: ")
        for a in line:
            if a in charst:
                print(f"        {a}", end='')
                char_list.append(a)
            if a not in list(string.ascii_letters):
                print(f"        {a}", end='')
                char_list.append(a)

        with open("chars.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            
            # Phần đầu - lấy hex_list
            for char in char_list:
                found = False
                for line in lines:
                    line = line.strip()
                    if  len(parts) >= 2 and parts[1] == char:
                        hex_code = parts[0]
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
def spell_inj(linecasio):
    char_list = list(linecasio)
    hex_list = []
    with open('chars.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for char in char_list:
            found = False
            for line in lines:
                line = line.strip()
                parts = line.split(' : ')
                if len(parts) >= 2 and parts[1] == char:
                    hex_code = parts[0]
                    hex_list.append(hex_code)
                    found = True
                    break
    with open('output.txt', 'a', encoding="utf-8") as f:
        for i in range(0, len(hex_list), 16):
            group = hex_list[i:i+16]  # Lấy 16 phần tử mỗi times
            f.write(' '.join(group) + '\n')  # Ghi dòng và xuống dòng
        f.write('[Fit 00 until full 3 small lines in Casio] \n')

a = input("How do you want to spell on the Casio fx-580VN X? Using variables A, B, C or using the Inject method?\n Type 'var' to spell using variables A, B, C\n Type 'inj' to spell using the Inject method.\n")

if a == 'var':
    b=input("Input line do you want to spell (English or France): ")
    spell_var(b)
if a == 'inj':
    e=int(input("How many lines do you want to spell on the Casio fx-580VN X using the Inject method ?\n"))
    u=[]

    if e>4:
        print(f"Over lines in Casio :v")
    else:
        for i in range(e):
            a = input(f"Input line do you want to spell at line {i+1}, not supported for special characters like , ; * > < etc\n")
            u.append(a)
            b=list(a)
            if len(a) > 17:
                print('That line was over 17 chars !')
            space=17-len(b)
            if space % 2==0:
                c=space//2
                b=[' ' for _ in range(c)] + b
                b=b + [' ' for _ in range(c)]
            elif space%2==1:
                c=(space-1)//2
                d=c+1
                b=[' ' for _ in range(c)] + b
                b=b+[' ' for _ in range(d)]
            h=''.join(b)
            print(h)
            spell_inj(h)
            if e<4:
                if len(u)==e:
                    g=17*(4-e)
                    with open('output.txt', 'a', encoding="utf-8") as file:
                        for i in range(4-e):
                            file.write(f'(20)×17 [Fit 00 until full 3 small lines in Casio]\n')
    with open("output.txt", "r", encoding="utf-8") as file:
        lines=file.read()
        print("Inject this code to address EA30 (Go to by QuickCPY++):")
        print(lines)
    file.close()
    with open("output.txt", "w") as f:
        pass
