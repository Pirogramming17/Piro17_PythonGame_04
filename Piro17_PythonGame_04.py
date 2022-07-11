import random
import copy
import requests
from bs4 import BeautifulSoup as bs
import re

player_list = []
max_drink = {'1':2, '2':4, '3':6, '4':8, '5':10}
computer_name = ["나현", "한서", "석범", "도윤", "석현"]

# 게임 시작 시 y/n 외의 입력
# 본인 주량 / 게임 선택 시 1-5번 사이의 범위 외의 입력
# 같이 게임 할 인원수
class RangeException(Exception):
  def __init__(self):
    super().__init__('선택 범위 내의 입력이 아닙니다.')

class NoInputException(Exception):
  def __init__(self):
    super().__init__('입력이 없습니다.')

class Player:
  def __init__(self, name, max, drink, state):
    self.name = name #이름
    self.max = max #치사량
    self.drink = drink #마신 잔 수
    self.state = state #컴퓨터인지 사람인지

def computer_print(friends_num):
  for i in range (friends_num):
    cname = random.choice(computer_name)
    computer_name.remove(cname)
    cmax = random.randint(2,10)
    player_list.append(Player(cname, cmax, 0, 'computer'))
    print(f"오늘 함께 취할 친구는 {cname}입니다! (치사량 : {cmax})")

def drink_print(player_list):
  print('\n')
  for i in range (len(player_list)):
    print(f"{player_list[i].name}(은)는 지금까지 {player_list[i].drink}🍺! 치사량까지 {player_list[i].max}")
  print("\n")

def check_game_end(player_list):
  for i in range (len(player_list)):
    if(player_list[i].max == 0):
      print(f"{player_list[i].name}(이)가 전사했습니다 ... 꿈나라에서는 편히 쉬시길 ..zzz")
      print("⊂((・▽・))⊃⊂((・▽・))⊃  🍺 다음에 술 마시면 또 불러주세요! 안녕! 🍺  ⊂((・▽・))⊃⊂((・▽・))⊃" )
      exit()

def crawl_station():
    headers = {
        'Referer': 'http://www.seoulmetro.co.kr/kr/cyberStation.do?menuIdx=538',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }

    response = requests.get(
        'http://www.seoulmetro.co.kr/kr/getLineData.do', headers=headers, verify=False)

    soup = bs(response.text, "html.parser")

    linename = re.compile('{}(.*){}'.format(re.escape('"data-label" : "'),
                        re.escape('"'))).findall(response.text)
    stname = re.compile('{}|{}(.*){}'.format(re.escape('"data-label" : "'),
                        re.escape('"station-nm": "'), re.escape('"'))).findall(response.text)
    del stname[0]

    stname.append("")

    stations = {}
    for i in range(len(linename)):
        line = []

        while True:
            if stname[0] == "":
                del stname[0]
                break
            line.append(stname[0].replace("\\n", " "))
            del stname[0]

        stations[linename[i]] = line
    
    return stations

#############################################################################
####                         1. 369 GAME  - 도윤                           ####
#############################################################################
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

def play_369(player_list, idx_first):
  print("""ــہہــــــــ٨ــــــــــــ❥ــ٨ـــــــــہــــــــــ❥ــ٨ــــــــــ""")
  print("""
 ______  # _______ # _______ # _______ #       #       #       #
(_____ \ #(_______)#(_______)#(_______)#       #       #       #
 _____) )# ______  # _______ # _   ___ # _____ # ____  # _____ #
(_____ ( #|  ___ \ #(_____  |#| | (_  |#(____ |#|    \ #| ___ |#
 _____) )#| |___) )#      | |#| |___) |#/ ___ |#| | | |#| ____|#
(______/ #|______/ #      |_|# \_____/ #\_____|#|_|_|_|#|_____)#
  """)
  print("""ــہہــــــــ٨ــــــــــــ❥ــ٨ـــــــــہــــــــــ❥ــ٨ــــــــــ""")
  print("~~~~~~~~~~~~~~~ 3 6 9 ~~ 3 6 9 ~~ 3 6 9 ~~ 3 6 9 ~~~~~~~~~~~~~~~ ")
  print(f"{player_list[idx_first].name}부터 시작!")
  
  # 게임 순서 결정 (게임을 선택한 사람이 첫번째))
  player = []
  player.append(player_list[idx_first])
  for l in range(len(player_list)):
    if(player[0].name == player_list[l].name):
      continue
    else:
      player.append(player_list[l])

  curnum = 1
  while(True):
      for turn in range (len(player)):
      ## player의 차례
        if(player[turn].state == 'player'):
          pl_choice = input("당신의 차례입니다! 숫자 또는 '짝'을 입력하세요! : ")
          result = replace_curnum(curnum)
          str_pl = pl_choice.strip()
          if(str_pl == result):
            curnum += 1
            continue
          else:
            print(f"오답입니다! 이 잔(🍺)의 주인공은 {player[turn].name}입니다!🍺")
            for k in range (len(player)):
              if(player[turn] == player_list[k]):
                player_list[k].max -= 1
                player_list[k].drink += 1
                return player_list[k].name
                ## 컴퓨터의 차례
        else:
          print(f"{player[turn].name}의 차례입니다!")
          result = replace_curnum(curnum)
          choice_li = [result, str(curnum)]
          cp_choice = random.choice(choice_li)
          if(cp_choice == result):
            print(f"{player[turn].name} : {cp_choice}")
            curnum += 1
            continue
          else:
            print(f"{player[turn].name} : {cp_choice}")
            print(f"오답입니다! 이 잔(🍺)의 주인공은 {player[turn].name}입니다!🍺")
            for k in range (len(player)):
              if(player[turn] == player_list[k]):
                player_list[k].max -= 1
                player_list[k].drink += 1
                return player_list[k].name


##############################################################################
####                   2. The Game Of Death  - 석범                       ####
#############################################################################
def play_thegameofdeath(player_list):
    print("#######                   #####                                           ######                             ")
    print("   #    #    # ######    #     #   ##   #    # ######     ####  ######    #     # ######   ##   ##### #    # ")
    print("   #    #    # #         #        #  #  ##  ## #         #    # #         #     # #       #  #    #   #    # ")
    print("   #    ###### #####     #  #### #    # # ## # #####     #    # #####     #     # #####  #    #   #   ###### ")
    print("   #    #    # #         #     # ###### #    # #         #    # #         #     # #      ######   #   #    # ")
    print("   #    #    # #         #     # #    # #    # #         #    # #         #     # #      #    #   #   #    # ")
    print("   #    #    # ######     #####  #    # #    # ######     ####  #         ######  ###### #    #   #   #    # ")

    array = []

    for i in range(len(player_list)-1):
        num = len(player_list)-1
        array.append(player_list[i+1].name)
    array.append(player_list[0].name)
    startman = player_list[turn].name
    startmannum = array.index(startman)
    print(startman, '님이 술래! \U0001F601')
    print('~~~~~ 아 신난다 \U0001F606 아 재미난다 \U0001F923 더 게임 오브 데 스! ~~~~~')
    print(startman)
    if startman == player_list[0].name:
        while True:
            try:
                number = int(input('2이상 8이하의 정수를 외쳐 주세요! '))
            except ValueError:
                print("정수 값을 입력해주세요!")
            else:
                if 2 > number or 8 < number:
                    print('잘못된 숫자입니다. 다시입력해주세요!')
                else:
                    break
    else:
        number = random.randint(2, 8)
        print('2이상 8이하의 정수를 외쳐 주세요! ', number)
    array2 = []
    for i in range(len(player_list)):
        numbering = [j for j in range(len(player_list))]
        del numbering[i]
        array2.append(random.choice(numbering))

    for i in range(-num+startmannum-1, startmannum):
        print(array[i], '\U0001F449', array[array2[i]])

    for i in range(int(number)):
        print(array[startmannum], " : ", i+1,
              '! \U0001F60E \U0001F449', array[array2[startmannum]])
        startmannum = array.index(array[array2[startmannum]])
        if i == int(number)-1:
            print(array[startmannum], " : \U0001F92E")
            for i in range(len(player_list)):
                if array[startmannum] == player_list[i].name:
                    player_list[i].max -= 1
                    player_list[i].drink += 1
            return array[startmannum]



#############################################################################
####                           3. 손병호 게임 - 나현                         ####
#############################################################################
def play_sonbyungho(player_list):
    #인트로
    print("""˚⋆☂˚｡⋆｡˚☽˚｡⋆..⋆｡⋆☂˚｡⋆｡˚☽˚｡⋆..⋆｡⋆☂˚｡⋆｡˚☽˚｡⋆..⋆｡⋆☂˚｡⋆｡˚☽˚｡⋆..⋆｡⋆☂˚｡⋆｡˚☽˚｡⋆.""")
    print("""
  #####                     ######                                       ##   ##          
 ##   ##                    ##   ##                                      ##   ##          
 ##        #####   ## ###   ##   ##  ##  ##   ##   ##  ## ###    ######  ##   ##   #####  
  #####   ##   ##  ###  ##  ######   ##  ##   ##   ##  ###  ##  ##   ##  #######  ##   ## 
      ##  ##   ##  ##   ##  ##   ##  ##  ##   ##   ##  ##   ##  ##   ##  ##   ##  ##   ## 
 ##   ##  ##   ##  ##   ##  ##   ##  ##  ##   ##  ###  ##   ##  ##   ##  ##   ##  ##   ## 
  #####    #####   ##   ##  ######    #####    ### ##  ##   ##   ######  ##   ##   #####  
                                         ##                          ##                   
                                      ####                       ##### 
""")
    print("""˚⋆☂˚｡⋆｡˚☽˚｡⋆..⋆｡⋆☂˚｡⋆｡˚☽˚｡⋆..⋆｡⋆☂˚｡⋆｡˚☽˚｡⋆..⋆｡⋆☂˚｡⋆｡˚☽˚｡⋆..⋆｡⋆☂˚｡⋆｡˚☽˚｡⋆.""")
    print("지금부터 손병호 게임을 시작합니다.")
    print("여러분들은 모두 손가락을 펴주시길 바라겠습니다.")
            
    #질문 리스트
    que_li = ["염색한 사람 접어","반지 낀 사람 접어" \
              ,"반바지 입은 사람 접어"\
              ,"술 마시고 싶은 사람 접어","집 가고 싶은 사람 접어"\
              ,"밤 샌 사람 접어","겨울 좋은 사람 접어","여름 좋은 사람 접어"\
              ,"여행 가고 싶은 사람 접어","번지점프 해본 사람 접어"\
              ,"개발자 되고 싶은 사람 접어","누나 있는 사람 접어","언니 있는 사람 접어"\
              ,"여동생 있는 사람 접어","오빠 있는 사람 접어","형 있는 사람 접어"\
              ,"남동생 있는 사람 접어","17학번 접어","18학번 접어","19학번 접어","20학번 접어"\
              ,"21학번 접어","22학번 접어","민트초코 안먹는 사람 접어","민트초코 먹는 사람 접어"\
              ,"부먹인 사람 접어","찍먹인 사람 접어","소주파인 사람 접어","맥주파인 사람 접어","소맥파인 사람 접어"\
              ]    
    
    finger = [5,5,5,5]
    choice_list = ['y', 'n']

    while(1):
        for turn in range(len(player_list)):
            #각 참여자들의 손가락 개수

            print("="*25)
            print(f"👍{player_list[turn].name}의 차례입니다.")
            print("="*25)
            #현재 차례가 사람인 경우
            if player_list[turn].state == "player":
                while(1):
                    try:
                        choice = int(input("접을 사람을 골라주세요!(1-30) ")) #문제를 골라주세요
                    except ValueError:
                        print("정수 값을 입력해주세요!")
                    else:
                        if choice > 30 or choice < 1:
                            print("1 ~ 30사이에서 골라주세요!")
                        else:
                            print(que_li[choice-1])
                            break
                        
            #현재 차례가 컴퓨터인 경우
            else:
                choice = random.randint(1, 30)
                print(que_li[choice-1])

            #사람이 선택할 답변
            while(1):
                try:
                    p_answer = input("손가락을 접을까요?(y/n) ")
                    if(p_answer != "y" and p_answer != "n"):
                      raise RangeException
                except Exception as e:
                    print(e)
                else:
                    break
        
            #컴퓨터가 고를 답변
            for j in range(len(player_list)):
                if player_list[j].state != "player":
                    c_answer = random.choice(choice_list)
                    if (c_answer=='y'):
                        print(f"{player_list[j].name}(이)가 손가락을 접었습니다. ")
                        finger[j] -= 1
                else:
                    if(p_answer == 'y'):
                        print(f"{player_list[j].name}(이)가 손가락을 접었습니다. ")
                        finger[j] -= 1        

            #누군가의 손가락이 다 소진되면 그 사람이 술 마시고 종료
            #여러명이면 랜덤으로 선택
            if (finger[0] == 0 or finger[1] == 0 or finger[2] == 0 or finger[3] == 0):
                nextSelecter = []
                for k in range(len(player_list)):
                  if finger[k] == 0:
                    player_list[k].drink += 1
                    player_list[k].max -= 1
                    nextSelecter.append(player_list[k].name)
                    print(f"👏👏👏{player_list[k].name}(이)의 손가락이 모두 접혔습니다!")
                
                for l in range(len(nextSelecter)):
                  print(nextSelecter[l], end = '')
                  print("가 술을 마십니다!🥃")

                return random.choice(nextSelecter)

#############################################################################
####                     4. 지하철 게임 (크롤링) - 한서                       ####
#############################################################################
def subway_game(player_list):
    STATIONS = crawl_station()

    print("===================================================================================")
    print("""
     _____         _                               _____                         
    /  ___|       | |                             |  __ \                        
    \ `--.  _   _ | |__  __      __  __ _  _   _  | |  \/  __ _  _ __ ___    ___ 
     `--. \| | | || '_ \ \ \ /\ / / / _` || | | | | | __  / _` || '_ ` _ \  / _  
    /\__/ /| |_| || |_) | \ V  V / | (_| || |_| | | |_\ \| (_| || | | | | ||  __/
    \____/  \__,_||_.__/   \_/\_/   \__,_| \__, |  \____/ \__,_||_| |_| |_| \___|
                                            __/ |                                
                                           |___ /                                 
    """)

    print("===================================================================================")
    print("~~~~~~~~~~~~~~~~~~~~~~~~지하철! 지하철! 지하철! 지하철!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    player = player_list[turn]
    while 1:  # 호선 입력
        

        if player.state == 'player':
            station = input("몇호선~~~~몇호선~~~~??(입력형식 : 0호선) : ")
            if station in STATIONS.keys():
                break
            print("없는 노선입니다. 지하철 노선 이름을 정확히 입력하세요.")
        else:
            print("몇호선~~~~몇호선~~~~??")
            station = random.choice(list(STATIONS.keys()))
            print(f"{station}이 선택됐습니다.")
            break

    visited = []  # 한 번 대답한 역 이름 모아두는 곳

    i = 0
    while 1:
        player = player_list[i]
        if player.state == 'player':
            answer = input(f"[{player.name}] {station} 역을 입력하세요.: ")
            if answer not in STATIONS[station]:  # answer가 역 이름 목록 안에 없을 때
                print("🤪탈락!!!!!!!!!!!그런 역은 없지!!한 잔(🍺) 마시기!!!")
                player.drink += 1
                player.max -= 1
                return player.name

            if answer in visited:
                print("🤪탈락!!!!!!!!!!이미 했지!!!한 잔(🍺) 마시기!!!")
                player.drink += 1
                player.max -= 1

                return player_list[i].name
                break
            else:
                visited += [answer]
                print("정답입니다!")

        else:
            answer = random.choice(random.choice(list(STATIONS.values())))
            print(f"[{player.name}] ", answer)
            if answer not in STATIONS[station]:  # answer가 역 이름 목록 안에 없을 때
                print("🤪탈락!!!!!!!!!!!그런 역은 없지!!한 잔(🍺) 마시기!!!")
                player.drink += 1
                player.max -= 1
                return player.name

            if answer in visited:
                print("🤪탈락!!!!!!!!!!이미 했지!!!한 잔(🍺) 마시기!!!")
                player.drink += 1
                player.max -= 1
                return player_list[i].name
                break
            else:
                visited += [answer]
                print("정답입니다!")

        i += 1
        i %= len(player_list)

#############################################################################
####                         5. ZERO GAME - 석현                          ####
#############################################################################
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
    order = []
    order = player_list.copy()
    random.shuffle(order)
    while(1):
        for turn in order:
            #참여자들이 올린 손가락 수의 합
            sum = 0

            #현재 차례의 컴퓨터 혹은 사람이 외칠 숫자
            answer = 0

            #사람이 들어올릴 손가락의 수
            p_thumb = 0

            #컴퓨터가 들어올릴 손가락의 수
            c_thumb = 0

            print("="*30)
            print(f"👍{turn.name}의 차례입니다.")
            print("="*30)
            #현재 차례가 사람인 경우
            if turn.state == "player":
                while(1):
                    try:
                        answer = int(input("외칠 숫자를 입력하세요. "))
                    except ValueError:
                        print("정수 값을 입력해주세요!")
                    else:
                        if answer > len(player_list)*2 or answer < 0:
                            print(f"🤪🤪🤪🤪🤪🤪🤪🤪 바보~ 외칠 수 있는 숫자는 0 ~ {len(player_list)*2}개 입니다!")
                            print(f"👏👏👏{turn.name}(이)가 바보샷 당첨!")
                            turn.drink += 1
                            turn.max -= 1
                            return turn.name
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
                nextSelecter = []
                for k in player_list:
                    if turn.name != k.name:
                        k.drink += 1
                        k.max -= 1
                        nextSelecter.append(k.name)
                print("@"*40)
                print(f"👏👏👏{turn.name}(이)가 숫자를 맞췄습니다!")
                print(f"🥃{turn.name}을/를 제외한 모든 참여자가 술을 마십니다!")
                print("@"*40)

                return random.choice(nextSelecter)


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
        break
  except Exception as e:
    print(e)

while(True):
  try:
    myname = input("🍺 오늘 거하게 취해볼 당신의 이름은? : ")
    if(myname == ''):
      raise NoInputException
    else:
      break
  except Exception as n:
    print(n)

print("\n▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄ 🍺 소주 기준 당신의 주량은? 🍺 ▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀")
print("▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄ 🍺 1. 소주 반병 (2잔)")
print("▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄ 🍺 2. 소주 반병에서 한병 (4잔)")
print("▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄ 🍺 3. 소주 한병에서 한병 반 (6잔)")
print("▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄ 🍺 4. 소주 한병 반에서 두병 (8잔)")
print("▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄ 🍺 5. 소주 두병 이상 (10잔)")
print("▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀")

while(True):
  try:
    max_choice = input("🍺 당신의 치사량(주량)은 얼마만큼인가요? (1 ~ 5를 선택해주세요) : ")
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
    friends_num = int(input("🍺 함께 취할 친구들은 얼마나 필요하신가요? (최대 3명) : "))
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

# #############################################################################
# ####                           실제 게임 플레이 영역                          ####
# #############################################################################
turn = 0
while(True):
  print("\n▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄ 🍺 오 늘 의 술 게 임 🍺 ▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀")
  print("▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄ 🍺 1. 3 6 9 ")
  print("▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄ 🍺 2. 더 게임 오브 데스 ")
  print("▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄ 🍺 3. 손병호 게임")
  print("▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄ 🍺 4. 지하철 게임")
  print("▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄ 🍺 5. 제로 게임")
  print("▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀")

  while(True):
    try:
      if(player_list[turn].state == 'player'):
        choice = input(f"{player_list[turn].name}이(가) 좋아하는 랜덤~ 게임~ 무슨~ 게임~ 게임~ 스타트~ : ")
        if(choice != '1' and choice != '2' and choice != '3' and choice != '4' and choice != '5'):
          raise RangeException()
        else:
          break;
      else:
        cont = input("술게임 진행중! 다른 사람의 턴입니다. 그만하고 싶으면 'exit'를, 계속 하시려면 아무 키나 눌러주세요! : ")
        if(cont == 'exit'):
          print("중간에 그만두시는군요..? 뭐 .. 그럴 수 있죠.. 아쉽지만 술게임을 종료합니다! 다음에 또 봐요 안녕~~~~")
          exit()
        else:
          choice = str(random.randint(1, 5))
          print(f"{player_list[turn].name}이 좋아하는 랜덤~ 게임~ 무슨~ 게임~ 게임~ 스타트~ : ", choice)
          break;
    except Exception as e:
      print(e)

  # 369 게임
  if(choice == '1'):
    loser_name = play_369(player_list, turn)
    drink_print(player_list)
    check_game_end(player_list)

  # 더 게임 오브 데스
  elif(choice == '2'):
    loser_name = play_thegameofdeath(player_list)
    drink_print(player_list)
    check_game_end(player_list)

  # 손병호 게임
  elif(choice == '3'):
    loser_name = play_sonbyungho(player_list)
    drink_print(player_list)
    check_game_end(player_list)

# 지하철 게임
  elif(choice == '4'):
    loser_name = subway_game(player_list)
    drink_print(player_list)
    check_game_end(player_list)
  
  # 제로 게임
  elif(choice == '5'):
    loser_name = zeroGame(player_list)
    drink_print(player_list)
    check_game_end(player_list)
  
  # 다음 차례의 사람을 선택
  for i in range(len(player_list)):
    if(player_list[i].name == loser_name):
      turn = i