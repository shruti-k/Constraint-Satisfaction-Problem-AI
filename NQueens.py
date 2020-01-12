import copy
import time,sys
from collections import deque
class Solve_N_Queens:

    def __init__(self,n,result_file):
        #Initializes the class with board, number of solutions, backtrack_count, domain 
        #of each queen
        self.count = 0
        self.backtrack_count = 0
        self.n = n
        self.board = [[0 for i in range(int(n))] for j in range(int(n))]
        self.var_domain = {}
        for i in range(0,self.n):
            d = []
            for j in range(0,self.n):
                d.append(j)
            self.var_domain[i] = d
        self.result_file = result_file
        self.start_time = time.time()
            
    def get_possible_moves_fc(self,board,row):
        #returns the allowed moves for the queen in given row
        possible_moves = []
        for col in range(self.n):
            if board[row][col] == 0:
                possible_moves.append(col)
        return possible_moves

    def forward_check(self,curr_row):
        #checks for available positions for remainming queens after
        #a queen has been placed
        var_domain_copy = copy.deepcopy(self.var_domain)
        board_copy = copy.deepcopy(self.board)
        placement = []
        for r in range(0,self.n):
            for c in range(0,self.n):
                if(self.board[r][c] == 1):
                    placement.append([r,c])
        for i in range(0,len(placement)):
            move = placement[i]
            row = move[0]
            col = move[1]
            for r in range(0,self.n):
                board_copy[r][col] = 1
            for r in range(0,self.n):
                for c in range(0,self.n):
                    if(r!=row and c!=col):
                        if((row+col) == (r+c) or (row-col) == (r-c)):
                            board_copy[r][c] = 1
        for neighbour in range(curr_row+1,self.n):
            possible_moves = self.get_possible_moves_fc(board_copy,neighbour)
            var_domain_copy[neighbour] = possible_moves
        return var_domain_copy
        
    def solve_FC(self,curr_row):
        if curr_row == self.n:
            if int(self.count) >= 2*int(n):
                result_file.write("Number of solutions: "+str(self.count)+"\n")        
                result_file.write("Number of backtracking steps: "+str(self.backtrack_count)+"\n")
                result_file.write("Execution time: "+str(time.time()-self.start_time)+"\n")
                result_file.close()
                sys.exit()
            self.count += 1
            self.result_file.write("Solution: "+str(self.count)+"\n")
            for r in range(0,self.n):
                row = ""
                for c in range(0,self.n):
                    if(self.board[r][c]==1):
                        row = row+" Q"
                    else:
                        row = row+" -"
                row = row+"\n"
                self.result_file.write(row)
            self.result_file.write("\n")
            
            return True
        #checks for all values in the domain of current queen
        for x in self.var_domain[curr_row]:
            self.board[curr_row][x] = 1
            self.var_domain = self.forward_check(curr_row)
            flag = True
            for i in range(0,self.n):
                if len(self.var_domain[i]) == 0:
                   flag = False 
                   break
            if flag:
                result = self.solve_FC(curr_row+1)
            #if domain of any queen is empty, then backtrack
            self.backtrack_count += 1
            self.board[curr_row][x] = 0 
        return False
    
    
    def get_possible_moves_ac3(self,board,row):
        possible_moves = []
        for col in range(self.n):
            if board[row][col] == 0:
                possible_moves.append(col)
        return possible_moves

    def revise(self,xi,xj):
        revised = False
        #checks if arc is consistent for given values in domain
        for var in self.var_domain[xi]:
            graph = self.mark_restricted_cells(xi,var)
            possible_moves = self.get_possible_moves_ac3(graph,xj)
            if(len(possible_moves) == 0):
                self.var_domain[xi].remove(var)
                revised = True
        return revised
        
    def mark_restricted_cells(self,row1,col1):
        board_copy = copy.deepcopy(self.board)
        placement = []
        for r in range(0,self.n):
            for c in range(0,self.n):
                if(self.board[r][c] == 1):
                    placement.append([r,c])
        for i in range(0,len(placement)):
            move = placement[i]
            row = move[0]
            col = move[1]
            for r in range(0,self.n):
                board_copy[r][col] = 1
            for r in range(0,self.n):
                for c in range(0,self.n):
                    if(r!=row and c!=col):
                        if((row+col) == (r+c) or (row-col) == (r-c)):
                            board_copy[r][c] = 1
        for r in range(0,self.n):
            board_copy[r][col1] = 1
        for r in range(0,self.n):
            for c in range(0,self.n):
                if(r!=row1 and c!=col1):
                    if((row1+col1) == (r+c) or (row1-col1) == (r-c)):
                        board_copy[r][c] = 1
        return board_copy
        
    def ac3(self,curr_row):
        #adds all arcs to the queue
        q = deque()
        for i in range(curr_row,self.n):
            for j in range(curr_row,self.n):
                if i!=j:
                    q.append([i,j])
        while len(q)!=0:
            arc = q.popleft()
            x = arc[0]
            y = arc[1]
            if self.revise(x,y):
                #if domain is empty,exit
                if len(self.var_domain[x]) == 0:
                    return False 
                for j in range(curr_row+1,self.n):
                    if j!=y:
                        q.append([j,x])    
        return True

    def forward_check_mac(self,curr_row):
        var_domain_copy = copy.deepcopy(self.var_domain)
        board_copy = copy.deepcopy(self.board)
        placement = []
        for r in range(0,self.n):
            for c in range(0,self.n):
                if(self.board[r][c] == 1):
                    placement.append([r,c])
        for i in range(0,len(placement)):
            move = placement[i]
            row = move[0]
            col = move[1]
            for r in range(0,self.n):
                board_copy[r][col] = 1
            for r in range(0,self.n):
                for c in range(0,self.n):
                    if(r!=row and c!=col):
                        if((row+col) == (r+c) or (row-col) == (r-c)):
                            board_copy[r][c] = 1
        for neighbour in range(curr_row+1,self.n):
            possible_moves = self.get_possible_moves_ac3(board_copy,neighbour)
            var_domain_copy[neighbour] = possible_moves
        return var_domain_copy

    def solve_MAC(self,curr_row):
        if curr_row == self.n:
            if int(self.count) >= 2*int(n):
                result_file.write("Number of solutions: "+str(self.count)+"\n")        
                result_file.write("Number of backtracking steps: "+str(self.backtrack_count)+"\n")
                result_file.write("Execution time: "+str(time.time()-self.start_time)+"\n")
                result_file.close()
                sys.exit()
            self.count += 1
            self.result_file.write("Solution: "+str(self.count)+"\n")
            for r in range(0,self.n):
                row = ""
                for c in range(0,self.n):
                    if(self.board[r][c]==1):
                        row = row+" Q"
                    else:
                        row = row+" -"
                row = row+"\n"
                self.result_file.write(row)
            self.result_file.write("\n")
            return True
        #checks consistency of all arcs which are not yet assigned values
        val = self.ac3(curr_row)
        if not val:
            return False
        for x in self.var_domain[curr_row]:
            if val: 
                self.board[curr_row][x] = 1
                self.var_domain = self.forward_check_mac(curr_row)
                flag = True
                for i in range(0,self.n):
                    if len(self.var_domain[i]) == 0:
                       flag = False 
                       break
                if flag:
                    result = self.solve_MAC(curr_row+1)
                self.backtrack_count += 1
                self.board[curr_row][x] = 0
              
        return False
def write_cfile(constraint_file,n):
    #writes variables,domains,constraints to the constraint_file
    constraint_file.write("The variables for the constraint satisfaction are as follows:\n\n")
    v = "{ "
    for i in range(0,n):
        v = v + "Q"+str(i)+", "
    v = v[:-2]
    v = v + " }"
    constraint_file.write(v)
    constraint_file.write("\n\n\nThe code places the queens row-wise and each row has domain corresponding to each column in the board.\n\n")
    
    for i in range(0,n):
        d = "Q"+str(i)+" = {"
        for j in range(0,n):
            d = d + "("+str(i)+","+str(j)+"),"
        d = d[:-1]
        d = d + "}\n"
        constraint_file.write(d)
    constraint_file.write("\n\nThe constraints for the solving the problem are as follows:\n")
    constraint_file.write("\nLet Qx1 and Qx2 be any two queens in the problem where x1, x2 are row numbers such that x1 != x2 and their positions are y1 and y2 respectively\n")
    constraint_file.write("\nThe queens in different rows cannot be placed in same columns:\n")
    constraint_file.write("y1 != y2 where 0 <= y1,y2 < "+str(n))
    constraint_file.write("\n\nThe queens in different rows cannot be placed in same diagonal:\n")
    constraint_file.write("(x1 + y1)!=(x2 + y2) or (x1 - y1)!=(x2 - y2) where 0 <= x1,x2,y1,y2 < "+str(n))
    
       
if __name__== "__main__":
    
    alg = sys.argv[1]
    n = sys.argv[2]
    cfile = sys.argv[3]
    rfile = sys.argv[4]
    constraint_file = open(cfile, "w")
    result_file = open(rfile, "w")
    write_cfile(constraint_file,int(n))
    constraint_file.close()
    QueenGraph = Solve_N_Queens(int(n),result_file)
    if alg == 'FOR':
        result_file.write("Forward Checking\n") 
        QueenGraph.solve_FC(0)
        result_file.write("Number of solutions: "+str(QueenGraph.count)+"\n")        
        result_file.write("Number of backtracking steps: "+str(QueenGraph.backtrack_count)+"\n")
        result_file.write("Execution time: "+str(time.time()-QueenGraph.start_time)+"\n")
        result_file.close()
        
    elif alg == 'MAC':
        result_file.write("MAC\n")
        start = time.time()
        QueenGraph.solve_MAC(0) 
        result_file.write("Number of solutions: "+str(QueenGraph.count)+"\n") 
        result_file.write("Number of backtracking steps: "+str(QueenGraph.backtrack_count)+"\n")
        result_file.write("Execution time: "+str(time.time()-QueenGraph.start_time)+"\n")
        result_file.close()
    else:
        print("Enter valid Algorithm Name : FOR / MAC \n")