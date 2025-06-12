#!/usr/bin/env python3
"""Simple dashboard collecting telemetry data."""
from __future__ import annotations

from flask import Flask, request, render_template_string

app = Flask(__name__)

telemetry_store: dict[str, dict] = {}


template = """
<!doctype html>
<title>Telemetry Dashboard</title>
<h1>Telemetry Dashboard</h1>
<table border="1" cellpadding="5" cellspacing="0">
  <tr>
    <th>Agent</th>
    <th>RAM %</th>
    <th>CPU %</th>
    <th>Users</th>
    <th>Root Usage %</th>
  </tr>
  {% for agent, data in telemetry.items() %}
  <tr>
    <td>{{ agent }}</td>
    <td>{{ '%.1f'|format(data.get('ram_percent', 0)) }}</td>
    <td>{{ '%.1f'|format(data.get('cpu_percent', 0)) }}</td>
    <td>{{ data.get('users', 0) }}</td>
    <td>{{ '%.1f'|format(data.get('root_usage_percent', 0)) }}</td>
  </tr>
  {% endfor %}
</table>
"""


@app.post('/telemetry')
def telemetry() -> str:
    data = request.get_json(force=True)
    agent = data.get('agent_id', 'unknown')
    telemetry_store[agent] = data
    return 'ok'


@app.get('/')
def index() -> str:
    return render_template_string(template, telemetry=telemetry_store)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

