from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Dict,
    KeysView,
    List,
    Literal,
    NamedTuple,
    Optional,
    Set,
    Type,
    Union,
)

if TYPE_CHECKING:

    from starlite.types import ASGIApp, Method, RouteHandlerType
    from starlite.types.internal_types import PathParameterDefinition


class ASGIHandlerTuple(NamedTuple):
    """Encapsulation of a route handler node."""

    asgi_app: "ASGIApp"
    """An ASGI stack, composed of a handler function and layers of middleware that wrap it."""
    handler: "RouteHandlerType"
    """The route handler instance."""


@dataclass(unsafe_hash=True)
class RouteTrieNode:
    """A radix trie node."""

    __slots__ = (
        "asgi_handlers",
        "child_keys",
        "child_path_parameters",
        "child_path_parameter_types",
        "children",
        "is_asgi",
        "is_mount",
        "is_path_type",
        "path_type_path_param_definition",
        "path_parameters",
    )

    asgi_handlers: Dict[Union["Method", Literal["websocket", "asgi"]], "ASGIHandlerTuple"]
    """
    A mapping of ASGI handlers stored on the node.
    """
    child_keys: KeysView[Union[str, "PathParameterDefinition"]]
    """
    A set containing the child keys, same as the children dictionary - but as a set, which offers faster lookup.
    """
    child_path_parameters: List["PathParameterDefinition"]
    """
    Path parameter definition of immediate child nodes.
    """
    child_path_parameter_types: Set[Type]
    """
    Types of path parameters of existing child path parameters.
    """
    children: Dict[Union[str, "PathParameterDefinition"], "RouteTrieNode"]
    """
    A dictionary mapping path components or using the PathParameterSentinel class to child nodes.
    """
    path_type_path_param_definition: Optional["PathParameterDefinition"]
    """
    A path parameter definition of type "path" if one has been registered on the node.
    """
    is_asgi: bool
    """
    Designate the node as having an `@asgi` type handler.
    """
    is_mount: bool
    """
    Designate the node as being a mount route.
    """
    path_parameters: List["PathParameterDefinition"]
    """
    A list of tuples containing path parameter definitions. This is used for parsing extracted path parameter values.
    """


def create_node() -> RouteTrieNode:
    """Create a RouteMapNode instance.

    Returns:
        A route map node instance.
    """

    children: Dict[Union[str, "PathParameterDefinition"], "RouteTrieNode"] = {}
    return RouteTrieNode(
        asgi_handlers={},
        child_keys=children.keys(),
        child_path_parameters=[],
        child_path_parameter_types=set(),
        children=children,
        is_asgi=False,
        is_mount=False,
        path_type_path_param_definition=None,
        path_parameters=[],
    )
