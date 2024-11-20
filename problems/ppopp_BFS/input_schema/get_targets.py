import json

data = json.loads(open("CONFIG.json").read())


targets = data['default_run_targets']


targets = [x+'.json' for x in targets]
print(",".join(targets), end='')
