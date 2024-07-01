#!/bin/env python3
import os
import sys
import re
import argparse
import shutil
from pathlib import Path

# Constants
CONFIG_DIR = Path(os.path.expanduser("~/.config/bbReportFormatter"))
CURRENT_REPORT_FILE = CONFIG_DIR / "current_report"

REQUEST_REGEX = re.compile(r"^\w?GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS|TRACE|CONNECT")
RESPONSE_REGEX = re.compile(r"^\w?HTTP/[01]\.[0-9]")

def get_current_report_dir():
    if CURRENT_REPORT_FILE.exists():
        with open(CURRENT_REPORT_FILE, 'r') as f:
            report_id = f.read().strip()
    else:
        report_id = str(len(list(CONFIG_DIR.iterdir())))
        with open(CURRENT_REPORT_FILE, 'w') as f:
            f.write(report_id)
    
    report_dir = CONFIG_DIR / f"Report{report_id}"
    report_dir.mkdir(parents=True, exist_ok=True)
    return report_dir

def create_new_report_dir():
    if CURRENT_REPORT_FILE.exists():
        report_id = len(list(CONFIG_DIR.iterdir())) - 1
    else:
        report_id = len(list(CONFIG_DIR.iterdir()))
    report_dir = CONFIG_DIR / f"Report{report_id}"
    report_dir.mkdir(parents=True, exist_ok=True)
    with open(CURRENT_REPORT_FILE, 'w') as f:
        f.write(str(report_id))
    return report_dir

def clear_report():
    if CURRENT_REPORT_FILE.exists():
        report_id = len(list(CONFIG_DIR.iterdir())) - 2
    else:
        report_id = len(list(CONFIG_DIR.iterdir())) - 1
    report_dir = CONFIG_DIR / f"Report{report_id}"
    shutil.rmtree(str(report_dir))
    return 


def store_data(report_dir, entity, index, data):
    file_path = report_dir / f"{entity}{index}"
    with open(file_path, 'w') as f:
        f.write(data)

def load_report(report_dir):
    report = {}
    for file in report_dir.iterdir():
        entity, index = re.match(r"(\w+)(\d+)", file.name).groups()
        with open(file, 'r') as f:
            content = f.read()
        if entity not in report:
            report[entity] = {}
        report[entity][index] = content
    return report

def print_report(report):
    for index in map(str, range(1,50)):
        for entity in ['request', 'response', 'comment']:
            if entity in report:
                if str(index) in report[entity].keys():
                    print(f"{entity.capitalize()} {index}:")
                    print("```")
                    print(report[entity][index])
                    print("```")

def main():
    parser = argparse.ArgumentParser(description="Bug Bounty Report Formatter")
    parser.add_argument('--req', type=int, help='Specify request number')
    parser.add_argument('--resp', type=int, help='Specify response number')
    parser.add_argument('--comment', type=int, help='Specify comment number')
    parser.add_argument('--report', type=int, help='Specify report number to work with')
    parser.add_argument('--clear', action='store_true', help='Clear current report.')
    parser.add_argument('--print-report', action='store_true', help='Print the current report')
    parser.add_argument('--print-report-preview', action='store_true', help='Print the current report')
    args = parser.parse_args()

    if args.clear:
        clear_report()
        return

    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if args.report is not None:
        report_dir = CONFIG_DIR / f"Report{args.report}"
        if not report_dir.exists():
            print(f"Report {args.report} does not exist.")
            return
        with open(CURRENT_REPORT_FILE, 'w') as f:
            f.write(str(args.report))
    else:
        report_dir = get_current_report_dir()
    
    if args.print_report or args.print_report_preview:
        report = load_report(report_dir)
        print_report(report)
        if not args.print_report_preview:
            create_new_report_dir()
        return

    data = sys.stdin.read().strip()
    
    if args.req:
        store_data(report_dir, 'request', args.req, data)
    elif args.resp:
        store_data(report_dir, 'response', args.resp, data)
    elif args.comment:
        store_data(report_dir, 'comment', args.comment, data)
    else:
        if REQUEST_REGEX.match(data):
            index = len([f for f in report_dir.iterdir() if f.name.startswith('request')]) + 1
            store_data(report_dir, 'request', index, data)
        elif RESPONSE_REGEX.match(data):
            index = len([f for f in report_dir.iterdir() if f.name.startswith('response')]) + 1
            store_data(report_dir, 'response', index, data)
        else:
            index = len([f for f in report_dir.iterdir() if f.name.startswith('comment')]) + 1
            store_data(report_dir, 'comment', index, data)

if __name__ == "__main__":
    main()
