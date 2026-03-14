#!/usr/bin/env python3
"""Hello world example job. Prints JSON output to stdout."""
import json
from datetime import datetime

print(json.dumps({
    "message": "Hello from job runner!",
    "timestamp": datetime.now().isoformat(),
}))
