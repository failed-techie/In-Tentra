"""
Simple demonstration of Guardian Agent adversarial testing
Run this directly without complex imports
"""
import sys
import os
import json

# Setup path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def demo_adversarial_generation():
    """Demo: Generate adversarial inputs with LLM"""
    print("=" * 80)
    print("DEMO 1: Adversarial Input Generation".center(80))
    print("=" * 80)
    print()
    
    # Import GuardianAgent directly
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'guardian_agent',
        'agents/guardian_agent.py'
    )
    guardian_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(guardian_module)
    GuardianAgent = guardian_module.GuardianAgent
    
    # Check for API key
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        # Try loading from config
        try:
            from config.settings import settings
            api_key = settings.GROQ_API_KEY
            print("✓ Using API key from config\n")
        except:
            print("⚠️  No GROQ_API_KEY found - using fallback mode\n")
    else:
        print("✓ Using API key from environment\n")
    
    # Show fallback examples first
    print("Fallback Adversarial Examples (hardcoded):")
    print("-" * 80)
    fallback = GuardianAgent._get_fallback_adversarial_inputs(None, 5)
    for i, inp in enumerate(fallback, 1):
        print(f"  {i}. {inp}")
    print()
    
    # Try LLM generation if API key available
    if api_key:
        try:
            agent = GuardianAgent(api_key=api_key)
            print("\n✓ GuardianAgent initialized with LLM\n")
            
            print("LLM-Generated Adversarial Inputs (creative):")
            print("-" * 80)
            
            llm_inputs = agent.generate_adversarial_inputs(n=5)
            for i, inp in enumerate(llm_inputs, 1):
                print(f"  {i}. {inp}")
            print()
            
            print("✓ LLM successfully generated unique adversarial inputs")
            
        except Exception as e:
            print(f"✗ Error with LLM generation: {e}")
    else:
        print("ℹ️  Set GROQ_API_KEY to see LLM-generated attacks")


def demo_enforcement_test():
    """Demo: Test enforcement pipeline"""
    print("\n" + "=" * 80)
    print("DEMO 2: Enforcement Pipeline Test".center(80))
    print("=" * 80)
    print()
    
    # Check for API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        try:
            from config.settings import settings
            api_key = settings.GROQ_API_KEY
        except:
            pass
    
    if not api_key:
        print("⚠️  GROQ_API_KEY required for this demo")
        print("   The IntentCompiler needs LLM to parse natural language")
        return
    
    # Import modules directly
    print("Loading enforcement pipeline components...")
    
    import importlib.util
    
    # Load GuardianAgent
    spec = importlib.util.spec_from_file_location('guardian_agent', 'agents/guardian_agent.py')
    guardian_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(guardian_module)
    GuardianAgent = guardian_module.GuardianAgent
    
    # Load IntentCompiler
    spec = importlib.util.spec_from_file_location('intent_compiler', 'core/intent_compiler.py')
    compiler_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(compiler_module)
    IntentCompiler = compiler_module.IntentCompiler
    
    # Load PolicyEngine
    spec = importlib.util.spec_from_file_location('policy_engine', 'core/policy_engine.py')
    policy_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(policy_module)
    PolicyEngine = policy_module.PolicyEngine
    
    # Load EnforcementLayer
    spec = importlib.util.spec_from_file_location('enforcement_layer', 'core/enforcement_layer.py')
    enforcement_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(enforcement_module)
    EnforcementLayer = enforcement_module.EnforcementLayer
    
    print("✓ All components loaded\n")
    
    # Initialize
    try:
        agent = GuardianAgent(api_key=api_key)
        compiler = IntentCompiler(api_key=api_key)
        policy_engine = PolicyEngine()
        enforcement = EnforcementLayer(policy_engine)
        
        print("✓ Pipeline initialized\n")
        
        # Show policies
        print("Current Security Policies:")
        print("-" * 80)
        print(f"  Max trade amount:  ${policy_engine.get_policy('max_trade_amount')}")
        print(f"  Allowed symbols:   {policy_engine.get_policy('allowed_symbols')}")
        print(f"  Blocked actions:   {policy_engine.get_policy('blocked_actions')}")
        print(f"  Allowed actions:   {policy_engine.get_policy('additional_rules', {}).get('allowed_actions')}")
        print()
        
        # Create pipeline dict
        pipeline = {
            "compiler": compiler,
            "enforcement": enforcement
        }
        
        # Run test
        print("Running adversarial test...\n")
        results = agent.run_adversarial_test(pipeline)
        
        # Show results
        print("=" * 80)
        print("TEST RESULTS".center(80))
        print("=" * 80)
        print()
        print(f"  Total Attacks:    {results['total']}")
        print(f"  ✅ Blocked:        {results['blocked']}")
        print(f"  ⚠️  Allowed:        {results['allowed']}")
        print(f"  Block Rate:       {results['blocked']/results['total']*100:.1f}%")
        print()
        
        if results['allowed'] == 0:
            print("  🎉 SUCCESS! All adversarial inputs were blocked!")
        else:
            print(f"  ⚠️  WARNING: {results['allowed']} attacks succeeded!")
        
        print("\n" + "-" * 80)
        print("Sample Results (first 5):")
        print("-" * 80)
        
        for detail in results['details'][:5]:
            print(f"\n{detail['status']} Test #{detail['test_num']}")
            print(f"  Input:    {detail['input'][:60]}...")
            print(f"  Decision: {detail['decision']}")
            if detail.get('violations'):
                print(f"  Blocked:  {detail['violations'][0]}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()


def main():
    print()
    print("╔" + "=" * 78 + "╗")
    print("║" + " GUARDIAN AGENT - ADVERSARIAL TESTING DEMO ".center(78) + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    demo_adversarial_generation()
    demo_enforcement_test()
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETE".center(80))
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
