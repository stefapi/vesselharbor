// src/types/user.ts

export interface UserAssignment {
  group: {
    environment_id: number | null
    functions: { name: string }[]
  }
}

export interface User {
  id: number
  email: string
  is_superadmin: boolean
  user_assignments?: UserAssignment[]
  created_at?: string
  updated_at?: string
  // Ajouter d'autres propriétés communes si nécessaire
}
