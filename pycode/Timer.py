import time
class Timer:
    def __init__(self):
      self.start = time.time()
    
    def stop(self, round=15):
       return f"{time.time() - self.start:.{round}f}"