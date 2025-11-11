"""
Script completo per analizzare i log .txt e categorizzare i risultati
Legge direttamente dai file .txt nella directory
"""

import re
from pathlib import Path
import json

# ============================================================================
# CATEGORIZZAZIONE DEI 40 TEST (IN ORDINE)
# ============================================================================

CATEGORIES = {
    'Tracing': list(range(0, 8)),        # Test 0-7
    'Syscalls': list(range(8, 16)),      # Test 8-15
    'Networking': list(range(16, 24)),   # Test 16-23
    'Filesystem': list(range(24, 32)),   # Test 24-31
    'Advanced': list(range(32, 40))      # Test 32-39
}

# ============================================================================
# FUNZIONE PER PARSARE UN SINGOLO FILE LOG
# ============================================================================

def parse_single_log(filepath):
    """
    Parsa un singolo file .txt e estrae i risultati per test
    
    Returns:
        dict: {
            'model_name': str,
            'test_results': {test_num: success (True/False)}
        }
    """
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Estrai nome modello dal filename
    model_name = Path(filepath).stem.replace('few_shot_3trails_and_smt-', '')
    
    # Split per test case
    test_cases = content.split('Running test case')
    
    test_results = {}
    
    for test_block in test_cases[1:]:  # Skip il primo che è vuoto
        
        # Estrai numero test case
        test_num_match = re.search(r'^\s*(\d+):', test_block)
        if not test_num_match:
            continue
        
        test_num = int(test_num_match.group(1))
        
        # Trova tutti i returncode
        returncode_matches = re.findall(r'"returncode":\s*(\d+)', test_block)
        
        if not returncode_matches:
            continue
        
        attempts = [int(rc) for rc in returncode_matches]
        
        # Determina se c'è stato almeno un successo
        success = any(rc == 0 for rc in attempts)
        
        test_results[test_num] = success
    
    return {
        'model_name': model_name,
        'test_results': test_results
    }

# ============================================================================
# FUNZIONE PER ANALIZZARE TUTTI I LOG
# ============================================================================

def analyze_all_logs(directory):
    """
    Analizza tutti i file .txt nella directory
    
    Returns:
        dict: {model_name: {category: {successes, total, rate}}}
    """
    
    log_dir = Path(directory)
    
    # Trova tutti i file .txt rilevanti
    log_files = list(log_dir.glob('few_shot_3trails_and_smt-*.txt'))
    
    if not log_files:
        print(f"❌ No log files found in: {directory}")
        print("   Looking for files matching: few_shot_3trails_and_smt-*.txt")
        return {}
    
    print(f"📁 Found {len(log_files)} log files:")
    for f in sorted(log_files):
        print(f"   • {f.name}")
    print()
    
    all_results = {}
    
    for log_file in log_files:
        print(f"📄 Processing: {log_file.name}...", end=' ')
        
        parsed = parse_single_log(log_file)
        model_name = parsed['model_name']
        test_results = parsed['test_results']
        
        # Calcola performance per categoria
        category_results = {}
        
        for category, test_indices in CATEGORIES.items():
            successes = 0
            total = len(test_indices)
            
            for test_num in test_indices:
                if test_num in test_results and test_results[test_num]:
                    successes += 1
            
            success_rate = (successes / total * 100) if total > 0 else 0
            
            category_results[category] = {
                'successes': successes,
                'total': total,
                'rate': success_rate
            }
        
        all_results[model_name] = category_results
        
        # Calcola successo totale
        total_success = sum(1 for v in test_results.values() if v)
        print(f"✓ ({total_success}/40 total)")
    
    print()
    return all_results

# ============================================================================
# FUNZIONE PER STAMPARE RISULTATI
# ============================================================================

def print_category_results(results):
    """Stampa i risultati in formato tabella"""
    
    print("\n" + "="*100)
    print("SUCCESS RATE PER CATEGORIA")
    print("="*100 + "\n")
    
    # Header
    print(f"{'Model':<30}", end='')
    for cat in CATEGORIES.keys():
        print(f"{cat:>15}", end='')
    print()
    print("-" * 100)
    
    # Ordine modelli
    model_order = [
        'codellama7b', 
        'codellama:13b', 
        'codellama:70b', 
        'deepseek-coder-v2:16b', 
        'deepseek-coder-v2:236b'
    ]
    
    for model_key in model_order:
        if model_key not in results:
            continue
        
        model_data = results[model_key]
        print(f"{model_key:<30}", end='')
        
        for cat in CATEGORIES.keys():
            cat_data = model_data[cat]
            rate = cat_data['rate']
            succ = cat_data['successes']
            tot = cat_data['total']
            
            print(f"{rate:>7.1f}% ({succ}/{tot})", end='  ')
        print()
    
    print("\n")

# ============================================================================
# FUNZIONE PER GENERARE LATEX TABLE
# ============================================================================

def generate_latex_table(results):
    """Genera codice LaTeX per tabella riassuntiva"""
    
    print("\n" + "="*100)
    print("LATEX TABLE CODE")
    print("="*100 + "\n")
    
    print(r"\begin{table}[h]")
    print(r"\centering")
    print(r"\caption{Success rate per categoria di test}")
    print(r"\label{tab:category_performance}")
    print(r"\begin{tabular}{|l|c|c|c|c|c|}")
    print(r"\hline")
    print(r"\textbf{Model} & \textbf{Tracing} & \textbf{Syscalls} & \textbf{Network} & \textbf{Filesystem} & \textbf{Advanced} \\")
    print(r"\hline")
    
    model_order = [
        'codellama7b', 
        'codellama:13b', 
        'codellama:70b', 
        'deepseek-coder-v2:16b', 
        'deepseek-coder-v2:236b'
    ]
    
    model_names_latex = {
        'codellama7b': 'CodeLlama-7B',
        'codellama:13b': 'CodeLlama-13B',
        'codellama:70b': 'CodeLlama-70B',
        'deepseek-coder-v2:16b': 'DeepSeek-16B',
        'deepseek-coder-v2:236b': 'DeepSeek-236B'
    }
    
    for model_key in model_order:
        if model_key not in results:
            continue
        
        model_data = results[model_key]
        latex_name = model_names_latex[model_key]
        
        print(f"{latex_name}", end='')
        
        for cat in CATEGORIES.keys():
            cat_data = model_data[cat]
            rate = cat_data['rate']
            
            print(f" & {rate:.1f}\\%", end='')
        
        print(r" \\")
    
    print(r"\hline")
    print(r"\end{tabular}")
    print(r"\end{table}")
    print("\n")

# ============================================================================
# FUNZIONE PER SALVARE JSON
# ============================================================================

def save_category_results(results, output_file):
    """Salva i risultati in JSON"""
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✅ Results saved to: {output_file}")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import sys
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║       CATEGORY PERFORMANCE ANALYZER - Thesis Analysis        ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    print("\n📊 Test Categorization:")
    print("-" * 70)
    for cat, indices in CATEGORIES.items():
        print(f"   {cat:15s}: Tests {indices[0]:2d}-{indices[-1]:2d} ({len(indices)} tests)")
    print("-" * 70 + "\n")
    
    # Ottieni directory
    if len(sys.argv) > 1:
        log_dir = sys.argv[1]
    else:
        log_dir = input("📁 Enter directory with .txt logs: ").strip()
    
    if not log_dir:
        print("❌ No directory provided!")
        sys.exit(1)
    
    if not Path(log_dir).exists():
        print(f"❌ Directory not found: {log_dir}")
        sys.exit(1)
    
    # Analizza
    results = analyze_all_logs(log_dir)
    
    if not results:
        print("❌ No valid data found!")
        sys.exit(1)
    
    # Stampa risultati
    print_category_results(results)
    
    # Genera LaTeX
    generate_latex_table(results)
    
    # Salva JSON
    output_json = Path(log_dir) / 'category_analysis.json'
    save_category_results(results, output_json)
    
    print("\n" + "="*100)
    print("✅ ANALYSIS COMPLETE!")
    print("="*100)
    print("\n💡 Next step: Use this data to generate category performance charts")
    print(f"   Data saved in: {output_json}\n")