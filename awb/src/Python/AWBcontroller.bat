@echo off
REM CSMARTer.bat

REM Set the initial tabbed pane to be displayed
REM 0 is the Overview pane
REM 1 is the Rule Editor
REM 2 is the Society Editor
REM 3 is the Agent Laydown
set INITIAL_PANE="3"

python agentController.py %INITIAL_PANE%