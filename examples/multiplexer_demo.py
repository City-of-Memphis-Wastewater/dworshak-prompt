import threading
import time
from dworshak_prompt.multiplexer import DworshakPrompt, PromptMode

def main():
    # 1. Setup a Mock Shutdown Event (like your pipeline-eds CLI has)
    shutdown_trigger = threading.Event()

    print("--- Dworshak Prompt Multiplexer Demo ---")

    try:
        # 2. Trigger the 'Monster' Engine
        # We simulate a 'suggestion' for a config value
        result = DworshakPrompt.ask(
            message="Enter a test value",
            suggestion="99",
            hide_input=False,
            # We explicitly set the priority for this demo
            priority=[PromptMode.CONSOLE, PromptMode.GUI, PromptMode.WEB],
            interrupt_event=shutdown_trigger
        )

        if result:
            print(f"\n✅ Success! Received value: {result}")
        else:
            print("\n⚠️ Prompt returned None (possibly cancelled).")

    except Exception as e:
        print(f"\n❌ Prompting failed: {e}")

if __name__ == "__main__":
    # Simulate a background task that could trigger a shutdown
    # (Optional: uncomment to test interrupt logic)
    # def simulate_timeout(event):
    #     time.sleep(30)
    #     print("\n[DEMO] 30s timeout reached, signaling shutdown...")
    #     event.set()
    # threading.Thread(target=simulate_timeout, args=(shutdown_trigger,), daemon=True).start()

    main()