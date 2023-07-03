import os
import numpy as np
import pandas as pd
import simpy
from tqdm import tqdm

dir_path = os.path.dirname(os.path.realpath(__file__))
log_path = dir_path + "log/"

np.random.seed(420)
NUM_EMPLOYEES_RANGE = range(3, 33, 3)  # 3~30 customers. Add 3 customers per simulation.
CUSTOMER_PER_MIN_RATE_LST = [0.5, 1, 2]  # Poisson distribution lambda.
SIMULATION_TIME = 480  # 480min (8hrs)
SIMULATION_REPEAT = 30  # Repeat simulation with same parameters 30 times

AVG_SUPPORT_TIME = 10
AVG_SUPPORT_TIME_STD = 3
SLA_TIME_THRESHOLD = 10
AVG_DROP_TIME_THRESHOLD = 15
AVG_DROP_TIME_THRESHOLD_STD = 5


class CallCenter:
    """
    CallCenter class representing a call center simulation.
    """

    def __init__(
        self,
        env: simpy.Environment,
        num_employees: int,
        avg_support_time: int,
        avg_support_time_std: int,
        params_id: str,
        sim_id: str,
    ) -> None:
        """
        Initialize the CallCenter object.

        Args:
            env (simpy.Environment): SimPy environment object.
            num_employees (int): Number of employees in the call center.
            avg_support_time (int): Average support time per call.
            avg_support_time_std (int): Standard deviation of the support time.
            params_id (str): ID representing the parameters of the simulation.
            sim_id (str): ID representing the simulation number.
        """
        self.env = env
        self.staff = simpy.Resource(env, num_employees)
        self.avg_support_time = avg_support_time
        self.avg_support_time_std = avg_support_time_std
        self.params_id = params_id
        self.sim_id = sim_id

    def support(self, customer: str) -> None:
        """
        Process the customer support call.

        Args:
            customer (str): ID representing the customer.
        """
        call_entry_time = self.env.now
        actual_support_time = max(
            1, round(np.random.normal(self.avg_support_time, self.avg_support_time_std))
        )
        yield self.env.timeout(actual_support_time)
        call_time = self.env.now - call_entry_time
        logs_lst.append(
            [
                self.params_id,
                self.sim_id,
                f"case{customer}",
                "Finished_call",
                self.env.now,
                None,
                call_time,
            ]
        )

    def customer(self, name: int) -> None:
        """
        Process the customer's interaction with the call center.

        Args:
            name (int): ID representing the customer.
        """
        global customer_handled, no_sla_total, drop_total
        logs_lst.append(
            [
                self.params_id,
                self.sim_id,
                f"case{name}",
                "In_queue",
                self.env.now,
                None,
                None,
            ]
        )
        queue_entry_time = self.env.now
        with self.staff.request() as request:
            yield request
            queue_time = self.env.now - queue_entry_time
            customer_leave_time = max(
                1,
                round(
                    np.random.normal(
                        AVG_DROP_TIME_THRESHOLD, AVG_DROP_TIME_THRESHOLD_STD
                    )
                ),
            )
            if queue_time > customer_leave_time:
                logs_lst.append(
                    [
                        self.params_id,
                        self.sim_id,
                        f"case{name}",
                        "Dropped",
                        self.env.now,
                        customer_leave_time,
                        None,
                    ]
                )
                drop_total += 1
                return

            if queue_time > SLA_TIME_THRESHOLD:
                no_sla_total += 1

            logs_lst.append(
                [
                    self.params_id,
                    self.sim_id,
                    f"case{name}",
                    "In_call",
                    self.env.now,
                    queue_time,
                    None,
                ]
            )

            yield self.env.process(self.support(name))
            customer_handled += 1


def setup(
    env: simpy.Environment,
    num_employees: int,
    avg_support_time: int,
    avg_support_time_std: int,
    customer_interval: float,
    params_id: str,
    sim_id: str,
) -> None:
    """
    Set up the call center simulation.

    Args:
        env (simpy.Environment): SimPy environment object.
        num_employees (int): Number of employees in the call center.
        avg_support_time (int): Average support time per call.
        avg_support_time_std (int): Standard deviation of the support time.
        customer_interval (float): Time interval between customers.
        params_id (str): ID representing the parameters of the simulation.
        sim_id (str): ID representing the simulation number.
    """
    global customer_total
    call_center = CallCenter(
        env, num_employees, avg_support_time, avg_support_time_std, params_id, sim_id
    )

    i = 0
    while True:
        yield env.timeout(np.random.poisson(customer_interval))
        i += 1
        env.process(call_center.customer(i))
        customer_total += 1


if __name__ == "__main__":
    kpi_lst = []
    logs_columns = [
        "parameters",
        "simulationID",
        "caseID",
        "status",
        "timestamp",
        "queue_time",
        "call_time",
    ]
    for customer_per_min in tqdm(
        CUSTOMER_PER_MIN_RATE_LST, total=len(CUSTOMER_PER_MIN_RATE_LST)
    ):
        customer_interval = 1 / customer_per_min
        for num_employees in NUM_EMPLOYEES_RANGE:
            params_lst = [
                num_employees,
                customer_per_min,
                SIMULATION_TIME,
                SIMULATION_REPEAT,
                AVG_SUPPORT_TIME,
                AVG_SUPPORT_TIME_STD,
                SLA_TIME_THRESHOLD,
                AVG_DROP_TIME_THRESHOLD,
                AVG_DROP_TIME_THRESHOLD_STD,
            ]
            params_lst = [str(param).zfill(2) for param in params_lst]
            params_id = "-".join(params_lst)
            param_log_lst = []
            for simulation in range(SIMULATION_REPEAT):
                logs_lst = []
                customer_total = 0
                customer_handled = 0
                no_sla_total = 0
                drop_total = 0
                sim_id = str(simulation + 1)
                env = simpy.Environment()
                env.process(
                    setup(
                        env,
                        num_employees,
                        AVG_SUPPORT_TIME,
                        AVG_SUPPORT_TIME_STD,
                        customer_interval,
                        params_id,
                        sim_id,
                    )
                )
                env.run(until=SIMULATION_TIME)

                # Calculate KPIs
                log_df = pd.DataFrame(logs_lst, columns=logs_columns)
                param_log_lst.extend(logs_lst)
                total_not_traced = customer_total - (customer_handled + drop_total)
                customer_total_traced = customer_total - total_not_traced
                avg_queue_time = log_df["queue_time"].mean()
                avg_call_time = log_df["call_time"].mean()
                avg_drop_time = log_df.loc[
                    (log_df["status"] == "Dropped"), "queue_time"
                ].mean()
                no_sla_ratio = no_sla_total / customer_handled
                drop_ratio = drop_total / customer_total_traced
                kpi_lst.append(
                    [
                        params_id,
                        sim_id,
                        customer_total,
                        customer_total_traced,
                        total_not_traced,
                        customer_handled,
                        no_sla_total,
                        drop_total,
                        avg_queue_time,
                        avg_call_time,
                        avg_drop_time,
                        no_sla_ratio,
                        drop_ratio,
                    ]
                )
            param_log_df = pd.DataFrame(param_log_lst, columns=logs_columns)
            log_file_path = log_path + f"{params_id}.txt"
            os.makedirs(log_path, exist_ok=True)
            with open(log_file_path, "w") as f:
                param_log_string = param_log_df.to_string(index=False)
                f.write(param_log_string)
    kpi_columns = [
        "parameters",
        "simulationID",
        "total",
        "total_traced",
        "total_not_traced",
        "handled",
        "handled_no_sla",
        "dropped",
        "avg_queue_time",
        "avg_call_time",
        "avg_drop_time",
        "no_sla_ratio",
        "drop_ratio",
    ]

    kpi = pd.DataFrame(kpi_lst, columns=kpi_columns)
    kpi_agg = kpi.groupby("parameters")[kpi_columns[2:]].mean().reset_index()

    kpi_summary_path = dir_path + f"log-summary.csv"
    kpi_summary_agg_path = dir_path + f"log-summary-average.csv"
    kpi.to_csv(kpi_summary_path, index=False)
    kpi_agg.to_csv(kpi_summary_agg_path, index=False)
    print(f"saved logs to {log_path}")
    print(f"saved log summary to {kpi_summary_path}")
    print(f"saved log summary average to {kpi_summary_agg_path}")
