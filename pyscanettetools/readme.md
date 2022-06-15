# python-scanette-tools
## fakegenerator
### generation.py
Allows you to generate a big scanette dataset in small amount of time

    from ScannetteGenerator import ScannetteGenerator
    g=ScannetteGenerator(number_of_sessions=150) #choose the number of session to generate
    g.balanced_dataset() #if you need to generate a dataset with is not unbalanced with regards to the distribution of the various scenario
    g.create_raw_dataset() #create a dataset without parameters
    g.export_dataset(path='../csv/fake_generation_150.csv') #export the dataset with parameters and a standard csv format
 ## replay
 ### samplequality.py
 Every function from this module takes as input an abstract traceset whose format is list_of_list or a GROUPED agilkia.Traceset object.
 For instance :

    list_of_traces=[['debloquer_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'transmission_0', 'abandon_?', 'payer_1'],['ajouter_0']]
Each action or event should be encoded in this fashion *action+separative_token+return_code*
 
 #### executability
 Take as input an abstract traceset and return the executability of the traceset : How many traces are well formed and can be executed as successful tests on the scanette code.
####  coverage
 Take as input an abstract traceset and print a coverage report of the traces executed as tests on the scanette code
 

#### examples
With a list_of_traces :

    traceset_grouped=[['debloquer_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'transmission_0', 'abandon_?', 'payer_1'],['ajouter_0']]  
	 print(executability(traceset_grouped))

With a abstract agilkia traceset  

    from utils_example import read_traces_csv  
       from pathlib import Path  
       traceset = read_traces_csv(Path("../csv/1026-steps.csv"))  
       traceset2 = traceset.with_traces_grouped_by("sessionID", property=True)  
       print(executability(traceset2))  
       coverage(traceset2)
  
## src
Sources of the scanette code inspired by Java Frederic Dadeau
https://github.com/PHILAE-PROJECT/scanette
You can find a javascript implementation as well :
https://github.com/fdadeau/scanette
## test
Human-written test based on the original implementation


