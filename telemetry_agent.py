#!/usr/bin/env python3
"""Telemetry agent posting system metrics to a server."""
from __future__ import annotations

import argparse
import os
import time

import psutil
import requests


def collect_metrics() -> dict:
    """Collect RAM, CPU, user count and root storage usage."""
    mem = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=1)
    users = len(psutil.users())
    disk = psutil.disk_usage('/')
    return {
        'ram_percent': mem.percent,
        'cpu_percent': cpu,
        'users': users,
        'root_usage_percent': disk.percent,
    }


def post_metrics(url: str, agent_id: str) -> None:
    """Collect metrics and POST them to *url* with *agent_id*."""
    payload = {'agent_id': agent_id}
    payload.update(collect_metrics())
    try:
        requests.post(url, json=payload, timeout=5)
    except requests.RequestException as exc:
        print(f"Failed to post telemetry: {exc}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Send telemetry metrics")
    parser.add_argument('--server', default='http://localhost:5000/telemetry',
                        help='Telemetry server URL')
    parser.add_argument('--agent-id', default=os.uname().nodename,
                        help='Unique agent identifier')
    parser.add_argument('--interval', type=int, default=60,
                        help='Seconds between posts')
    args = parser.parse_args()

    while True:
        post_metrics(args.server, args.agent_id)
        time.sleep(args.interval)


if __name__ == '__main__':
    main()

