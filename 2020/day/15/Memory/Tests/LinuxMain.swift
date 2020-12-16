import XCTest

import MemoryTests

var tests = [XCTestCaseEntry]()
tests += MemoryTests.allTests()
XCTMain(tests)
