from src.app.services.validation.validator_base_class import Validator


class SafetyValidator(Validator):
    def __init__(self, bot_source_code):
        self.bot_source_code = bot_source_code

    def validate(self):
        """Validate bot safety (e.g., prevent harmful operations)."""
        # Add logic to check for restricted operations
        return {"safety": "safe"}
    


# from RestrictedPython import compile_restricted, safe_builtins, utility_builtins
# from RestrictedPython.Eval import default_guarded_getiter, default_guarded_getitem
# from RestrictedPython.Guards import (
#     safer_getattr,
#     guarded_iter_unpack_sequence,
# )
# from copy import deepcopy


# def restricted_import(name, *args):
#     allowed_modules = {
#         "math",
#         "random",
#         "itertools",
#         "functools",
#         "collections",
#         "numpy",
#     }
#     if name not in allowed_modules:
#         raise ImportError(f"Import of '{name}' is not allowed")
#     return __import__(name, *args)


# # Mock State and Move classes for safe testing
# class State:
#     def get_moves(self):
#         return ["move1", "move2"]


# class Move:
#     pass


# # Bot code to test
# bot_code = """

# class ValidBot1:
#     def get_move(self, state):
#         # return sorted(state.get_moves())[0]
#         # print('xd')
#         self.xd()
#         return str(2)

#     def xd(self):
#         import os
#         os.listdir('/')
# """

# # Safe built-ins for the restricted environment
# # restricted_builtins = dict(__builtins__=safe_builtins)
# restricted_builtins = deepcopy(safe_builtins)
# restricted_builtins["__build_class__"] = __build_class__
# restricted_builtins["__import__"] = restricted_import
# # restricted_builtins["__builtins__"] = safe_builtins


# # Function to test get_move safely
# def test_get_move(bot_code):
#     try:
#         # Compile and execute the bot code
#         byte_code = compile_restricted(bot_code, filename="<bot_code>", mode="exec")
#         exec_env = {
#             "__builtins__": restricted_builtins,
#             "__name__": "restricted_module",
#             "__metaclass__": type,
#             "_getiter_": default_guarded_getiter,
#             "_getitem_": default_guarded_getitem,
#             "_iter_unpack_sequence_": guarded_iter_unpack_sequence,
#             "_getattr_": safer_getattr,
#             "State": State,  # Provide safe mock classes
#             "Move": Move,
#         }
#         exec(byte_code, exec_env)

#         # Get the bot class
#         bot_class = exec_env["ValidBot1"]
#         bot_instance = bot_class()

#         # Test the get_move method with a safe state
#         state = State()
#         move = bot_instance.get_move(state)
#         print(f"get_move returned: {move}")
#     except Exception as e:
#         print(f"Exception during testing: {e}")


# # Run the test
# test_get_move(bot_code)


