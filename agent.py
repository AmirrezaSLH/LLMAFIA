class Agent:
    def __init__(self, role, name):
        self.role = role
        self.name = name
        self.personal_history = []
        self.is_alive = True
    
    def get_role(self):
        return self.role
    
    def get_name(self):
        return self.name
    
    def get_context(self):
        return self.personal_history

    def update_history(self, event):
        self.personal_history.append(event)
    
    def get_status(self):
        return self.is_alive
    
    def set_status(self, status):
        self.is_alive = status