import random

player_list = []
max_drink = {'1':2, '2':4, '3':6, '4':8, '5':10}
computer_name = ["나현", "한서", "석범", "도윤", "석현"]

# 게임 시작 시 y/n 외의 입력
# 본인 주량 / 게임 선택 시 1-5번 사이의 범위 외의 입력
# 같이 게임 할 인원수
class RangeException(Exception):
  def __init__(self):
    super().__init__('선택 범위 내의 입력이 아닙니다.')

class Player:
  def __init__(self, name, max, drink, state):
    self.name = name #이름
    self.max = max #치사량
    self.drink = drink #마신 잔 수
    self.state = state #컴퓨터인지 사람인지

def computer_print(friends_num):
  for i in range (friends_num):
    cname = computer_name[i]
    cmax = random.randint(1,10)
    player_list.append(Player(cname, cmax, 0, 'computer'))
    print(f"오늘 함께 취할 친구는 {cname}입니다! (치사량 : {cmax})")

def drink_print(player_list):
  for i in range (len(player_list)):
    print(f"{player_list[i].name}(은)는 지금까지 {player_list[i].drink}🍺! 치사량까지 {player_list[i].max}")
  print("/n")

def check_game_end(player_list):
  for i in range (len(player_list)):
    if(player_list[i].drink == player_list[i].max):
      print(f"{player_list[i].name}(이)가 전사했습니다 ... 꿈나라에서는 편히 쉬시길 ..zzz")
      print("⊂((・▽・))⊃⊂((・▽・))⊃          🍺 다음에 술 마시면 또 불러주세요! 안녕! 🍺          ⊂((・▽・))⊃⊂((・▽・))⊃" )
      exit()

def replace_curnum(curnum):
    st_curnum = "{}".format(curnum)
    answer = []
    cnt = 0
    for idx in range(len(st_curnum)):
        if(st_curnum[idx] == '3'):
            answer.append(st_curnum[idx].replace('3', '짝'))
            cnt += 1
        elif(st_curnum[idx] == '6'):
            answer.append(st_curnum[idx].replace('6', '짝'))
            cnt += 1
        elif(st_curnum[idx] == '9'):
            answer.append(st_curnum[idx].replace('9', '짝'))
            cnt += 1
        else:
            answer.append(st_curnum[idx])
    res = ''.join(answer)
    if cnt == 0:
        return res
    else: 
        new_res = ''
        for i in range(cnt):
            new_res += '짝'
        return new_res

def play_369(player_list):
    curnum = 1
    while(True):
        for turn in range (len(player_list)):
        ## player의 차례
            if(player_list[turn].state == 'player'):
                pl_choice = input("당신의 차례입니다! 숫자 또는 '짝'을 입력하세요! : ")
                result = replace_curnum(curnum)
                str_pl = pl_choice.strip()
                if(str_pl == result):
                    curnum += 1
                    continue
                else:
                    print(f"오답입니다! 이 잔(🍺)의 주인공은 {player_list[turn].name}입니다!🍺")
                    return curnum

                ## 컴퓨터의 차례
            else:
                print(f"{player_list[turn].name}의 차례입니다!")
                result = replace_curnum(curnum)
                choice_li = [result, str(curnum)]
                cp_choice = random.choice(choice_li)
                if(cp_choice == result):
                    print(f"{player_list[turn].name} : {cp_choice}")
                    curnum += 1
                    continue
                else:
                    print(f"{player_list[turn].name} : {cp_choice}")
                    print(f"오답입니다! 이 잔(🍺)의 주인공은 {player_list[turn].name}입니다!🍺")
                    return curnum

def zeroGame(player_list):
    #인트로
    print("""
ヽ(･̑ᴗ･̑)ﾉヽ(･̑ᴗ･̑)ﾉヽ(･̑ᴗ･̑)ﾉヽ(･̑ᴗ･̑)ﾉヽ(･̑ᴗ･̑)ﾉヽ(･̑ᴗ･̑)ﾉヽ(･̑ᴗ･̑)ﾉヽ(･̑ᴗ･̑)ﾉヽ(･̑ᴗ･̑)ﾉヽ(･̑ᴗ･̑)ﾉヽ(･̑ᴗ･̑)ﾉ

 #######  ######  ######    #####              ######   ###    ##   ##   ######  
     ###  ##      ##   ##  ##   ##            ####     ## ##   ### ###   ##      
    ###   ##      ##   ##  ##   ##            ###     ##   ##  #######   ##      
   ###    #####   ##  ##   ##   ##            ###     ##   ##  #######   #####   
  ###     ##      #####    ##   ##            ###  ## #######  ## # ##   ##      
          ##      ## ###   ##   ##                ### ##   ##  ##   ##   ##      
########  ######  ##  ###   #####            ##### ## ##   ##  ##   ##   ######

ヽ(･̑ᴗ･̑)ﾉヽ(･̑ᴗ･̑)ﾉヽ(･̑ᴗ･̑)ﾉヽ(･̑ᴗ･̑)ﾉヽ(･̑ᴗ･̑)ﾉヽ(･̑ᴗ･̑)ﾉヽ(･̑ᴗ･̑)ﾉヽ(･̑ᴗ･̑)ﾉヽ(･̑ᴗ･̑)ﾉヽ(･̑ᴗ･̑)ﾉヽ(･̑ᴗ･̑)ﾉ
    """)

    while(1):
        for turn in player_list:
            #참여자들이 올린 손가락 수의 합
            sum = 0

            #현재 차례의 컴퓨터 혹은 사람이 외칠 숫자
            answer = 0

            #사람이 들어올릴 손가락의 수
            p_thumb = 0

            #컴퓨터가 들어올릴 손가락의 수
            c_thumb = 0

            print("="*25)
            print(f"👍{turn.name}의 차례입니다.")
            print("="*25)
            #현재 차례가 사람인 경우
            if turn.state == "player":
                while(1):
                    try:
                        answer = int(input("외칠 숫자를 입력하세요. "))
                    except ValueError:
                        print("정수 값을 입력해주세요!")
                    else:
                        if answer > len(player_list)*2 or answer < 0:
                            print(f"외칠 수 있는 숫자는 0 ~ {len(player_list)*2}개 입니다.")
                        else:
                            break
            #현재 차례가 컴퓨터인 경우
            else:
                answer = random.randint(0, len(player_list)*2)

            #사람이 들어올릴 손가락의 수 입력
            while(1):
                try:
                    p_thumb = int(input("들어올릴 손가락의 개수를 입력하세요. "))
                except ValueError:
                    print("정수 값을 입력해주세요!")
                else:
                    if p_thumb > 2 or p_thumb < 0:
                        print("올릴 수 있는 엄지 손가락의 개수는 0 ~ 2개 입니다.")
                    else:
                        break
                     
            print(f"{turn.name} : {answer}!!")

            #컵퓨터가 들어올릴 손가락의 수 설정
            for j in player_list:
                if j.state != "player":
                    if turn.name == j.name:
                        c_thumb = random.randint(0, min(2, answer))
                    else:
                        c_thumb = random.randint(0, 2)
                    print(f"{j.name}(이)가 {c_thumb}개 손가락을 올렸습니다. ")
                    sum += c_thumb
                else:
                    print(f"{j.name}(이)가 {p_thumb}개 손가락을 올렸습니다. ")
                    sum += p_thumb
            #정답을 맞춘 경우 정답자를 제외한 나머지 참여자들이 한잔씩 마시고 게임 종료
            if sum == answer:
                nextPlayer = []
                for k in player_list:
                    if turn.name != k.name:
                        k.drink += 1
                        k.max -= 1
                        
                print(f"👏👏👏{turn.name}(이)가 숫자를 맞췄습니다!")
                print(f"🥃{turn.name}을 제외한 모든 참여자가 술을 마십니다!")
                return

#############################################################################
####                        게임 시작 이전 초기화 작업                         ####
#############################################################################
print("▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀")
print("""          __   __     ___   __   _  _   __   __           ___   __   _  _  ____ 
         / _\ (  )   / __) /  \ / )( \ /  \ (  )         / __) / _\ ( \/ )(  __)
        /    \/ (_/\( (__ (  O )) __ ((  O )/ (_/\      ( (_ \/    \/ \/ \ ) _) 
        \_/\_/\____/ \___) \__/ \_)(_/ \__/ \____/       \___/\_/\_/\_)(_/(____) """)
print("\n▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄ 🍺 A.L.C.O.H.O.L. G.A.M.E. 🍺 ▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀")

while(True):
  try:
    game_start = input("🍺 게임을 진행할까요?(y/n) : ")
    if(game_start == 'n'):
      print("🍺🍺 게임을 종료합니다~~ 다음에 또 봐요~!~!🍺🍺")
      exit()
    else:
      if(game_start != 'y'):
        raise RangeException
      else:
        myname = input("🍺 오늘 거하게 취해볼 당신의 이름은? : ")
        break;
  except Exception as e:
    print(e)
    
print("\n▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄ 🍺 소주 기준 당신의 주량은? 🍺 ▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀")
print("▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄ 🍺 1. 소주 반병 (2잔)")
print("▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄ 🍺 2. 소주 반병에서 한병 (4잔)")
print("▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄ 🍺 3. 소주 한병에서 한병 반 (6잔)")
print("▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄ 🍺 4. 소주 한병 반에서 두병 (8잔)")
print("▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄ 🍺 5. 소주 두병 이상 (10잔)")
print("▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀")

while(True):
  try:
    max_choice = input("\n🍺 당신의 치사량(주량)은 얼마만큼인가요? (1 ~ 5를 선택해주세요) : ")
    if(max_choice != '1' and max_choice != '2' and max_choice != '3' and max_choice != '4' and max_choice !='5'):
      raise RangeException()
    else: 
      mymax = max_drink.get(max_choice)
      player_list.append(Player(myname, mymax, 0,  'player'))
      break;
  except Exception as e:
    print(e)
  
while(True):
  try: 
    friends_num = int(input("\n🍺 함께 취할 친구들은 얼마나 필요하신가요? (최대 3명) : "))
  except ValueError:
    print("입력 받은 값이 정수가 아닙니다.")
  else:
    try:
      if(friends_num != 1 and friends_num != 2 and friends_num != 3):
        raise RangeException()
      else: 
        computer_print(friends_num)
        for i in range(len(player_list)):
          print(f"{player_list[i].name}(은)는 지금까지 {player_list[i].drink}🍺! 치사량까지 {player_list[i].max}")
        break;
    except Exception as e:
      print(e)

#############################################################################
####                           실제 게임 플레이 영역                          ####
#############################################################################

zeroGame(player_list)
drink_print(player_list)