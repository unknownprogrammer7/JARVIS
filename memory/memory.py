class KnowledgeBase:
    def __init__(self):
        self.data = {}

    def add_data(self, key, value):
        self.data[key] = value

    def get_data(self, key):
        return self.data.get(key, None)


class MemoryManager:
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base

    def save_memory(self, key, value):
        self.knowledge_base.add_data(key, value)

    def retrieve_memory(self, key):
        return self.knowledge_base.get_data(key)