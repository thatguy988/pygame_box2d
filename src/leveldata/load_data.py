from leveldata.level_1 import level_1_data
from leveldata.level_2 import level_2_data

def load_level_data(level_id):
    if level_id in level_1_data:
        return level_1_data[level_id].leveldata
    elif level_id in level_2_data:
        return level_2_data[level_id].leveldata
    else:
        return None  # Return None for unknown level IDs

def get_node_id(level_id, direction):
    # Return the node ID of the connected node in the specified direction
    if level_id in level_1_data:
        if direction == "up":
            return level_1_data[level_id].connected_nodes[0]
        elif direction == "right":
            return level_1_data[level_id].connected_nodes[1]
        elif direction == "down":
            return level_1_data[level_id].connected_nodes[2]
        elif direction == "left":
            return level_1_data[level_id].connected_nodes[3]
    elif level_id in level_2_data:
        if direction == "up":
            return level_2_data[level_id].connected_nodes[0]
        elif direction == "right":
            return level_2_data[level_id].connected_nodes[1]
        elif direction == "down":
            return level_2_data[level_id].connected_nodes[2]
        elif direction == "left":
            return level_2_data[level_id].connected_nodes[3]
    return None
