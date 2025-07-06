/*
 * Copyright (c) 2025.  VesselHarbor
 *
 * ____   ____                          .__    ___ ___             ___.
 * \   \ /   /____   ______ ______ ____ |  |  /   |   \_____ ______\_ |__   ___________
 *  \   Y   // __ \ /  ___//  ___// __ \|  | /    ~    \__  \\_  __ \ __ \ /  _ \_  __ \
 *   \     /\  ___/ \___ \ \___ \\  ___/|  |_\    Y    // __ \|  | \/ \_\ (  <_> )  | \/
 *    \___/  \___  >____  >____  >\___  >____/\___|_  /(____  /__|  |___  /\____/|__|
 *               \/     \/     \/     \/            \/      \/          \/
 *
 *
 * MIT License
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 *
 */

// Environment related types
export interface Environment {
  id: number
  name: string
  description?: string
  organization_id: number
  status: 'active' | 'inactive' | 'maintenance'
  created_at: string
  updated_at: string
  elements_count?: number
  tags?: string[]
}

export interface EnvironmentCreate {
  name: string
  description?: string
  organization_id: number
  status?: 'active' | 'inactive' | 'maintenance'
  tags?: string[]
}

export interface EnvironmentUpdate {
  name?: string
  description?: string
  status?: 'active' | 'inactive' | 'maintenance'
  tags?: string[]
}

export interface Element {
  id: number
  name: string
  type: string
  environment_id: number
  configuration: Record<string, unknown>
  status: 'running' | 'stopped' | 'error' | 'pending'
  created_at: string
  updated_at: string
}

export interface ElementCreate {
  name: string
  type: string
  environment_id: number
  configuration: Record<string, unknown>
}

export interface ElementUpdate {
  name?: string
  type?: string
  configuration?: Record<string, unknown>
  status?: 'running' | 'stopped' | 'error' | 'pending'
}
