from ...environment import MicrogridEnvironment
from ...reinforcement_learning.agents import IAgent
from ...reinforcement_learning.brains import IBrain
from ..registry import Registry
from ...config.configuration.args import Args


class AgentFactory:
    @classmethod
    def create(
        cls,
        environment: MicrogridEnvironment,
        args: Args,
    ) -> IAgent:
        BrainClass: type[IBrain] = Registry.get("IBrain", args.brain.value)
        input_dim = environment.get_observation_dim()
        output_dim = environment.get_action_dim()
        brain: IBrain = args.call(
            BrainClass,
            input_dim=input_dim,
            output_dim=output_dim,
            learning_rate=args.learning_rate,
        )

        AgentClass: type[IAgent] = Registry.get("IAgent", args.agent.value)
        agent: IAgent = args.call(
            AgentClass,
            environment=environment,
            brain=brain,
            batch_size=args.batch_size,
        )
        return agent
