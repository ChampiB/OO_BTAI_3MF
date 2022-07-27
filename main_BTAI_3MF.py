import time
from env.ArenaEnv import ArenaEnv
from agent.inference.TemporalSliceBuilder import TemporalSliceBuilder
from env.wrapper.dSpritesPreProcessingWrapper import dSpritesPreProcessingWrapper
from agent.BTAI_3MF import BTAI_3MF
import torch


def main():
    """
    A simple example of how to use the BTAI_3MF framework.
    :return: nothing.
    """

    # Create the environment.
    env = ArenaEnv({})
    # TODO env = dSpritesPreProcessingWrapper(env)

    # Define the parameters of the generative model.
    # TODO a = env.a()
    # TODO b = env.b()
    # TODO c = env.c()
    # TODO d = env.d(uniform=True)

    # Define the temporal slice structure.
    # TODO ts = TemporalSliceBuilder("A_0", env.n_actions) \
    # TODO     .add_state("S_pos_x", d["S_pos_x"]) \
    # TODO     .add_state("S_pos_y", d["S_pos_y"]) \
    # TODO     .add_state("S_shape", d["S_shape"]) \
    # TODO     .add_state("S_scale", d["S_scale"]) \
    # TODO     .add_state("S_orientation", d["S_orientation"]) \
    # TODO     .add_observation("O_pos_x", a["O_pos_x"], ["S_pos_x"]) \
    # TODO     .add_observation("O_pos_y", a["O_pos_y"], ["S_pos_y"]) \
    # TODO     .add_observation("O_shape", a["O_shape"], ["S_shape"]) \
    # TODO     .add_observation("O_scale", a["O_scale"], ["S_scale"]) \
    # TODO     .add_observation("O_orientation", a["O_orientation"], ["S_orientation"]) \
    # TODO     .add_transition("S_pos_x", b["S_pos_x"], ["S_pos_x", "A_0"]) \
    # TODO     .add_transition("S_pos_y", b["S_pos_y"], ["S_pos_y", "A_0"]) \
    # TODO     .add_transition("S_shape", b["S_shape"], ["S_shape"]) \
    # TODO     .add_transition("S_scale", b["S_scale"], ["S_scale"]) \
    # TODO     .add_transition("S_orientation", b["S_orientation"], ["S_orientation"]) \
    # TODO     .add_preference(["O_pos_x", "O_pos_y", "O_shape"], c["O_shape_pos_x_y"]) \
    # TODO     .build()

    # Create the agent.
    # TODO agent = BTAI_3MF(ts, max_planning_steps=150, exp_const=2.4)

    # Implement the action-perception cycles.
    n_trials = 100
    # TODO score = 0
    # TODO ex_times_s = torch.zeros([n_trials])
    for i in range(n_trials):
        obs = env.reset(new_map=True)
        env.render()
        # TODO agent.reset(obs)
        # TODO ex_times_s[i] = time.time()
        while not env.done():
            # TODO action = agent.step()
            mage_action = int(input("Mage action:"))
            warrior_action = int(input("Warrior action:"))
            obs = env.execute({
                ("mage", 0): mage_action,
                ("warrior", 0): warrior_action,
            })
            time.sleep(1)
            env.render()
            # TODO agent.update(action, obs)
        # TODO ex_times_s[i] = time.time() - ex_times_s[i]
        # TODO score += env.get_reward()

    # Display the performance of the agent.
    # TODO print("Percentage of task solved: {}".format((score + n_trials) / (2 * n_trials)))
    # TODO print("Execution time (sec): {} +/- {}".format(ex_times_s.mean().item(), ex_times_s.std(dim=0).item()))


if __name__ == '__main__':
    main()
