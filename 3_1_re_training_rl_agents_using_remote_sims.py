########### les imports ###############
import datetime
import os
import sys
import logging

import gym.spaces
import numpy as np
import tensorflow as tf

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# l'import de client.py et sac_agent_base.py
from client import Client
from sac_agent_base import SAC

# Create an App-level child logger
logger = logging.getLogger("TFRL-cookbook-ch7-training-with-sim-server")
# Set handler for this logger to handle messages
logger.addHandler(logging.StreamHandler())
# Set logging-level for this logger's handler
logger.setLevel(logging.DEBUG)

current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
train_log_dir = os.path.join("logs", "TFRL-Cookbook-Ch4-SAC", current_time)
summary_writer = tf.summary.create_file_writer(train_log_dir)


if __name__ == "__main__":

    ### Apres execution tradegym_http_server.py , nous allons creer 
    # un objet client de tradegym_http_client.py 
    sim_service_address = "http://127.0.0.1:6666"
    client = Client(sim_service_address)

    ### Nous creons l'id de l'instance client pour pouvoir l'utiliser 
    # apres pour mettre en place l'agent
    env_id = "StockTradingContinuousEnv-v0"
    instance_id = client.env_create(env_id)

    ### Mise en place de l'agent
    observation_space_info = client.env_observation_space_info(instance_id)
    observation_shape = observation_space_info.get("shape")
    action_space_info = client.env_action_space_info(instance_id)
    action_space = gym.spaces.Box(
        np.array(action_space_info.get("low")),
        np.array(action_space_info.get("high")),
        action_space_info.get("shape"),
    )
    agent = SAC(observation_shape, action_space)

    # charger les modeles
    agent.load_actor("sac_actor_final_episode.h5")
    agent.load_critic("sac_critic_final_episode.h5")
    ### Configure training
    # Nombre maximum d'episode
    max_epochs = 30000
    random_epochs = 0.6 * max_epochs
    # Nombre d'etape
    max_steps = 100
    # Frequence a la quelle on enreigistre le modele
    save_freq = 500
    reward = 0
    done = False

    done, use_random, episode, steps, epoch, episode_reward = (
        False,
        True,
        0,
        0,
        0,
        0,
    )
    # Initialisation de l'etat de l'agent. 
    # Ca nous donne l'observation initiale de l'espace
    cur_state = client.env_reset(instance_id)

    ### Commencer l'entrainement
    while epoch < max_epochs:
        if steps > max_steps:
            done = True

        if done:
            episode += 1
            logger.info(
                f"episode:{episode} cumulative_reward:{episode_reward} steps:{steps} epochs:{epoch}"
            )
            with summary_writer.as_default():
                tf.summary.scalar("Main/episode_reward", episode_reward, step=episode)
                tf.summary.scalar("Main/episode_steps", steps, step=episode)
            summary_writer.flush()

            done, cur_state, steps, episode_reward = (
                False,
                client.env_reset(instance_id),
                0,
                0,
            )
            if episode % save_freq == 0:
                agent.save_model(
                    f"sac_actor_episode{episode}_{env_id}.h5",
                    f"sac_critic_episode{episode}_{env_id}.h5",
                )

        if epoch > random_epochs:
            use_random = False
        #print(f"le contenu de cur_state:{cur_state}")
        action = agent.act(np.array(cur_state), use_random=use_random)
        next_state, reward, done, _ = client.env_step(
            instance_id, action.numpy().tolist()
        )
        #print(f"le contenu de action:{action} dans 3")
        agent.train(np.array(cur_state), action, reward, np.array(next_state), done)

        cur_state = next_state
        episode_reward += reward
        steps += 1
        epoch += 1

        # Update Tensorboard with Agent's training status
        agent.log_status(summary_writer, epoch, reward)
        summary_writer.flush()

    agent.save_model(
        f"sac_actor_final_episode_{env_id}.h5", f"sac_critic_final_episode_{env_id}.h5"
    )
