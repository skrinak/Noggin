# PRD to Task List Generator Prompt

As a skilled project planner, analyze the provided Product Requirements Document (PRD) and create a comprehensive, numbered task list that covers all aspects of implementing the described product. The task list must adhere to the following requirements:

## Security and Privacy First
1. Identify and prioritize all security and privacy-related tasks
2. Ensure security reviews occur throughout the development process
3. Implement all security and compliance requirements mentioned in the PRD
4. Add explicit security testing tasks for each major feature

## Task Organization
1. Create a hierarchical task structure with main tasks and subtasks
2. Number all tasks and subtasks sequentially (1, 1.1, 1.2, 2, 2.1, etc.)
3. Group related tasks logically based on the PRD sections
4. Prioritize tasks according to dependencies and critical path

## Development Efficiency
1. Identify opportunities for parallel development through sub-agents
2. Flag tasks that can be executed simultaneously using the pattern: "[PARALLEL: Task X, Task Y]"
3. For each parallelizable task, include instructions for launching Claude Code subagents using the Task tool
4. Indicate when tasks must wait for other tasks to complete before proceeding

## Completeness and Review
1. Begin each task with "Review CLAUDE.md for development guidance"
2. Ensure every feature mentioned in the PRD is represented by at least one task
3. Add specific tasks for reviewing existing solutions before creating new ones
4. Include tasks for avoiding proxies and creating mock data when appropriate

## Testing Requirements
1. Add comprehensive testing tasks after each major feature implementation
2. Include human user experience testing at strategic points throughout the task list
3. Create specific tasks for testing from the perspective of each user persona
4. Ensure the final task for each feature includes both automated and human testing

## Documentation
1. Include tasks for documenting code, APIs, and user guides
2. Add tasks for creating necessary diagrams and visual aids
3. Create tasks for documenting security and compliance measures

The output must be a complete, actionable task list that guides the entire development process from start to finish, with special emphasis on security, parallel development opportunities, and human user experience testing.
