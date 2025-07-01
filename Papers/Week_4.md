# Not a paper - General Q RL
- General Tradeoff of maximizing the reward in the current step and maximizing the future reward
- Set by the gamma hyper parameter
- Example used was a maze taking any step was a -1 reward but reaching the goal gives a 100 reward 

# Human-Level Control Through Deep Reinforcement Learning
- Introduces deep RL which maps a state directly to an action using a neural network
  - Their example was Atari games so they used a CNN to map to a vector of different possible controls to input
- Uses a loss function of the ([current reward + max(next state) - current q score])
  - Trying to predict the recusrsive nature of Q RL
- Able to outperform people on Atari games

# Continuous Control With Deep Reinforcement Learning
- Add noise to the output of the critic model to encourage exploration (if there was no noise the critic would output the same V(s) for the action for each state exploring the same action over and over again)
- Actor: Maps current state to an action
- Critic: Evaluates from the state and action picked how well it can perform in the future, the V(s) value which is a prediction of how much reward can be picked up in the future
- Seperates the roles really nicely and easier to follow imo
- Doesn't need to be two seperate networks - can share a backbone, since it is the same problem, and have an actor classification head and critic regression head


# Safe Exploration in RL-Based Industrial Automation: Constraints Handling and Failure Recovery
- In regular RL agents can explore any possible action at each state including unsafe actions
- So the unsafe actions are not tested while continously training
- Limit strict actions, limit probabilities of failure actions, and temporal (if X is followed by Y it is unsafe) (can be modeled as a DFA)
- Comes down to what is considered a safe and unsafe set of actions
- The RL model can either go to the closest safe action if chooses an unsafe action or a large penalty is placed on unsafe actions (-infinity if breaks something that needs to be safe)
- Safety Concerns Brought up that apply to networking:
  - Set QoS requirements cannot test an action that goes below that guaranteed
- Incorporating Constraints:
  - Safety Shielding
    - External shield classifies action as safe/unsafe then if unsafe makes the action safe by redirecting to the closest safe actionhard to classify unsafe actions
  - Model Predictive Control - Predicts future actions taken then redirects those actions away from an unsafe state
  - Human in the loop :(
- Recovering if entered a unsafe region
  - Dynamic re planning
    - Plan a way back to a safe state
    - Learn from failure - get negative rewards when entering an unsafe area



# Asynchronous Methods for Deep Reinforcement Learning
- Trains on a multi-core CPU instead of a GPU!!
- Mentions n-step Q learning where the reward is only updated after n steps so it has to look into the future
- Runs each simulation with different exploration policies in parallel -> each agent exploring sends its gradient to the model which updates itself (kind of like DLP on GPUs on supervised learning)
- Scales well with the number of CPU threads available
- Using an LSTM backbone outperforms a FF but takes about the same amount of time to train. Shows structure of backbone matters (so GNN could be better)
- Also uses actor + critic model with a shared backbone and seperate prediction heads (logits and regression)


# Modeling TCP Performance using Graph Neural Networks
- Had a good graph representation - modeled the flows+ACK flow as nodes as well as the topology
- Shows a big decrease in error
- I really liked the diagrams easy to follow
- Short prediction time (5 ms on CPU and 7 ms on GPU)