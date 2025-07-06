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

import { apiGet, apiPost, apiPut, apiDelete } from './api'

// Types for group operations
export interface Group {
  id: number
  name: string
  description: string
  organization_id: number
  created_at: string
  updated_at: string
}

export interface GroupCreate {
  name: string
  description?: string
}

export interface GroupUpdate {
  name?: string
  description?: string
}

export interface User {
  id: number
  email: string
  first_name: string
  last_name: string
  is_active: boolean
}

export interface Policy {
  id: number
  name: string
  description: string
}

export interface Tag {
  id: number
  name: string
  color: string
}

// Group CRUD operations
export async function listAllGroups() {
  return apiGet<{ status: string; message: string; data: Group[] }>('/groups')
}

export async function getGroup(groupId: number) {
  return apiGet<{ status: string; message: string; data: Group }>(`/groups/${groupId}`)
}

export async function createGroup(organizationId: number, groupData: GroupCreate) {
  return apiPost<{ status: string; message: string; data: Group }>(`/groups/${organizationId}`, groupData)
}

export async function updateGroup(groupId: number, groupData: GroupUpdate) {
  return apiPut<{ status: string; message: string; data: Group }>(`/groups/${groupId}`, groupData)
}

export async function deleteGroup(groupId: number) {
  return apiDelete<{ status: string; message: string; data: {} }>(`/groups/${groupId}`)
}

// User management within groups
export async function getGroupUsers(groupId: number) {
  return apiGet<{ status: string; message: string; data: User[] }>(`/groups/${groupId}/users`)
}

export async function addUserToGroup(groupId: number, userId: number) {
  return apiPost<{ status: string; message: string; data: {} }>(`/groups/${groupId}/users/${userId}`)
}

export async function removeUserFromGroup(groupId: number, userId: number) {
  return apiDelete<{ status: string; message: string; data: {} }>(`/groups/${groupId}/users/${userId}`)
}

// Policy management within groups
export async function getGroupPolicies(groupId: number) {
  return apiGet<{ status: string; message: string; data: Policy[] }>(`/groups/${groupId}/policies`)
}

export async function addPolicyToGroup(groupId: number, policyId: number) {
  return apiPost<{ status: string; message: string; data: {} }>(`/groups/${groupId}/policies/${policyId}`)
}

export async function removePolicyFromGroup(groupId: number, policyId: number) {
  return apiDelete<{ status: string; message: string; data: {} }>(`/groups/${groupId}/policies/${policyId}`)
}

// Tag management within groups
export async function getGroupTags(groupId: number) {
  return apiGet<{ status: string; message: string; data: Tag[] }>(`/groups/${groupId}/tags`)
}

export async function addTagToGroup(groupId: number, tagId: number) {
  return apiPost<{ status: string; message: string; data: {} }>(`/groups/${groupId}/tags/${tagId}`)
}

export async function removeTagFromGroup(groupId: number, tagId: number) {
  return apiDelete<{ status: string; message: string; data: {} }>(`/groups/${groupId}/tags/${tagId}`)
}

// Legacy functions for backward compatibility (these might be used by existing components)
export async function assignUserToGroup(groupId: number, userId: number) {
  return addUserToGroup(groupId, userId)
}

export async function getGroupFunctions(groupId: number) {
  // This seems to be a legacy function - mapping to policies for now
  return getGroupPolicies(groupId)
}

export async function addFunctionToGroup(groupId: number, functionId: number) {
  // This seems to be a legacy function - mapping to policies for now
  return addPolicyToGroup(groupId, functionId)
}

export async function removeFunctionFromGroup(groupId: number, functionId: number) {
  // This seems to be a legacy function - mapping to policies for now
  return removePolicyFromGroup(groupId, functionId)
}

export async function getAvailableFunctions() {
  // This would need to be implemented based on available policies
  // For now, return empty array
  return { data: { status: 'success', message: 'Available functions', data: [] } }
}
