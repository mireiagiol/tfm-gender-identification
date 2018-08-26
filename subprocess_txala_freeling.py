import subprocess
import json
from tree_dependencies_features import parse_json

def init_subprocess(tweet):
    cmd = "/usr/bin/analyze -f ca.cfg --flush  --output=json --outlv dep --dep txala --txala /usr/share/freeling/ca/dep_txala/dependences.dat"
    analyzer = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                close_fds=False)
    trees = analyzer.communicate(input=tweet.encode())[0].decode()
    json_data = json.loads(trees)
    return parse_json(json_data)
