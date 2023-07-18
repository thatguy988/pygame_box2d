from leveldata.level_1 import level_1_data
from leveldata.level_2 import level_2_data


level_data_dict = {
    1: level_1_data,
    2: level_1_data,
    3: level_1_data,
    4: level_1_data,
    5: level_2_data
    
}


def load_level_data(level_id):
    level_data = level_data_dict.get(level_id)
    if level_data is not None:
        return level_data[level_id].leveldata
    else:
        return None  # Return None for unknown level IDs


def get_node_id(level_id, direction):
    level_data = level_data_dict.get(level_id)
    if level_data is not None:
        index = {"up": 0, "right": 1, "down": 2, "left": 3}
        connected_nodes = level_data[level_id].connected_nodes
        return connected_nodes[index[direction]]
    return None
