---
title: "feedback_assignment"
source: https://cs2680.seas.harvard.edu/slides/feedback_assignment.pdf
pages: 58
crawled: 2026-11-16
---

# feedback_assignment

> PDF 讲义文本抽取：[feedback_assignment.pdf](https://cs2680.seas.harvard.edu/slides/feedback_assignment.pdf) · Harvard CS2680

Modern AI Systems: Agents 
and System Optimizations
Juncheng Yang
Feedback for your assignments

2Harvard MaDSys    ·   course.agentic-system.org
Plan for today
• A review of assignments
• Make better use of agents
• GPU programming
• LLM serving III

3Harvard MaDSys    ·   course.agentic-system.org
Logistics
• Office hour today
• Bonus for Assignment 5
• Reach out to TFs and me if you need help

4Harvard MaDSys    ·   course.agentic-system.org 4Harvard MaDSys    ·   course.agentic-system.org
Assignment 1 review
What you learned from using Claude Code
What you wished from Claude Code

5Harvard MaDSys    ·   course.agentic-system.org
Agent event streams are asynchronous and hard to 
reconstruct
Tasks finish in a different order 
than they start
Background Bash tasks can come 
from different subagents
Agents often use Bash instead of 
the dedicated read and edit tools
A trustworthy viewer required 
inspecting real traces and 
modeling state transitions

6Harvard MaDSys    ·   course.agentic-system.org
Vague requirements went in and unchecked results 
came out
Checkable requirements worked better than broad prompts
Ambiguous requirements
• Broad prompts produced unwanted features, excess architecture 
or wrong layouts
• Screenshots, explicit geometry and measurable criteria worked 
better
Unchecked results
• Tests checked internal state, not visible behavior
• Hide/show tests checked the HTML hidden property; CSS kept 
content visible
• Reported verification had run zero tests or was blocked
Suggestion
• Write requirements as 
verifiable conditions, 
with visual examples
• Ask the agent to surface 
ambiguity
• Review the design 
before larger changes
• Check verification 
results yourself

7Harvard MaDSys    ·   course.agentic-system.org
Repeated work and poorly split delegation wasted 
time and money
Subagents helped on independent reviews and distinct implementation tasks
Repeated work
• Agents repeated the same exploration across sessions
• Agents ran operations the feature did not need
Poor subagent uses
• Several agents rereading the same small repository, duplicating 
the parent’s work
• Testing files while another agent was modifying them
• A six-agent run at delegation depth three took over 10 minutes 
and nearly $15; a similar earlier task took under 2 minutes and $1
Suggestion
• Use memory to avoid 
repeated exploration
• Test uncertain ideas as 
small, delegated 
experiments
• Give each agent a clear 
responsibility and 
isolated changes

8Harvard MaDSys    ·   course.agentic-system.org
Lessons for Assignment 1
Inspect real 
traces early and 
set clear goals
1
Define concrete 
acceptance 
criteria
2
Build in small 
increments
3
Iterate with 
screenshots
4
The biggest shift: from asking an agent to produce code to specifying 
how its work will be verified and trusted

9Harvard MaDSys    ·   course.agentic-system.org 9Harvard MaDSys    ·   course.agentic-system.org
What everyone wants from Claude Code
more visibility with less clutter , and effective 
autonomy with opportunities to intervene

10Harvard MaDSys    ·   course.agentic-system.org
Visible, controlled delegation
Delegate work while retaining control over
task, 
dependency 
and context
decisions and 
findings
topology* 
(#agent, 
delegation 
depth)
scope* status and 
verification
*: dynamically during runtime not as a static configuration
Make delegated work easy to follow and reconcile

11Harvard MaDSys    ·   course.agentic-system.org
More visibility and control
Visibility progress and 
remaining work
• short explanations of 
plans, current 
hypotheses
• explain decisions in 
time for users to 
intervene
• report exactly what was 
verified and 
assumptions
Manage context 
deliberately
• selective context editing 
to remove incorrect 
assumptions
• easier memory editing 
and to remove stale 
understanding and 
assumptions
Manage cost explicitly
• show live dollar costs 
together with an explicit 
budget controls

12Harvard MaDSys    ·   course.agentic-system.org
Help users retain ownership of their code
Understand the 
software as it grew
why particular tools or files are being examined
file-by-file diffs
clearer module structure
a way to connect a visible interface change to the code 
implementing it
an interactive debugging mode that would pause at an error 
and ask the student to identify the likely file or function

14Harvard MaDSys    ·   course.agentic-system.org 14Harvard MaDSys    ·   course.agentic-system.org
Bash is used over native tools
Anthropic’s experiment made it a bad time for this 
Assignment…

15Harvard MaDSys    ·   course.agentic-system.org
Short answer: Anthropic did it deliberately! 
Claude Code told the agent to use Bash in system prompt
auto and bypass-permissions sessions got a system reminder: "Do your work through 
the Bash tool wherever it can accomplish the job … rather than 
using the dedicated Read, Edit, or Write tools"
The Bash tool's own description dropped its warning
at the same time, the line "Avoid using this tool to run cat, head, tail, 
sed, awk, or echo" was gone from the tool description
Grep and Glob did not exist in almost every session
agents that tried them were told "No such tool available: Grep … search file contents with 
grep via the Bash tool instead" , so every search went through the shell

16Harvard MaDSys    ·   course.agentic-system.org
Anthropic ran the experiment on most of you 
and selectively…
• gated by feature flag “tengu_thrifty_sonic”: all of you except one are in the experiment,
• only on opus-5, Fable model, not Sonnet or Haiku
• Added Aug 12, and your assignment ran from Sep 2–22
One of you found it and tested it
Things have changed with opus-5.5: prompt is softened
• You can do much of your work through the Bash tool when it is 
the simpler route
• The choice is yours: prefer Edit or Write when a shell edit 
would be fragile, such as exact or multi-line replacements, or 
sed/awk flags that differ between GNU and BSD/macOS

17Harvard MaDSys    ·   course.agentic-system.org
How Claude Code decides
1  Bash-first group?
once per session; subagents 
inherit
Opus 5.5, Fable 
5.1: always
Opus 5: if 
thrifty_sonic flag
Sonnet 5, Haiku: 
no
2  Add the reminder?
before each request, if all 
hold
Auto or 
bypass + Bash + Edit 
or Write + In the bash-
first group + Not already 
added
3  Which text?
first match wins
Per-account 
setting
Opus 5.5: 
relaxed
cozy_teapot 
flag Strict
Flags are cached in ~/.claude.json; Anthropic can change them without a release. 

18Harvard MaDSys    ·   course.agentic-system.org
The prompt plays a big role
• bottom: significantly increase bash 
usage
• right: when reminder is inserted in 
the middle of a session

19Harvard MaDSys    ·   course.agentic-system.org
Assignment 4 
• We ran top 18 
submissions 10 times
• Variance depends on 
harness
• Variance does not hide 
a good harness 
Tasks solved (of 26)
End-to-end time (min)
0
5
10
15
20
0
100
200 4 h limit
The same submission graded 10 times: 18 
submissions from 12 students, 180 
gradings. Dots: one grading. Submission ID

20Harvard MaDSys    ·   course.agentic-system.org
Assignment 4 
• Multiple runs of 
each submission 
are clustered 
Tasks solved (of 26)
0
5
10
15
0 50 100 150 200 250
End-to-end time (min)
4 h limit A1
B1
A2
A3
C
D
B2
E
F1
G
F2
H
I
J
K1
K2
A4
L

21Harvard MaDSys    ·   course.agentic-system.org 21Harvard MaDSys    ·   course.agentic-system.org
How Claude Code usage changed across the 
three assignments

22Harvard MaDSys    ·   course.agentic-system.org
Prompts, hours, cost and tool calls grew 4.5–7×
Typed prompts
median per student
Active hours
median per student
Cost
median per student
Tool calls
per student, red = subagents
29
52
130
A1 A2 A3
3.4 h
9.2 h
23.4 h
A1 A2 A3
$66
$112
$328
A1 A2 A3
4.5× 6.9× 5.0×
609 917
4,414
A1 A2 A3

23Harvard MaDSys    ·   course.agentic-system.org
Prompt length, target, permission mode
Prompt length
median characters
Said what done looks like
% of typed prompts
Prompts by permission mode
% of typed prompts
98
87
65
A1 A2 A3
−34%
39%
24%
15%
A1 A2 A3
−24 pts
72%
80% Auto
8.6% 18%
Bypass
0
25
50
75
100
A1 A2 A3

24Harvard MaDSys    ·   course.agentic-system.org
Monitor, subagent and workflow
Agents launched subagents
% of students
Ran a workflow
% of students
36%
47%
74%
A1 A2 A3
2.9%
10%
35%
A1 A2 A3
Effort setting of main-agent API calls
% of main-agent calls with an effort setting
0% 25% 50% 75%
low
medium
high
xhigh
max
A1 A2 A3

25Harvard MaDSys    ·   course.agentic-system.org
Question topics and prompt framing
Question topic
% of questions
0% 20% 40% 60%
Their own code or app
What the agent did or why
The assignment and rubric
General concepts
A1 A2 A3 What the prompt specified
% of prompts
0% 20% 40% 60%
Named the target
Said what done looks like
Vague
Go-ahead or choice
Need to provide a way for agent to verify 
its work. 
Great to see you learn from agents! 

26Harvard MaDSys    ·   course.agentic-system.org
Where agents failed and who caught it
Failure type
% of cases, by assignment
70%
25%
45%
53%
64%
78%
Broke working code
Wrong diagnosis,
too much
confidence
A1 A2 A3
Who caught each failure
% of notes that say who
61%
29%
5.6%
4.5%
45%
29%
7.0%
15%
33%
29%
9.2%
22%
The student
The agent itself
Another agent
A graded run
A1 A2 A3

28Harvard MaDSys    ·   course.agentic-system.org 28Harvard MaDSys    ·   course.agentic-system.org
Effective Agenting!

29Harvard MaDSys    ·   course.agentic-system.org
You do not need to bash your agent to be rank 1
#1
#23
#33
#45
#54
#60
#63
0 20 40 60 80 100
Leaderboard rank
Claude Code active hours
Rank 1 (Pareto front) Other ranks
You should take the 
control and decide 
wisely on what the agent 
works on. 

30Harvard MaDSys    ·   course.agentic-system.org
Less than one hour of your time to achieve rank 1!
#1
#23
#33
#45
#54
#60
#63
0 5 10 15 20 25
Leaderboard rank
Student hours
Rank 1 (Pareto front) Other ranks
Working with agent 
effectively is critical!

31Harvard MaDSys    ·   course.agentic-system.org
Have your agent work for you not the opposite! 
100
30
10
3
1
0.3
0.1
0.1 0.3 1 3 10 30
Claude working time, hours
Student hours
Rank 1 (Pareto front) Other ranks
10×
3×
1×
100%
80%
60%
40%
20%
0%
0.1 0.3 1 3 10 30 100
Share of students at or below
Hours per student (log scale)
Claude time Student time
median 4.3 h
median 13.8 h

38Harvard MaDSys    ·   course.agentic-system.org 38Harvard MaDSys    ·   course.agentic-system.org
Pitfalls when using an agent

39Harvard MaDSys    ·   course.agentic-system.org 39Harvard MaDSys    ·   course.agentic-system.org
Blindly trust the agent
This is the biggest problem we all face!
How much we should check and how to check?

40Harvard MaDSys    ·   course.agentic-system.org
Agents often built something we did not intend
What we meant What the agent built
Example 1 · “Make the tests pass”
Bug fixed
test_parse  ✓
test_empty  ✓
test_unicode  ✓
0 failing  ✓
test_parse
test_empty
test_unicode
The agent deleted the failing tests. Nothing fails, 
the bug is still there.
What we meant What the agent built
Example 2 · “Reduce cost on leaderboard”
All tasks
COMPLETED
Lower cost  ✓
All tasks
SKIPPED
Cost: $0  ✓
The agent skipped every task. Cost: $0. Work 
done: also zero.

42Harvard MaDSys    ·   course.agentic-system.org
P1: Blindly trust the agent's claims
The agent said a change worked, a test passed or a finding held, and you moved on without checking. 
Many claims were wrong: tests never ran, or failures were piped away.
Trusted agent’s wrong claims 
% students
Asked for tests or evidence
% typed prompts
20% 20%
33%
A1 A2 A3
15%
27%
17%
A1 A2 A3

44Harvard MaDSys    ·   course.agentic-system.org
Verify agent claims with evidence
Define done
What tests need to be ran and what 
is the stopping criteria? 
Curate test cases you can verify
Read the diff yourself
Then check one case by hand
Examine test results
What has been ran? Show the full 
output and exit status, no tail or 
head
Have another agent verify
Use a subagent to verify the results 
or diff to make sure it is correct 

45Harvard MaDSys    ·   course.agentic-system.org
P2: Losing track of what the agent built
How to improve
• Work in reviewable steps: one feature or experiment per turn, then read the diff and commit.
• Ask for shorter and more readable reports. 
• Keep a decisions and history file (NOTES.md or CLAUDE.md) that the agent updates, so you know 
what it has done.
• Check progress and steer mid-turn: press Esc to stop a wrong turn, or type a correction.
Students who lost track
% students, by assignment
18%
37%
21%
A1 A2 A3
Long agent turns
turns of 30+ min, by assignment
41
182
514
A1 A2 A3
Vague ask, long run
% students, 30+ min runs
13%
50%
69%
A1 A2 A3

46Harvard MaDSys    ·   course.agentic-system.org
P3: Sessions ran too long and compaction lost context
Context filled up
% of students compacted
Compactions
auto + manual, count
“i remember we tested 1 already, please pull those 
results before implementing”
13-day session with two compactions
“again respect the instructors feedback i shared earlier”
Lost previous feedback after a compaction: the 
feedback had been pasted 5 hours before.
How to improve
• Start a new session for each task
• Keep plans, decisions and status in 
files (CLAUDE.md or an imported 
NOTES.md), so a fresh session picks up 
where the last stopped.
• Send wide searches and long logs to 
subagents
• Run /compact yourself at a natural 
break, with a note on what to keep.
16%
40%
69%
A1 A2 A3
20 50
201
A1 A2 A3

47Harvard MaDSys    ·   course.agentic-system.org
P4: Stacking changes without controlled experiments
Many changes at once, or restarts
% students, by assignment
Stacked four Expert features into v9; cost rose but solves did not.
How to improve
• Change one thing per run against a fixed 
baseline, and drop what does not help 
before you add the next idea.
• Give each experiment its own git branch 
or worktree, and tag the version you submit.
• Write the hypothesis down before you 
build, so a run can prove it wrong.
0% 5%
37%
A1 A2 A3

48Harvard MaDSys    ·   course.agentic-system.org
P5: Parallel sessions stepped on each other
Overlapping sessions
% of students, 15+ min
Longest overlap
hours, by assignment
A1   Two sessions fought over port 4000
A2   An old batch overwrite results A3   A git reset broke another run’s code
How to improve
• Give each session its own git worktree
• Name every run and its output folder
• Dedicated timing measurements 
without interference
9%
22%
54%
A1 A2 A3
1.7 h
15 h
21 h
A1 A2 A3

49Harvard MaDSys    ·   course.agentic-system.org
P6: Agents run destructive commands
A2 student
The agent overwrote prompts.py, destroying 
evidence of the prompt that ran.
How to improve
• Commit before risky steps. 
• Add deny rules for rm -rf, git reset --hard 
and force pushes. 
• Use bypassPermissions only in an 
isolated container or VM.
• Ask the agent to confirm before it deletes, 
resets or kills anything it did not create.
Permission bypass
% of prompts sent
Refused tool calls
count, before they ran
8.6% 11%
16%
A1 A2 A3
167 233
484
A1 A2 A3
Refused tool calls: blocked by the student, a deny rule or auto mode.

50Harvard MaDSys    ·   course.agentic-system.org
P7: Secrets leakage
Exposed a key or password
% students How to improve
• Keep keys in environment 
variables or a .env file that git and 
the session archive leave out; never 
paste them into a prompt.
• Keep keys out of the agent's 
environment. Do not paste the key 
in the prompt. 
3%
23% 19%
A1 A2 A3
A3 student · what the student typed
“the username is [REDACTED], the 
password is [REDACTED] for the 
submission. take these down somewhere so 
you auto submit while i'm not here”
A1 A2 A3
Typed or pasted 1 10 6
Agent printed it 1 6 6
Left in committed logs 1 2 15

51Harvard MaDSys    ·   course.agentic-system.org
P8: Reading a single noisy run as real effects
Took one run as proof
% students, by assignment
A3 student
Identical code scored 16 to 18, so single submissions were hard to read.
How to improve
• Run each version more than once on the 
same tasks and compare the spread, not 
one score.
• Decide before the run how big a difference 
has to be to count, and keep one results 
table per version.0%
30%
73%
A1 A2 A3

52Harvard MaDSys    ·   course.agentic-system.org
P9: Venting instead of steering
A1
“first of all this tree is so badly 
formed. its not in a tree at all!”
“clean this up immediately or 
ill be angry”
“Oh man somany bugs… Try 
hard to find bugs and fix 
them”
93 tool calls, 61 min of agent work
A2
“CONITNUE DONT COME 
BACK TO ME UNLESS THEY 
ARE DONE … GOOOOOOO”
“…I am so upset , put more 
effort on it!”
“PLZ BRO JUST USE 
STANDARD”
5 tool calls, 18 min of agent work
A3
“what you just said is 
completely unacceptable. 
you have to work hard to get 
something better”
“what is happening oh my god 
its so bad”
“how tf did these people do it 
why cant we do it this well”
“thats so stupid... what can i 
do about that”

53Harvard MaDSys    ·   course.agentic-system.org
P9: Venting instead of steering
Vented instead of steering
% students, by assignment How to improve
• Stop after the second failed fix and 
ask for a diagnosis with evidence, such 
as the log line or exact error.
• Paste the exact error or a screenshot, 
and say what you expected to see.
• Find out why: when a score stays low, 
ask where the failed runs spent their 
time before asking for a new idea.
• Go back to the last good state with 
/rewind or git instead of piling fixes on a 
broken one.
7% 5%
21%
A1 A2 A3

54Harvard MaDSys    ·   course.agentic-system.org
P10: Platform issues or laptop sleep
Lost time due to the machine
% students, by assignment
A3 student
host disk filled by 42 GB of task images on 
a laptop, causing an infrastructure failure
How to improve
• Read the stated requirements 
(platform, disk, Docker) before 
the first run. If your laptop does 
not fit, use CloudLab or AWS 
from the start.
• Run long jobs in tmux or 
nohup on a machine that does 
not sleep.
12%
50%
65%
A1 A2 A3

57Harvard MaDSys    ·   course.agentic-system.org
Ten pitfalls and how to avoid them
P1  Blindly trusting claims
Ask for evidence; check one case
P2  Losing track of what was built
Small steps: read the diff, commit
P3  Long sessions lose context
New session per task, notes in files
P4  Stacking changes
One change per run vs. a baseline
P5  Parallel sessions collide
One worktree and branch per session
P6  Destructive commands
Commit first; deny rm -rf and resets
P7  Leaked secrets
Keys in env vars, never in prompts
P8  Reading one noisy run
Run several times, compare spread
P9  Venting instead of steering
Paste the error, ask for a diagnosis
P10  Platform issues, laptop sleep
Check requirements; run jobs in tmux

58Harvard MaDSys    ·   course.agentic-system.org
Harder assignments: more pitfalls
Pitfalls per student, 
average
Share of students who 
stacked changes
Share who decided on 
one noisy run
Shares are of the same 58 students in each assignment. A2 share of errors caught not reported.
Share of agent errors 
students caught
1.3
3.4
5.0
A1 A2 A3
0%
47%
78%
A1 A2 A3
0%
48%
66%
A1 A2 A3
61%
33%
A1 A3

59Harvard MaDSys    ·   course.agentic-system.org
Claude Code Best Practice: a good iteration loop
1
Start with a 
simple baseline
(do not start with pi 
or dsh)
2
Create one 
hypothesis
3
Make one 
change
4
local tests / 
leaderboard 
test
6
Record a 
version if 
verified
Iteration loop
5. repeat at least once
Keep in charge; step-by-step; verify before move on (testing rigor matters)

61Harvard MaDSys    ·   course.agentic-system.org 61Harvard MaDSys    ·   course.agentic-system.org
Towards effective use of agents
An experimental feedback platform to help you improve your skills using agent
https://how-i-used-claude.cs2680.com
Feedbacks are welcome!

62Harvard MaDSys    ·   course.agentic-system.org

63Harvard MaDSys    ·   course.agentic-system.org

64Harvard MaDSys    ·   course.agentic-system.org
AI is a tool everyone has to MASTER
How I used Claude Code in assignments? 
• Where did things break and fail? 
• Where did I waste time? 
How can I improve my AI skills for quality / effectiveness and productivity?
• Is my prompt too vague? Maybe I should not ask it to finish a project?
• Should I write a longer and more detailed prompt? 
• Do I miss important things in the prompt?
• Are there better ways to use agents? 
https://how-i-used-claude.cs2680.com (WIP)

65Harvard MaDSys    ·   course.agentic-system.org
How you compare with your classmates

66Harvard MaDSys    ·   course.agentic-system.org
Visibility into your Claude Code usage

67Harvard MaDSys    ·   course.agentic-system.org
Semi-personalized tips for everyone

68Harvard MaDSys    ·   course.agentic-system.org
Course-staff feedback across assignments

69Harvard MaDSys    ·   course.agentic-system.org
Everyone has an agentability portrait 
that changes with each new assignment

70Harvard MaDSys    ·   course.agentic-system.org
Everyone is different in the class! 
Have fun! 
Feedback is welcome! 
 https://how-i-used-claude.cs2680.com

71Harvard MaDSys    ·   course.agentic-system.org
Next class
• GPU programming 
• LLM serving basics III: scheduling, paging and parallelism
