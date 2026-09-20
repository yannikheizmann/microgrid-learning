▷ [**Usage-Guide**](../../../README.md#usage) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
☐ [**Structure-Guide**](../README.md#structure) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
⧉ [**Extension-Guide**](../README.md#extension) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
⚙ [**Configuration-Guide**](#configuration) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
❖ [**Pattern-Guide**](#patterns) 
 
---


<a id="toc"></a>

# Table of Contents

- [**Applied Patterns**](#patterns)
  - [Registry](#patterns.registry)
  - [Factory](#patterns.factory)  
   
<br>

- [**Configuration**](#configuration)
  - [Static](#configuration.static)
  - [Options](#configuration.options)
  - [Microgrid](#configuration.microgrid)
  - [Application Variables](#configuration.args)

<br>
<br>

<a id="patterns"></a>

# **❖ Applied Patterns**   
To keep the framework not only as easy to extend, but also as easy to instantiate and configure as possible when running the application, two key software-architectural patterns have been applied. The concept of those, as well as the idea behind their usage will be explained in the following.

> # **TL;DR**   
> Two core software-architectural patterns have been applied to ensure easy extendability and configuration of the application. 
>
> - Registry Pattern   
>   The Registry Pattern generally provides easy access to objects throughout the whole code and is applied to enable the interchanging of components from the run-command
>
> - Factory Pattern   
>   The Factory Pattern is generally used to separate the initialization logic of components from the core component logic and is applied to keep implementations of components free from complex initialization logic based on different configurations   
> 

<a id="patterns.registry"></a>

## **Registry [>](./registry/)**  
The first pattern used is the [Registry-Pattern](https://www.geeksforgeeks.org/registry-pattern/), a pattern generally used to simplify the access to objects or instances throughout the whole application.      


The motivation to apply this pattern was to keep the configuration as simple as possible and allow the user to specify which components (with "components" referring to the key interchangeable parts of this framework that will be mentioned later) to use within the run-command. To not having to keep a dictionary updated that maps some string to be passed by the user to the respective class to be instantiated, the Registry-Pattern has been applied for the respective components to be registered automatically on definition and made accessible via the name of their respective class.   

The following core components are connected to the Registry-Pattern:   
- Agent [>](../reinforcement_learning/agents/)
- Brain [>](../reinforcement_learning/brains/)
- Reward [>](../environment/reward/)
- MicrogridFactory [>](./factory/)

This means, each of the respective interfaces ([`IAgent`](../reinforcement_learning/agents/_base.py), [`IBrain`](../reinforcement_learning/brains/_base.py), [`IReward`](../environment/reward/_base.py), [`IMicrogridFactory`](./factory/_base.py)) inherit from the [`RegistryMeta`](./registry/_meta.py) metaclass which handles the registration of concrete implementations of those interfaces. The reason a metaclass has been used instead of a simple class to be inherited from or maybe even a class whose `register()` method is called manually, is to ensure the classes are registered on definition, not only on instantiation. The metaclass registers each concrete implementation under a certain key, corresponding to the name of the interface imlemented, within the [`Registry`](./registry/_registry.py) class. The user defines components to be used simply by the name of their respective class and the types are retrived from the registry.   
<span style="color: grey; font-size: 11px;">(For more detailed information on the definition of new components in context of the registry, please refer to the respective [Extension-Guide ▷](../README.md#extension))</span>   

<a id="patterns.factory"></a>

## **Factory [>](./factory/)**  
The second pattern applied is the [Factory-Pattern](https://www.geeksforgeeks.org/factory-method-for-designing-pattern/), a creational pattern generally used to take over the initialization of "products" by using factories.     


The motivation to use this pattern was to keep the entry point to this framework as well as the concrete components free of initialization logic and extract it into a separate class. It also provides a common package to change the initialization of the application without the need to go through all packages of the framework and change the initialization.    

The following factories are defined:   
- [`AgentFactory`](./factory/_agent.py/)
- [`EnvironmentFactory`](./factory/_environment.py/)
- [`IMicrogridFactory`](./factory/_base_.py/)
- Microgrid-Components-Factories [>](./factory/)

Both the [`AgentFactory`](./factory/_agent.py/) and [`EnvironmentFactory`](./factory/_environment.py/) are defined rather static, i.e., with no abstract factory interface that would allow to define other concrete factories for those two components. The reason for that is that the initialization of those components is statically defined by the respective classes and interfaces. Those components therefore get initialized in the same respective way each time, and different behavior or logic is rather defined by the components passed at initialization, e.g. the brain [▷](../README.md#structure.rl.brains) for the agent [▷](../README.md#structure.rl.agents) or the reward [▷](../README.md#structure.environment.reward) for the environment [▷](../README.md#structure.environment). The changing of the logic or behavior of those components is tehrefore handled by the registry pattern [▲](#patterns.registry), rather than the factory pattern.   

The factories related to the microgrid [▷](../README.md#structure.microgrid), however, are kept dyamically and open for definition of new factories to change the initialisation logic of the microgrid and it's components.   
For each respective component and the microgrid itself, a respective factory interface has been defined for concrete factories to implement. The basic factories for the components of the microgrid ([`BasicBatteryFactory`](./factory/components/_battery.py), [`BasicExternalGridFactory`](./factory/components/_external_grid.py), [`BasicResidentialLoadsFactory`](./factory/components/_residential_load.py), [`BasicDERFactory`](./factory/components/_distributed_energy_resources.py)) all use configuration values for the respective component defined in this [config file](./configuration/microgrid/_microgrid.py), which contains a config class for each component.   
<span style="color: grey; font-size: 11px;">(For more detailed information on the definition of new factories, please refer to the respective [Extension-Guide ▷](../README.md#extension),   
for more detailed information on the configuration file for the microgrid components, please refer to the respective [Configuration-Guide ▼](#configuration.microgrid))</span>   

<div style="text-align: right;">
  <a href="#toc">Back to top ↑</a>
</div>

<br>
<br>
<br>
<br>

<a id="configuration"></a>

# **⚙ Configuration [>](./configuration/)**  
This framework provides the broad functionality to apply different RL-Algorithms to the domain of energy management in a microgrid. Because of that, it also provides a number of variables to be set and configurations to be changed when running the application.   
A large effort has been made to bundle all configuration in dedicated files within a separate package, to prevetnt having to go into the source code to change the behavior of the application. These core configuration files will be presented in the following. 

> # **TL;DR**   
> The configuration package provides a centralized location for configuration files to alter the behavior of the application. They are split into the following sub-packages:
>
> - Static    
>   This package contains rather static configuration variables like paths or default values 
>
> - Options   
>   This package provides a list of options for interchangeable components of the system to be selected when running the application
>
> - Microgrid   
>   This package contains all configuration variables regarding the modelling and simulation of the microgrid
>
> - Args   
>   This package provides configuration of the arguments that can be passed directly as flags within the run-command
>
> This ensures an easy configuration of the whole application, also directly from within the run-command, without the need to change variables throughout the source code, and separates the implementation of the application logic and behavior from its configuration.

<a id="configuration.static"></a>

## **Static [>](./configuration/static/)**  
Within the static package of the configuration, there are a few files that specify some rather static variables, i.e. variables that are rather not used for frequent configuration of the application and are changed rather rarely.   
This includes [general information](./configuration/static/_info.py) about the project, [paths and formats](./configuration/static/_static.py) and [default values](./configuration/static/_defaults.py) used for the arguments of the run-command.   

<a id="configuration.options"></a>

## **Options [>](./configuration/options/)** 
The options package simply specifies some enums for the [options](./configuration/options/_options.py) for the interchangeable components of the application, that can be passed via the run-command. All implemented options get listed here for each component that provides multiple options.  
<span style="color: grey; font-size: 11px;">(For more detailed information on the definition of new options for components, please refer to the respective [Extension-Guide ▷](../README.md#extension))</span>   

<a id="configuration.microgrid"></a>

## **Microgrid [>](./configuration/microgrid/)** 
The microgrid package within the configuration provides all configuration variables regarding the simulation of the microgrid, i.e. for the [components of the microgrid](./configuration/microgrid/_microgrid.py) itself, as well as for the [microgrid environment](./configuration/microgrid/_microgrid_environment.py).  

The configuration variables are grouped in separate config classes for each component, containing descriptions for each variable to be set.   
The provided values represent the default values for the respective config class and may be overwritten by some factories, for example if values get retrieved from a separate API.   
Basic factories, however, solely use the configuration values defined in those files.    
<span style="color: grey; font-size: 11px;">(For more detailed information on the definition of new respective factories that may leverage other configuration values than the defaults specified, please refer to the respective [Extension-Guide ▷](../README.md#extension))</span>   

<a id="configuration.args"></a>

## **Application Variables [>](./configuration/args/)**
To keep the registration of arguments for the run-command as minimal and simple, especially for new arguments, the [`Args`](./configuration/args/_args.py) class has been implemented to represent all arguments that can be passed to the run-command as application variables, alongside a fitting description of each argument and a default value. 
Further than that, an [`ArgsParser`](./configuration/args/_parsing.py) class has been implemented, that handles the registration of all attributes of the [`Args`](./configuration/args/_args.py) class as valid command arguments, as well as the conversion of the `argparse.Namespace` retrieved from the variables passed to the run-command into an [`Args`](./configuration/args/_args.py) instance.   

This means, that there is simply a single class that represents the application variables to be set via the command, which simplifies the overview over all existing variables, as well as the addition of new ones.   
<span style="color: grey; font-size: 11px;">(For more detailed information on definition of new variables to be passed to the run-command, please refer to the respective [Extension-Guide ▷](../README.md#extension.config.variables))</span>  


<div style="text-align: right;">
  <a href="#toc">Back to top ↑</a>
</div>