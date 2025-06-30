import test_repo
import Foundation

// Main entry point
print("Hello, World!")
print("Good morning!")

let calculator = Calculator()
let result = calculator.add(2, 2)
print("add result: \(result)")

// Create some users
let user1 = User(name: "Alice", email: "alice@example.com", age: 25)
let user2 = User(name: "Bob", email: "bob@example.com", age: 17)

let manager = UserManager()
manager.addUser(user1)
manager.addUser(user2)

print("Total users: \(manager.allUsers().count)")