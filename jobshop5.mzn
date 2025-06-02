% Use this editor as a MiniZinc scratch book
include "globals.mzn";
int: n_machines;
int: n_jobs;
int: n_tasks_per_job = n_machines;
set of int: jobs = 1..n_jobs;
set of int: tasks = 1..n_tasks_per_job;

array [jobs, tasks] of 0..(n_machines - 1): job_task_machine;
array [jobs, tasks] of int: job_task_duration;

int: min_duration = max([sum([job_task_duration[i, j] | j in tasks]) | i in jobs]);
int: max_duration = sum([job_task_duration[i, j] | i in jobs, j in tasks]);

array [jobs, tasks] of var 0..max_duration: job_task_start;
var min_duration..max_duration: t_end;

constraint
    forall(j in jobs, k in 1..n_tasks_per_job - 1) (
        job_task_start[j, k] + job_task_duration[j, k] <= job_task_start[j, k + 1]
    );

constraint
    forall(j in jobs)( job_task_start[j, 1] >= 0 );

constraint
    forall(m in 0..n_machines - 1) (
        let {
            array[int] of var 0..max_duration: s =
                array1d([
                    job_task_start[j, k]
                    | j in jobs, k in tasks where job_task_machine[j, k] = m
                ]),
            array[int] of int: d =
                array1d([
                    job_task_duration[j, k]
                    | j in jobs, k in tasks where job_task_machine[j, k] = m
                ])
        } in
        disjunctive(s, d)
    );

constraint
    forall(j in jobs) (
        job_task_start[j, n_tasks_per_job] + job_task_duration[j, n_tasks_per_job] <= t_end
    );

solve 
  minimize t_end;

output [
    "t_end = ", show(t_end), "\n"
];


