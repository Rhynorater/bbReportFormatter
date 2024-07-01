# bbReportFormatter

bbReportFormatter (bbrf) is a tool to be used with the `write_hackerone_report` [fabric](https://github.com/danielmiessler/fabric) pattern to format the report data and store various request/response/comments for consumption by the AI.

## Usage:
```bash
echo "GET /" | bbrf # Store a request
echo "HTTP/1.1 200 OK" | bbrf # Store a response
echo "This request is vulnerable to IDOR..." | bbrf # Store a comment
```

These will store the various items into their respective categories. Then

```bash
bbrf --print-report | fabric --sp write_hackerone_report
```
Will generate the AI-power bug bounty report.


## Installation
1. Clone the repo
2. Run `chmod +x install.sh; ./install.sh` and never move the project.

## Disclaimer

This is a work in progress! Please feel free to open issues or make PRs.
