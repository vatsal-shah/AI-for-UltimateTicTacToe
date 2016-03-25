import copy

class Player74:
	def __init__(self):
		pass
	def move(self, temp_board, temp_block, old_move, flag):
		if old_move == (-1,-1):
			return (4,4)
		else:
			l = copy.deepcopy(temp_board)
			list_of_permitted_cells = self.get_valid_cells(l,old_move)
			alpha = -100000000
			beta = 100000000
			for cell in list_of_permitted_cells:
				if alpha < beta:
					val = self.abc(l,cell,flag,0,-1,alpha,beta,temp_block)
					if val[0] > alpha:
						ans = cell
						alpha = val[0]
			return ans

	def get_permitted_cells(self,a,temp_board):
		ans=[]
		for tup in a:
			x = tup[0]
			y = tup[1]
			for i in range(3*x, 3*x + 3):
				for j in range(3*y, 3*y + 3):
					if temp_board[i][j] == '-':
						ans.append((i,j))
		return ans


	def get_permitted_blocks(self,old_move):
		permitted_blocks = []
		# if old_move == (-1,-1):
		# 	for i in range(3):
		# 		for j in range(3):
		# 			permitted_blocks.append((i,j))
		#else:
		row = old_move[0]
		col = old_move[1]
		if row%3 == 0:
			if col%3 == 0:
				permitted_blocks.append((0,1))
				permitted_blocks.append((1,0))
			elif col%3 == 1:
				permitted_blocks.append((0,0))
				permitted_blocks.append((0,2))
			elif col%3 == 2:
				permitted_blocks.append((0,1))
				permitted_blocks.append((1,2))
		elif row%3 == 1:
			if col%3 == 0:
				permitted_blocks.append((0,0))
				permitted_blocks.append((2,0))
			elif col%3 == 1:
				permitted_blocks.append((1,1))
			elif col%3 == 2:
				permitted_blocks.append((0,2))
				permitted_blocks.append((2,2))
		elif row%3 == 2:
			if col%3 == 0:
				permitted_blocks.append((1,0))
				permitted_blocks.append((2,1))
			elif col%3 == 1:
				permitted_blocks.append((2,0))
				permitted_blocks.append((2,2))
			elif col%3 == 2:
				permitted_blocks.append((1,2))
				permitted_blocks.append((2,1))
		return permitted_blocks

	def check_block_for_validity(self,a,board):
		ans = []
		for tup in a:
			flag = 0
			x = tup[0]
			y = tup[1]
			if board[3*x][3*y] == board[3*x][3*y + 1] and board[3*x][3*y + 1] == board[3*x][3*y + 2] and board[3*x][3*y] != '-':
				flag = 1
			elif board[3*x + 1][3*y] == board[3*x + 1][3*y + 1] and board[3*x + 1][3*y + 1] == board[3*x + 1][3*y + 2] and board[3*x + 1][3*y] != '-':
				flag = 1
			elif board[3*x + 2][3*y] == board[3*x + 2][3*y + 1] and board[3*x + 2][3*y + 1] == board[3*x + 2][3*y + 2] and board[3*x + 2][3*y] != '-':
				flag = 1
			elif board[3*x][3*y] == board[3*x + 1][3*y] and board[3*x + 1][3*y] == board[3*x + 2][3*y] and board[3*x][3*y] != '-':
				flag = 1
			elif board[3*x][3*y + 1] == board[3*x + 1][3*y + 1] and board[3*x + 1][3*y + 1] == board[3*x + 2][3*y + 1] and board[3*x][3*y + 1] != '-':
				flag = 1
			elif board[3*x][3*y + 2] == board[3*x + 1][3*y + 2] and board[3*x + 1][3*y + 2] == board[3*x + 2][3*y + 2] and board[3*x][3*y + 2] != '-':
				flag = 1
			elif board[3*x][3*y] == board[3*x + 1][3*y + 1] and board[3*x + 1][3*y + 1] == board[3*x + 2][3*y + 2] and board[3*x][3*y] != '-':
				flag = 1
			elif board[3*x][3*y + 2] == board[3*x + 1][3*y + 1] and board[3*x + 1][3*y + 1] == board[3*x + 2][3*y] and board[3*x][3*y + 2] != '-':
				flag = 1
			flag2 = 0
			for i in range(3*x,3*x + 3):
				if flag2 != 1:
					for j in range(3*y, 3*y + 3):
						if board[i][j] == '-':
							flag2 = 1
							break
			if flag == 0 and flag2 == 1:
				ans.append(tup)
		return ans

	def get_valid_cells(self,temp_board,old_move):
		list_of_permitted_blocks = self.get_permitted_blocks(old_move)
		list_of_checked_blocks = self.check_block_for_validity(list_of_permitted_blocks,temp_board)
		list_of_final_blocks = list_of_checked_blocks[:]
		if not list_of_checked_blocks:
			for i in range(3):
				for j in range(3):
					if (i,j) not in list_of_permitted_blocks:
						list_of_final_blocks.append((i,j))
		list_of_blocks = self.check_block_for_validity(list_of_final_blocks,temp_board)
		list_of_permitted_cells = self.get_permitted_cells(list_of_blocks,temp_board)
		return list_of_permitted_cells

	def evaluate_block_heuristic(self,board,tup,flag):
		x = tup[0]
		y = tup[1]
		myflag = flag
		oppflag = 'x'
		if flag == 'x':
			oppflag = 'o'
		val = 0.0
		prob = 0.0
		for i in range(3*x,3*x+3):
			if prob != 1 and prob != -1:
				if board[i][3*y]==oppflag and board[i][3*y+1]=='-' and board[i][3*y+2]=='-':
					val -= 1
				elif board[i][3*y]=='-' and board[i][3*y+1]==oppflag and board[i][3*y+2]=='-':
					val -= 1
				elif board[i][3*y]=='-' and board[i][3*y+1]=='-' and board[i][3*y+2]==oppflag:
					val -= 1
				elif board[i][3*y]==oppflag and board[i][3*y+1]==oppflag and board[i][3*y+2]=='-':
					val -= 10
				elif board[i][3*y]==oppflag and board[i][3*y+1]=='-' and board[i][3*y+2]==oppflag:
					val -= 10
				elif board[i][3*y]=='-' and board[i][3*y+1]==oppflag and board[i][3*y+2]==oppflag:
					val -= 10
				elif board[i][3*y]==oppflag and board[i][3*y+1]==oppflag and board[i][3*y+2]==oppflag:
					prob = -1
					break
				elif board[i][3*y]==myflag and board[i][3*y+1]=='-' and board[i][3*y+2]=='-':
					val += 1
				elif board[i][3*y]=='-' and board[i][3*y+1]==myflag and board[i][3*y+2]=='-':
					val += 1
				elif board[i][3*y]=='-' and board[i][3*y+1]=='-' and board[i][3*y+2]==myflag:
					val += 1
				elif board[i][3*y]==myflag and board[i][3*y+1]==myflag and board[i][3*y+2]=='-':
					val += 10
				elif board[i][3*y]==myflag and board[i][3*y+1]=='-' and board[i][3*y+2]==myflag:
					val += 10
				elif board[i][3*y]=='-' and board[i][3*y+1]==myflag and board[i][3*y+2]==myflag:
					val += 10
				elif board[i][3*y]==myflag and board[i][3*y+1]==myflag and board[i][3*y+2]==myflag:
					prob = 1
					break
		for j in range(3*y,3*y+3):
			if prob != 1 and prob != -1:
				if board[3*x][j]==oppflag and board[3*x+1][j]=='-' and board[3*x+2][j]=='-':
					val -= 1
				elif board[3*x][j]=='-' and board[3*x+1][j]==oppflag and board[3*x+2][j]=='-':
					val -= 1
				elif board[3*x][j]=='-' and board[3*x+1][j]=='-' and board[3*x+2][j]==oppflag:
					val -= 1
				elif board[3*x][j]==oppflag and board[3*x+1][j]==oppflag and board[3*x+2][j]=='-':
					val -= 10
				elif board[3*x][j]==oppflag and board[3*x+1][j]=='-' and board[3*x+2][j]==oppflag:
					val -= 10
				elif board[3*x][j]=='-' and board[3*x+1][j]==oppflag and board[3*x+2][j]==oppflag:
					val -= 10
				elif board[3*x][j]==oppflag and board[3*x+1][j]==oppflag and board[3*x+2][j]==oppflag:
					prob = -1
					break
				elif board[3*x][j]==myflag and board[3*x+1][j]=='-' and board[3*x+2][j]=='-':
					val += 1
				elif board[3*x][j]=='-' and board[3*x+1][j]==myflag and board[3*x+2][j]=='-':
					val += 1
				elif board[3*x][j]=='-' and board[3*x+1][j]=='-' and board[3*x+2][j]==myflag:
					val += 1
				elif board[3*x][j]==myflag and board[3*x+1][j]==myflag and board[3*x+2][j]=='-':
					val += 10
				elif board[3*x][j]==myflag and board[3*x+1][j]=='-' and board[3*x+2][j]==myflag:
					val += 10
				elif board[3*x][j]=='-' and board[3*x+1][j]==myflag and board[3*x+2][j]==myflag:
					val += 10
				elif board[3*x][j]==myflag and board[3*x+1][j]==myflag and board[3*x+2][j]==myflag:
					prob = 1
					break
		if prob != 1 and prob != -1:
			if board[3*x][3*y] == oppflag and board[3*x+1][3*y+1] == '-' and board[3*x+2][3*y+2] == '-':
				val -= 1
			elif board[3*x][3*y] == '-' and board[3*x+1][3*y+1] == oppflag and board[3*x+2][3*y+2] == '-':
				val -= 1
			elif board[3*x][3*y] == '-' and board[3*x+1][3*y+1] == '-' and board[3*x+2][3*y+2] == oppflag:
				val -= 1
			elif board[3*x][3*y] == oppflag and board[3*x+1][3*y+1] == oppflag and board[3*x+2][3*y+2] == '-':
				val -= 10
			elif board[3*x][3*y] == oppflag and board[3*x+1][3*y+1] == '-' and board[3*x+2][3*y+2] == oppflag:
				val -= 10
			elif board[3*x][3*y] == '-' and board[3*x+1][3*y+1] == oppflag and board[3*x+2][3*y+2] == oppflag:
				val -= 10
			elif board[3*x][3*y] == oppflag and board[3*x+1][3*y+1] == oppflag and board[3*x+2][3*y+2] == oppflag:
				prob = -1
			elif board[3*x][3*y] == myflag and board[3*x+1][3*y+1] == '-' and board[3*x+2][3*y+2] == '-':
				val += 1
			elif board[3*x][3*y] == '-' and board[3*x+1][3*y+1] == myflag and board[3*x+2][3*y+2] == '-':
				val += 1
			elif board[3*x][3*y] == '-' and board[3*x+1][3*y+1] == '-' and board[3*x+2][3*y+2] == myflag:
				val += 1
			elif board[3*x][3*y] == myflag and board[3*x+1][3*y+1] == myflag and board[3*x+2][3*y+2] == '-':
				val += 10
			elif board[3*x][3*y] == myflag and board[3*x+1][3*y+1] == '-' and board[3*x+2][3*y+2] == myflag:
				val += 10
			elif board[3*x][3*y] == '-' and board[3*x+1][3*y+1] == myflag and board[3*x+2][3*y+2] == myflag:
				val += 10
			elif board[3*x][3*y] == myflag and board[3*x+1][3*y+1] == myflag and board[3*x+2][3*y+2] == myflag:
				prob = 1
		if prob != 1 and prob != -1:
			if board[3*x][3*y+2] == oppflag and board[3*x+1][3*y+1] == '-' and board[3*x+2][3*y] == '-':
				val -= 1
			elif board[3*x][3*y+2] == '-' and board[3*x+1][3*y+1] == oppflag and board[3*x+2][3*y] == '-':
				val -= 1
			elif board[3*x][3*y+2] == '-' and board[3*x+1][3*y+1] == '-' and board[3*x+2][3*y] == oppflag:
				val -= 1
			elif board[3*x][3*y+2] == oppflag and board[3*x+1][3*y+1] == oppflag and board[3*x+2][3*y] == '-':
				val -= 10
			elif board[3*x][3*y+2] == oppflag and board[3*x+1][3*y+1] == '-' and board[3*x+2][3*y] == oppflag:
				val -= 10
			elif board[3*x][3*y+2] == '-' and board[3*x+1][3*y+1] == oppflag and board[3*x+2][3*y] == oppflag:
				val -= 10
			elif board[3*x][3*y+2] == oppflag and board[3*x+1][3*y+1] == oppflag and board[3*x+2][3*y] == oppflag:
				prob = -1
			elif board[3*x][3*y+2] == myflag and board[3*x+1][3*y+1] == '-' and board[3*x+2][3*y] == '-':
				val += 1
			elif board[3*x][3*y+2] == '-' and board[3*x+1][3*y+1] == myflag and board[3*x+2][3*y] == '-':
				val += 1
			elif board[3*x][3*y+2] == '-' and board[3*x+1][3*y+1] == '-' and board[3*x+2][3*y] == myflag:
				val += 1
			elif board[3*x][3*y+2] == myflag and board[3*x+1][3*y+1] == myflag and board[3*x+2][3*y] == '-':
				val += 10
			elif board[3*x][3*y+2] == myflag and board[3*x+1][3*y+1] == '-' and board[3*x+2][3*y] == myflag:
				val += 10
			elif board[3*x][3*y+2] == '-' and board[3*x+1][3*y+1] == myflag and board[3*x+2][3*y] == myflag:
				val += 10
			elif board[3*x][3*y+2] == myflag and board[3*x+1][3*y+1] == myflag and board[3*x+2][3*y] == myflag:
				prob = 1
		if prob != 1 and prob != -1:
			prob = (float(val))/100
		return prob

	def evaluate_board_heuristic(self,board,flag):
		oppflag = flag
		myflag = 'x'
		if oppflag == 'x':
			myflag = 'o'
		blocks = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
		block_values = [[0,0,0],[0,0,0],[0,0,0]]
		ans = 0.0
		for tup in blocks:
			temp = self.evaluate_block_heuristic(board,tup,myflag)
			block_values[tup[0]][tup[1]] = temp
		for i in range(0,3):
			if block_values[i][0] == 1 and block_values[i][1] == 1 and block_values[i][2] == 1:
				ans = 100
				break
			elif block_values[i][0] == -1 and block_values[i][1] == -1 and block_values[i][2] == -1:
				ans = -100
				break
			elif block_values[i][0] == 1 and block_values[i][1] == 1 and self.check(block_values[i][2]) == True:
				if block_values[i][2] >= 0:
					ans += 7 + block_values[i][2]*10
				else:
					temp = 4 + block_values[i][2]*10
					if temp < 0 :
						temp = 0
					ans += temp
			elif block_values[i][0] == 1 and block_values[i][2] == 1 and self.check(block_values[i][1]) == True:
				if block_values[i][1] >= 0:
					ans += 7 + block_values[i][1]*10
				else:
					temp = 4 + block_values[i][1]*10
					if temp < 0 :
						temp = 0
					ans += temp
			elif block_values[i][1] == 1 and block_values[i][2] == 1 and self.check(block_values[i][0]) == True:
				if block_values[i][0] >= 0:
					ans += 7 + block_values[i][0]*10
				else:
					temp = 4 + block_values[i][0]*10
					if temp < 0 :
						temp = 0
					ans += temp 
			elif block_values[i][0] == 1 and self.check(block_values[i][1]) == True and self.check(block_values[i][2]) == True:
				temp = 1 + 6*(block_values[i][1] + block_values[i][2])
				if temp < 0:
					temp = 0
				ans += temp
			elif block_values[i][1] == 1 and self.check(block_values[i][0]) == True and self.check(block_values[i][2]) == True:
				temp = 1 + 6*(block_values[i][0] + block_values[i][2])
				if temp < 0:
					temp = 0
				ans += temp
			elif block_values[i][2] == 1 and self.check(block_values[i][1]) == True and self.check(block_values[i][0]) == True:
				temp = 1 + 6*(block_values[i][1] + block_values[i][0])
				if temp < 0:
					temp = 0
				ans += temp
			elif self.check(block_values[i][0]) == True and self.check(block_values[i][1]) == True and self.check(block_values[i][2]) == True:
				temp = (block_values[i][0] + block_values[i][1] + block_values[i][2])
				ans += temp
			elif block_values[i][0] == -1 and block_values[i][1] == -1 and self.check(block_values[i][2]) == True:
				if block_values[i][2] <= 0:
					ans -= 7 - block_values[i][2]*10
				else:
					temp = 4 - block_values[i][2]*10
					if temp < 0 :
						temp = 0
					ans -= temp
			elif block_values[i][0] == -1 and block_values[i][2] == -1 and self.check(block_values[i][1]) == True:
				if block_values[i][1] <= 0:
					ans -= 7 - block_values[i][1]*10
				else:
					temp = 4 - block_values[i][1]*10
					if temp < 0 :
						temp = 0
					ans -= temp
			elif block_values[i][2] == -1 and block_values[i][1] == -1 and self.check(block_values[i][0]) == True:
				if block_values[i][0] <= 0:
					ans -= 7 - block_values[i][0]*10
				else:
					temp = 4 - block_values[i][0]*10
					if temp < 0 :
						temp = 0
					ans -= temp
			elif block_values[i][0] == -1 and self.check(block_values[i][1]) == True and self.check(block_values[i][2]) == True:
				temp = 1 - 6*(block_values[i][1] + block_values[i][2])
				if temp < 0:
					temp = 0
				ans -= temp
			elif block_values[i][1] == -1 and self.check(block_values[i][0]) == True and self.check(block_values[i][2]) == True:
				temp = 1 - 6*(block_values[i][0] + block_values[i][2])
				if temp < 0:
					temp = 0
				ans -= temp
			elif block_values[i][2] == -1 and self.check(block_values[i][1]) == True and self.check(block_values[i][0]) == True:
				temp = 1 - 6*(block_values[i][1] + block_values[i][0])
				if temp < 0:
					temp = 0
				ans -= temp
		if ans != 100:
			for j in range(0,3):
				if block_values[0][j] == 1 and block_values[1][j] == 1 and block_values[2][j] == 1:
					ans = 100
					break
				elif block_values[0][j] == -1 and block_values[1][j] == -1 and block_values[2][j] == -1:
					ans = -100
					break
				elif block_values[0][j] == 1 and block_values[1][j] == 1 and self.check(block_values[2][j]) == True:
					if block_values[2][j] >= 0:
						ans += 7 + block_values[2][j]*10
					else:
						temp = 4 + block_values[2][j]*10
						if temp < 0 :
							temp = 0
						ans += temp
				elif block_values[0][j] == 1 and block_values[2][j] == 1 and self.check(block_values[1][j]) == True:
					if block_values[1][j] >= 0:
						ans += 7 + block_values[1][j]*10
					else:
						temp = 4 + block_values[1][j]*10
						if temp < 0 :
							temp = 0
						ans += temp
				elif block_values[1][j] == 1 and block_values[2][j] == 1 and self.check(block_values[0][j]) == True:
					if block_values[0][j] >= 0:
						ans += 7 + block_values[0][j]*10
					else:
						temp = 4 + block_values[0][j]*10
						if temp < 0 :
							temp = 0
						ans += temp 
				elif block_values[0][j] == 1 and self.check(block_values[1][j]) == True and self.check(block_values[2][j]) == True:
					temp = 1 + 6*(block_values[1][j] + block_values[2][j])
					if temp < 0:
						temp = 0
					ans += temp
				elif block_values[1][j] == 1 and self.check(block_values[0][j]) == True and self.check(block_values[2][j]) == True:
					temp = 1 + 6*(block_values[0][j] + block_values[2][j])
					if temp < 0:
						temp = 0
					ans += temp
				elif block_values[2][j] == 1 and self.check(block_values[1][j]) == True and self.check(block_values[0][j]) == True:
					temp = 1 + 6*(block_values[1][j] + block_values[0][j])
					if temp < 0:
						temp = 0
					ans += temp
				elif self.check(block_values[0][j]) == True and self.check(block_values[1][j]) == True and self.check(block_values[2][j]) == True:
					temp = (block_values[0][j] + block_values[1][j] + block_values[2][j])
					ans += temp
				elif block_values[0][j] == -1 and block_values[2][j] == -1 and self.check(block_values[1][j]) == True:
					if block_values[1][j] <= 0:
						ans -= 7 - block_values[1][j]*10
					else:
						temp = 4 - block_values[1][j]*10
						if temp < 0 :
							temp = 0
						ans -= temp
				elif block_values[0][j] == -1 and block_values[1][j] == -1 and self.check(block_values[2][j]) == True:
					if block_values[2][j] <= 0:
						ans -= 7 - block_values[2][j]*10
					else:
						temp = 4 - block_values[2][j]*10
						if temp < 0 :
							temp = 0
						ans -= temp
				elif block_values[1][j] == -1 and block_values[2][j] == -1 and self.check(block_values[0][j]) == True:
					if block_values[0][j] <= 0:
						ans -= 7 - block_values[0][j]*10
					else:
						temp = 4 - block_values[0][j]*10
						if temp < 0 :
							temp = 0
						ans -= temp
				elif block_values[0][j] == -1 and self.check(block_values[1][j]) == True and self.check(block_values[2][j]) == True:
					temp = 1 - 6*(block_values[1][j] + block_values[2][j])
					if temp < 0:
						temp = 0
					ans -= temp
				elif block_values[1][j] == -1 and self.check(block_values[0][j]) == True and self.check(block_values[2][j]) == True:
					temp = 1 - 6*(block_values[0][j] + block_values[2][j])
					if temp < 0:
						temp = 0
					ans -= temp
				elif block_values[2][j] == -1 and self.check(block_values[1][j]) == True and self.check(block_values[0][j]) == True:
					temp = 1 - 6*(block_values[1][j] + block_values[0][j])
					if temp < 0:
						temp = 0
					ans -= temp
		if ans != 100:
			if block_values[0][0] == 1 and block_values[1][1] == 1 and block_values[2][2] == 1:
				ans = 100
			elif block_values[0][0] == -1 and block_values[1][1] == -1 and block_values[2][2] == -1:
				ans = -100
			elif block_values[0][0] == 1 and block_values[1][1] == 1 and self.check(block_values[2][2]) == True:
				if block_values[2][2] >= 0:
					ans += 7 + block_values[2][2]*10
				else:
					temp = 4 + block_values[2][2]*10
					if temp < 0 :
						temp = 0
					ans += temp
			elif block_values[0][0] == 1 and block_values[2][2] == 1 and self.check(block_values[1][1]) == True:
				if block_values[1][1] >= 0:
					ans += 7 + block_values[1][1]*10
				else:
					temp = 4 + block_values[1][1]*10
					if temp < 0 :
						temp = 0
					ans += temp
			elif block_values[1][1] == 1 and block_values[2][2] == 1 and self.check(block_values[0][0]) == True:
				if block_values[0][0] >= 0:
					ans += 7 + block_values[0][0]*10
				else:
					temp = 4 + block_values[0][0]*10
					if temp < 0 :
						temp = 0
					ans += temp 
			elif block_values[0][0] == 1 and self.check(block_values[1][1]) == True and self.check(block_values[2][2]) == True:
				temp = 1 + 6*(block_values[1][1] + block_values[2][2])
				if temp < 0:
					temp = 0
				ans += temp
			elif block_values[1][1] == 1 and self.check(block_values[0][0]) == True and self.check(block_values[2][2]) == True:
				temp = 1 + 6*(block_values[0][0] + block_values[2][2])
				if temp < 0:
					temp = 0
				ans += temp
			elif block_values[2][2] == 1 and self.check(block_values[1][1]) == True and self.check(block_values[0][0]) == True:
				temp = 1 + 6*(block_values[1][1] + block_values[0][0])
				if temp < 0:
					temp = 0
				ans += temp
			elif self.check(block_values[0][0]) == True and self.check(block_values[1][1]) == True and self.check(block_values[2][2]) == True:
				temp = (block_values[0][0] + block_values[1][1] + block_values[2][2])
				ans += temp
			elif block_values[0][0] == -1 and block_values[1][1] == -1 and self.check(block_values[2][2]) == True:
				if block_values[2][2] <= 0:
					ans -= 7 - block_values[2][2]*10
				else:
					temp = 4 - block_values[2][2]*10
					if temp < 0 :
						temp = 0
					ans -= temp
			elif block_values[0][0] == -1 and block_values[2][2] == -1 and self.check(block_values[1][1]) == True:
				if block_values[1][1] <= 0:
					ans -= 7 - block_values[1][1]*10
				else:
					temp = 4 - block_values[1][1]*10
					if temp < 0 :
						temp = 0
					ans -= temp
			elif block_values[2][2] == -1 and block_values[1][1] == -1 and self.check(block_values[0][0]) == True:
				if block_values[0][0] <= 0:
					ans -= 7 - block_values[0][0]*10
				else:
					temp = 4 - block_values[0][0]*10
					if temp < 0 :
						temp = 0
					ans -= temp
			elif block_values[0][0] == -1 and self.check(block_values[1][1]) == True and self.check(block_values[2][2]) == True:
				temp = 1 - 6*(block_values[1][1] + block_values[2][2])
				if temp < 0:
					temp = 0
				ans -= temp
			elif block_values[1][1] == -1 and self.check(block_values[0][0]) == True and self.check(block_values[2][2]) == True:
				temp = 1 - 6*(block_values[0][0] + block_values[2][2])
				if temp < 0:
					temp = 0
				ans -= temp
			elif block_values[2][2] == -1 and self.check(block_values[0][0]) == True and self.check(block_values[1][1]) == True:
				temp = 1 - 6*(block_values[0][0] + block_values[1][1])
				if temp < 0:
					temp = 0
				ans -= temp
		if ans != 100:
			if block_values[0][2] == 1 and block_values[1][1] == 1 and block_values[2][0] == 1:
				ans = 100
			elif block_values[0][2] == -1 and block_values[1][1] == -1 and block_values[2][0] == -1:
				ans = -100
			elif block_values[0][2] == 1 and block_values[1][1] == 1 and self.check(block_values[2][0]) == True:
				if block_values[2][0] >= 0:
					ans += 7 + block_values[2][0]*10
				else:
					temp = 4 + block_values[2][0]*10
					if temp < 0 :
						temp = 0
					ans += temp
			elif block_values[0][2] == 1 and block_values[2][0] == 1 and self.check(block_values[1][1]) == True:
				if block_values[1][1] >= 0:
					ans += 7 + block_values[1][1]*10
				else:
					temp = 4 + block_values[1][1]*10
					if temp < 0 :
						temp = 0
					ans += temp
			elif block_values[1][1] == 1 and block_values[2][0] == 1 and self.check(block_values[0][2]) == True:
				if block_values[0][2] >= 0:
					ans += 7 + block_values[0][2]*10
				else:
					temp = 4 + block_values[0][2]*10
					if temp < 0 :
						temp = 0
					ans += temp 
			elif block_values[0][2] == 1 and self.check(block_values[1][1]) == True and self.check(block_values[2][0]) == True:
				temp = 1 + 6*(block_values[1][1] + block_values[2][0])
				if temp < 0:
					temp = 0
				ans += temp
			elif block_values[1][1] == 1 and self.check(block_values[0][2]) == True and self.check(block_values[2][0]) == True:
				temp = 1 + 6*(block_values[0][2] + block_values[2][0])
				if temp < 0:
					temp = 0
				ans += temp
			elif block_values[2][0] == 1 and self.check(block_values[1][1]) == True and self.check(block_values[0][2]) == True:
				temp = 1 + 6*(block_values[1][1] + block_values[0][2])
				if temp < 0:
					temp = 0
				ans += temp
			elif self.check(block_values[0][2]) == True and self.check(block_values[1][1]) == True and self.check(block_values[2][0]) == True:
				temp = (block_values[0][2] + block_values[1][1] + block_values[2][0])
				ans += temp
			elif block_values[0][2] == -1 and block_values[1][1] == -1 and self.check(block_values[2][0]) == True:
				if block_values[2][0] <= 0:
					ans -= 7 - block_values[2][0]*10
				else:
					temp = 4 - block_values[2][0]*10
					if temp < 0 :
						temp = 0
					ans -= temp
			elif block_values[2][0] == -1 and block_values[1][1] == -1 and self.check(block_values[0][2]) == True:
				if block_values[0][2] <= 0:
					ans -= 7 - block_values[0][2]*10
				else:
					temp = 4 - block_values[0][2]*10
					if temp < 0 :
						temp = 0
					ans -= temp
			elif block_values[0][2] == -1 and block_values[2][0] == -1 and self.check(block_values[1][1]) == True:
				if block_values[1][1] <= 0:
					ans -= 7 - block_values[1][1]*10
				else:
					temp = 4 - block_values[1][1]*10
					if temp < 0 :
						temp = 0
					ans -= temp
			elif block_values[0][2] == -1 and self.check(block_values[1][1]) == True and self.check(block_values[2][0]) == True:
				temp = 1 - 6*(block_values[2][0] + block_values[1][1])
				if temp < 0:
					temp = 0
				ans -= temp
			elif block_values[2][0] == -1 and self.check(block_values[1][1]) == True and self.check(block_values[0][2]) == True:
				temp = 1 - 6*(block_values[0][2] + block_values[1][1])
				if temp < 0:
					temp = 0
				ans -= temp
			elif block_values[1][1] == -1 and self.check(block_values[0][2]) == True and self.check(block_values[2][0]) == True:
				temp = 1 - 6*(block_values[2][0] + block_values[0][2])
				if temp < 0:
					temp = 0
				ans -= temp
		return ans

	def check(self,flag):
		if flag != 1 and flag != -1 and flag != 0 and flag < 1 and flag > -1:
			return True
		else:
			return False

	def oppositeof(self,flag):
		if flag == 'x':
			return 'o'
		else:
			return 'x'

	def abc(self,board,tup,flag,depth,minimax,alpha,beta,block):
		temp_board = copy.deepcopy(board)
		x = tup[0]
		y = tup[1]
		temp_board[x][y] = flag
		if depth%2 == 0:
			myflag = flag
			oppflag = self.oppositeof(flag)
		else:
			myflag = self.oppositeof(flag)
			oppflag = flag
		if self.check_win(temp_board,block) == myflag:
			return 100,tup[0],tup[1]
		if self.check_win(temp_board,block) == oppflag:
			return -100,tup[0],tup[1]
		yoyo = self.oppositeof(flag)
		if depth == 4 :
			heuristic = self.evaluate_board_heuristic(temp_board,yoyo)
			return heuristic,tup[0],tup[1]
		else:
			new_list = self.get_valid_cells(temp_board,tup)
			new_alpha = -100000000
			new_beta = 100000000
			if flag == 'x':
				marker = 'o'
			elif flag == 'o':
				marker = 'x'
			if not new_list:
				if flag == 'x':
					new_flag = 'o'
				elif flag == 'o':
					new_flag = 'x'
				if depth%2 == 0:
					blabla = self.evaluate_board_heuristic(temp_board,new_flag)
				elif depth%2 == 1:
					blabla = self.evaluate_board_heuristic(temp_board,flag)
				return blabla,x,y
			if minimax == 1:
				new_beta = beta
			if minimax == -1:
				new_alpha = alpha
			for cell in new_list:
				if new_alpha < new_beta:
					val = self.abc(temp_board,cell,marker,depth+1,-minimax,new_alpha,new_beta,block)[0]
					if minimax == 1:
						if val > new_alpha:
							new_alpha = val
							row = cell[0]
							col = cell[1]
					elif minimax == -1:
						if val < new_beta:
							new_beta = val
							row = cell[0]
							col = cell[1]
			if minimax == 1:
				return new_alpha,row,col
			elif minimax == -1:
				return new_beta,row,col

	def check_win(self,board,block):
		for i in range(0,3):
			if block[3*i] == block[3*i + 1] and block[3*i + 1] == block[3*i + 2]:
				return block[3*i]
		for j in range(0,3):
			if block[j] == block[3+j] and block[j] == block[6+j]:
				return block[j]
		if block[0] == block[4] and block[0] == block[8]:
			return block[4]
		if block[2] == block[4] and block[4] == block[6]:
			return block[4]
		if '-' in block:
			return '-'
		cx = 0
		co = 0
		for i in range(0,9):
			if block[i] == 'x':
				cx += 1
			elif block[i] == 'o':
				co += 1
		if cx > co:
			return 'x'
		elif co > cx:
			return 'o'
		else:
			co = 0
			cx = 0
			for i in range(1,8,3):
				for j in range(1,8,3):
					if board[i][j] == 'x':
						cx += 1
					elif board[i][j] == 'o':
						co += 1
			if cx > co:
				return 'x'
			elif co > cx:
				return 'o'
		return '-'