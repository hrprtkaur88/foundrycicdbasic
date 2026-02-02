import agent_framework.observability as obs
print("=== Available in agent_framework.observability ===")
print(dir(obs))

print("\n=== All submodules in agent_framework ===")
import agent_framework
import pkgutil
for m in pkgutil.walk_packages(agent_framework.__path__, agent_framework.__name__ + '.'):
    print(m.name)