▷ [**Usage-Guide**](../../README.md#usage) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
☐ [**Structure-Guide**](#structure) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
⧉ [**Extension-Guide**](#extension) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
⚙ [**Configuration-Guide**](./config/README.md#configuration) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
❖ [**Pattern-Guide**](./config/README.md#patterns) 
 
---

<a id="toc"></a>

# **Table of Contents**

- [**Structure**](#structure)
  - [Reinforcement Learning](#structure.rl)
    - [Agents](#structure.rl.agents)
      - [SB3 Agents](#structure.rl.agents.sb3)
        - [Policies](#structure.rl.agents.sb3.policies)
      - [Custom Agents](#structure.rl.agents.custom)
    - [Brains](#structure.rl.brains)
  - [Environment](#structure.environment)
    - [Reward](#structure.environment.reward)
  - [Microgrid](#structure.microgrid)
    - [Components](#structure.microgrid.components)
    - [Actions](#structure.microgrid.actions)   

<br>  

- [**Extension**](#extension)
  - [Extending Reinforcement Learning](#extension.rl)
    - [New Agents](#extension.rl.agents)
        - [New SB3 Agents](#extension.rl.agents.sb3)
    - [New Brains](#extension.rl.brains)
  - [Extending Environment](#extension.environment)
    - [New Reward](#extension.environment.reward)
  - [Extending Microgrid](#extension.microgrid)
    - [Extending Components](#extension.microgrid.components)
        - [New Components](#extension.microgrid.components.new)
        - [Existing Components](#extension.microgrid.components.existing)
    - [New Actions](#extension.microgrid.actions)
    - [New Microgrid Factory](#extension.microgrid.factory)
  - [Extending Config](#extension.config)
    - [New Application Variables](#extension.config.variables)

<br>
<br>

<a id="structure"></a>

# **☐ Structure**
This project provides a framework to run different Reinforcement Learning (**RL**) algorithms to learn the management of a microgrid. The key components/ parts of the framework will be described in the following.     
<span style="color: grey; font-size: 11px;">(For a quick overview over the existing classes, please refer to this [UML ▷](https://github.com/yaHzm/rlmicrogrid/blob/121cbf17646a0119f842eedc9336c2abcc18f5f3/docs/uml.md))</span>

<div style="height: 400px; transform: scale(0.9); transform-origin: top;">
  <a href="#structure">
    <img src="https://github.com/yaHzm/rlmicrogrid/blob/121cbf17646a0119f842eedc9336c2abcc18f5f3/docs/svg/structure.svg" alt="structure" style="vertical-align: top;">
  </a>
</div>

> # **TL;DR**   
> There are three key parts:
>
> - Reinforcement Learning
> - Microgrid  
> - Environment
>
> The RL part includes the agents, representing RL-Algorithms to train NNs, as well as the brains, representing said NNs. Each agent holds 
> such a brain.   
>
> The microgrid part represents the domain of this application and framework. It consists of the components making up the microgrid as well
> as actions that can be used to alter its state.    
>
> The environment part is the common interface to apply the RL to the domain of the microgrid. It enables the agent to simulate actions on 
> the microgrid and returns a reward describing the value of an action. 
>
> The agent applies a specific RL algorithm to try actions and adjust it's brain parameters based on the feedback received from the 
> environment. 


<a id="structure.rl"></a>

## **Reinforcement Learning [>](./reinforcement_learning/)**
The first key part is the **Reinforcement Learning** part, containing the agents that define the RL-Algorithm to be used and interact with the environment, as well as the brains for the agents, i.e., the Neural Networks (**NN**) to be trained by the agent. 

<a id="structure.rl.agents"></a>

### **Agents [>](./reinforcement_learning/agents/)**   
Agents are instances that define a RL-Algorithm to train a brain [▼](#structure.rl.brains), and interact with the environment [▼](#structure.environment) to receive a feedback (reward) for actions and adjust the brain parameters accordingly.    
All agents (and sub-interfaces for agents) implement the [`IAgent`](./reinforcement_learning/agents/_base.py) interface. This is necessary when implementing a new agent for it to be registered in the [`AgentRegistry`](./config/registry/_registry.py) and to be easily instantiated when passed as argument to the run-command of the application.    
<span style="color: grey; font-size: 11px;">(For more detailed information on the usage of this framework, please refer to the [Usage-Guide ▷](../../README.md#usage),   
for more detailed information on the definition of new agents, please refer to the respective [Extension-Guide ▼](#extension.rl.agents))</span>   

<a id="structure.rl.agents.sb3"></a>

#### **SB3 Agents [>](./reinforcement_learning/agents/sb3/)**    
The framework supports the usage of predefined agents from [Stable-Baselines3](https://stable-baselines3.readthedocs.io/en/master/). For that, the [`ISB3Agent`](./reinforcement_learning/agents/sb3/_base.py) interface, which itself is a sub-interface of the `IAgent` interface, has to be extended by the wrapper class for the respective SB3 agent.   
Each agent is bound to a policy [▼](#structure.rl.agents.sb3.policies) that holds the brain of the agent to be used as Neural Network to be trained.   
<span style="color: grey; font-size: 11px;">(For more detailed information on the definition of new SB3 Agents, please refer to the respective [Extension-Guide ▼](#extension.rl.agents.sb3))</span>   

<a id="structure.rl.agents.sb3.policies"></a>

##### **Policies [>](./reinforcement_learning/agents/sb3/policies/)**   
In SB3, policies represent the Neural Network trained by agents. To be able to use the specified brain [▼](#structure.rl.brains) of this framework both for custom implementations of RL-Agents, as well as the SB3 agents, a custom policy implementing the [`IBrainPolicy`](./reinforcement_learning/agents/sb3/policies/_base.py) interface is needed that wraps and combines the built-in standard policy of an agent from SB3 with the implementation of brains within our framework. Such built-in policies within SB3 are quite unique for each agent which is why it is necessary for each new SB3 agent to implement such a wrapper class to include brains within the agents policy and which is why each agent is genuinly bound to a single unique policy.   
<span style="color: grey; font-size: 11px;">(For more detailed information on the role of policies within SB3, please refer to the respective [Documentation](https://stable-baselines3.readthedocs.io/en/master/guide/custom_policy.html),   
for more information on the creation of new policies to use brains, please refer to the respective [Extension-Guide ▼](#extension.rl.agents.sb3.policies))</span>  

<a id="structure.rl.agents.custom"></a>

#### **Custom [>](./reinforcement_learning/agents/custom/)**     
Besides off-the-shelf RL-Agents from StableBaselines3, this framework also supports custom implementations of RL-Agents. Respective classes simply have to implement the `IAgent` interface as mentioned. 

<a id="structure.rl.brains"></a>

### **Brains [>](./reinforcement_learning/brains/)**  
Brains simply represent Neural Networks and get passed to agents [▲](#structure.rl.agents) to be trained. All brains implement the [`IBrain`](./reinforcement_learning/brains/_base.py) interface. As for the agents for example as well, this is necessary for implemented brains to be registered in the [`BrainRegistry`](./config/registry/_registry.py) and to be easily instantiated when passed as argument to the run-command of the application.    
<span style="color: grey; font-size: 11px;">(For more detailed information on the definition of new brains, please refer to the respective [Extension-Guide ▼](#extension.rl.brains))</span>   

<a id="structure.environment"></a>

## **Environment [>](./environment/)**   
The second key part is the **environment** part, enabling the agent [▲](#structure.rl.agents) to interact with the microgrid [▼](#structure.microgrid) by simulating actions [▼](#structue.microgrid.actions) and returning a feedback in form of a reward [▼](#structure.environment.reward) to the agent to be used to adjust the brain accordingly.   
This framework leverages the [Gymnasium](https://gymnasium.farama.org) library (*Farama Foundation, OpenAI*) and the [`gym.Env`](https://gymnasium.farama.org/api/env/) class as standardized interface for the interaction of agents and the simulation of environments.  

<a id="structure.environment.reward"></a>

### **Reward [>](./environment/reward/)**    
The reward is used to rate actions [▼](#structue.microgrid.actions) made by the agent [▲](#structure.rl.agents). The agent uses this feedback to adjust its parameters.   
All rewards implement the [`IReward`](./environment/reward/_base.py) interface. As for the agents and brains for example as well, this is necessary for implemented rewards to be registered in the [`RewardRegistry`](./config/registry/_registry.py) and to be easily instantiated when passed as argument to the run-command of the application.   
<span style="color: grey; font-size: 11px;">(For more detailed information on the definition of new rewards, please refer to the respective [Extension-Guide ▼](#extension.environment.reward))</span>   


<a id="structure.microgrid"></a>

## **Microgrid [>](./microgrid/)**   
The third key part, representing the domain of this RL-Application/ -Framework, is the **microgrid** part. A microgrid represents the energy generation, energy consumption and energy storage of a household. The microgrid is used within the environment [▲](#structure.environment) for simulations for the agent [▲](#structure.rl.agents) to train the management of such a microgrid.     

<a id="structure.microgrid.components"></a>

### **Components [>](./microgrid/components/)**
A microgrid within our model of the domain consists of the following components:  

- [`(House)  Battery`](./microgrid/components/_battery.py)
- Car Battery
- [`DistributedEnergyResources (DER)`](./microgrid/components/_distributed_energy_resources.py)  
- [`ExternalGrid`](./microgrid/components/_external_grid_.py)
- [`ResidentialLoads`](./microgrid/components/_residential_load.py)

These represent the households energy storage (House/ Car Battery), its energy generation (DER (internally), External Grid (externally)) and its energy consumption (Residential Loads). As Components of the microgrid are generally quite different and unique and are therefore modeled as such, i.e., with component-specific methods and attributes, there is no Component-Interface for components to implement.    
All components get combined within the [`Microgrid`](./microgrid/_microgrid.py) class. New components have to be added there to be represented within the model of a microgrid.    
<span style="color: grey; font-size: 11px;">(For more detailed information on the definition of new components, please refer to the respective [Extension-Guide ▼](#extension.microgrid.components))</span>  

<a id="structure.microgrid.actions"></a>

### **Actions [>](./microgrid/actions/)**   
In order for the agent [▲](#structure.rl.agents) to simulate the management of the microgrid, it provides a set of actions it can use to alter the state of the microrgid and interact with its components. In each step of the training of the agent, the agent calls the `step()` method of the environment [▲](#structure.environment), providing an action to be executed, for the environment to carry out the action and return a reward [▲](#structure.environment.reward) based on the subsequent state of the microgrid. The brain of the agent therefore learns to predict the right action based on the state of the microgrid.   

All Actions implement the [`IAction`](./microgrid/actions/_base.py) interface. This interface provides a method to be implemented to execute the respective action on a given micogrid state and return an [`ActionResult`](./microgrid/actions/_base.py) describing the effects of the action on the microgrid state. It also provides a method to be implemented to create the respective action from an integer, as actions generally get handled as integers, as the Brain's Neural Network predicts scalars representing actions.  

<div style="text-align: right;">
  <a href="#toc">Back to top ↑</a>
</div>

<br>
<br>
<br>
<br>

<a id="extension"></a>
 
# **⧉ Extension**   
Besides the possbility to run and test the already implemented components of this RL-Application in the domain of energy management in a microgrid, this framework was also kept as easy as possible to extend in each part of the framework (Reinforcement Learning, Microgrid, Environment and Application Configuration) by design, i.e. by applying common software-architectural patterns, as well as by defining core interfaces to define the behavior of exchangeable components of the application.  
The possibilities to extend the existing framework for further development will be described in the following.   
<span style="color: grey; font-size: 11px;">(For an introduction into the applied patterns, please refer to the [Pattern-Guide ▷](./config/README.md#applied-patterns))</span>


<div style="height: 400px; transform: scale(0.9); transform-origin: top;">
  <a href="#extension">
    <img src="https://github.com/yaHzm/rlmicrogrid/blob/121cbf17646a0119f842eedc9336c2abcc18f5f3/docs/svg/extension.svg" alt="extension" style="vertical-align: top;">
  </a>
</div>


> # **TL;DR**   
> The framework is designed for modularity and easy extensibility using common interfaces, dependency injection, and the factory pattern. This enables new components to be implemented or existing ones to be extended with minimal changes to the core system.   
> 
> Each main part of the application provides the opportunity to be easily extended: 
> 
> - Reinforcement Learning  
>   - New agents to apply new RL-Algorithms, both custom or prebuilt by SB3   
>   - New brains to train new NN-Architectures
> 
> - Environemnt   
>   - New reward calculations
> 
> - Microgrid   
>   - New components to be added to the model of a microgrid (or the extension of existing ones)   
>   - New actions to interact with and change the state of the microgrid
>   - New microgrid factories 
> 
> To be able to easily configure the application and define the behavior via arguments passed to the run-command, also for extended functionalities, the configuration can also be easily extended by new application variables. 

<a id="extension.rl"></a>

## **Extending Reinforcement Learning [▲](#structure.rl)**   
Within the RL part, obviously different RL-Algorithms can be used within agents to train NNs for the task of managing the microgrid at hand, as well as different NN-Architectures within the brain. This framework provides the possibility to easily exchange those components of the application.   

<a id="extension.rl.agents"></a>

### **New Agents [▲](#structure.rl.agents)**   
As mentioned, all agents implement the [`IAgent`](./reinforcement_learning/agents/_base.py) interface. When implementing new agents, i.e. a new RL-Algorithm to be applied, the respective class simply has to implement this interface with its respective abstract methods and can already be used by passing the class name to the `--agent` flag of the run-command. However, make sure to add it to the [`AgentOptions`](./config/configuration/options/_options.py) enum first as new attribute for it to be recognized as valid option for the agent argument.   
What to do, in case the new agent should be initialized with a not yet implemented variable passed to the run-command, without having to write a new factory, will be described in the section on the extension of the config package [▼](#extension.config).    

Implementations of new custom agents (not leveraging prebuilt agents from SB3), should by convention be placed within the reinforcement_learning.agents.custom [>](./reinforcement_learning/agents/custom/) package within a new separate file and named like `{RL-Algorithm}Agent`.   
<span style="color: grey; font-size: 11px;">(For more detailed information on the interface to be implemented, please refer to the respective [`Incode-Documentation`](./reinforcement_learning/agents/_base.py),    
for an example of an agent implementation, please refer to the [`DQNAgent`](./reinforcement_learning/agents/custom/_dqn.py) class)</span>  

<a id="extension.rl.agents.sb3"></a>

#### **New SB3 Agents [▲](#structure.rl.agents.sb3)**   
In case a new prebuilt SB3 agent should be introduced into the framework, the respective Sub-Interface of the [`IAgent`](./reinforcement_learning/agents/_base.py) interface has already been specified, namely the [`ISB3Agent`](./reinforcement_learning/agents/sb3/_base.py) interface, which has to be implemented by new wrappers for SB3 agents.     
In SB3, custom brains can be passed to an agent within a policy class. This means, for new SB3 agents, a new custom policy has to be implemented as well to be able to use the custom brains of this framework.   
The policy base class from SB3, that has to be implemented by the custom policy class, differs based on the type of RL-Algorithm implemented by the agent, as does its implementation, which is why this framework cannot specify a common interface for new policies that can easily be used within new agents. The implementation of a custom policy for a new agent may also require the definition of further custom classes, as for example the [`CustomQNetwork`](./reinforcement_learning/agents/sb3/policies/_dqn.py) for the [`SB3_DQNAgent`](./reinforcement_learning/agents/sb3/_sb3_dqn.py). For percise information on needed policy classes and possibilities to introduce custom brain implementations into them, please refer to the official [SB3 Docs](https://stable-baselines3.readthedocs.io/en/master/guide/custom_policy.html).   

Implementations of new SB3 agents should by convention be placed within the reinforcement_learning.agents.sb3 [>](./reinforcement_learning/agents/sb3/) package within a new separate file and named like `SB3_{RL-Algorithm}Agent`,   
and new policies should by convention be placed within the reinforcement_learning.agents.sb3.policies [>](./reinforcement_learning/agents/sb3/policies/) package within a new separate file and named like `{RL-Algorithm}BrainPolicy`.   
<span style="color: grey; font-size: 11px;">(For more detailed information on the interface to be implemented, please refer to the respective [`Incode-Documentation`](./reinforcement_learning/agents/sb3/_base.py),    
for an example of an SB3 agent and policy implementation, please refer to the [`SB3_DQNAgent`](./reinforcement_learning/agents/sb3/_sb3_dqn.py) and [`DQNBrainPolicy`](./reinforcement_learning/agents/sb3/policies/_dqn.py) classes)</span> 


<a id="extension.rl.brains"></a>

### **New Brains [▲](#structure.rl.brains)**  
Brains simply specify different NN-Architectures. New brains have to implement the [`ÌBrain`](./reinforcement_learning/brains/_base.py) interface to be used by passing the class name to the `--brain` flag of the run-command. Generally, brains simply build a [PyTorch-Module](https://docs.pytorch.org/docs/stable/generated/torch.nn.Module.html)  representing a NN of the respective Architecture, which is kept variable towards different input-  (size of the observation space) and output- (size of the action space) dimensions.  
How to introduce further variables to be passed by the run-command, as was done for the [`MLPBrain`](./reinforcement_learning/brains/_mlp.py) class with the `hidden_dims`parameter for example, will be described in the section on the extension of the config package [▼](#extension.config).     

Implementations of new brains should by convention be placed within the reinforcement_learning.brains [>](./reinforcement_learning/brains/) package within a new separate file, named like `{NN-Architecture}Brain` and added as option in the [`BrainOptions`](./config/configuration/options/_options.py) class to be recognized when passed to the run-command.    
<span style="color: grey; font-size: 11px;">(For more detailed information on the interface to be implemented, please refer to the respective [`Incode-Documentation`](./reinforcement_learning/brains/_base.py),    
for an example of a brain implementation, please refer to the [`MLPBrain`](./reinforcement_learning/brains/_mlp.py) class)</span>  



<a id="extension.environment"></a>

## **Extending Environment [▲](#structure.environment)**
The logic of the environment class as interface between the RL and the domain is always the same, i.e., executing an action passsed from the agent, calculating the reward and returning the observation. There is therefore no need to be able to have different factories for the initialization of an environment (as the components passed on initialization implement comon interfaces) or different environment implementations for different step-logics. However, what can be interchanged within the environment package is the reward calculation logic.  

<a id="extension.environment.reward"></a>

### **New Reward [▲](#structure.environment.reward)**  
New rewards have to implement the [`ÌReward`](./environment/reward/_base.py) interface, which basically consits of only a single method to be implemented to calculate the reward, to be used by passing the class name to the `--reward` flag of the run-command. For the calculation of a reward, the current state of the microgrid is passed as well as some accumulated metrics regarding the results of an action in form of a [`CompositeResult`](./microgrid/actions/_composite.py). All of these provided informations can be regarded in the calculation. New information needed for the calculation has to be added to either one of those to be accessible by the reward class.   

Implementations of new rewards should by convention be placed within the environment.reward [>](./environment/reward/) package within a new separate file, named like `{Name}Reward` and added as option in the [`RewardOptions`](./config/configuration/options/_options.py) class to be recognized when passed to the run-command.    
<span style="color: grey; font-size: 11px;">(For more detailed information on the interface to be implemented, please refer to the respective [`Incode-Documentation`](./environment/reward/_base.py),    
for an example of a reward implementation, please refer to the [`BasicReward`](./environment/reward/_basic_reward.py) class)</span>  



<a id="extension.microgrid"></a>

## **Extending Microgrid [▲](#structure.microgrid)**   
The microgrid offers a lot of opportunities for extension, as there is an arbitrary number of ways to simulate and model a microgrid, starting with the decision of which components to include and how many, their respective concrete implementations and of course the actions to provide the agent with to interact with it. As the interface between the microgrid package and the rest of the application are to a big part the actions executed by the agent, the logic of the components and the actions strongly interconnects and the extension of the microgrid in regards of components may include appropriate adjustments in the latter and vice versa. 

<a id="extension.microgrid.components"></a>

### **Extending Components [▲](#structure.microgrid.components)**   

<a id="extension.microgrid.components.new"></a>

#### **New Components**  
Components of the microgrid follow no common interface, as their implementation is specific to their logic and role, as is the interaction with them via actions. 
New components can therefore be defined freely without any restrictions by interfaces to be matched.   
By convention, arguments passed to a component on initialization are bundled in a config class that is unique to the respective component.   

Such config classes implement the [`IConfig`](./config/configuration/microgrid/_base.py) interface and are simply pydantic `BaseModel`s with attributes specifying the arguments a component takes, alongside a description and a default value. New config classes for new components should be implemented within the respective configuration file [▷](./config/configuration/microgrid/_microgrid.py).  
The initialization logic of components is extracted to respective factories.  For new components, a new interface for factories for the respective component has to be defined, that follows the scheme of the other component factory interfaces and simply specifies the config class used for the initalization. This interface should be implemented in the respective base file [▷](./config/factory/_base.py) alongside the other interfaces for factories.    

Concrete factories for a new component can then be implemented within a separate file for the component within the config.factory.components [>](./config/factory/components/) package. Usually, there is one basic factory that simply uses the config class initialized with no arguments for the initialization of the component, effectively using the defaults specified.    
How to include new components within a used model of a microgrid will be described in the section on how to add new microgrod factories [▼](#extension.microgrid.factory).   
<span style="color: grey; font-size: 11px;">(For more detailed information on the factory pattern used, refer to the respective [Pattern-Guide ▷](./config/README.md#patterns.factory),   
for an example of a component with a respective config class, a respective interface for factories and a concrete factory, please refer to the [`Battery`](./microgrid/components/_battery.py) class with the [`BatteryConfig`](./config/configuration/microgrid/_microgrid.py) config class, as well as the [`IBatteryFactory`](./config/factory/_base.py) as factory interface and the [`BasicBatteryFactory`](./config/factory/components/_battery.py) as concrete factory)</span>  

<a id="extension.microgrid.components.existing"></a>

#### **Existing Components**  
Not only can new components be implemented, but also existing ones extended.   
When adding, removing or changing parameters passed to the component at initialization, these changes have to be implemented within the respective config class in the configuration file [▷](./config/configuration/microgrid/_microgrid.py). The concrete factories for the respective component obviously have to reflect these changes as well (apart from the basic factory, where the config is initialized without arguments).   

Another way to extend existing components would be to change the source of the values used for parameters of a component. For the basic usage, these values are defined within the config classes (as defaults), however, these values may rather be extracted from specific APIs or data sources, for example for the energy generation of the external grid. In that case, simply a new concrete factory has to be implemented, that handles the data retrieval from the data source or API and initializes the config for the respective component with the retrieved values.  

As mentioned before in the section on implementing new components [▲](#extension.microgrid.components.new),
implementations of factories for a component should by convention be placed within the a single according file within the config.factory.components [>](./config/factory/components/) package and named like `{Name}{Component}Factory`.   


<a id="extension.microgrid.actions"></a>
<!-- TODO: Possibly adjust as soon as composite actions is changed to be more extendable -->

### **New Actions [▲](#structure.microgrid.actions)**  
Upfront, actions define opportunities for the agent to change the state of the microgrid and its components. This means, that new actions may require new respective methods on the side of the components to be altered/ interacted with. 

New actions have to implement the [`IAction`](./microgrid/actions/_base.py) interface. Actions are provided to an agent via the [`CompositeAction`](./microgrid/actions/_composite.py) class that bundles all actions that can be executed by an agent. 
New actions therefore have to be included in the action execution logic of this class, as well as the initialization of the [`ACTIONS`](./microgrid/actions/_composite.py) array, specifying all combinations of actions there are. 
For specific results to be included in the calculation of the reward for an action, the result has to be added to the [`CompositeResult`](./microgrid/actions/_composite.py) class to be made accessible within the environment for the reward calculation.   
<span style="color: grey; font-size: 11px;">(For more detailed information on the interface to be implemented, please refer to the respective [`Incode-Documentation`](./microgrid/actions/_base.py))</span>  



<a id="extension.microgrid.factory"></a>
<!-- TODO: Possibly adjust as soon as microgrid class has been adjusted to be 
more flexible towards differetn compositions of components -->

### **New Microgrid Factory [▷](./config/README.md#patterns.factory)**  
The initialization of the microgrid from its components is implemented in factories for the microgrid. The composition of components to form the model of the microgrid is static. However, different factories for each component may be available, resulting in a number of possible combinations of component-specific factories to be used to initialize the components of the microgrid.   

New factories for the microgrid have to implement the [`ÌMicrogridFactory`](./config/factory/_base.py) interface to be used by passing the class name to the `--microgrid` flag of the run-command.  
Concrete factories implementing this interface simply have to pick a factory for each component of the microgrid and specify where to get the values for the [`MicrogridConfig`](./config/configuration/microgrid/_microgrid.py) from.   

The [`BasicMicrogridFactory`](./config/factory/_microgrid.py), for example, simply uses the basic factory for each component and uses the default values for the config class.   

Implementations of new microgrid factories should by convention be placed within the respective factory file [▷](./config/factory/_microgrid.py), named like `{Name}MicrogridFactory` and added as option in the [`MicrogridFactoryOptions`](./config/configuration/options/_options.py) class to be recognized when passed to the run-command.   
<span style="color: grey; font-size: 11px;">(For more detailed information on the factory pattern used, refer to the respective [Pattern-Guide ▷](./config/README.md#patterns.factory))</span> 

<a id="extension.config"></a>

## **Extending Config [>](./config/)**   
The arguments that can be passed to the run-command to configure the used components and general application variables are repersented by the [`Args`](./config/configuration/args/_args.py) class.    
<span style="color: grey; font-size: 11px;">(For more information on the [`Args`](./config/configuration/args/_args.py) class and the general configuration, please refer to the [Configuration-Guide ▷](./config/README.md#configuration))</span> 

<a id="extension.config.variables"></a>

### **New Application Variables [▷](./config/README.md#configuration)**
New components, agents, rewards, or any other extension to the framework may introduce new parameters that should additionally be specified or possible to be specified within the run-command.   

Firstly, In order to not have to adjust a bunch of classes to propagate some parameter to the right class, the initialization logic has been kept rather flat and Dependency Injection has been widely used, so the application arguments passed are accessible by most of the initialization logic. That means, that new arguments don't have to be passed thorugh a long row of classes to be acessible at initialization of the respective class who the parameter belongs to, and therefore adding new arguments won't require changing any other classes (in most cases).   

Secondly, the [`Args`](./config/configuration/args/_args.py) class implements a specific `call()` method that takes another method, that will extract the necessary arguments for the passed method from its attributes and call it.   
This means, that if an attribute is added to the constructor of a class, as well as the [`Args`](./config/configuration/args/_args.py) class, and the initialization of the class is wrapped with the `Args.call()` method, there is no need to adjust anything within the initialization logic. 

Here is a concrete example:  
Imagine a new brain class is implemented ([`MLPBrain`](./reinforcement_learning/brains/_mlp.py)) that has an additional parameter (`hidden_dims`) to the ones defined by the [`IBrain`](./reinforcement_learning/brains/_base.py) interface, and the goal is for this parameter to be passed to the run-command.  
The class would simply be implemented with the respective additional parameter to be passed to the constructor.  
Then, it would simply be added as a new attribute of the [`Args`](./config/configuration/args/_args.py) class, registering it automatically as an argument that can be passed to the run-command, alongside a description of the parameter and a fitting default value.  
As the initialization of the brain, i.e., the call of the constructor of the new brain class, is wrapped with the `Args.call()` method within the [`AgentFactory`](./config/factory/_agent.py), the new parameter will automatically be extracted from the arguments and passed to the constructor, without the need to add it manually to the initialization like `MLPBrain(..., hidden_dims=hidden_dims)`.

New application variables can be simply added as attributes to the [`Args`](./config/configuration/args/_args.py) class, but to further group the arguments, sub-classes for additional agent arguments ([`AdditionalAgentArgs`](./config/configuration/args/)) and additional brain arguments ([`AdditionalBrainArgs`](./config/configuration/args/)) have been introduced, where respective new variables should be appended. 
 
<span style="color: grey; font-size: 11px;">(For more detailed information on the conversion of the [`Args`](./config/configuration/args/_args.py) class to command-variables, please refer to the [Configuration-Guide ▷](./config/README.md#configuration))</span>


<div style="text-align: right;">
  <a href="#toc">Back to top ↑</a>
</div>