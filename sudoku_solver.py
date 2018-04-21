from collections import defaultdict, Counter

class sudoku():

    def __init__(self, numbers, size=3):
        def is_proper(numbers):
            if len(numbers) != size**2:
                return False
            for row in numbers:
                if len(row) != size**2:
                    return False
            return True
        if is_proper(numbers):
            self.numbers = numbers
            self.size = size
        else:
            raise TypeError("invalid size (size is "+str(size)+")")

    def __repr__(self):
        size = self.size
        strs = ['' for _ in range(size**2)]
        for col in range(size**2):
            max_len_digit = max([self.get_element(row,col)
                                 for row in range(size**2)],
                                key=digit_len)
            max_len = digit_len(max_len_digit)
            if (col+1) % size == 0 and col != size**2-1:
                for row, n in enumerate(self.get_col(col)):
                    len_n = digit_len(n)
                    strs[row] += str(n) + " "*(max_len-len_n+1) + '| '
            else:
                for row, n in enumerate(self.get_col(col)):
                    len_n = digit_len(n)
                    strs[row] += str(n) + " "*(max_len-len_n+1)
        for row in range(size**2):
            strs[row] += "\n"
        for col in range(size-1):
            strs.insert(size + (size+1)*col, "-"*len(strs[0])+"\n")

        result = ""
        for s in strs:
            result += s
        return result
    
    def __eq__(self, s):
        return self.numbers == s.numbers

    def __getitem__(self, i):
        return self.numbers[i]

    def get_row(self, i):
        return self.numbers[i].copy()
    
    def get_col(self, j):
        return [self.numbers[i][j] for i in range(self.size**2)]

    def get_element(self, i, j):
        return self.numbers[i][j]

    def set_element(self, i, j, n):
        self.numbers[i][j] = n
    
    def get_block(self, i):
        size = self.size
        arranged = self.arrange_widely()
        block = []
        for row in arranged:
            block.append(row[size*i:size*(i+1)])
        return block

    def get_block_as_list(self, i):
        size = self.size
        block_as_list = []
        arranged = self.arrange_widely()
        for row in arranged:
            block_as_list.extend(row[size*i:size*(i+1)])
        return block_as_list

    def copy(self):
        size = self.size
        numbers = []
        for row in self.numbers:
            copied = row.copy()
            numbers.append(copied)
        return sudoku(numbers, size)

    def arrange_widely(self):
        size = self.size
        arranged = []
        for i in range(size):
            row_i = []
            for j in range(size):
                row_i += self.get_row(i + j*size)
            arranged.append(row_i)
        return arranged
    
    def is_solved(self):
        size = self.size
        check_list = []
        numbers = list(range(1,size**2 + 1))
        for i in range(size**2):
            check_list.append(is_same_list(self.get_row(i), numbers))
            check_list.append(is_same_list(self.get_col(i), numbers))
            check_list.append(is_same_list(self.get_block_as_list(i), numbers))
        return all(check_list)


def digit_len(n):
    return len(str(n))

def is_same_list(list1, list2):
    if len(list1) != len(list2):
        return False
    for e in list1:
        if e not in list2:
            return False
    return True

def copy_candidates(size, candidates):
    copy = dict()
    for block in candidates.keys():
        copy[block] = defaultdict(list)
        for n in range(1, size**2 + 1):
            coordinates = candidates[block][n].copy()
            copy[block][n] = coordinates
    return copy

def check(sudoku, i, j, n):
    num = sudoku.get_element(i,j)
    if type(num) == int:
        return num == 0
    else:   # string
        return str(n) in num

def is_same_row(coordinates):
    if len(coordinates) == 0:
        return { "bool" : False }
    else:
        row_checker = coordinates[0][0]
        for coordinate in coordinates:
            if coordinate[0] != row_checker:
                return { "bool" : False }
        return { "bool" : True, "row" : row_checker }

def is_same_col(coordinates):
    if len(coordinates) == 0:
        return { "bool" : False }
    else:
        col_checker = coordinates[0][1]
        for coordinate in coordinates:
            if coordinate[1] != col_checker:
                return { "bool" : False }
        return { "bool" : True, "col" : col_checker}

def find_same_coordinates(candidates_i):
    coordinates = Counter([tuple(value) for value in candidates_i.values()])
    duplicated_coords = [item[0] for item in coordinates.items()
                         if len(item[0]) == item[1] and item[1] != 1]
    same_coordinates = defaultdict(list)
    for item in candidates_i.items():
        if tuple(item[1]) in duplicated_coords:
            same_coordinates[tuple(item[1])].append(item[0])
    return same_coordinates

def find_same_row(size, candidates, hidden_numbers):
    for i in range(size):
        for n in range(1, size**2+1):
            row_candidates_n = dict()
            for j in range(size*i, size*(i+1)):
                row_candidates_n["block_"+str(j)] = \
                tuple(set([c[0] for c in candidates["block_"+str(j)][n]])) # row
            row_counter = Counter([rs for rs in row_candidates_n.values()])
            for item in row_counter.items():
                if item[1] != 1 and len(item[0]) == item[1]:
                    rows = item[0]
                    blocks = [block for block in row_candidates_n.keys()
                              if row_candidates_n[block] == rows]
                    for row in rows:
                        hidden_numbers["row_"+str(row)].add((str(blocks), n))

def find_same_col(size, candidates, hidden_numbers):
    for i in range(size):
        for n in range(1, size**2+1):
            col_candidates_n = dict()
            for j in range(size*i, size*(i+1)):
                col_candidates_n["block_"+str(j)] = \
                tuple(set([c[1] for c in candidates["block_"+str(j)][n]])) # col
            col_counter = Counter([cs for cs in col_candidates_n.values()])
            for item in col_counter.items():
                if item[1] != 1 and len(item[0]) == item[1]:
                    cols = item[0]
                    blocks = [block for block in col_candidates_n.keys()
                              if col_candidates_n[block] == cols]
                    for col in cols:
                        hidden_numbers["col_"+str(col)].add((str(blocks), n))
            

def solve(sudoku):
    s = sudoku.copy()
    size = s.size
    no_improvement = False
    hidden_numbers = defaultdict(set)
    candidates = dict()
    while True:


        prev_candidates = copy_candidates(size, candidates)
        for block in range(size**2):
            block_i = "block_" + str(block)
            candidates[block_i] = defaultdict(list)
            
            for n in range(1, size**2 + 1):
                start_row = size * int(block/size)
                start_col = size * (block%size)

                for i in range(start_row, start_row+size):
                    for j in range(start_col, start_col+size):
                        if check(s, i, j, n):
                            check_list = s.get_block_as_list(block) + \
                                         s.get_row(i) + \
                                         s.get_col(j) + \
                                         [t[1]
                                          for t in hidden_numbers["row_"+str(i)]
                                          if block_i not in t[0]] + \
                                         [t[1]
                                          for t in hidden_numbers["col_"+str(j)]
                                          if block_i not in t[0]]
                            if n not in check_list:
                                candidates[block_i][n].append((i, j))

                if len(candidates[block_i][n]) == 1:
                    coordinate = candidates[block_i][n][0]
                    s.set_element(*coordinate, n)

                elif is_same_row(candidates[block_i][n])["bool"]:
                    row = is_same_row(candidates[block_i][n])["row"]
                    hidden_numbers["row_"+str(row)].add((block_i, n))

                elif is_same_col(candidates[block_i][n])["bool"]:
                    col = is_same_col(candidates[block_i][n])["col"]
                    hidden_numbers["col_"+str(col)].add((block_i, n))


            same_coordinates = find_same_coordinates(candidates[block_i])
            for item in same_coordinates.items():
                string = str()
                for n in item[1]:
                    string += str(n) + ","
                for coord in item[0]:
                    s.set_element(*coord, string)

        find_same_row(size, candidates, hidden_numbers)
        find_same_col(size, candidates, hidden_numbers)


        if s.is_solved():
            return s
        elif prev_candidates == candidates:
             print("Sorry, I can't solve")
             return s



if __name__ == "__main__":
    s = sudoku([[0,0,4,0,1,0,0,0,0],\
                [0,2,0,0,0,7,6,0,0],\
                [1,0,0,5,0,0,0,3,0],\
                [0,1,0,0,0,0,8,0,0],\
                [3,0,0,0,4,0,0,0,9],\
                [0,0,6,0,0,0,0,2,0],\
                [0,5,0,0,0,1,0,0,8],\
                [0,0,7,2,0,0,0,4,0],\
                [0,0,0,0,3,0,9,0,0]])
    result = solve(s)
    print(result)
    
    s2 = sudoku([[0,0,3,0,5,6,0,0,9,0,0,12,13,0,0,0],\
                 [0,6,7,8,9,10,0,12,13,14,15,0,0,2,0,4],\
                 [0,10,0,12,0,14,0,16,1,2,0,0,5,0,7,8],\
                 [0,0,15,0,0,0,3,4,5,0,0,8,0,0,0,0],\
                 [2,3,0,0,0,7,8,9,10,11,12,0,14,15,16,1],\
                 [6,7,8,0,10,0,12,0,14,15,16,0,2,3,0,0],\
                 [0,11,12,13,0,15,0,1,2,3,4,5,0,7,8,9],\
                 [0,0,16,0,2,0,0,5,6,0,0,9,0,11,0,13],\
                 [3,0,5,0,7,0,0,10,11,0,0,14,0,16,0,0],\
                 [7,8,9,0,11,12,13,14,15,0,1,2,3,4,5,0],\
                 [0,0,13,14,0,16,1,2,0,4,0,6,0,8,9,10],\
                 [15,16,1,2,0,4,5,6,7,8,9,0,0,0,13,14],\
                 [0,0,0,0,8,0,0,11,12,13,0,0,0,1,0,0],\
                 [8,9,0,11,0,0,14,15,16,0,2,0,4,0,6,0],\
                 [12,0,14,0,0,1,2,3,4,5,0,7,8,9,10,0],\
                 [0,0,0,3,4,0,0,7,0,0,10,11,0,13,0,0]], size=4)
    result2 = solve(s2)
    print(result2)
