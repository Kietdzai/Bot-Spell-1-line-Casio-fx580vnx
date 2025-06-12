print("Chương trình hỗ trợ Spell Casio fx580vnx. Phiên bản 2.4")
print("Chương trình này không hỗ trợ spell các kí tự đặc biệt như ! , . ; > < v.v")
print("Phần chia Hex có thể bị lỗi, thông cảm cho tôi nhé")
a = input("Nhập câu bạn muốn spell (Câu Tiếng Anh): ")

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
            if part == '20': #Dòng này đẹp nè, có lẽ không ai để ý đâu hehe
                break
            if len(part) == 2:
                before_20 += 1

    if found_20:
        return after_20, before_20
    else:
        total = after_20
        return total, None

def spell (line):
    char_list = []
    str = line.replace(" ", "/")
    charst = ['a','b','c','d','e','f','g','j','k','L','M','N','O','T','U','V','W','X','Y','Z']
    char1=[]
    ds=list(str)
    hex_list=[]
    found_keys={}
    if len(str) > 17:
        print("Câu bạn vừa nhập quá 1 dòng (17 kí tự) ! ")
    else:
        print("Ok")
        print("Các kí tự cần: ")
        for i in str:
            if i == "/":
                print("    Space", end=' ')
            else:
                print(f"    {i}", end=' ')

        print("\nCác kí tự không thể viết trên bàn phím: ")
        for a in str:
            if a in charst:
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
                    print(f"{char} : Can't found in file")
            
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
            ds=['/' for _ in range(a)] + ds
            ds=ds + ['/' for _ in range(a)]
        elif space % 2 == 1:
            a = (space-1) // 2
            b = a + 1
            ds=['/' for _ in range(b)] + ds
            ds=ds+['/' for _ in range(a)]
        str_spell="".join(ds)
        print(str_spell)
        s=0
        for b in hex_list:
            for ch in b:
                if ch.isalpha():
                    char1.append(ch)
        char1.append('C')
        print("[v] có nghĩa là nhấn xuống\n[<] có nghĩa là nhấn sang trái\n[>] có nghĩa là nhấn sang phải\n[^] có nghĩa là nhấn lên")
        print('Bước 1: Reset máy: \n [shift] [9] [3] [=] [=]')
        print('Bước 2: Vào LineI/O: \n [shift] [menu] [1] [3]')
        print('Bước 3: Vào Basic Overflow: \n [x] [alpha] [CALC] [shift] [x] [x] [shift] [)] [9] [shift] [)] [9] [9] [9] [CALC] {[=] [AC]}-> fast [<] [del] [del] [CALC] [=] [<] [shift] [.]')
        print('Bước 4: Lấy các kí tự Hex cần thiết: \n ' + "".join(char1))
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
        print('([<] [9] [DEL])×', len(char1), '[DEL]×10', "[alpha] [∫]\nSau đó, làm sao cho màn hình Casio hiển thị như thế này:")
        template_A = ['1.0000', '__', '__', '__', '_!', '!_', '×10', '!!']
        template_B = ['1.', '__', '__', '__', '__', '__', '_!', '!_', '×10', '!!']
        template_C = ['1.', '__', '__', '__', '__', '__', '_!', '!_', '×10', '!!']

        filled_outputs = []
        hex_index = 0

        print("x:")
        for label, template in zip(['A', 'B', 'C'], [template_A, template_B, template_C]):
            result, hex_index, done, byte_count = fill_template(template, hex_list, hex_index)
            filled_outputs.append(f"{label} = {' '.join(result)}")
            if done:
                break
#Chắc không ai để ý đâu nhể ? Đoạn này nè
        for line in filled_outputs:
            print(line + ':')
            variables_printed = set()

            for line in filled_outputs:
                if '=' in line:
                    var_name = line.split('=')[0].strip()
                    variables_printed.add(var_name)

        print(f'[CALC] [=]×{len(variables_printed)+1} times')
        print('Bước 5: Lấy "an":\n[x] [alpha] [CALC] [shift] [x] [x] [shift] [)] [9] [shift] [)] [9] [CALC] [=] [<] [shift] [.] [shift] [.] [<] [<] [DEL] [v] [shift] [8] [v] [2] [6] [<] [<] [>] [9] [DEL] [<] [)] [+] [100 số bất kì]\n[CALC] [=]')
        print('Bước 6: Lấy "@":\n[x] [alpha] [CALC] [shift] [x] [x] [shift] [)] [9] [shift] [)] [9] [CALC] [=] [<] [shift] [.]', end='')
        if len(variables_printed) == 1:
            print('[shift] [7] [4] [8]', end=' ')
            print('([<] [9] [DEL])×1\n[DEL]×10',end='')
            print('[<] [9 optional numbers] [>] [alpha] [∫] [>] [alpha] [CALC] [alpha] [(-)]\n[CALC] ([=])×2 [^]')
        elif len(variables_printed) == 2:
            print('[shift] [7] [4] [8] [shift] [7] [4] [9]', end=' ')
            print('([<] [9] [DEL])×2\n[DEL]×10',end='')
            print('[<] [9 optional numbers] [>] [alpha] [∫] [>] [alpha] [CALC] [alpha] [(-)] [alpha] [∫] [>] [alpha] [CALC] [alpha] [□ \' "]\n[CALC] ([=])×3 [^]')
        elif len(variables_printed) == 3:
            print('[shift] [7] [4] [8] [shift] [7] [4] [9] [shift] [7] [1] [4]', end=' ')
            print('([<] [9] [DEL])×3\n[DEL]×10',end='')
            print('[<] [9 optional numbers] [>] [alpha] [∫] [>] [alpha] [CALC] [alpha] [(-)] [alpha] [∫] [>] [alpha] [CALC] [alpha] [□ \' "] [alpha] [∫] [>] [alpha] [CALC] [alpha] [x^-1]\n[CALC] ([=])×4 [^]')
        print('Bước 7: Xóa các byte không cần thiết:')
        results = []
        for raw in filled_outputs:
            label, parts = parse_line(raw)
            label, actions = process_template(label, parts)
            results.append((label, actions))

        for label, actions in reversed(results[:3]):
            for action in actions:
                print(f"  {action}", end='')

        print('\nBước 8: Làm giống y hệt đoạn dưới đây: ')
        for char in ds:
            if char in found_keys:
                print(f"{found_keys[char]}", end=' ')
            else:
                print(f"[>]", end=' ')
        p=0
        for h in ds:
            if h == "/":
                p+=1
        print(f'[{17-p} số bất kì] [shift] [(] [>] [2] [x]')
        print('Bước cuối: [CALC] [=]')
        file.close()
        print("Tôi thêm rồi đấy ! Dev: AxesMC")
        print("Bản sau, là bản 3.0 tôi sẽ cho các chức năng của Hex F4 vào, có thể sẽ hơi lâu đó")
spell(a)
