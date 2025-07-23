import string
import random
def fill_template(template, hex_list, hex_index):
    filled = []
    i = hex_index
    byte_count = 0

    while_part = 0
    while while_part < len(template):
        part = template[while_part]

        if part == '__' or any(s in part for s in ['_!', '!_', '!!']):
            if i >= len(hex_list):
                # Không thêm gì nữa nếu hết hex
                return filled, i, True

            byte = hex_list[i]

            # Kiểm tra nếu là slot cấm chữ
            if '!' in part and (not byte.isdigit() and not byte[-1].isdigit()):
                filled.append('20')  # fill dummy skibidi
                # KHÔNG tăng i (vì byte không dùng được)
                while_part += 1
                continue
            else:
                filled.append(byte)
                i += 1

        elif not part.startswith('x'):
            filled.append(part)
            if len(part) == 2 and part != '1.' and not part.startswith('1.'):
                byte_count += 1
        while_part += 1

    return filled, i, False
#VN area
def spell_var_vn (line):
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
        j=list(string.ascii_letters)
        j.append("!")
        j.append('"')
        j.append('#')
        j.append(' ')
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
                    parts = line.split(" : ")
                    if len(parts) >= 2 and parts[1] == char:
                        hex_code = parts[0]
                        print(f"\n{char} = {hex_code}")
                        found = True
                        hex_list.append(hex_code)
                        break
                if not found:
                    print(f"{char} : Can't found in file (Hmm bạn cứ coi như không có gì đi. Tính năng đấy)")
            
            # Phần hai - lấy found_keys
            for line in lines:
                line = line.strip()
                if " : " in line:
                    parts = line.split(" : ")
                    if len(parts) == 3:
                        hex_code, char, button = parts
                        if char in ds:
                            found_keys[char] = button
        #Bốc kí tự Hex
        with open('takechars.txt','r', encoding='utf-8') as s:
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
        hex_list.append("3C")
        hex_list.append("23")
        print("[v] có nghĩa là nhấn nút xuống\n[<] có nghĩa là nhấn nút trái\n[>] có nghĩa là nhấn nút phải\n[^] có nghĩa là nhấn lên")
        print('Bước 1: Reset: \n [shift] [9] [3] [=] [=]')
        print('Bước 2: Go to LineI/O: \n [shift] [menu] [1] [3]')
        print('Bước 3: Basic Overflow: \n [x] [alpha] [CALC] [shift] [x] [x] [shift] [)] [9] [shift] [)] [9] [9] [9] [CALC] {[=] [AC]}-> nhấn nhanh [<] [del] [del] [CALC] [=] [<] [shift] [.]')
        print('Bước 4: Take: \n ' + "".join(char1))

        print('([<] [9] [DEL])×', len(char1), '[DEL]×10', "[alpha] [∫]\nSau đó, làm sao cho màn hình Casio hiển thị như thế này:")
        template_A = ['1.0000', '__', '__', '__', '_!', '!_', '×10', '!!']
        template_B = ['1.', '__', '__', '__', '__', '__', '_!', '!_', '×10', '!!']
        template_C = ['1.', '__', '__', '__', '__', '__', '_!', '!_', '×10', '!!']

        filled_outputs = []
        hex_index = 0
        list_lo=[]
        for label, template in zip(['A', 'B', 'C'], [template_A, template_B, template_C]):
            result, hex_index, done = fill_template(template, hex_list, hex_index)
            filled_outputs.append(f"{label} = {' '.join(result)}")
            for z in result:
                list_lo.append(z)
            if done:
                break  # Dừng khi hết hex_list

        # In kết quả
        for line in filled_outputs:
            print(line + ':')
            variables_printed = set()

            for line in filled_outputs:
                if '=' in line:
                    var_name = line.split('=')[0].strip()
                    variables_printed.add(var_name)

        print(f'[CALC] ([=])×{len(variables_printed)+1} lần')
        print('Bước 5: Lấy "an":\n[x] [alpha] [CALC] [shift] [x] [x] [shift] [)] [9] [shift] [)] [9] [CALC] [=] [<] [shift] [.] [shift] [.] [<] [<] [DEL] [v] [shift] [8] [v] [2] [6] [<] [<] [>] [9] [DEL] [<] [)] [+] [100 số bất kì]\n[CALC] [=]')
        print('Bước 6: Lấy "@":\n[x] [alpha] [CALC] [shift] [x] [x] [shift] [)] [9] [shift] [)] [9] [CALC] [=] [<] [shift] [.]', end='')
        if len(variables_printed) == 1:
            print('[shift] [7] [4] [8]', end=' ')
            print('([<] [9] [DEL])×1\n[DEL]×10',end=' ')
            print('[<] [9 số bất kì] [>] [alpha] [∫] [>] [alpha] [CALC] [alpha] [(-)]\n[CALC] ([=])×2 [^]')
        elif len(variables_printed) == 2:
            print('[shift] [7] [4] [8] [shift] [7] [4] [9]', end=' ')
            print('([<] [9] [DEL])×2\n[DEL]×10',end=' ')
            print('[<] [9 số bất kì] [>] [alpha] [∫] [>] [alpha] [CALC] [alpha] [(-)] [alpha] [∫] [>] [alpha] [CALC] [alpha] [□ \' "]\n[CALC] ([=])×3 [^]')
        elif len(variables_printed) == 3:
            print('[shift] [7] [4] [8] [shift] [7] [4] [9] [shift] [7] [1] [4]', end=' ')
            print('([<] [9] [DEL])×3\n[DEL]×10',end=' ')
            print('[<] [9 số bất kì] [>] [alpha] [∫] [>] [alpha] [CALC] [alpha] [(-)] [alpha] [∫] [>] [alpha] [CALC] [alpha] [□ \' "] [alpha] [∫] [>] [alpha] [CALC] [alpha] [x^-1]\n[CALC] ([=])×4 [^]')
        print('Bước 7: Xóa các byte không cần thiết:')
        count=0
        list_lo.reverse()
        for i in list_lo:
            if i=='20':
                if count==0:
                    print("[DEL]",end=" ")
                else:
                    print(f"[<]x{count} [DEL]",end=" ")
                count=0
            elif i=='1.':
                if count==0:
                    print("[DEL]x2",end=" ")
                else:
                    print(f"[<]x{count} [DEL]x2",end=" ")
                count=0
            elif i=='1.0000':
                if count==0:
                    pass
                else:
                    print(f"[<]x{count}",end=" ")
                count=0
            elif i == '×10':
                pass
            else:
                count+=1
        p=0
        print('\nBước 8: Làm giống y hệt đoạn dưới đây: ')
        for char in ds:
            if char in found_keys:
                print(f"{found_keys[char]}", end=' ')
            if char not in found_keys:
                if char == " ":
                    print("[shift] [8] [3] [4]", end=' ')  # Thay thế cho dấu cách
                    p+=1
                if char not in j:
                    p+=1
                    print(f"[>]", end=' ')
                if char not in charst:
                    print(f"[>]", end=' ')
        print(f'[{17-p} số bất kì] [shift] [(] [>] [2] [x]')
        print('Bước cuối: [CALC] [=]')
        file.close()
def spell_inj_4_ol_vn(b):
    for i in range(b):
        a = input(f"Bạn muốn spell câu gì ở dòng số {i+1} trên Casio (Tiếng Việt hoặc Tiếng Anh). Hỗ trợ một vài kí tự đặc biệt như , : > < = ?\n")
        g=list(a)
        if len(g)>32:
            raise Exception("Dòng bạn vừa nhập quá 32 kí tự ~ 1 line !")
        space=32-len(g)
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
                        print(f"Không tìm thấy {char} trong chars.txt\n Báo thiếu kí tự lên github.com đi rồi tui sẽ thêm vào cho (Phải có trong chars của Casio đấy nhé !)")
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
        print("Inject các đoạn code sau vào EA30 (Vào bằng QuickCPY++)\n")
        print(''.join(f.readlines()))
        for i in range(4-e):
            print("20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20\n20 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")
            print("[menu] [3]")

def spell_inj_8_ol_vn(b):
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
        a = input(f"Bạn muốn spell câu gì ở dòng {i+1} trên Casio (Tiếng Anh) ?\n")
        for z in a:
            if z not in m:
                raise Exception("Dòng bạn nhập có kí tự đặc biệt !")
        if len(a)>32:
            raise Exception("Dòng bạn mới nhập quá 32 kí tự ~ 1 dòng !")
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
                        print(f"Không tìm thấy {char} trong chars.txt\n Báo thiếu kí tự lên github.com đi rồi tui sẽ thêm vào cho (Phải có trong chars của Casio đấy nhé !)")
    for z in range(8-e):
        for a in range(32):
            all_hex.append("20")
    with open("output.txt", "a", encoding="utf-8") as f:
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
        f.write("DA 7B 31 30 08 01 30 EA 30 30 30 30 CC 3D 32 30")
        f.write("12 9D 30 30 08 09 CC 3D 32 30 12 9D 30 30 08 11")
        f.write("CC 3D 32 30 12 9D 30 30 08 19 CC 3D 32 30 12 9D")
        f.write("30 30 08 21 CC 3D 32 30 12 9D 30 30 08 29 CC 3D")
        f.write("32 30 12 9D 30 30 08 31 CC 3D 32 30 12 9D 30 30")
        f.write("08 39 CC 3D 32 30 7E 94 30 30 DE 3D 32 30 00 00")
        f.write("[Menu] [3]")
    with open("output.txt", "r", encoding="utf-8") as f:
        print("Inject đoạn các đoạn code sau vào E9E0 (Vào bằng QuickCPYMax)")
        print(f.read())
    with open("QuickCPY.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        thay = False
        for line in lines:
            line = line.strip()
            if line.startswith("Launcher 8 lines (non-an)"):
                thay = True
            if thay and line =="-----":
                break
            if thay:
                print(line)

def spell_inj_6_vn(b):
    n=input("Bạn có chắc muốn spell 6 lines ? Vì nó không thể skip đâu, bạn làm 1 lần là phải làm lại đó\nNhấn Enter nếu muốn tiếp tục\nGõ x để làm spell có thể skip\n")
    if n=="\n":
        pass
    elif n=="x":
        spell_inj_8_ol_vn(e)
    all_hex = []
    hexl=[]
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
        a = input(f"Bạn muốn spell câu gì ở dòng {i+1} trên Casio (Tiếng Anh) ?\n")
        for z in a:
            if z not in m:
                raise Exception("Dòng bạn nhập có kí tự đặc biệt !")
        if len(a)>32:
            raise Exception("Dòng bạn mới nhập quá 32 kí tự ~ 1 dòng !")
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
                        hexl.append(hex_code)
                        found = True
                        break
                if not found:
                    if char == " ":
                        hexl.append("20")
                    else:
                        print(f"Không tìm thấy {char} trong chars.txt\n Báo thiếu kí tự lên github.com đi rồi tui sẽ thêm vào cho (Phải có trong chars của Casio đấy nhé !)")
    with open("output.txt", "a", encoding="utf-8") as fi:
        fi.write("A8 9F 30 30 E0 A0 30 30 5C A0 30 30 60 8C 30 30\n")
        fi.write("A5 30 31 30 0A 01 B0 DC 30 30 30 30 CC 3D 32 30\n")
        fi.write("A5 30 31 30 0A 0B D0 DC 30 30 30 30 CC 3D 32 30\n")
        fi.write("A5 30 31 30 0A 15 F0 DC 30 30 30 30 CC 3D 32 30\n")
        fi.write("A5 30 31 30 0A 1F 10 DD 30 30 30 30 CC 3D 32 30\n")
        fi.write("A5 30 31 30 0A 29 30 DD 30 30 30 30 CC 3D 32 30\n")
        fi.write("[menu] [3]\n")
    all_hex.append("A5")
    all_hex.append("30")
    all_hex.append("31")
    all_hex.append("30")
    all_hex.append("0A")
    all_hex.append("33")
    all_hex.append("50")
    all_hex.append("DD")
    all_hex.append("30")
    all_hex.append("30")
    all_hex.append("30")
    all_hex.append("30")
    all_hex.append("CC")
    all_hex.append("3D")
    all_hex.append("32")
    all_hex.append("30")
    all_hex.append("62")
    all_hex.append("3F")
    all_hex.append("32")
    all_hex.append("30")
    for i in range(12):
        all_hex.append("00")
    for i in hexl:
        all_hex.append(i)
    for z in range(6-e):
        for a in range(32):
            all_hex.append("20")
    with open("output.txt", "a", encoding="utf-8") as f:
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
        print("Inject đoạn các đoạn code sau vào DC30 (Vào bằng QuickCPYMax)")
        print(f.read())
    with open("QuickCPY.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        thay = False
        for line in lines:
            line = line.strip()
            if line.startswith("Launcher 6 lines (non-an)"):
                thay = True
            if thay and line =="-----":
                break
            if thay:
                print(line)


# EN area
def spell_var_en (line):
    char_list = []
    charst = ['a','b','c','d','e','f','g','j','k','L','M','N','O','T','U','V','W','X','Y','Z']
    char1=[]
    ds=list(line)
    hex_list=[]
    found_keys={}
    if len(line) > 17:
        print("The line you inputed was over 17 chars (~ 1 line)")
    else:
        print("Ok")
        print("Chars needed: ")
        for i in line:
            if i == " ":
                print("    Space", end=' ')
            else:
                print(f"    {i}", end=' ')

        print("\nChars can't write in keyboard: ")
        j=list(string.ascii_letters)
        j.append("!")
        j.append('"')
        j.append('#')
        j.append(' ')
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
                    parts = line.split(" : ")
                    if len(parts) >= 2 and parts[1] == char:
                        hex_code = parts[0]
                        print(f"\n{char} = {hex_code}")
                        found = True
                        hex_list.append(hex_code)
                        break
                if not found:
                    print(f"{char} : Can't found in file (Not thing :) This is a feature ! :v)")
            
            # Phần hai - lấy found_keys
            for line in lines:
                line = line.strip()
                if " : " in line:
                    parts = line.split(" : ")
                    if len(parts) == 3:
                        hex_code, char, button = parts
                        if char in ds:
                            found_keys[char] = button
        #Bốc kí tự Hex
        with open('takechars.txt','r', encoding='utf-8') as s:
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
        hex_list.append("3C")
        hex_list.append("23")
        print("[v] means press down button\n[<] means press left button\n[>] means press right button\n[^] means press up button")
        print('Step 1: Reset: \n [shift] [9] [3] [=] [=]')
        print('Step 2: Go to LineI/O: \n [shift] [menu] [1] [3]')
        print('Step 3: Basic Overflow: \n [x] [alpha] [CALC] [shift] [x] [x] [shift] [)] [9] [shift] [)] [9] [9] [9] [CALC] {[=] [AC]}-> nhấn nhanh [<] [del] [del] [CALC] [=] [<] [shift] [.]')
        print('Step 4: Take needed Hex chars: \n ' + "".join(char1))

        print('([<] [9] [DEL])×', len(char1), '[DEL]×10', "[alpha] [∫]\nSau đó, làm sao cho màn hình Casio hiển thị như thế này:")
        template_A = ['1.0000', '__', '__', '__', '_!', '!_', '×10', '!!']
        template_B = ['1.', '__', '__', '__', '__', '__', '_!', '!_', '×10', '!!']
        template_C = ['1.', '__', '__', '__', '__', '__', '_!', '!_', '×10', '!!']

        filled_outputs = []
        hex_index = 0
        list_lo=[]
        for label, template in zip(['A', 'B', 'C'], [template_A, template_B, template_C]):
            result, hex_index, done = fill_template(template, hex_list, hex_index)
            filled_outputs.append(f"{label} = {' '.join(result)}")
            for z in result:
                list_lo.append(z)
            if done:
                break  # Dừng khi hết hex_list

        # In kết quả
        for line in filled_outputs:
            print(line + ':')
            variables_printed = set()

            for line in filled_outputs:
                if '=' in line:
                    var_name = line.split('=')[0].strip()
                    variables_printed.add(var_name)

        print(f'[CALC] ([=])×{len(variables_printed)+1} lần')
        print('Step 5: Take "an":\n[x] [alpha] [CALC] [shift] [x] [x] [shift] [)] [9] [shift] [)] [9] [CALC] [=] [<] [shift] [.] [shift] [.] [<] [<] [DEL] [v] [shift] [8] [v] [2] [6] [<] [<] [>] [9] [DEL] [<] [)] [+] [100 số bất kì]\n[CALC] [=]')
        print('Step 6: Take "@":\n[x] [alpha] [CALC] [shift] [x] [x] [shift] [)] [9] [shift] [)] [9] [CALC] [=] [<] [shift] [.]', end='')
        if len(variables_printed) == 1:
            print('[shift] [7] [4] [8]', end=' ')
            print('([<] [9] [DEL])×1\n[DEL]×10',end=' ')
            print('[<] [9 optional numbers] [>] [alpha] [∫] [>] [alpha] [CALC] [alpha] [(-)]\n[CALC] ([=])×2 [^]')
        elif len(variables_printed) == 2:
            print('[shift] [7] [4] [8] [shift] [7] [4] [9]', end=' ')
            print('([<] [9] [DEL])×2\n[DEL]×10',end=' ')
            print('[<] [9 optional numbers] [>] [alpha] [∫] [>] [alpha] [CALC] [alpha] [(-)] [alpha] [∫] [>] [alpha] [CALC] [alpha] [□ \' "]\n[CALC] ([=])×3 [^]')
        elif len(variables_printed) == 3:
            print('[shift] [7] [4] [8] [shift] [7] [4] [9] [shift] [7] [1] [4]', end=' ')
            print('([<] [9] [DEL])×3\n[DEL]×10',end=' ')
            print('[<] [9 optional numbers] [>] [alpha] [∫] [>] [alpha] [CALC] [alpha] [(-)] [alpha] [∫] [>] [alpha] [CALC] [alpha] [□ \' "] [alpha] [∫] [>] [alpha] [CALC] [alpha] [x^-1]\n[CALC] ([=])×4 [^]')
        print('Step 7: Delete not needed bytes: ')
        count=0
        list_lo.reverse()
        for i in list_lo:
            if i=='20':
                if count==0:
                    print("[DEL]",end=" ")
                else:
                    print(f"[<]x{count} [DEL]",end=" ")
                count=0
            elif i=='1.':
                if count==0:
                    print("[DEL]x2",end=" ")
                else:
                    print(f"[<]x{count} [DEL]x2",end=" ")
                count=0
            elif i=='1.0000':
                if count==0:
                    pass
                else:
                    print(f"[<]x{count}",end=" ")
                count=0
            elif i == '×10':
                pass
            else:
                count+=1
        p=0
        print('\nStep 8: Do like this: ')
        for char in ds:
            if char in found_keys:
                print(f"{found_keys[char]}", end=' ')
            if char not in found_keys:
                if char == " ":
                    print("[shift] [8] [3] [4]", end=' ')  # Thay thế cho dấu cách
                    p+=1
                if char not in j:
                    p+=1
                    print(f"[>]", end=' ')
                if char not in charst:
                    print(f"[>]", end=' ')
        print(f'[{17-p} optional numbers] [shift] [(] [>] [2] [x]')
        print('Final step: [CALC] [=]')
        file.close()
def spell_inj_4_ol_en(b):
    for i in range(b):
        a = input(f"Enter your sentence do you want to spell at line {i+1} in Casio (France, Vietnamese or English supported). Support some special characters like , : > < = ?\n")
        g=list(a)
        if len(g)>17:
            raise Exception("The code you inputed was over 17 chars ! (~ 1 line)")
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
                        print(f"Can't found {char} in chars.txt\n Contact me on Github and I will add (remember this character have in Casio fx580vnx's characters)")
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
        print("Inject these Hex code, addr start EA30 (Go to by QuickCPY++)\n")
        print(''.join(f.readlines()))
        for i in range(4-e):
            print("20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20\n20 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")
            print("[menu] [3]")

def spell_inj_8_ol_en(b):
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
        a = input(f"Enter your sentence do you want to spell at line {i+1} in Casio (English only) ?\n")
        for z in a:
            if z not in m:
                raise Exception("The line you inputed was had special character !")
        if len(a)>32:
            raise Exception("The line you inputed was over 32 chars (~ 1 line) !")
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
                        print(f"Can't found {char} in chars.txt\n Contact me on Github and I will add (remember this character have in Casio fx580vnx's characters)")
    for z in range(8-e):
        for a in range(32):
            all_hex.append("20")
    with open("output.txt", "a", encoding="utf-8") as f:
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
        f.write("DA 7B 31 30 08 01 30 EA 30 30 30 30 CC 3D 32 30")
        f.write("12 9D 30 30 08 09 CC 3D 32 30 12 9D 30 30 08 11")
        f.write("CC 3D 32 30 12 9D 30 30 08 19 CC 3D 32 30 12 9D")
        f.write("30 30 08 21 CC 3D 32 30 12 9D 30 30 08 29 CC 3D")
        f.write("32 30 12 9D 30 30 08 31 CC 3D 32 30 12 9D 30 30")
        f.write("08 39 CC 3D 32 30 7E 94 30 30 DE 3D 32 30 00 00")
        f.write("[Menu] [3]")
    with open("output.txt", "r", encoding="utf-8") as f:
        print("Inject these Hex code, addr start E9E0 (Go to by QuickCPYMax)")
        print(f.read())
    with open("QuickCPY.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        thay = False
        for line in lines:
            line = line.strip()
            if line.startswith("Launcher 8 lines (non-an)"):
                thay = True
            if thay and line =="-----":
                break
            if thay:
                print(line)

def spell_inj_6_en(b):
    n=input("Are you sure you want to spell 6 lines ? Because if you press [shift] [9] [3] [=] [=] all data will deleted\nPress Enter to continue\nPress x to spell 6 lines but safer\n")
    if n=="\n":
        pass
    elif n=="x":
        spell_inj_8_ol_en(e)
    all_hex = []
    hexl=[]
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
        a = input(f"Enter your sentence do you want to spell at line {i+1} in Casio (English only) ?\n")
        for z in a:
            if z not in m:
                raise Exception("The line you inputed was had special character !")
        if len(a)>32:
            raise Exception("The line you inputed was over 32 chars (~1 line) !")
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
                        hexl.append(hex_code)
                        found = True
                        break
                if not found:
                    if char == " ":
                        hexl.append("20")
                    else:
                        print(f"Can't not found character: {char} in chars.txt\n Contact me on Github and I will add, remember this character have in Casio fx580vnx's character !")
    with open("output.txt", "a", encoding="utf-8") as fi:
        fi.write("A8 9F 30 30 E0 A0 30 30 5C A0 30 30 60 8C 30 30\n")
        fi.write("A5 30 31 30 0A 01 B0 DC 30 30 30 30 CC 3D 32 30\n")
        fi.write("A5 30 31 30 0A 0B D0 DC 30 30 30 30 CC 3D 32 30\n")
        fi.write("A5 30 31 30 0A 15 F0 DC 30 30 30 30 CC 3D 32 30\n")
        fi.write("A5 30 31 30 0A 1F 10 DD 30 30 30 30 CC 3D 32 30\n")
        fi.write("A5 30 31 30 0A 29 30 DD 30 30 30 30 CC 3D 32 30\n")
        fi.write("[menu] [3]\n")
    all_hex.append("A5")
    all_hex.append("30")
    all_hex.append("31")
    all_hex.append("30")
    all_hex.append("0A")
    all_hex.append("33")
    all_hex.append("50")
    all_hex.append("DD")
    all_hex.append("30")
    all_hex.append("30")
    all_hex.append("30")
    all_hex.append("30")
    all_hex.append("CC")
    all_hex.append("3D")
    all_hex.append("32")
    all_hex.append("30")
    all_hex.append("62")
    all_hex.append("3F")
    all_hex.append("32")
    all_hex.append("30")
    for i in range(12):
        all_hex.append("00")
    for i in hexl:
        all_hex.append(i)
    for z in range(6-e):
        for a in range(32):
            all_hex.append("20")
    with open("output.txt", "a", encoding="utf-8") as f:
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
        print("Inject these Hex code, addr start is DC30 (Go to by QuickCPYMax)")
        print(f.read())
    with open("QuickCPY.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        thay = False
        for line in lines:
            line = line.strip()
            if line.startswith("Launcher 6 lines (non-an)"):
                thay = True
            if thay and line =="-----":
                break
            if thay:
                print(line)

lang = input("Enter your lang. : English (Type 'EN') or Vietnamese (Type 'VN') ?\nNhập ngôn ngữ : Tiếng Anh (Gõ 'EN') hay Tiếng Việt (Gõ 'VN') ?\n")
if lang in ["Vn", "vn", "VN"]:
    print("Chương trình hỗ trợ Spell Casio fx580vnx. Phiên bản 3.0.7")
    print("Phần chia Hex có thể bị lỗi, thông cảm cho tôi nhé")
    a = input("Bạn muốn spell trên Casio fx580vnx kiểu gì ? Spell bằng các biến A, B, C hay bằng Inject \n Nhập 'var' để spell theo kiểu biến A, B, C \n Nhập 'inj' để spell bằng cách Inject (cho mấy ông thực sự biết làm QuickCPY++) \n")

    if a == 'var':
        b=input("Nhập câu bạn muốn spell (Tiếng Anh hoặc Tiếng Việt): ")
        spell_var_vn(b)
    if a == 'inj':
        with open("output.txt", "w", encoding='utf-8') as e:
            pass
        e=int(input("Bạn muốn spell mấy dòng trên Casio fx580vnx bằng phương pháp Inject ?\n"))
        if e<=4:
            spell_inj_4_ol_vn(e)
            print("Chi tiết hơn về QuickCPY++ vui lòng xem: https://drive.google.com/file/d/1UyLRde6fr7F0hiBt6naTSaba7vM20gmW/view?usp=drivesdk")
            print("Không hiểu thì có thể liên hệ Phong2k11 hoặc mình tại Discord nhé <3")
        elif e<=8 and e>4:
            if e==6:
                spell_inj_6_vn(e)
                print("Chi tiết hơn về QuickCPYMax tại địa chỉ DC30 vui lòng xem: https://drive.google.com/drive/folders/1Kzt-7rOwMWdnD0Em9ZwKpyvgMaMxOalU?usp=drive_link")
            elif e!=6:
                spell_inj_8_ol_vn(e)
                print("Chi tiết hơn về QuickCPYMax tại địa chỉ EA30 vui lòng xem: https://drive.google.com/drive/folders/1qe5C6_YtAQCWAGTPTxgtEUdAjOUShdEs?usp=drive_link")
        elif e>8:
            print("Số dòng quá trên Casio rồi :v")
    print("Dev lỏ: AxesMC\nDiscord: Casio My Life (@kiet130218_80627) và Kiet1802181 (@Kiet1302181)")
    if random.randint(1,100) == 1:
        print("Chúc bạn spell thành công !")
        
elif lang in ["En", "en", "EN"]:
    print("Program spell for Casio fx580vnx. Version 3.0.7")

    a = input("What method do you like to spell ? Spell by A, B, C variables or Inject \n Type 'var' to spell by A, B, C variables \n Type 'inj' to spell by Inject method (for who really know about QuickCPYs) \n")

    if a == 'var':
        b=input("Enter sentence do you want to spell in Casio fx580vnx: ")
        spell_var_en(b)
    if a == 'inj':
        with open("output.txt", "w", encoding='utf-8') as e:
            pass
        e=int(input("How many lines do you want to spell with Inject method ?\n"))
        if e<=4:
            spell_inj_4_ol_en(e)
            print("For all details about QuickCPY++: https://drive.google.com/file/d/1UyLRde6fr7F0hiBt6naTSaba7vM20gmW/view?usp=drivesdk")
            print("If you don't know, you can contact me or Phong2k11 (@phong2k11_4)")
        elif e<=8 and e>4:
            if e==6:
                spell_inj_6_en(e)
                print("For all details about QuickCPYMax at addr DC30: https://drive.google.com/drive/folders/1Kzt-7rOwMWdnD0Em9ZwKpyvgMaMxOalU?usp=drive_link")
            elif e!=6:
                spell_inj_8_ol_en(e)
                print("For all details about QuickCPYMax at addr EA30: https://drive.google.com/drive/folders/1qe5C6_YtAQCWAGTPTxgtEUdAjOUShdEs?usp=drive_link")
        elif e>8:
            print("Over lines but Casio fx580vnx can handle !")
        print("Sorry if my English so bad")
    print("Dev: AxesMC\nDiscord: Casio My Life (@kiet130218_80627) và Kiet1802181 (@Kiet1302181)")
    if random.randint(1,100) == 1:
        print("Good luck !")
if random.randint(1,1000) == 1:
        print("This dev wants to play Dead Rails :) My secret")
