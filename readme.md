# expert system

## algorithm

backward-chaining with queue

add queries to goal queue
while there are goals
	for each goal
		if goal is in facts
			remove goal from goals
			add goal to facts
	for each rule
		if rule leads to any goal
			mark goal as to be removed
			add antecedent to goals
	remove all goals that have been marked
	if no rule leads to goal
		failure
for each query
	if query in goals
		success

backward-chaining with graph

add each query to graph and to open set
for each goal from open set
	for each rule
		if goal is concequent of rule
			add an edge between goal and antecedent of rule
			add antecedent to open set
			if antecedent is in facts
				follow path from antecedent to goal

backward-chaining

for each query
	initialize goals queue
	add query to goals
	for each goal
		if goal is in facts
			query is successful
		else for each rule
			if concequent is goal
				if antecedent is in facts
					add concequent to facts
				else
					add antecedent to goals
