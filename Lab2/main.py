from Lab2.Environment import Environment

agents_count = 5
char_count = 100

if __name__ == "__main__":
    print("=" * char_count)
    print("Start agent initialize")
    print("=" * char_count)

    env = Environment(agents_count)
    env.give_patents()

    print("\n" + "-" * char_count)
    print("Simulation started")
    print("-" * char_count)

    env.simulate()

    print("\n" + "*" * char_count)
    print("Simulation ended")
    print("" + "*" * char_count)
