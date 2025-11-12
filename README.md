# Kgent: Kernel Extensions Large Language Model Agent

This repository contains the code and evaluation for the paper [Kgent: Kernel Extensions Large Language Model Agent](https://dl.acm.org/doi/10.1145/3672197.3673434).

---

## Thesis Extension: Local Deployment, Evaluation, and System Improvements

This repository has been extended as part of the **Bachelor’s thesis of Giovanni Grillo**, focused on the re-implementation and evaluation of Kgent in a fully local, open-source environment.  
The goal was to migrate the Kgent framework from a cloud-based setup to a **self-contained distributed infrastructure** capable of running large language models (LLMs) locally with GPU acceleration, ensuring data privacy, reproducibility, and zero-cost experimentation.

**Thesis PDF:** [Bachelor_Thesis_Grillo_Giovanni.pdf](./Bachelor_Thesis_Grillo_Giovanni.pdf)

### Overview of the Extension

This thesis builds upon the original Kgent system while preserving its logic and dataset structure.  
The following major enhancements and architectural modifications were introduced:

#### 1. Local LLM Inference with Ollama
Replaced OpenAI-based API calls with a **local REST interface** powered by [Ollama](https://ollama.ai), enabling the execution of open-source models directly on GPU hardware.  
The baseline model was **CodeLlama-7B-Instruct**, later extended to a multi-model configuration supporting:
- CodeLlama (7B–70B)
- DeepSeek-Coder (6.7B–236B)
- WizardCoder (13B)

This setup provides full local control, eliminates dependency on proprietary APIs, and allows rapid switching between models through configuration changes only.

#### 2. Distributed Architecture
Implemented a **two-machine setup** within the HPC4AI infrastructure:
- **alpha-v100** – Ubuntu 24.04 LTS, NVIDIA Tesla V100; dedicated to model inference via Ollama.  
- **alpha-relay** – Ubuntu 22.04 LTS; used for compilation and testing of generated eBPF programs, with limited `sudo` privileges.

The machines communicate via HTTP POST requests handled by a custom Python module, `ollama_utils.py`, which encapsulates prompt management, response handling, and error recovery.

#### 3. Embedding Migration
Replaced `OpenAIEmbeddings` with `HuggingFaceEmbeddings` using the `sentence-transformers/all-MiniLM-L6-v2` model.  
This required a complete re-embedding of the FAISS vector database, resulting in a fully open, reproducible, and offline semantic retrieval system.

#### 4. Compatibility and Reliability Fixes
- Downgraded **bpftrace** to version 0.16.0 to restore compatibility with legacy syntax (e.g., `BEGIN` triggers).  
- Improved parsing and code-extraction logic in `chain.py` to handle verbose or Markdown-formatted outputs.  
- Unified inference parameters (`temperature`, `max_tokens`) across modules for consistent, deterministic generation.  
- Adjusted retry logic in `verifier.py` to correctly distinguish between environmental and syntactic errors.

#### 5. Experimental Evaluation
A benchmark campaign was conducted on **40 test cases** covering five eBPF categories: Tracing, Syscalls, Networking, Filesystem, and Advanced.  
All experiments were executed locally using the distributed setup described above.

| Model                          | Parameters | Success Rate | Notes                      |
|--------------------------------|------------|--------------|----------------------------|
| DeepSeek-Coder-V2-236B         | 236B       | **92.5%**    | Highest overall accuracy   |
| CodeLlama-13B / DeepSeek-16B   | 13–16B     | ~55–57%      | Balanced cost–performance  |
| CodeLlama-7B                   | 7B         | 47.5%        | Strong retry dependence    |

Smaller models benefited significantly from the automatic retry mechanism, while larger models produced correct code on the first attempt in most cases.

#### 6. Summary
This extension validates that **open-source local models** can effectively replace proprietary LLMs for eBPF program generation and verification.  
The local setup ensures:
- Zero API cost  
- Full control over computation and data  
- Reproducibility and independence from external services

---

## Key Idea

Kgent leverages recent advances in large language models (LLMs) to simplify the creation of eBPF (extended Berkeley Packet Filter) programs, which are traditionally challenging due to the deep knowledge of OS internals and the constraints enforced by the eBPF verifier.

### Highlights

- **Natural language to eBPF** – Translates user prompts in natural language into eBPF programs.  
- **Combination of techniques** – Employs program comprehension, symbolic execution, and feedback loops to ensure semantic equivalence between the generated code and the user’s intent.  
- **Evaluation** – Demonstrates a 2.67× improvement over GPT-4 in producing correct eBPF programs, with high accuracy and minimal false positives.

---

## Potential Use Cases

Kgent and its extended local implementation can be applied in various contexts:

1. **System Administrators** – Simplifies the creation and maintenance of eBPF programs without deep kernel expertise.  
2. **DevOps Engineers** – Assists in developing kernel extensions for monitoring and tracing, improving observability and performance.  
3. **Patch Makers** – Enables the generation of kernel patches from natural-language descriptions of issues or fixes.  
4. **Kernel Developers** – Accelerates prototyping and validation of kernel extensions.  
5. **Education and Training** – Serves as a learning tool for students and new developers.  
6. **Research and Experimentation** – Provides a reproducible, fully local platform for testing new eBPF applications.  
7. **Network Tools Development** – Simplifies the creation of custom network performance and security tools.

---

## Links

- eBPF ’24 paper: [Kgent: Kernel Extensions Large Language Model Agent](https://dl.acm.org/doi/10.1145/3672197.3673434)  
- arXiv version: [KEN: Kernel Extensions using Natural Language](https://arxiv.org/abs/2312.05531)  
- Simplified tools: [GPTtrace](https://github.com/eunomia-bpf/GPTtrace) and [GPTtrace Web Demo](https://github.com/eunomia-bpf/GPTtrace-web)

---

## Contents

- [dataset](dataset): datasets used in Kgent.  
  - [dataset/libbpf/output.json](dataset/libbpf/output.json): libbpf examples database with descriptions.  
  - [dataset/bpftrace/output.json](dataset/bpftrace/output.json): bpftrace examples database with descriptions.  
  - [dataset/spec/helper_spec.json](dataset/spec/helper_spec.json): Z3 specs for helper functions.  
  - [dataset/spec/kprobe_spec.json](dataset/spec/kprobe_spec.json): Z3 specs for kprobe functions.  
- [evaluation](evaluation): evaluation code and experiments.

---

## Citation

```bibtex
@inproceedings{10.1145/3672197.3673434,
  author    = {Zheng, Yusheng and Yang, Yiwei and Chen, Maolin and Quinn, Andrew},
  title     = {Kgent: Kernel Extensions Large Language Model Agent},
  year      = {2024},
  isbn      = {9798400707124},
  publisher = {Association for Computing Machinery},
  address   = {New York, NY, USA},
  url       = {https://doi.org/10.1145/3672197.3673434},
  doi       = {10.1145/3672197.3673434},
  booktitle = {Proceedings of the ACM SIGCOMM 2024 Workshop on eBPF and Kernel Extensions},
  pages     = {30--36},
  numpages  = {7},
  keywords  = {Large Language Model, Symbolic Execution, eBPF},
  location  = {Sydney, NSW, Australia},
  series    = {eBPF '24}
}
```
