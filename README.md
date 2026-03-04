# SPOT: Process Resource Monitoring and Anomaly Detection

This project explores process-level resource monitoring using `prmon` and implements a statistical anomaly detection system to identify resource irregularities like memory leaks and CPU spikes.

---

## 1. Install and Familiarize with prmon
I installed `prmon` to monitor resource usage metrics, including:
* **RSS / PSS** (Physical memory)
* **CPU time** (User and System)
* **Threads** and **Virtual Memory**

Initially, I attempted to use the built-in burner tests, but due to setup compatibility issues, I transitioned to a custom C++ implementation.

## 2. Custom Burner Implementation
I created `burner.cpp` to simulate a controlled workload.
* **Baseline:** Allocated **500 MB** of memory before the main loop.
* **Observed PSS:** ~503 MB (RSS ≈ PSS).
* **Logic:** Since there were no shared libraries or memory segments, PSS accurately reflected the total physical memory used.

## 3. Dataset Generation
Using `prmon`, I generated multiple time-series datasets:

### Normal Runs (3 Datasets)
* Stable runs with 500 MB allocated once. 
* Variations accounted for OS scheduling and background tasks.

### Anomaly Runs (3 Types)
1.  **Memory Spike:** 500 MB for 30s, then a jump to 1 GB (Level shift).
2.  **Memory Leak:** Simulated by allocating an extra 15 MB every second (`std::vector`).
3.  **CPU Runaway:** Continuous spawning of multiple threads to spike CPU usage and thread count.

---

## 4. Feature Extraction
Extracted the following features from `.txt` time-series files for analysis:
* **Memory:** `rss_mean`, `rss_max`, `rss_std`, `rss_growth`
* **CPU:** `utime_mean`, `utime_max`, `utime_std`, `stime_mean`, `stime_max`, `cpu_growth`
* **Threads:** `nthreads_mean`, `nthreads_max`

## 5. Challenges Faced
* **NaN in rss_std:** Occurred in single-point files. **Fix:** Replaced NaNs with 0 and dropped empty runs.
* **Feature Scaling:** Memory values (~500,000) dwarfed CPU values (~30). **Fix:** Applied `StandardScaler`.
* **Small Dataset:** Only 6 runs total. While unstable for deep supervised learning, it served as a successful prototype for statistical detection.

---

## 6. Detection Strategy
### Initial Attempt: Rolling Z-Score (Failed)
Attempted to use local neighborhood averages. This failed because sustained level shifts and gradual leaks eventually "normalized" within the rolling window, masking the anomaly.

### Final Approach: Statistical Baseline
I built a baseline using **Normal Runs only** and calculated a threshold:
$$\text{Threshold} = \mu (\text{mean}) + 3 \times \sigma (\text{std})$$

**Results:**
* **Memory Spike:** 15 anomalies detected (Success).
* **Memory Leak:** 30 anomalies detected (Success).
* **CPU Spike:** 0 detected via memory-baseline; requires CPU-specific baseline.

---

## 7. Evaluation & Suitability
* **Advantages:** Simple, interpretable, and highly effective for level shifts.
* **Limitations:** Metric-specific; struggles with complex multi-dimensional patterns. 
* **Future Scope:** For large-scale systems, models like **Isolation Forest** or **LSTMs** would provide better behavioral detection.

## 8. AI Usage Disclosure
AI was utilized for:
* Debugging code issues and suggesting ML preprocessing fixes.
* Structuring detection logic and formatting this report.
* *Note: All design decisions, anomaly injection methods, and interpretations were performed manually.*

## Conclusion
The project successfully demonstrates the ability to monitor process resources, generate realistic synthetic anomalies, and implement a valid statistical detection system.
