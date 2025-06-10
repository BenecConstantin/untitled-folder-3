\documentclass[a4paper,12pt]{article}

\title{Comparative Study of Classical SAT Solvers: Resolution, Davis-Putnam, and DPLL}
\author{Costi Benec Constantin-Ștefan}
\date{\today}

\begin{document}

\maketitle

\begin{abstract}
This paper presents an experimental comparison of three classical SAT solvers: Resolution, Davis-Putnam (DP), and Davis-Putnam-Logemann-Loveland (DPLL). Implemented and evaluated on randomly generated CNF formulas of varying sizes on a MacBook Pro (2.6 GHz 6-Core Intel i7, Intel UHD Graphics 630, 16 GB DDR4 2667 MHz RAM), results show Resolution’s runtime grows exponentially, becoming impractical beyond the smallest instances. DP and DPLL perform efficiently on small and medium formulas, with DPLL generally faster and more memory efficient. Detailed timing and memory usage data are provided along with practical insights on their trade-offs.
\end{abstract}

\section{Introduction}

SAT (Boolean satisfiability) asks if a propositional CNF formula can be satisfied by some assignment of truth values. Despite NP-completeness, classical algorithms such as Resolution, DP, and DPLL are fundamental. This study implements these algorithms and empirically compares their performance.

\section{System Specifications}

Experiments were run on a MacBook Pro with:
\begin{itemize}
    \item CPU: 2.6 GHz 6-Core Intel i7
    \item GPU: Intel UHD Graphics 630 (1536 MB)
    \item RAM: 16 GB DDR4 at 2667 MHz
\end{itemize}

\section{Results Summary}

\begin{itemize}
    \item Resolution was only run on the smallest input (5 variables, 15 clauses), taking 1.85 seconds and 1.12 MB RAM, and skipped thereafter due to exponential runtime and memory usage.
    \item DP performs well on small to medium inputs but runtime grows significantly for larger problems (6.1 seconds on 100 variables, 200 clauses).
    \item DPLL consistently outperforms DP on larger formulas, solving 100-variable instances in under 0.04 seconds with comparable or less memory.
    \item Detailed timing and memory usage are summarized in Table~\ref{tab:results}.
\end{itemize}

\section{Table of Results}

\begin{tabular}{|c|c|c|c|c|}
\hline
Variables & Clauses & Algorithm & Time (s) & Memory (MB) \\
\hline
5 & 15 & Resolution & 1.8516 & 1.1221 \\
5 & 15 & DP & 0.0003 & 0.0047 \\
5 & 15 & DPLL & 0.0002 & 0.0029 \\
10 & 20 & DP & 0.0006 & 0.0080 \\
10 & 20 & DPLL & 0.0004 & 0.0058 \\
20 & 40 & DP & 0.0015 & 0.0346 \\
20 & 40 & DPLL & 0.0016 & 0.0360 \\
30 & 60 & DP & 0.0041 & 0.0752 \\
30 & 60 & DPLL & 0.0036 & 0.0736 \\
40 & 60 & DP & 0.0045 & 0.1055 \\
40 & 60 & DPLL & 0.0047 & 0.1054 \\
50 & 100 & DP & 0.0106 & 0.1995 \\
50 & 100 & DPLL & 0.0092 & 0.1925 \\
100 & 200 & DP & 6.1078 & 0.8082 \\
100 & 200 & DPLL & 0.0347 & 0.7453 \\
\hline
\end{tabular}

\section{Conclusion}

Resolution is not practical for larger CNFs due to exponential blow-up. DP has conceptual simplicity but slower runtimes on bigger problems. DPLL, with its search pruning and heuristics, shows superior speed and memory usage. This aligns with theory and supports DPLL’s use in practical SAT solving.

\end{document}
