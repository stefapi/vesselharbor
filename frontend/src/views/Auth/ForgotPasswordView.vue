<template>
  <div class="forgot-password">
    <h1>Mot de passe oublié</h1>
    <form @submit.prevent="submit">
      <div>
        <label for="email">Entrez votre email</label>
        <Field name="email" id="email" type="email" placeholder="Votre email" />
        <ErrorMessage name="email" class="error" />
      </div>
      <button type="submit">Envoyer le lien de réinitialisation</button>
    </form>
    <router-link to="/login">Retour à la connexion</router-link>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useForm, Field, ErrorMessage } from 'vee-validate';
import * as yup from 'yup';
import { useRouter } from 'vue-router';
import api from '@/services/api';

export default defineComponent({
  name: 'ForgotPasswordView',
  components: { Field, ErrorMessage },
  setup() {
    const router = useRouter();
    const schema = yup.object({
      email: yup.string().email('Email invalide').required('Email requis'),
    });

    const { handleSubmit } = useForm({
      validationSchema: schema,
    });

    const submit = handleSubmit(async (values) => {
      try {
        await api.post('/users/reset_password_request', values);
        alert("Si cet email est enregistré, vous recevrez un lien de réinitialisation.");
        router.push({ name: 'Login' });
      } catch (error) {
        console.error("Erreur lors de la demande de réinitialisation", error);
      }
    });

    return { submit };
  },
});
</script>

<style scoped>
.forgot-password {
  max-width: 400px;
  margin: auto;
  padding: 2rem;
}
.error {
  color: red;
}
</style>

