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

## Table of Contents
1. [Introduction](#introduction)

2. [Data preparation](#data-preparation)

3. [Exploratory Data Analysis](#exploratory-data-analysis)

4. [Conclusion and future works](#conclusion-and-future-works)

- [Built with](#built-with)
- [Author](#author)

---

## Introduction

The call center simulation aims to model the interaction between customers and call center employees. It considers factors such as the number of employees, average support time per call, customer arrival rate, service level agreement (SLA) time threshold, and customer dropout rates. By simulating different scenarios and parameters, the project provides insights into call center performance and helps identify areas for improvement.

---

## Data preparation

The simulation requires the following inputs:

Number of employees: Specifies the number of employees available to handle customer calls.
- Average support time: Represents the average time taken to resolve a customer issue.
- Average support time standard deviation: Reflects the variability in support time.
- Customer arrival rate: Defined as the number of customers per minute following a Poisson distribution.
- SLA time threshold: Indicates the maximum acceptable wait time for customers before escalating their cases.
- Customer dropout time threshold: Represents the maximum time a customer is willing to wait before abandoning the call.
- Customer dropout time standard deviation: Captures the variability in customer dropout time.

---

## Exploratory Data Analysis

The simulation generates log data that captures various events during the call center operations. The log data includes information such as customer arrival, waiting time, call duration, and call outcomes (e.g., completed, dropped). The project performs exploratory data analysis on the generated logs to derive insights and calculate KPIs.

---

## Conclusion and future works

Based on the simulation and analysis of the call center, the project draws conclusions regarding the performance and efficiency of the call center operations. It identifies key factors influencing KPIs such as customer wait time, call handling time, and dropout rates. The conclusions highlight the strengths and weaknesses of the call center and provide recommendations for improvement.

The call center simulation project lays the foundation for further research and enhancements. Some potential areas for future work include:

- Optimization: Apply optimization techniques to determine the optimal number of employees, support time, and other parameters to maximize call center performance.
- Real-time simulation: Develop a real-time simulation framework to evaluate call center performance under dynamic conditions and changing customer arrival patterns.
- Machine learning integration: Explore the integration of machine learning algorithms to predict call volumes, customer behavior, and optimize call center resource allocation.
- Sensitivity analysis: Conduct sensitivity analysis to assess the impact of changing parameters on KPIs and identify the most influential factors.

By addressing these future works, the project can further enhance the accuracy and practicality of the call center simulation model.

---


## Built With

* **Software Packages:**  [Python](https://www.python.org/), [Simpy](https://simpy.readthedocs.io/en/latest/), [Numpy](https://numpy.org/), [Pandas](https://pandas.pydata.org/docs/)
## Author

* **Takeshi Sugiyama** - *Data Scientist*
  * [Linkedin](https://www.linkedin.com/in/takeshi-sugiyama/)
  * [Tableau](https://public.tableau.com/profile/takeshi.sugiyama)
