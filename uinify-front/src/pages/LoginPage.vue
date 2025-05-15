<template>
  <div class="flex items-center justify-center min-h-screen">
    <div class="p-8 rounded shadow-md w-full max-w-md">
      <span class="text-2xl font-bold mb-6 text-center">Login</span>
      <q-input v-model="username" label="Username" filled class="mb-4" />
      <q-input
        v-model="password"
        label="Password"
        type="password"
        filled
        class="mb-6"
      />
      <q-btn
        label="Login"
        color="primary"
        class="w-full"
        @click="handleLogin"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "stores/auth";

const username = ref("");
const password = ref("");
const router = useRouter();
const auth = useAuthStore();

const handleLogin = () => {
  if (username.value && password.value) {
    auth.storageAuthSave({
      token: import.meta.env.VITE_WGER_TOKEN,
    });
    router.push("/");
  } else {
    alert("Please enter username and password");
  }
};
</script>
