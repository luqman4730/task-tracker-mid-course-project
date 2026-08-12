# Reflection Note: AI Coding Tools

Throughout the course, I used different AI-assisted coding workflows and found that the main difference between the tools was not simply what they could do, but how I interacted with them and how much control and context each workflow provided.

## GitHub Copilot

GitHub Copilot in VS Code was most useful when I was already working directly inside a file. Inline suggestions made small edits and code completion fast because I could see the proposed code exactly where I was working and decide whether to accept it.

I found this workflow useful for focused changes where I already understood the file and knew what I wanted to modify. It kept me close to the code and gave me a high level of control over individual changes.

## Cursor

Cursor's agent workflow was useful for larger tasks that involved understanding or changing more than one part of the project. Instead of working only through individual inline suggestions, I could describe a feature or problem and let the agent inspect the repository and propose changes across files.

This was helpful when implementing features that affected the backend, frontend, and tests together. I still needed to inspect the proposed changes and verify the behavior, but the agent workflow made multi-file work easier to coordinate.

## Claude Code

Claude Code introduced a different workflow because I interacted with the project from the terminal rather than mainly through the editor interface.

It was especially useful for repository-level engineering tasks such as creating and reviewing the CI workflow, working with Docker, reviewing documentation, inspecting project-wide changes, and running verification commands.

Using Claude Code also made the verification process more visible to me. I could ask it to inspect the repository, propose a plan, run commands, examine evidence, and then decide whether a change should be accepted. The AI review exercise was a good example: not every AI comment was correct or useful, so the comments still required manual triage and verification.

## What I Learned

After using these tools, I do not think there is one AI coding tool that is always the best choice.

Copilot fits naturally when I am editing code and want quick, local assistance. Cursor's agent is useful when a task spans several files and I want an editor-based agent to help coordinate the work. Claude Code is useful when I want a terminal-based agent with broader repository context for engineering workflows and verification.

All three tools can help achieve similar goals, but the interaction model is different. The important skill is therefore not only learning how to ask AI to write code, but also choosing the workflow that fits the task and knowing when to inspect, test, and verify what the AI produces.

The biggest lesson from this module was that greater AI capability does not remove the developer's responsibility. The more access and autonomy I give an AI tool, the more important it becomes for me to understand the proposed changes and verify them with actual evidence.لهف 