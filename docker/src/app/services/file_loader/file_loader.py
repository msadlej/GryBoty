import os
import importlib.util
import inspect


class FileLoader:
    """
    A utility class to dynamically load modules and retrieve classes from a file.
    """

    @staticmethod
    def get_class(path, class_name=None):
        """
        Load a class from a file.

        Args:
            path (str): Path to the file.
            class_name (str, optional): Name of the class to load. If None, attempts to
                                         infer the class name from the file name.

        Returns:
            type: The loaded class.

        Raises:
            FileNotFoundError: If the file does not exist.
            AttributeError: If the specified class is not found in the module.
        """
        module = FileLoader.load_module(path)
        return FileLoader.retrieve_class(module, class_name)

    @staticmethod
    def load_module(path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        module_name = os.path.splitext(os.path.basename(path))[0]
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    @staticmethod
    def load_file_as_string(path):
        with open(path, "r") as file:
            file_content = file.read()
        return file_content

    @staticmethod
    def retrieve_class(module, class_name=None):
        if class_name is None:
            # Infer class name from file/module name
            classes = inspect.getmembers(
                module,
                lambda member: inspect.isclass(member)
                and member.__module__.lower() == member.__name__.lower(),
            )
            if not classes:
                raise AttributeError("No matching class found in the module.")
            return classes[0][1]
        else:
            if not hasattr(module, class_name):
                raise AttributeError(f"Class '{class_name}' not found in the module.")
            return getattr(module, class_name)
