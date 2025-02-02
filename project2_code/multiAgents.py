# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
#        return successorGameState.getScore()
        score = successorGameState.getScore()
        foodList = newFood.asList()
        if foodList:
            foodDistance_list = [manhattanDistance(newPos, food) for food in foodList]
            nearest_FoodDistance = min(foodDistance_list)
            score += 10.0 / nearest_FoodDistance

        for i, ghostState in enumerate(newGhostStates):
            ghostPos = ghostState.getPosition()
            distance_to_ghost = manhattanDistance(newPos, ghostPos)
            if newScaredTimes[i] > 0:
                score += 200.0 / distance_to_ghost
            else:
                if distance_to_ghost > 0:
                    score -= 10.0 / distance_to_ghost
        score -= len(foodList) * 100.0
        if action == Directions.STOP:
            score -= 500
        return score

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.minimax(gameState, 0, 0)[1]
#        util.raiseNotDefined()
    def minimax(self, gameState, agentIndex, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None
        num_Agents = gameState.getNumAgents()
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, depth)
        else:
            return self.minValue(gameState, agentIndex, depth)

    def maxValue(self, gameState, agentIndex, depth):
        legal_Actions = gameState.getLegalActions(agentIndex)
        if not legal_Actions:
            return self.evaluationFunction(gameState), None
        best_Score = float('-inf')
        best_Action = None

        for action in legal_Actions:
            successorState = gameState.generateSuccessor(agentIndex, action)
            score = self.minimax(successorState, 1, depth)[0]
            if score > best_Score:
                best_Score = score
                best_Action = action
        return best_Score, best_Action

    def minValue(self, gameState, agentIndex, depth):
        legal_Actions = gameState.getLegalActions(agentIndex)
        if not legal_Actions:
            return self.evaluationFunction(gameState), None
        best_Score = float('inf')
        best_Action = None

        for action in legal_Actions:
            successorState = gameState.generateSuccessor(agentIndex, action)
            if agentIndex == gameState.getNumAgents() - 1:
                score = self.minimax(successorState, 0, depth + 1)[0]
            else:
                score = self.minimax(successorState, agentIndex + 1, depth)[0]

            if score < best_Score:
                best_Score = score
                best_Action = action
        return best_Score, best_Action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
#        util.raiseNotDefined()
        alpha = float('-inf')
        beta = float('inf')
        value, action = self.alphaBeta(gameState, 0, 0, alpha, beta)
        return action

    def alphaBeta(self, gameState, agent_Index, depth, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None
        num_Agents = gameState.getNumAgents()
        if agent_Index == 0:
            return self.maxValue(gameState, agent_Index, depth, alpha, beta)
        else:
            return self.minValue(gameState, agent_Index, depth, alpha, beta)

    def maxValue(self, gameState, agent_Index, depth, alpha, beta):
        best_Value = float('-inf')
        best_Action = None
        legal_Actions = gameState.getLegalActions(agent_Index)
        if not legal_Actions:
            return self.evaluationFunction(gameState), None

        for action in legal_Actions:
            successorState = gameState.generateSuccessor(agent_Index, action)
            value, _ = self.alphaBeta(successorState, agent_Index + 1, depth, alpha, beta)

            if value > best_Value:
                best_Value = value
                best_Action = action
            if best_Value > beta:
                return best_Value, best_Action
            alpha = max(alpha, best_Value)
        return best_Value, best_Action

    def minValue(self, gameState, agent_Index, depth, alpha, beta):
        best_Value = float('inf')
        best_Action = None

        legal_Actions = gameState.getLegalActions(agent_Index)
        if not legal_Actions:
            return self.evaluationFunction(gameState), None

        for action in legal_Actions:
            successorState = gameState.generateSuccessor(agent_Index, action)
            if agent_Index == gameState.getNumAgents() - 1:
                next_Agent_Index = 0
                next_Depth = depth + 1
            else:
                next_Agent_Index = agent_Index + 1
                next_Depth = depth
            value, _ = self.alphaBeta(successorState, next_Agent_Index, next_Depth, alpha, beta)
            if value < best_Value:
                best_Value = value
                best_Action = action
            if best_Value < alpha:
                return best_Value, best_Action
            beta = min(beta, best_Value)
        return best_Value, best_Action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectimax(gameState, depth, agent_Index):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)

            if agent_Index == 0:
                return max(expectimax(gameState.generateSuccessor(agent_Index, action), depth, 1)
                           for action in gameState.getLegalActions(agent_Index))

            else:
                nextAgent = agent_Index + 1
                if agent_Index == gameState.getNumAgents() - 1:
                    nextAgent = 0
                    depth -= 1

                legalActions = gameState.getLegalActions(agent_Index)
                if not legalActions:
                    return self.evaluationFunction(gameState)

                probability = 1 / len(legalActions)
                expectedValue = sum(expectimax(gameState.generateSuccessor(agent_Index, action), depth, nextAgent)
                                    for action in legalActions) * probability
                return expectedValue

        bestAction = max(gameState.getLegalActions(0),
                         key=lambda action: expectimax(gameState.generateSuccessor(0, action), self.depth, 1))
        return bestAction

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacman_Position = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghosts = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()
    score = currentGameState.getScore()

    food_Distances = [manhattanDistance(pacman_Position, foodPos) for foodPos in food.asList()]
    if food_Distances:
        closest_Food_Distance = min(food_Distances)
    else:
        closest_Food_Distance = 0

    ghost_Distances = [manhattanDistance(pacman_Position, ghost.getPosition()) for ghost in ghosts]
    scared_Times = [ghost.scaredTimer for ghost in ghosts]

    capsule_Distances = [manhattanDistance(pacman_Position, capsule) for capsule in capsules]
    if capsule_Distances:
        closest_Capsule_Distance = min(capsule_Distances)
    else:
        closest_Capsule_Distance = 0

    food_Score = -1.5 * closest_Food_Distance
    ghost_Score = 0
    capsule_Score = -2 * closest_Capsule_Distance if capsules else 0
    scared_Ghost_Score = 0
    remaining_Food_Score = -4 * len(food.asList())
    remaining_Capsule_Score = -20 * len(capsules)

    for i in range(len(ghosts)):
        if scared_Times[i] > 0:
            scared_Ghost_Score += 200 / (ghost_Distances[i] + 1)
        else:
            if ghost_Distances[i] > 0:
                ghost_Score += -10 / ghost_Distances[i]

    evaluation = score + food_Score + ghost_Score + capsule_Score + scared_Ghost_Score + remaining_Food_Score + remaining_Capsule_Score
    return evaluation

better = betterEvaluationFunction
