import random

board = [str(i) for i in range(1,101)] 

def print_board(board):# Вывод доски на экран
	for i in range(100):
		print(board[i], end='\t')
		if (i + 1) % 10 == 0:
			print('\n')

def select_mark():# Выбор игроком своей роли
	player_mark = ''
	while player_mark not in ('X', 'O'):
		player_mark = input('Please, choose your marker: X or O: ').upper()
		if player_mark == 'X':
			computer_mark = 'O'
		else:
			computer_mark = 'X'
	return player_mark, computer_mark

remain_cells = [str(i) for i in range(1,101)] 

def put_mark_remove_cell(index, mark, remain_cells, board):#Установка маркера в ячейку и удаление ячейки из списка оставшихся ячеек
	remain_cells.remove(board[index])
	board[index] = mark


def check_diagonal_line(index, mark, board):# Проверка ряда по двум диагоналям
	count = 1
	step = 0
	for i in range(9-index//10):
		if (index + step + 1) % 10 != 0 and (index + step) // 10 != 9: 
			step += 11
			if board[index+step] == mark:
				count += 1
			else:
				break
		else:
			break
	step = 0
	for i in range(index//10):
		if (index + step + 1) % 10 != 1 and (index + step) // 10 != 0: 
			step -= 11
			if board[index+step] == mark:
				count += 1
			else:
				break
		else:
			break
	if count >= 5:
		return True
	count = 1
	step = 0
	for i in range(9-index//10): 
		if (index + step + 1) % 10 != 1 and (index + step) // 10 != 9: 
			step += 9
			if board[index+step] == mark:
				count += 1
			else:
				break
		else:
			break
	step = 0
	for i in range(index//10):
		if (index + step + 1) % 10 != 0 and (index + step) // 10 != 0:
			step -= 9
			if board[index+step] == mark:
				count += 1
			else:
				break
		else:
			break
	if count >= 5:
		return True

def check_gorizontal_line(index, mark, board):#Проверка ряда по горизонтали
	count = 1
	step = 1
	while True:
		if (index + 1) % 10 != 0: 
			for i in range(9-index%10):
				if board[index+step] == mark:
					count += 1
					step += 1
				else:
					break
		step = -1
		if (index + 1) % 10 != 1: 
			for i in range(index%10):
				if board[index+step] == mark:
					count += 1
					step -= 1
				else:
					break
		break
		
	if count >= 5:
		return True

def check_vertical_line(index, mark, board):#Проверка ряда по вертикали
	count = 1
	step = 10
	while True:
		if index // 10 != 9: 
			for i in range(9-index//10):
				if board[index+step] == mark:
					count += 1
					step += 10
				else:
					break
		step = -10
		if index // 10 != 0: 
			for i in range(index//10):
				if board[index+step] == mark:
					count += 1
					step -= 10
				else:
					break
		break
	if count >= 5:
		return True

def check_game_finish(index, mark, board):# Финальная проверка на наличие пяти маркеров подряд
	if check_gorizontal_line(index, mark, board) or check_vertical_line(index, mark, board) or check_diagonal_line(index, mark, board):
		return True

def replay():#Функция для начала новой игры
    decision = ""
    while decision not in ('y', 'n'):
        decision = input(
            'Would you like to play again? Type "y" or "n"'
        ).lower()

    return decision == 'y'

def clear_screen():# Очищение экрана путём добавления пустых строк
    print('\n' * 100)



def computer_loose_check(computer_mark, remain_cells, board):#Проверка хода компьютера, набирается 5 в ряд и он ищет новую позицию
	remain_cells_in_cycle = remain_cells.copy()	
	for i in range(len(remain_cells)):
		index = int(random.choice(remain_cells_in_cycle)) - 1
		remain_cells_in_cycle.remove(board[index])
		tmp = board[index]
		put_mark_remove_cell(index, computer_mark, remain_cells, board)
		if check_game_finish(index, computer_mark, board) and i != len(remain_cells):
			remain_cells.append(tmp)
			board[index] = tmp
			continue
		elif not check_game_finish(index, computer_mark, board):
			return True
		else:
			return False	

def space_check(index, board): # Проверка занята ли уже ячейка
		return board[index] in ('X', 'O')

def start_new_game(): # Начало новой игры
	board = [str(i) for i in range( 1,101)]
	remain_cells = [str(i) for i in range(1,101)]
	player_mark, computer_mark = select_mark()

	return board, remain_cells, player_mark, computer_mark

player_mark, computer_mark = select_mark()

def main_game(player_mark, computer_mark, board, remain_cells):# Основная функция игры
	print_board(board)
	print('\n\n')
	while True:# Ход игрока
		if len(remain_cells) > 0:
			index = int(input('Choose your next position : ')) - 1
			assert index in range(100),'Wrong value.'
			if space_check(index, board):
				print('Position busy')
				continue
			put_mark_remove_cell(index, player_mark, remain_cells, board)
			if check_game_finish(index, player_mark, board):
				print_board(board)
				print('You lose')
				if replay():
					board, remain_cells, player_mark, computer_mark = start_new_game()
					print_board(board)
					print('\n\n')
					continue
				else:
					return
			

			if computer_loose_check(computer_mark, remain_cells, board): #Ход компьютера
				print_board(board)
				continue
			else:
				print_board(board)
				print('Computer lose') 
				if replay():
					board, remain_cells, player_mark, computer_mark = start_new_game()
					print_board(board)
					print('\n\n')
					continue
				else:
					return
			print_board(board)	
		else:
			print('The game ended in a draw.') # Ничья
			if replay():
				board, remain_cells, player_mark, computer_mark = start_new_game()
				print_board(board)
				print('\n\n')
				continue
			else:
				return

if __name__ == '__main__':
	main_game(player_mark, computer_mark, board, remain_cells)
