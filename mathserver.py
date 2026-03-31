"""
MathServer - A Model Context Protocol (MCP) server providing basic arithmetic operations.

This module provides mathematical tools (add, subtract, multiply, divide) that can be
called by LangChain agents through the MCP framework.
"""

from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server with a descriptive name
mcp = FastMCP("MathServer")


@mcp.tool()
def add(a: int, b: int) -> int:
    """
    Add two numbers together.
    
    Args:
        a (int): First number to add
        b (int): Second number to add
    
    Returns:
        int: The sum of a and b
    
    Raises:
        TypeError: If inputs are not integers
    """
    try:
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError(f"Expected numeric inputs, got {type(a).__name__} and {type(b).__name__}")
        return int(a + b)
    except Exception as e:
        raise ValueError(f"Addition operation failed: {str(e)}")


@mcp.tool()
def subtract(a: int, b: int) -> int:
    """
    Subtract one number from another.
    
    Args:
        a (int): Number to subtract from
        b (int): Number to subtract
    
    Returns:
        int: The result of a - b
    
    Raises:
        TypeError: If inputs are not integers
    """
    try:
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError(f"Expected numeric inputs, got {type(a).__name__} and {type(b).__name__}")
        return int(a - b)
    except Exception as e:
        raise ValueError(f"Subtraction operation failed: {str(e)}")


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """
    Multiply two numbers together.
    
    Args:
        a (int): First number to multiply
        b (int): Second number to multiply
    
    Returns:
        int: The product of a and b
    
    Raises:
        TypeError: If inputs are not integers
    """
    try:
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError(f"Expected numeric inputs, got {type(a).__name__} and {type(b).__name__}")
        return int(a * b)
    except Exception as e:
        raise ValueError(f"Multiplication operation failed: {str(e)}")


@mcp.tool()
def divide(a: int, b: int) -> float:
    """
    Divide one number by another.
    
    Args:
        a (int): Numerator (number to be divided)
        b (int): Denominator (number to divide by)
    
    Returns:
        float: The quotient of a / b
    
    Raises:
        ValueError: If b is zero (division by zero)
        TypeError: If inputs are not numeric
    """
    try:
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError(f"Expected numeric inputs, got {type(a).__name__} and {type(b).__name__}")
        if b == 0:
            raise ValueError("Cannot divide by zero. The denominator must be non-zero.")
        return float(a) / float(b)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Division operation failed: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error during division: {str(e)}")


if __name__ == "__main__":
    print("Starting MathServer...")
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        print(f"Error starting MathServer: {str(e)}")
        raise