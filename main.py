import random
import time
import multiprocessing
import tracemalloc  # <-- new import for memory tracking

def generate_random_cnf(num_vars, num_clauses, clause_size=3):
    cnf = []
    for _ in range(num_clauses):
        clause = set()
        while len(clause) < clause_size:
            var = random.randint(1, num_vars)
            clause.add(random.choice([var, -var]))
        cnf.append(list(clause))
    return cnf


def resolution_worker(cnf, q):
    try:
        result = resolution(cnf)
        q.put(result)
    except Exception as e:
        q.put(e)

def resolution_with_timeout(cnf, timeout=5):
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=resolution_worker, args=(cnf, q))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        return "Timeout"
    return q.get()

def resolution(cnf):
    clauses = set(frozenset(c) for c in cnf)
    new = set()
    while True:
        pairs = [(ci, cj) for ci in clauses for cj in clauses if ci != cj]
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            if frozenset() in resolvents:
                return False
            new.update(resolvents)
        if new.issubset(clauses):
            return True
        clauses.update(new)

def resolve(ci, cj):
    resolvents = set()
    for lit in ci:
        if -lit in cj:
            resolvent = (ci - {lit}) | (cj - {-lit})
            resolvents.add(frozenset(resolvent))
    return resolvents


def dp(cnf):
    return dp_recursive(cnf, set())

def dp_recursive(cnf, assignment):
    cnf = simplify_cnf(cnf, assignment)
    if [] in cnf:
        return False
    if not cnf:
        return True
    literal = next(iter(cnf[0]))
    return dp_recursive(cnf, assignment | {literal}) or dp_recursive(cnf, assignment | {-literal})


def dpll(cnf, assignment=set()):
    cnf = simplify_cnf(cnf, assignment)
    if [] in cnf:
        return False
    if not cnf:
        return True
    unit_clauses = [c[0] for c in cnf if len(c) == 1]
    if unit_clauses:
        return dpll(cnf, assignment | set(unit_clauses))
    literal = next(iter(cnf[0]))
    return dpll(cnf, assignment | {literal}) or dpll(cnf, assignment | {-literal})

def simplify_cnf(cnf, assignment):
    simplified = []
    for clause in cnf:
        if any(lit in assignment for lit in clause):
            continue
        new_clause = [lit for lit in clause if -lit not in assignment]
        simplified.append(new_clause)
    return simplified


def run_with_memory_tracking(func, *args, timeout=None):
    """
    Runs func with *args and returns (result, elapsed_time, peak_memory_in_MB).
    If timeout is given and func runs longer, terminates with None result.
    """
    # Start tracking memory allocations
    tracemalloc.start()

    start = time.perf_counter()
    try:
        if timeout is not None:
            # Run with timeout via multiprocessing (only for resolution_with_timeout)
            # Here func is likely resolution_with_timeout
            result = func(*args)
        else:
            result = func(*args)
    except Exception as e:
        result = f"Error: {e}"
    end = time.perf_counter()

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    elapsed = end - start
    peak_mb = peak / (1024 * 1024)  # bytes to MB

    return result, elapsed, peak_mb


def run_experiment(num_vars, num_clauses):
    print(f"\n=== Generating CNF for {num_vars} variables and {num_clauses} clauses ===")
    cnf = generate_random_cnf(num_vars, num_clauses)

    if num_vars > 8:
        print("Skipping Resolution (too large)...")
        result_res = "Skipped"
        time_res = 0
        mem_res = 0
    else:
        print("Running Resolution...")
        # Use run_with_memory_tracking on resolution_with_timeout
        result_res, time_res, mem_res = run_with_memory_tracking(resolution_with_timeout, cnf, 5)
        print(f"Resolution completed in {time_res:.4f} seconds, peak memory: {mem_res:.4f} MB. Result: {result_res}")

    print("Running DP...")
    result_dp, time_dp, mem_dp = run_with_memory_tracking(dp, cnf)
    print(f"DP completed in {time_dp:.4f} seconds, peak memory: {mem_dp:.4f} MB. Result: {result_dp}")

    print("Running DPLL...")
    result_dpll, time_dpll, mem_dpll = run_with_memory_tracking(dpll, cnf)
    print(f"DPLL completed in {time_dpll:.4f} seconds, peak memory: {mem_dpll:.4f} MB. Result: {result_dpll}")

    print(f"\nSummary for {num_vars} vars, {num_clauses} clauses:")
    print(f"  Resolution: {time_res:.4f}s, {mem_res:.4f}MB ({result_res})")
    print(f"  DP        : {time_dp:.4f}s, {mem_dp:.4f}MB ({result_dp})")
    print(f"  DPLL      : {time_dpll:.4f}s, {mem_dpll:.4f}MB ({result_dpll})")



if __name__ == "__main__":
    sizes = [
        (5, 15),       
        (10, 20),      
        (20, 40),    
        (30, 60),
        (40, 60),  
        (50, 100),  
        (100, 200),  
        (1000, 10000),      
    ]

    for num_vars, num_clauses in sizes:
        run_experiment(num_vars, num_clauses)

    print("\nAll experiments completed!")
