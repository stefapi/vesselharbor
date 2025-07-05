// src/services/environmentService.ts
import api from '@/services/api.ts';
import type { EnvironmentListParams } from '@/types/api';

export async function createEnvironment(env: { name: string }) {
  return api.post('/environments/', env);
}

export async function updateEnvironment(environmentId: number, env: { name: string }) {
  return api.put(`/environments/${environmentId}`, env);
}

export async function deleteEnvironment(environmentId: number) {
  return api.delete(`/environments/${environmentId}`);
}

export async function listEnvironments(params: EnvironmentListParams = {}) {
  return api.get('/environments', { params });
}

export async function getEnvironment(environmentId: number) {
  return api.get(`/environments/${environmentId}`);
}
