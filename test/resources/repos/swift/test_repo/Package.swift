// swift-tools-version: 5.9
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "test_repo",
    products: [
        // Products define the executables and libraries a package produces, making them visible to other packages.
        .library(
            name: "test_repo",
            targets: ["test_repo"]),
        .executable(
            name: "test_repo_cli",
            targets: ["test_repo_cli"]
        )
    ],
    targets: [
        // Targets are the basic building blocks of a package, defining a module or a test suite.
        // Targets can depend on other targets in this package and products from dependencies.
        .target(
            name: "test_repo"),
        .executableTarget(
            name: "test_repo_cli",
            dependencies: ["test_repo"]),
        .testTarget(
            name: "test_repoTests",
            dependencies: ["test_repo"]),
    ]
)