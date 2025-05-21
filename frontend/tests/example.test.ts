import { describe, it, expect } from 'vitest'

// A simple utility function to test
function sum(a: number, b: number): number {
  return a + b
}

describe('Basic Test Suite', () => {
  it('should add two numbers correctly', () => {
    expect(sum(1, 2)).toBe(3)
  })

  it('should handle negative numbers', () => {
    expect(sum(-1, -2)).toBe(-3)
  })

  it('should handle zero', () => {
    expect(sum(0, 0)).toBe(0)
  })
})
