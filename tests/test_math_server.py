"""
Unit tests for the Math Server MCP server.

Tests cover all arithmetic operations and error handling scenarios.
"""

import pytest
from mathserver import add, subtract, multiply, divide


class TestAddition:
    """Test cases for the add() function."""
    
    def test_add_positive_numbers(self):
        """Test addition of two positive numbers."""
        assert add(5, 3) == 8
        assert add(10, 20) == 30
        assert add(1, 1) == 2
    
    def test_add_negative_numbers(self):
        """Test addition with negative numbers."""
        assert add(-5, -3) == -8
        assert add(-10, 5) == -5
        assert add(10, -5) == 5
    
    def test_add_zero(self):
        """Test addition with zero."""
        assert add(0, 5) == 5
        assert add(5, 0) == 5
        assert add(0, 0) == 0
    
    def test_add_floats(self):
        """Test addition with floating point numbers."""
        assert add(5.5, 3.2) == 8
        assert add(1.1, 2.2) == 3


class TestSubtraction:
    """Test cases for the subtract() function."""
    
    def test_subtract_positive_numbers(self):
        """Test subtraction of two positive numbers."""
        assert subtract(10, 3) == 7
        assert subtract(20, 10) == 10
        assert subtract(5, 5) == 0
    
    def test_subtract_negative_numbers(self):
        """Test subtraction with negative numbers."""
        assert subtract(-5, -3) == -2
        assert subtract(-10, 5) == -15
        assert subtract(10, -5) == 15
    
    def test_subtract_zero(self):
        """Test subtraction with zero."""
        assert subtract(5, 0) == 5
        assert subtract(0, 5) == -5
        assert subtract(0, 0) == 0
    
    def test_subtract_floats(self):
        """Test subtraction with floating point numbers."""
        assert subtract(10.5, 3.2) == 7
        assert subtract(5.5, 2.2) == 3


class TestMultiplication:
    """Test cases for the multiply() function."""
    
    def test_multiply_positive_numbers(self):
        """Test multiplication of two positive numbers."""
        assert multiply(5, 3) == 15
        assert multiply(10, 2) == 20
        assert multiply(7, 8) == 56
    
    def test_multiply_negative_numbers(self):
        """Test multiplication with negative numbers."""
        assert multiply(-5, -3) == 15
        assert multiply(-10, 5) == -50
        assert multiply(10, -5) == -50
    
    def test_multiply_zero(self):
        """Test multiplication with zero."""
        assert multiply(0, 5) == 0
        assert multiply(5, 0) == 0
        assert multiply(0, 0) == 0
    
    def test_multiply_one(self):
        """Test multiplication by one (identity)."""
        assert multiply(1, 5) == 5
        assert multiply(5, 1) == 5
        assert multiply(1, 1) == 1
    
    def test_multiply_floats(self):
        """Test multiplication with floating point numbers."""
        assert multiply(5.5, 2.0) == 11
        assert multiply(2.5, 4.0) == 10


class TestDivision:
    """Test cases for the divide() function."""
    
    def test_divide_positive_numbers(self):
        """Test division of two positive numbers."""
        assert divide(10, 2) == 5.0
        assert divide(15, 3) == 5.0
        assert divide(20, 4) == 5.0
    
    def test_divide_negative_numbers(self):
        """Test division with negative numbers."""
        assert divide(-10, 2) == -5.0
        assert divide(10, -2) == -5.0
        assert divide(-10, -2) == 5.0
    
    def test_divide_by_one(self):
        """Test division by one (identity)."""
        assert divide(5, 1) == 5.0
        assert divide(100, 1) == 100.0
    
    def test_divide_floats(self):
        """Test division with floating point numbers."""
        assert divide(10.0, 2.0) == 5.0
        assert divide(7.5, 2.5) == 3.0
    
    def test_divide_by_zero_raises_error(self):
        """Test that division by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)
        
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(-5, 0)
    
    def test_divide_result_is_float(self):
        """Test that division always returns float."""
        result = divide(5, 2)
        assert isinstance(result, float)
        assert result == 2.5


class TestErrorHandling:
    """Test cases for error handling across all operations."""
    
    def test_invalid_input_type_add(self):
        """Test add() with invalid input types."""
        with pytest.raises(ValueError):
            add("5", 3)
        
        with pytest.raises(ValueError):
            add(5, "3")
    
    def test_invalid_input_type_subtract(self):
        """Test subtract() with invalid input types."""
        with pytest.raises(ValueError):
            subtract("10", 5)
    
    def test_invalid_input_type_multiply(self):
        """Test multiply() with invalid input types."""
        with pytest.raises(ValueError):
            multiply(5, None)
    
    def test_invalid_input_type_divide(self):
        """Test divide() with invalid input types."""
        with pytest.raises(ValueError):
            divide("10", 2)


class TestCalculationSequence:
    """Test cases for complex calculation sequences."""
    
    def test_order_of_operations(self):
        """Test complex expression: (5 + 3) + (12 / 3) - (2 * 4)"""
        # Step by step: (5 + 3) = 8
        step1 = add(5, 3)
        assert step1 == 8
        
        # Step 2: (12 / 3) = 4
        step2 = divide(12, 3)
        assert step2 == 4.0
        
        # Step 3: 8 + 4 = 12
        step3 = add(step1, int(step2))
        assert step3 == 12
        
        # Step 4: (2 * 4) = 8
        step4 = multiply(2, 4)
        assert step4 == 8
        
        # Step 5: 12 - 8 = 4
        result = subtract(step3, step4)
        assert result == 4
    
    def test_multiple_operations(self):
        """Test multiple chained operations."""
        a = add(10, 5)
        b = multiply(a, 2)
        c = divide(b, 5)
        assert c == 6.0


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
