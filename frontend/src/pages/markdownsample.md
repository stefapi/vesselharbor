---
route:
  name: AdminDashboard
  meta:
    requiresAuth: true
    requiredRole: superadmin
---

<script setup>
console.log('Page admin chargée ✅')
</script>

# 🛡️ Tableau de bord admin

Bienvenue dans le panneau de contrôle réservé aux administrateurs.

```ts
// Tu peux même insérer du code si tu utilises Shiki dans vite.config.ts
console.log('Admin only')
```
