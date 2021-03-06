from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
P0Asays1 = And(AKnight, AKnave)

knowledge0 = And(
    # TODO
    Not(And(AKnight, AKnave)),#A is not both a knight and a knave
    Implication(Not(P0Asays1),AKnave), #if Asays is false, A is a knave
    Implication(P0Asays1,AKnight) #if Asays is true, A is a knight
)

# Puzzle 1
# A says "We are both knaves."
P1Asays1 = And(BKnave, AKnave)

# B says nothing.
knowledge1 = And(
    # TODO
    Or(AKnight, AKnave), #A is either a KNight or knave
    Or(BKnight, BKnave), #B is either a KNight or knave
    Not(And(AKnight, AKnave)),#A is not both a knight and a knave
    Not(And(BKnight, BKnave)),#B is not both a knight and a knave


    #Implication(Not(P1Asays1),AKnave),#if Asays is false, A is a knave
    #Implication(P1Asays1,AKnight), #if Asays is true, A is a knight

    Biconditional(Not(P1Asays1),AKnave),#if Asays is false, A is a knave, if A is a knave, ASays is false

    #redundant statements ooops 
    #If p then p :^)
    #Implication(Not(P1Asays1),Not(P1Asays1)),#if Asays is false, A and B are both not knaves
    #Implication(P1Asays1,P1Asays1),#if Asays is true, A and B are both knave
)

# Puzzle 2
# A says "We are the same kind."
P2Asays1 = Or(Biconditional(AKnight,BKnight),Biconditional(AKnave,BKnave))
# B says "We are of different Kinds."
P2Bsays1 = Or(Biconditional(AKnight,BKnave),Biconditional(AKnave,BKnight))
knowledge2 = And(
    # TODO
    Or(AKnight, AKnave), #A is either a KNight or knave
    Or(BKnight, BKnave), #B is either a KNight or knave
    Not(And(AKnight, AKnave)),#A is not both a knight and a knave
    Not(And(BKnight, BKnave)),#B is not both a knight and a knave

    Biconditional(Not(P2Asays1),AKnave),#if Asays is false, A is a knave, if A is a knave, ASays is false

    Biconditional(Not(P2Bsays1),BKnave),#if Bsays is false, B is a knave, if B is a knave, BSays is false

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
P3Asays1 = And(Or(AKnight, AKnave),Not(And(AKnight, AKnave)))
# B says "A said 'I am a knave'."
P3Bsays1 = Or(Biconditional(AKnight,AKnave))#If A is Knight, A is Knave or If A is Knave, A is not Knave 
# B says "C is a knave."
P3Bsays2 = CKnave
# C says "A is a knight."
P3Csays1 = AKnight
knowledge3 = And(
    # TODO
    Or(AKnight, AKnave), #A is either a KNight or knave
    Or(BKnight, BKnave), #B is either a KNight or knave
    Not(And(AKnight, AKnave)),#A is not both a knight and a knave
    Not(And(BKnight, BKnave)),#B is not both a knight and a knave

    Or(CKnight, CKnave), #C is either a KNight or knave
    Not(And(CKnight, CKnave)),#C is not both a knight and a knave


    Biconditional(Not(P3Asays1),AKnave),#iff Asays is false, A is a knave, 

    Biconditional(And(Not(P3Bsays1),Not(P3Bsays2)),BKnave),#iff Bsays is false,
    Biconditional(Not(P3Csays1),CKnave),#iff Csays is false, C is a knave, 

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
