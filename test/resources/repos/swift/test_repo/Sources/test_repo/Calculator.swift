/// A simple calculator class for basic arithmetic operations
public class Calculator {
    public init() {}
    
    /// Adds two integers together
    public func add(_ a: Int, _ b: Int) -> Int {
        return a + b
    }
    
    /// Multiplies two integers
    public func multiply(_ a: Int, _ b: Int) -> Int {
        return a * b
    }
    
    /// Divides two integers
    public func divide(_ a: Int, _ b: Int) throws -> Int {
        guard b != 0 else {
            throw CalculatorError.divisionByZero
        }
        return a / b
    }
}

public enum CalculatorError: Error {
    case divisionByZero
}