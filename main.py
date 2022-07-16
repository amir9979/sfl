from sfl.Diagnoser.diagnoserUtils import write_json_planning_file, read_json_planning_instance, read_json_planning_file, readPlanningFile
from sfl.Diagnoser.Experiment_Data import Experiment_Data
from sfl.Diagnoser.Diagnosis_Results import Diagnosis_Results

ei = readPlanningFile(r"C:\Users\User\Downloads\SFL bug - why 16.txt")
ei.diagnose()
ei.diagnoses
ei = read_json_planning_file(r"C:\Users\User\Downloads\test_matrix1")
ei.diagnose()
print(Diagnosis_Results(ei.diagnoses, ei.initial_tests, ei.error, ei.pool, ei.get_id_bugs()).metrics)

import os

for root, dirs, files in os.walk(r"C:\Users\User\Downloads\projets_data\projets_data", topdown = False):
   for name in files:
      try:
         ei = read_json_planning_file(os.path.join(root, name))
         ei.diagnose()
         p = Diagnosis_Results(ei.diagnoses, ei.initial_tests, ei.error, ei.pool, ei.get_id_bugs()).precision
         if p< 0.1:
            raise Exception('del')
         print(os.path.join(root, name), p)
      except:
         os.remove(os.path.join(root, name))
