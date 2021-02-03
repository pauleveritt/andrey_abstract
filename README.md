# Interface Registry Experiment

Working with @vlasovskikh on a `wired`-style registry alternative using abstract class/method/member ideas instead of
protocols.

## Questions

0. Look at mypy warning.s
   
1. Is it wrong to use (abstract) classes as keys?

2. Let's add an example of "protecting" attributes.

3. Could we move the global registry to a class variable on each "directive" and use `__init_subclass__` to register?

4. Could you have "directives" that didn't subclass, but were just explicitly registered? Meaning, 
   `registry.register_class(View, CustomerView)` would work even if `CustomerView` didn't subclass.
   (This would be more of a protocol-ish, structural approach.)  
   
5. Is Java `interface` *really* part of nominal typing?