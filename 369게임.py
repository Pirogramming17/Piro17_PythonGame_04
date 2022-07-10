import random

class Player:
    def __init__(self, name, max, drink, state):
        self.name = name #이름
        self.max = max #치사량
        self.drink = drink #마신 잔 수
        self.state = state #컴퓨터인지 사람인지

player_list = []
player_list.append(Player("철수", 5, 0, 'player'))
player_list.append(Player("영희", 5, 0, 'computer'))
player_list.append(Player("감자", 5, 0, 'computer'))
player_list.append(Player("고구마", 5, 0, 'computer'))


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

def play_369():
    clap = ['3', '6', '9']
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
                    print(f"{player_list[turn].name} : {cp_choice} \n")
                    curnum += 1
                    continue
                else:
                    print(f"{player_list[turn].name} : {cp_choice}")
                    print(f"오답입니다! 이 잔(🍺)의 주인공은 {player_list[turn].name}입니다!🍺")
                    return curnum

res = play_369()
