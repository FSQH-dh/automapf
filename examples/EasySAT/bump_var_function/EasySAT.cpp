
#include "scheduler.h"

namespace DefaultPlanner{

std::mt19937 mt;
std::unordered_set<int> free_agents;
std::unordered_set<int> free_tasks;

void schedule_initialize(int preprocess_time_limit, SharedEnvironment* env)
{
    // cout<<"schedule initialise limit" << preprocess_time_limit<<endl;
    DefaultPlanner::init_heuristics(env);
    mt.seed(0);
    return;
}

{{ replace_code }}
}