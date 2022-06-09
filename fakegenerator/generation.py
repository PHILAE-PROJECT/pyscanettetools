import time
from ScannetteGenerator import ScannetteGenerator
b = time.time()
g = ScannetteGenerator(number_of_sessions=150)
g.balanced_dataset()
g.create_raw_dataset()
g.export_dataset(path='../csv/fake_generation_150.csv')
print(time.time() - b)