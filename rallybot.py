rallyjson = '{"OperationResult": {"_rallyAPIMajor": "2", "_rallyAPIMinor": "0", "Errors": [], "Warnings": [], "SecurityToken": "KWOEwL1wTHSesmkkRilyxbV4jwwfCEafl6IbkZiu9M"}}'

import json
parsed_json = json.loads(rallyjson)
print (parsed_json['SecurityToken'])

