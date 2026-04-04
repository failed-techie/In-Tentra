"""
Core module for INTENTRA
Contains intent compilation, policy engine, and enforcement logic

NOTE: Only import what you need to avoid unnecessary dependencies
"""

# Lazy imports to avoid dependency issues
def get_intent_compiler():
    from .intent_compiler import IntentCompiler
    return IntentCompiler

def get_policy_engine():
    from .policy_engine import PolicyEngine
    return PolicyEngine

def get_enforcement_layer():
    from .enforcement_layer import EnforcementLayer
    return EnforcementLayer


__all__ = ["get_intent_compiler", "get_policy_engine", "get_enforcement_layer"]
