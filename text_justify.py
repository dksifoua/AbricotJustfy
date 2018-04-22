import re
import numpy as np

class Justify :
    """ Author : Dimitri K. Sifoua <kemgangdimitri@gmail.com>
    Date : April 19, 2018
    This class is use to justify some text.
    Properties :
        - paragraphs = text divided into paragraphs
        - width = max length of each line
        - text_justified = array that contains each line of text justified
    """
    
    def __init__(self, data, w) :
        self.paragraphs = self.getP(data)
        self.width = w
        self.text_justified = []

    def getP(self, data) :
        fo = open("input.txt", "w")
        fo.write(data)
        fo.close()
        file = open('input.txt', 'r')
        data = file.readlines()
        paragraphs, new = [], True
        for d in data :
            if d == '' or re.match("^[ \t\n\r\f\v]+$", d) :
                new = True
                continue
            else :
                if new :
                    paragraphs.append(d)
                    new = False
                else :
                    paragraphs[len(paragraphs) - 1] += d
        file.close()
        return paragraphs
        
    def resolve(self) :
        for paragrah in self.paragraphs :
            words = paragrah.split()
            len_words = np.zeros(len(words), dtype = np.int64)
            i = 0
            for word in words :
                if word.find('\n') != -1 :
                    word = word[0:-2]
                if word.find(' \n') != -1 :
                    word = word[0:-3]
                len_words[i] = len(word)
                i += 1
            self.handleSolution(self.textJustify(len_words), len(words), words)
            
            
    def handleSolution(self, solution, n, words) :
        line = []
        col = 0
        if solution[n] == 1 :
            k = 1
        else :
            k = self.handleSolution(solution, solution[n] - 1, words) + 1
        
        for i in range(solution[n] - 1, n) :
            line.append(words[i])
            col += len(words[i]) + 1
        
        if len(line) == 1 :
            self.text_justified.append(' '.join(line).ljust(self.width))
        else :
            q, r = divmod(self.width - col + 1, len(line) - 1)
            if r == 0 :
                self.text_justified.append((' ' * (q + 1)).join(line))
            else :
                if n == len(words) :
                    self.text_justified.append((' ' * (q + 1)).join(line))
                else :
                    self.text_justified.append((' ' * (q + 2)).join(line[:r] + [(' ' * (q + 1)).join(line[r:])]))
        return k
                    
        
    def textJustify(self, len_words) :
        L = len(len_words) + 1
        over_spaces = np.zeros((L, L), dtype = np.int64)
        line_cost = np.zeros((L, L), dtype = np.float64)
        opt_cost = np.zeros(L, dtype = np.float64)
        solution = np.zeros(L, dtype = np.int64)
        
        # Over spaces of each line from i to j
        for i in range(1, L) :
            over_spaces[i][i] = self.width - len_words[i - 1]
            for j in range(i + 1, L) :
                over_spaces[i][j] = over_spaces[i][j - 1] - len_words[j - 1] - 1
          
        # Line cost of each line from i to j
        for i in range(1, L) :
            for j in range(i, L) :
                if over_spaces[i][j] < 0 :
                    line_cost[i][j] = float('inf')
                elif j == L - 1 and over_spaces[i][j] >= 0 :
                    line_cost[i][j] = 0
                else :
                    line_cost[i][j] = over_spaces[i][j] ** 2
             
        # Optimal cost to insert words on each line from i to j
        for j in range(1, L) :
            opt_cost[j] = float('inf')
            for i in range(1, j + 1) :
                if opt_cost[i-1] != float('inf') and line_cost[i][j] != float('inf') and opt_cost[i-1] + line_cost[i][j] < opt_cost[j] :
                    opt_cost[j] = opt_cost[i-1] + line_cost[i][j]
                    solution[j] = i
                    
        return solution