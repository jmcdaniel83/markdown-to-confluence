#!/usr/bin/env python3
"""
Jira Constants Module

This module contains all the constants used for Jira field values and IDs,
organized into logical classes for better maintainability and readability.
"""


class Components:
    """Jira component IDs"""
    CLIENT_PORTAL = "10010"      # All things related to Closinglock Client Experience
    COMPANY_PORTAL = "10011"     # Closinglock user home and TPS integrations
    EMPLOYEE_PORTAL = "10012"    # Employee Portal
    OTHER = "10013"              # Misc.
    PRICING_CALCULATOR = "10014" # Sales Pricing Calculator


class Categories:
    """Jira category values"""
    SOFTWARE_RESEARCH_DEV = "Software research & development"
    SOFTWARE_UPKEEP_MAINT = "Software upkeep & maintenance"


class IssueTypes:
    """Jira issue type names"""
    TASK = "Task"
    STORY = "Story"
    BUG = "Bug"
    EPIC = "Epic"


class Priorities:
    """Jira priority names"""
    HIGHEST = "Highest"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    LOWEST = "Lowest"


class CustomFields:
    """Jira custom field keys"""
    EPIC_LINK = "customfield_10008"
    SPRINT = "customfield_10010"
    CATEGORY = "customfield_10033"
    TESTER = "customfield_10074"