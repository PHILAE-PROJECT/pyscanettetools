import time
from .fakegenerator.ScannetteGenerator import ScannetteGenerator

def generation(path,number_of_sessions,balanced=True):
    g = ScannetteGenerator(number_of_sessions=150)
    if balanced:
        g.balanced_dataset()
    g.create_raw_dataset()
    g.export_dataset(path=path)
if '__name__'=='__main__':
    generation(path='csv/fake_generation_150.csv',number_of_session=150,balanced=True)