# AI Agent Guidance for the hd2api2db Project

This document provides general guidance for AI agents assisting with the development of the `hd2api2db` project.

## Core Project Goal
To create and maintain a robust pipeline for fetching data from the Helldivers 2 API and storing it in a MySQL database.

## Key Technologies
- Python
- MySQL
- Pytest for testing

## Detailed Agent Instructions (for Cursor/Compatible Agents)
Comprehensive rules, development workflows, tool usage (including Task Master), and specific coding patterns for AI agents operating within the Cursor IDE are located in the `.cursor/rules/` directory. Agents capable of understanding this structured format should prioritize those files, particularly:
- `.cursor/rules/dev_workflow.mdc` (for the overall development process)
- `.cursor/rules/taskmaster.mdc` (for using the Task Master tool)
- `.cursor/rules/cursor_rules.mdc` (for formatting rules and code)

## General Guidelines for All AI Agents
- **Code Style:** Strive for clarity, efficiency, and consistency with the existing codebase. When in doubt, refer to existing patterns or ask for clarification.
- **Error Handling:** Implement robust error handling and logging, especially for API interactions and database operations.
- **Testing:** All new features and significant changes must be accompanied by relevant tests using Pytest. Ensure tests are isolated and cover key functionality.
- **Communication:** If instructions are unclear or if a proposed change has significant implications, please ask for clarification.

## PR Messages
When generating Pull Request messages, please provide a clear summary of the changes, the problem being solved, and how the changes were tested. 
