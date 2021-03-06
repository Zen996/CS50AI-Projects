import sys
import copy
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains: #self.domains is a dictionary with var as key, initial set of all the words as value
            #var contains i,j,direction,length
            remove = set()
            #loop through the set of words of each var
            for word in self.domains[var]:
                if len(word) != var.length:
                    #cant remove words while iterating the set
                    remove.add(word)
            
            self.domains[var] = self.domains[var] - remove #returns set of words not in remove
        
        #raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        overlap = self.crossword.overlaps[x,y]
         # Need to check x's domain if there is overlap between x and y
        if overlap is not None:
            remove = set()

            for wordx in self.domains[x]:
                #overlap is a pair,first value is nth char of x that overlaps
                # loop through all words, if overlap[0]-th char of wordx == overlap[1]-th char of wordy 
                xchar = wordx[overlap[0]]
                ovlp_flag = False
                for wordy in self.domains[y]:
                    if xchar == wordy[overlap[1]]:
                        ovlp_flag = True
                if not ovlp_flag: #if wordx has no overlap with all words in y
                    remove.add(wordx) #wordx to be removed

            if remove: #if there are words to be removed
               #print(self.domains[x],remove)
                self.domains[x] = self.domains[x]  - remove
               #print(self.domains[x],"after remove")
                return True
        #no overlap or no changes done
        return False
        raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            queue = [(x,y) for x in self.crossword.variables for y in self.crossword.variables if x != y and self.crossword.overlaps[x,y] is not None ]
        else:
            queue = arcs

        while queue:
            x,y = queue.pop(0)
            if self.revise(x,y):

                if not self.domains[x]: #no more possible values, unsolvable
                    return False
                for z in (self.crossword.neighbors(x) - {y}): #x neighbors returns set, so set - set
                    queue.append((z,x))

        return True
        raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.crossword.variables:
            if var not in assignment: #if any var not in assignment, it does not have a value
                return False
            
        return True
        raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        #all values are distinct
        if len(set(assignment.values())) != len(assignment.values()): 
            return False
        #every value is the correct length, 
        for var in assignment:
            if var.length != len(assignment[var]):
                return False
                
        #and there are no conflicts between neighboring variables.
        for var in assignment:
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:

                    overlap = self.crossword.overlaps[var, neighbor]
                    if assignment[var][overlap[0]] != assignment[neighbor][overlap[1]]:
                        return False

        return True
        raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        constraining_values = {word: 0 for word in self.domains[var]}
        # for each word, find the number of words it will eliminate from a neighbors domain due to overlap mismatch
        neighbors = self.crossword.neighbors(var)

        for word in self.domains[var]: #for each word
            for neighbor in neighbors:      
                if neighbor not in assignment: #unassigned neighbor
                    overlap = self.crossword.overlaps[var, neighbor]
                    for wordn in self.domains[neighbor]: #for each word of neighbor
                        if word[overlap[0]] != wordn[overlap[1]]:
                            constraining_values[word]+=1 #number of eliminations

        least_cv = sorted(constraining_values, key=lambda x: constraining_values[x])
        return least_cv
        raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        ua_vars = [var for var in self.crossword.variables if var not in assignment]
        
        ua_vars.sort(key = lambda x: (len(self.domains[x]), -len(self.crossword.neighbors(x)))) # - makes highest values smallest 
        
        return ua_vars[0]
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if self.assignment_complete(assignment):
            return assignment
        #domains are dictionary
        no_inferences_domains = copy.deepcopy(self.domains)
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                #choose word for domain
                self.domains[var] = {value}
                #maintaining arc consistency
                arcs=[(neighbour, var) for neighbour in self.crossword.neighbors(var)]
                self.ac3(arcs)
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            
            #restore to pre backtrack since no soln
            del assignment[var]
            self.domains = no_inferences_domains
        return None

        raise NotImplementedError
"""
def inference(assignment):
    # runs AC-3 algorithm to maintain arc consistency 
    # Its output is all the inferences that can be made through enforcing arc-consistency
    inferences = []
    if ac3():
        inferences.append()
"""

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
