# factorOperations.py
# -------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from typing import List
from bayesNet import Factor
import functools
from util import raiseNotDefined

def joinFactorsByVariableWithCallTracking(callTrackingList=None):


    def joinFactorsByVariable(factors: List[Factor], joinVariable: str):
        """
        Input factors is a list of factors.
        Input joinVariable is the variable to join on.

        This function performs a check that the variable that is being joined on 
        appears as an unconditioned variable in only one of the input factors.

        Then, it calls your joinFactors on all of the factors in factors that 
        contain that variable.

        Returns a tuple of 
        (factors not joined, resulting factor from joinFactors)
        """

        if not (callTrackingList is None):
            callTrackingList.append(('join', joinVariable))

        currentFactorsToJoin =    [factor for factor in factors if joinVariable in factor.variablesSet()]
        currentFactorsNotToJoin = [factor for factor in factors if joinVariable not in factor.variablesSet()]

        # typecheck portion
        numVariableOnLeft = len([factor for factor in currentFactorsToJoin if joinVariable in factor.unconditionedVariables()])
        if numVariableOnLeft > 1:
            print("Factor failed joinFactorsByVariable typecheck: ", factor)
            raise ValueError("The joinBy variable can only appear in one factor as an \nunconditioned variable. \n" +  
                               "joinVariable: " + str(joinVariable) + "\n" +
                               ", ".join(map(str, [factor.unconditionedVariables() for factor in currentFactorsToJoin])))
        
        joinedFactor = joinFactors(currentFactorsToJoin)
        return currentFactorsNotToJoin, joinedFactor

    return joinFactorsByVariable

joinFactorsByVariable = joinFactorsByVariableWithCallTracking()

########### ########### ###########
########### QUESTION 2  ###########
########### ########### ###########

def joinFactors(factors: dict):
    # Jason
    """
    Input factors is a list of factors.  
    
    You should calculate the set of unconditioned variables and conditioned 
    variables for the join of those factors.

    Return a new factor that has those variables and whose probability entries 
    are product of the corresponding rows of the input factors.

    You may assume that the variableDomainsDict for all the input 
    factors are the same, since they come from the same BayesNet.

    joinFactors will only allow unconditionedVariables to appear in 
    one input factor (so their join is well defined).

    Hint: Factor methods that take an assignmentDict as input 
    (such as getProbability and setProbability) can handle 
    assignmentDicts that assign more variables than are in that factor.

    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """
    

    # We turn (factors: dic) into list of factors for easier access
    factors = list(factors) 
    # print("List---factor form: Factor{[unconditioned vars}, {conditioned vars}, [dict(varaible domains] \n", factors)
    
    # Create sets for unconditioned and conditioned variables to create our new factor
    unconditionedVarSet = set()
    conditionedVarSet = set()

    # Assume that all factors have the same domain dictionary per the directions above
    variableDomainDict = factors[0].variableDomainsDict()
    # print(variableDomainDict)
    
    # Update each set with the unconditional and conditioned variables from each factor
    for factor in factors:
        unconditionedVarSet.update(factor.unconditionedVariables())
        conditionedVarSet.update(factor.conditionedVariables())

    # The conditional set should not have anything that is in the unconditional set
    # print(unconditionedVarSet)
    # print(conditionedVarSet)
    conditionedVarSet = conditionedVarSet - unconditionedVarSet
    
    newFactor = Factor(unconditionedVarSet, conditionedVarSet, variableDomainDict)
    allAssignmentDicts = newFactor.getAllPossibleAssignmentDicts()
    
    for assignmentDict in allAssignmentDicts:
        # print("assignmentDic", assignmentDict)
        # For every combination of the factors (ex:Sun and Wet, Rain and Wet etc.)
        totalProbability = 1.0  
        # Initialize to one- multiplication identity
        
        for factor in factors:
            # Get the probability for each factor ex. Sun and multiply it together with existing probability 
            # print("Factor", factor)
            factorProbability = factor.getProbability(assignmentDict)
            totalProbability =  totalProbability * factorProbability
            
        newFactor.setProbability(assignmentDict, totalProbability)

    return newFactor

    # if len(factors) > 1:
    #     intersect = functools.reduce(lambda x, y: x & y, setsOfUnconditioned)
    #     if len(intersect) > 0:
    #         print("Factor failed joinFactors typecheck: ", factor)
    #         raise ValueError("unconditionedVariables can only appear in one factor. \n"
    #                 + "unconditionedVariables: " + str(intersect) + 
    #                 "\nappear in more than one input factor.\n" + 
    #                 "Input factors: \n" +
    #                 "\n".join(map(str, factors)))

    "*** YOUR CODE HERE ***"
    
    #raiseNotDefined()
    "*** END YOUR CODE HERE ***"

########### ########### ###########
########### QUESTION 3  ###########
########### ########### ###########

def eliminateWithCallTracking(callTrackingList=None):

    def eliminate(factor: Factor, eliminationVariable: str):
        """
        Input factor is a single factor.
        Input eliminationVariable is the variable to eliminate from factor.
        eliminationVariable must be an unconditioned variable in factor.
        
        You should calculate the set of unconditioned variables and conditioned 
        variables for the factor obtained by eliminating the variable
        eliminationVariable.

        Return a new factor where all of the rows mentioning
        eliminationVariable are summed with rows that match
        assignments on the other variables.

        Useful functions:
        Factor.getAllPossibleAssignmentDicts
        Factor.getProbability
        Factor.setProbability
        Factor.unconditionedVariables
        Factor.conditionedVariables
        Factor.variableDomainsDict
        """
        # autograder tracking -- don't remove
        if not (callTrackingList is None):
            callTrackingList.append(('eliminate', eliminationVariable))

        # typecheck portion
        if eliminationVariable not in factor.unconditionedVariables():
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Elimination variable is not an unconditioned variable " \
                            + "in this factor\n" + 
                            "eliminationVariable: " + str(eliminationVariable) + \
                            "\nunconditionedVariables:" + str(factor.unconditionedVariables()))
        
        if len(factor.unconditionedVariables()) == 1:
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Factor has only one unconditioned variable, so you " \
                    + "can't eliminate \nthat variable.\n" + \
                    "eliminationVariable:" + str(eliminationVariable) + "\n" +\
                    "unconditionedVariables: " + str(factor.unconditionedVariables()))

        "*** YOUR CODE HERE ***"
        print("original factor", factor)
        print("variable to eliminate", eliminationVariable)
        
        unconditionedVarSet = factor.unconditionedVariables()
        print("old unconditioned", unconditionedVarSet)
        print("the string is", eliminationVariable)
        eliminationVariableSet = {eliminationVariable}
        print("the set becomes", (eliminationVariableSet))
        unconditionedVarSet = unconditionedVarSet- (eliminationVariableSet)
        print("new unconditioned after elimination", unconditionedVarSet)  
        
        varDomainDict = factor.variableDomainsDict()
        print("varDomainDict", varDomainDict)
      
        newFactor = Factor(unconditionedVarSet, factor.conditionedVariables(), varDomainDict)

        
        allAssignmentDicts = factor.getAllPossibleAssignmentDicts()
        #Get all possible combinations for the old factor
        for assignmentDict in allAssignmentDicts:
            # print(assignmentDict)
            # For every combination of the factors (ex:Sun and Wet, Rain and Wet etc.)
            totalProbability = 0.0  
            # Initialize to 0.0- addition identity
            domainsWithElim = varDomainDict[eliminationVariable]
            for elimVar in (domainsWithElim):
                # For every domain with elimVar, we add up the total probability
                # print("elimVar",elimVar)

                assignmentDict[eliminationVariable] = elimVar

               # Add the probability of this current probability that contains elim to the total
                # print("elimVarProbability + previousProbability =", totalProbability, "+", factor.getProbability(assignmentDict))

                totalProbability =  totalProbability + factor.getProbability(assignmentDict)

                
            newFactor.setProbability(assignmentDict, totalProbability)

        return newFactor
        "*** END YOUR CODE HERE ***"

    return eliminate

eliminate = eliminateWithCallTracking()

