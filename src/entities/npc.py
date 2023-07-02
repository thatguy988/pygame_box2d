
class NPC:
    def __init__(self, x, y, width, height,dialogue):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dialogue = dialogue
        self.dialogue_index = 0  # Initialize the dialogue index

    def get_dialogue(self):
        return self.dialogue[self.dialogue_index]

    def next_dialogue(self):
        self.dialogue_index += 1
        if self.dialogue_index >= len(self.dialogue):
            self.dialogue_index = 0
    

        
    