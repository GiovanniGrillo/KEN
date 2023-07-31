# OpenCopilot: A LLM empowered eBPF info collection and codegen

- [ ] Stable Mapping from Natural Language to eBPF semantic
- [ ] Context Abstraction: thread isolation and information refinement 
- [ ] Can deal with prompt to do arbritrary jobs, like system data collection and scheduler, hardware control, etc.

## Usage and Setup 🛠

```console
$ python3 -m gpttrace -h
usage: GPTtrace [-h] [-c CMD_NAME QUERY] [-v] [-k OPENAI_API_KEY]
                input_string

Use ChatGPT to write eBPF programs (bpftrace, etc.)

positional arguments:
  input_string          Your question or request for a bpf program

options:
  -h, --help            show this help message and exit
  -c CMD_NAME QUERY, --cmd CMD_NAME QUERY
                        Use the bcc tool to complete the trace task
  -v, --verbose         Show more details
  -k OPENAI_API_KEY, --key OPENAI_API_KEY
                        Openai api key, see
                        `https://platform.openai.com/docs/quickstart/add-
                        your-api-key` or passed through `OPENAI_API_KEY`
```
