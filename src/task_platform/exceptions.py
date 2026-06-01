class TaskError(Exception):
    """Base class for task exceptions."""


class TaskValidationError(TaskError):
    """Raised when task data fails validation."""


class TaskStatusError(TaskValidationError):
    """Raised when a task has an invalid status."""


class TaskPriorityError(TaskValidationError):
    """Raised when a task has an invalid priority."""


class NoHandlerError(Exception):
    """Raised when no handler can process a task."""
