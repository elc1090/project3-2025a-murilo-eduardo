<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="shadow">
      <q-toolbar class="hidden">
        <q-btn flat dense round icon="menu" @click="toggleDrawer" />
        <q-toolbar-title>
          <img src="assets/uinify-logo.png" class="cursor-pointer h-[50px]" />
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-page-container class="text-dark">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRoute } from "vue-router";

const drawer = ref(true);
const route = useRoute();

function toggleDrawer() {
  drawer.value = !drawer.value;
}

const pageTitle = computed(() => {
  const titles = {
    "/dashboard": "Dashboard",
    "/treinos": "Treinos",
    "/exemplos": "Exemplos",
    "/videos": "Vídeos",
    "/montar-treino": "Montar Treino",
    "/nutricao": "Nutrição",
    "/perfil": "Perfil",
  };
  return titles[route.path] || "UInify";
});
</script>
