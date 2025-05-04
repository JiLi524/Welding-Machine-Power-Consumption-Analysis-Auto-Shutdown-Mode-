# Welding Machine Power Consumption Analysis with Auto Shutdown Strategy

*Note: The dataset is simulated using a custom Python script to mimic real-world equipment behavior.*
This project analyzes equipment power usage and evaluates the effectiveness of an **auto shutdown strategy**. The analysis is based on time-series power data, and visualizations are provided to support observations regarding energy savings, idle behavior, and operational patterns.

All related charts are saved in the `charts/` directory.

---

## Objective

The main goal is to assess how automatically shutting down equipment during idle times impacts total power consumption. This includes:

- Comparing daily energy usage before and after applying the shutdown strategy
- Understanding the distribution of idle durations
- Identifying potential for power optimization

---

## Key Visualizations

###  Daily Power Comparison: Before vs. After Shutdown Strategy

![Daily Power Comparison](charts/Comparison%20of%20auto_shutdown%20effects%20%28Daily%20Total%20Power%29.png)

This line chart compares the total daily power consumption with and without the auto shutdown strategy.  
The dashed line represents the data after applying shutdown logic, where power is set to zero during `auto_shutdown = True`.

There is a consistent reduction in daily power totals when the strategy is applied, particularly noticeable on high-consumption days.

---

###  Distribution of Operational States

![State Proportion](charts/Statistics%20on%20the%20proportion%20of%20each%20state.png)

The pie chart shows how often the system is in each operational state:

- Running: 50.2%
- Idle: 30.9%
- Shutdown: 18.9%

The significant percentage of time spent in idle suggests room for improvement through automated control.

---


### Idle Duration Density Curve

![Idle KDE](charts/Idle%20duration%20distribution%20curve.png)

The kernel density curve shows a right-skewed distribution of idle time.  
Short idle durations are the most common, but long idle periods also appear regularly, which justifies the use of an auto shutdown strategy.

---

## Conclusion

- The auto shutdown strategy effectively reduces energy usage across all recorded days.
- Idle time accounts for a significant portion of operation, and many idle periods are long enough to justify automated shutdown.
- These findings support the use of idle detection and shutdown logic to reduce unnecessary power consumption without compromising system performance.

---


