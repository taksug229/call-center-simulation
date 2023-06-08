# Call Center Simulation

![Cover](img/pexels-pixabay-267507.jpg)
Photo by [Pixabay](https://www.pexels.com/photo/gray-wooden-computer-cubicles-inside-room-267507/)

## Requirements

- Python 3.10
- venv

## Setup steps

```
python -m venv

souce venv/bin/activate

pip install -r requirements.txt
```

## Run Simulation

```
python call_center_simulation.py
```

## Table of Contents
1. [Abstract](#abstract)

2. [Data preparation](#data-preparation)

3. [Problem Definition](#problem-definition)

4. [Programming Overview](#programming-overview)

5. [Conclusion and future works](#conclusion-and-future-works)

- [Built with](#built-with)
- [Author](#author)

---

## Abstract

Process simulations have a variety of applications ranging across science, mathematics, and business. Businesses in particular establish protocol in servicing consumers and thus have predictable and reproducible behaviors that may be replicated via simulation. This project explores the scenario of a call center whose key performance metric is the percentage of calls dropped by customers due to late service times. We examine the minimum number of employees a call center must hire to lower this key performance metric to.

---

## Data preparation

The simulation requires the following inputs:

| Variable | Definition |
| ----------------------------- | -----------------------------: |
| Number of employees | employees available to handle customer calls |
| Average support time | average time taken to resolve a customer issue |
| Average support time standard deviation | variability in support time |
| Customer arrival rate | customers per minute following a Poisson distribution |
| SLA time threshold  | wait time we ideally want to pick up the phone |
| Customer dropout time threshold | maximum time a customer is willing to wait before abandoning the call |
| Customer dropout time standard deviation | variability in customer dropout time |


---

## Problem Definition

Executives have approached their analyst team with the following issue: there is insufficient staff to handle the current volume of customers, leading to customers dropping off calls at high rates. They ideally want only 5% of calls to be dropped by the customer. They have tasked the analyst team with drafting a recommendation for hiring the minimum number of call center employees to achieve the 5% drop goal.

In drafting this recommendation, the analyst team decides to create a process simulation that mimics caller behavior. This simulation has 2 stages:

- **Stage 1:** The caller calls the company that is directed toward the call center and enters the queue. At the time of arrival, if there are no customers in the queue and an employee is available, they immediately exit this stage and enter Stage 2. If no employees are available to service them, they wait at the front of the queue and will be the first to be extracted from the queue the moment an employee becomes available. If there are customers in the queue, they enter the back of the queue.
- **Stage 2:** The caller may exit the queue in one of three ways: either by receiving service, by leaving the queue on their own, or if the workday ends.

Like in real life, the callers in this problem do not arrive at perfectly consistent nor predictable intervals. Customers entering the queue are modeled via a poisson distribution where callers arrive at mean interval times. We test three mean interval times in this simulation: a caller arriving every 0.5 minutes, every 1 minute, and every 2 minutes. Likewise, not all callers drop out of the waiting queue at the same time; the time that they drop follows a normal distribution with a mean of 15 minutes and a standard deviation of 5 minutes. Additionally, the time for an employee to support a caller follows a normal distribution with a mean of 10 minutes and a standard deviation of 3 minutes. Employees may only service one caller at a time. After finishing servicing one customer, they remove a caller from the front of the queue and service them.

--

## Programming Overview
The code implements the call center simulation and evaluates KPIs to analyze the call center's performance. The simulation is run with different parameters, including the number of employees and customer arrival rates. There are 30 different parameters since there are 3 different arrival rates with 10 different numbers of employees. For each parameter, the simulation is run for 8 hours 30 times. It tracks metrics such as the total number of customers, handled and dropped calls, average queue and call times, and drop ratio. The simulation results are saved in log files, and summary statistics are calculated and stored in CSV files. This approach enables a comprehensive assessment of the call center's efficiency and provides insights for optimizing its operations.

---

## Conclusion and future works

We tested three different mean arrival times for customers: 0.5 minutes, 1 minute, and 2 minutes. Below is a table with those arrival times corresponding with the recommended number of call center employees to hire in order to ensure the caller drop rate is below 5%:

| Mean Arrival Time of Customer | Recommended Employees to Hire  |
| ----------------------------- | -----------------------------: |
| 0.5 minutes                   | 18                             |
| 1 minute                      | 12                             |
| 2 minutes                     | 6                              |

The call center simulation project lays the foundation for further research and enhancements. Some potential areas for future work include:

- **Optimization:** Apply optimization techniques to determine the optimal number of employees, support time, and other parameters to maximize call center performance.
- **Real-time simulation:** Develop a real-time simulation framework to evaluate call center performance under dynamic conditions and changing customer arrival patterns.
- **Machine learning integration:** Explore the integration of machine learning algorithms to predict call volumes, customer behavior, and optimize call center resource allocation.
- **Sensitivity analysis:** Conduct sensitivity analysis to assess the impact of changing parameters on KPIs and identify the most influential factors.

By addressing these future works, the project can further enhance the accuracy and practicality of the call center simulation model.

---

## Built With

* **Software Packages:**  [Python](https://www.python.org/), [Simpy](https://simpy.readthedocs.io/en/latest/), [Numpy](https://numpy.org/), [Pandas](https://pandas.pydata.org/docs/)
## Author

* **Takeshi Sugiyama** - *Data Scientist*
  * [Linkedin](https://www.linkedin.com/in/takeshi-sugiyama/)
  * [Tableau](https://public.tableau.com/profile/takeshi.sugiyama)
