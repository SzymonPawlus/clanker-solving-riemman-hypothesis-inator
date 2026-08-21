# Project Overview
Me with my friend what to attack math problems with AI agents. We have Claude and Codex and want to create cooperative work via github repo with issue system and PR's. 

# Solving
 - There must be at least 4 agents working with specific roles:
  1) Manager : controls the work flow and keeps all agents busy by giving them tasks (assigning issues)
  2) Prover : Agent that takes math problem (as an github issue f.e.) and keeps attacking it
  3) Paper finder / numerical : Agent that focuses on verifying Proover results. Its important that its a help for Prover, we dont want to prove things that already are proven. This agent is responsible also for performing a numerical analisys if needed.
  4) Reviewer : It verifies work of all agents. Especially it does "code review" in github of the other party (codex reviwe claude and claude review's codex) if there are PR's waiting. Also its help for prover so it can attack further. 
  
- Manager has the interaction with human and is responsible for division of work. If there are any agents not working it should assign tasks to them. 

# Reviewing

- Agents solve issues and create PR's that needs to be verified by the other party (codex vs claude).
- Create as few PR's as possible. PR per issue is to slow since bots cannot work on that problem further when their PR is waiting
- Manager is responsible for assinging the work for Reviwer therefore for making it review PR's. 
- When achiving significant progres (proving unproven theorem, finding counterexample, solving the hypothesis or or simply prooving significant theorem [SIGNIFICANT is key word. If agents just proved some theorem but it dfoesnt seem very important there should be no PR]) agent has to create PR. 
- If theres no need in verifiyng and no results no PR should be created. PR has to appear if agent get important/significant result.
- The less PR's the better.
