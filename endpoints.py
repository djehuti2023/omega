import os
import sys
from argparse import ArgumentParser

import gym.spaces
from flask import Flask, request
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sac_agent_runtime import SAC

parser = ArgumentParser(
    prog="TFRL-Cookbook-Ch7-Packaging-RL-Agents-For-Cloud-Deployments"
)

parser.add_argument("--agent", default="SAC", help="Name of Agent. Default=SAC")
parser.add_argument(
    "--host-ip",
    default="0.0.0.0",
    help="IP Address of the host server where Agent service is run. Default=127.0.0.1",
)
parser.add_argument(
    "--host-port",
    default="6666",
    help="Port on the host server to use for Agent service. Default=5555",
)
parser.add_argument(
    "--trained-models-dir",
    default="trained_models",
    help="Directory contained trained models. Default=trained_models",
)
parser.add_argument(
    "--config",
    default="runtime_config.json",
    help="Runtime config parameters for the Agent. Default=runtime_config.json",
)
parser.add_argument(
    "--observation-shape",
    default=(6, 11),
    help="Shape of observations. Default=(6, 11)",
)
parser.add_argument(
    "--action-space-low", default=[-1], help="Low value of action space. Default=[-1]"
)
parser.add_argument(
    "--action-space-high", default=[1], help="High value of action space. Default=[1]"
)
parser.add_argument(
    "--action-shape", default=(1,), help="Shape of actions. Default=(1,)"
)
parser.add_argument(
    "--model-version",
    default="final_episode",
    help="Trained model version. Default=final_episode",
)
args = parser.parse_args()


if __name__ == "__main__":
    if args.agent != "SAC":
        print(f"Unsupported Agent: {args.agent}. Using SAC Agent")
        args.agent = "SAC"
    # Set Agent's runtime configs
    observation_shape = args.observation_shape
    action_space = gym.spaces.Box(
        np.array(args.action_space_low),
        np.array(args.action_space_high),
        args.action_shape,
    )
    
    # La variable du nom de l'agent
    envd_m1 = "m1"
    envd_m5 = "m5"
    envd_m15 = "m15"

    
    # Creer une instance des agents
    agent_m1 = SAC(observation_shape, action_space)
    agent_m5 = SAC(observation_shape, action_space)
    agent_m15 = SAC(observation_shape, action_space)

    # Charger le modele entraine modele/cerveau
    model_version = args.model_version
    print(f"Chargement de l'agent avec une version de model entraine ")
    
    print(" ######################################## ")
    # m1
    print(" Les modeles M1 sont charges ")
    agent_m1.load_actor(
        os.path.join(args.trained_models_dir, f"sac_actor_{model_version}_{envd_m1}.h5")
    )
    agent_m1.load_critic(
        os.path.join(args.trained_models_dir, f"sac_critic_{model_version}_{envd_m1}.h5")
    )
    """ 
    # m5
    print(" Les modeles M5 sont charges ")
    agent_m5.load_actor(
        os.path.join(args.trained_models_dir, f"sac_actor_{model_version}_{envd_m5}.h5")
    )
    agent_m5.load_critic(
        os.path.join(args.trained_models_dir, f"sac_critic_{model_version}_{envd_m5}.h5")
    )

    # m15
    print(" Les modeles M15 sont charges ")
    agent_m15.load_actor(
        os.path.join(args.trained_models_dir, f"sac_actor_{model_version}_{envd_m15}.h5")
    )
    agent_m15.load_critic(
        os.path.join(args.trained_models_dir, f"sac_critic_{model_version}_{envd_m15}.h5")
    ) """
    print(" ######################################## ")
    print(" Les modeles sont charges ")

    # Setup Agent (http) service
    app = Flask(__name__)

    # les endpoints post de signaux M1, M5 et M15
    @app.route("/v1/act/m1", methods=["POST"])
    def get_action_m1():
        data = request.get_json()
        # print("data")
        # print(np.array(data.get("observation")))
        action = agent_m1.act(np.array(data.get("observation")), test=True)
        return {"action_de_M1": action.numpy().tolist()}
    """ 
    @app.route("/v1/act/m5", methods=["POST"])
    def get_action_m5():
        data = request.get_json()
        # print("data")
        # print(np.array(data.get("observation")))
        action = agent_m5.act(np.array(data.get("observation")), test=True)
        return {"action_de_M5": action.numpy().tolist()}
    
    @app.route("/v1/act/m15", methods=["POST"])
    def get_action_m15():
        data = request.get_json()
        # print("data")
        # print(np.array(data.get("observation")))
        action = agent_m15.act(np.array(data.get("observation")), test=True)
        return {"action_de_M15": action.numpy().tolist()} """
    # Launch/Run the Agent (http) service
    app.run(host=args.host_ip, port=args.host_port, debug=True)
