import bpy
import os

# Getting path
dir = os.path.dirname(bpy.data.filepath)

from . import LSystemsMeshGen as lsystemsGen
#lsystemsGen = bpy.data.texts["l-systems-mesh-gen.py"].as_module()

## For generating the complete pattern
def generate(sentence, generations, rules):
    # Number of generations/iterations loop
    for i in range(generations):
        # Creating a temporary string
        temp = ""
        
        # The sentence loop     
        for j in range(len(sentence)):
            # Error handling to prevent errors
            if(sentence[j] in rules):
                # Updating the string
                temp = temp + rules[sentence[j]]
            
            else:
                temp = temp + sentence[j]
                            
        sentence = temp
        
    return sentence

def processRule(str):
    ls = str.split(':')
    return ls[0], ls[1]
    
## Generating the pattern based on inputs
def lsystems(ax, gen, numR, ang, leng, ruleList):
    ### TODO : Integrate this into the UI
    # Axiom ; Starting Point
    #axiom = input("Enter the axiom (Starting point): ")
    axiom = ax
    
    # Generations : How many times to run the loop
    #generations = int(input("Enter the number of generations: "))
    generations = gen
    
    # numRules : Number of rules that will be evaluated while generating the pattern
    #numRules = int(input("Enter the number of Rules: "))
    numRules = numR
    
    # angle : Angle by which we will turn
    #angle = float(input("Enter the angle by which to rotate: "))
    #angle = ang
    
    # length : Length of each segment
    #length = float(input("Enter the length of each segment: "))
    #length = leng
    
    # The actual rules
    #print("Enter the rules in format 'A(Rule Variable):AB(Actual Rule)'")
    
    # The Rule(s)
    # We are using a dictionary for ease of use and expandability
    # Left Hand = Single symbol/chara
    # Right Hand = The replacement/sequence of symbols
    ## Left Hand -> Right Hand
    '''
    F/G : Go forward by some number of units
    B : Go backward by some number of units (TODO)
    X : Doesn't do anything, acts as a placeholder
    - : Turn left by some degrees
    + : Turn right by some degrees
    [ : Corresponds to saving the current values for position and angle
    ] : Executing the saved values in '['
    
    (We’ll turn by 60 degrees by default)
    '''
    
    ## Generating an empty dictionary
    rules = {}
    for i in range(numRules):
        #key, value = processRule(input("Rule {}: ".format(i+1)))
        key, value = processRule(ruleList[i])
        rules[key] = value    
        
    # Generating the string
    a = generate(axiom.upper(), generations, rules)
    
    return a

## Getting the final axiom
def generateLSystem(ax, gen, numR, ang, leng, ruleList):
    ## Final axiom after iterating over the generations
    axiomFinal = lsystems(ax, gen, numR, ang, leng, ruleList)
    
    lsystemsGen.generateMesh(axiomFinal, leng, ang)
    
    bpy.context.scene.presetVal = 'custom'