<template>
  <div class="flex items-center justify-center min-h-screen">
    <div class="p-8 rounded shadow-md w-full max-w-md">
      <span class="text-2xl font-bold mb-6 text-center">Login</span>
      <q-input v-model="form.username" label="Username" filled class="mb-4" />
      <q-input
        v-model="form.password"
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
import { login } from "src/services/DefaultService";
import { useQuasar } from "quasar";

const $q = useQuasar();
const router = useRouter();
const auth = useAuthStore();

const form = ref({
  username: "",
  password: "",
});

const handleLogin = async () => {
  if (!form.value.username || !form.value.password) {
    $q.notify({
      type: "negative",
      message: "Please enter username and password",
    });
    return;
  }
  try {
    const { data } = await login(form.value);
    auth.storageAuthSave({
      user: data,
    });
    router.push("/dashboard");
  } catch (error) {
    console.error(error);
  }
};
</script>
