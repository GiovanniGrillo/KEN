import requests

def query_ollama(prompt, max_tokens=1000):
    """
    
    Args:
        prompt (str): Il prompt da inviare al modello
        max_tokens (int): Numero massimo di token nella risposta
        
    Returns:
        str: La risposta del modello, None se errore
    """
    model = "codellama:70b"
    
    bpftrace_prompt = f"""Generate a complete bpftrace program for: {prompt}

Requirements:
- Use proper bpftrace syntax
- Include BEGIN and END blocks
- Use correct tracepoints/kprobes (check with 'bpftrace -l')
- For interrupts use: tracepoint:irq:irq_handler_entry
- For processes use: tracepoint:sched:sched_process_fork
- For syscalls use: tracepoint:syscalls:sys_enter_*
- Include proper printf statements
- Make it a complete, runnable program

Write ONLY the bpftrace program (no explanations):"""

    payload = {
        "model": model,
        "prompt": bpftrace_prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "max_tokens": max_tokens
        }
    }

    try:
        response = requests.post("http://111.11.11.111:12345/api/generate", json=payload)

        if response.status_code == 200:
            result = response.json()
            return result.get("response", "")
        else:
            print(f"Ollama Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Ollama connection error: {e}")
        return None


def query_ollama_verifier(prompt, max_tokens=1000):
    """
    Query Ollama API con DeepSeek Coder V2 16B per il verifier (senza prompt hardcoded)
    
    Args:
        prompt (str): Il prompt da inviare al modello (raw, senza modifiche)
        max_tokens (int): Numero massimo di token nella risposta

    Returns:
        str: La risposta del modello, None se errore
    """
    model = "codellama:70b"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "max_tokens": max_tokens
        }
    }

    try:
        response = requests.post("http://1111.11.11.111:12345/api/generate", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "")
        else:
            print(f"Ollama Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Ollama connection error: {e}")
        return None