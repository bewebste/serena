import Foundation

/// Represents a user in the system
public struct User {
    public let id: UUID
    public let name: String
    public let email: String
    public let age: Int
    
    public init(id: UUID = UUID(), name: String, email: String, age: Int) {
        self.id = id
        self.name = name
        self.email = email
        self.age = age
    }
    
    /// Returns the user's display name
    public func displayName() -> String {
        return "\(name) (\(email))"
    }
    
    /// Checks if the user is an adult
    public var isAdult: Bool {
        return age >= 18
    }
}

/// Manages a collection of users
public class UserManager {
    private var users: [UUID: User] = [:]
    
    public init() {}
    
    /// Adds a new user
    public func addUser(_ user: User) {
        users[user.id] = user
    }
    
    /// Finds a user by ID
    public func findUser(by id: UUID) -> User? {
        return users[id]
    }
    
    /// Returns all users
    public func allUsers() -> [User] {
        return Array(users.values)
    }
}