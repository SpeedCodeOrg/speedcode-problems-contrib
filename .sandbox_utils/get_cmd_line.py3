

import pickle
print(pickle.load(open('/sandbox/job_info.pobj', 'rb'))['command_line_arguments'])

