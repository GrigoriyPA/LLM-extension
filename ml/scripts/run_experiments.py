from configs.experiments_list import EXPERIMENTS_LIST
import configs.experiments_list


for experiment in EXPERIMENTS_LIST:
    experiment.launch()
