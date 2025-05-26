<template>
  <q-layout view="hHh lpR fFf">
    <!-- Header -->
    <q-header class="bg-white border-b border-gray-200 shadow-sm">
      <q-toolbar class="px-4 lg:px-6">
        <!-- Mobile Menu Button -->
        <q-btn
          v-if="isAuthenticated"
          flat
          dense
          round
          icon="menu"
          class="md:hidden mr-3 text-gray-600 hover:text-gray-900 hover:bg-gray-100 transition-colors duration-200"
          @click="toggleMobileMenu"
        />
        <nav class="flex items-center justify-between w-full">
          <!-- Logo/Brand -->
          <router-link to="/dashboard">
            <q-toolbar-title
              class="flex flex-nowrap items-center space-x-2 cursor-pointer"
              @click="navigateTo('/dashboard')"
            >
              <div
                class="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center"
              >
                <span class="text-white font-bold text-sm">UI</span>
              </div>
              <span
                class="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent"
              >
                UInify
              </span>
            </q-toolbar-title>
          </router-link>

          <!-- Desktop Navigation - Only show when authenticated -->
          <div
            v-if="isAuthenticated"
            class="hidden lg:!flex items-center space-x-1"
          >
            <q-btn
              flat
              :class="[
                'px-4 py-2 rounded-lg font-medium transition-all duration-200',
                isActiveRoute('/dashboard')
                  ? 'bg-blue-50 text-blue-600 border border-blue-200'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50',
              ]"
              icon="dashboard"
              label="Dashboard"
              @click="navigateTo('/dashboard')"
            />
            <q-btn
              flat
              :class="[
                'px-4 py-2 rounded-lg font-medium transition-all duration-200',
                isActiveRoute('/share')
                  ? 'bg-blue-50 text-blue-600 border border-blue-200'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50',
              ]"
              icon="share"
              label="Share Component"
              @click="navigateTo('/share')"
            />
            <q-btn
              flat
              :class="[
                'px-4 py-2 rounded-lg font-medium transition-all duration-200',
                isActiveRoute('/components')
                  ? 'bg-blue-50 text-blue-600 border border-blue-200'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50',
              ]"
              icon="widgets"
              label="Components"
              @click="navigateTo('/components')"
            />
          </div>

          <!-- User Profile & Actions -->
          <div v-if="isAuthenticated" class="flex items-center space-x-3 ml-4">
            <!-- Theme Toggle -->
            <q-btn
              flat
              dense
              round
              :icon="isDarkMode ? 'light_mode' : 'dark_mode'"
              class="text-gray-600 hover:text-gray-900 hover:bg-gray-100 transition-colors duration-200"
              @click="toggleTheme"
              :title="
                isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'
              "
            />

            <!-- Notifications -->
            <q-btn
              flat
              dense
              round
              icon="notifications"
              class="text-gray-600 hover:text-gray-900 hover:bg-gray-100 transition-colors duration-200"
            >
              <q-badge color="red" floating rounded>3</q-badge>
            </q-btn>

            <!-- User Menu -->
            <q-btn-dropdown
              flat
              dense
              class="text-gray-600 hover:text-gray-900 transition-colors duration-200"
            >
              <template v-slot:label>
                <div class="flex items-center space-x-2">
                  <div
                    class="w-8 h-8 bg-gradient-to-br from-green-400 to-blue-500 rounded-full flex items-center justify-center"
                  >
                    <span class="text-white font-medium text-sm">
                      {{ userInitials }}
                    </span>
                  </div>
                  <span class="hidden md:block font-medium">{{
                    userName
                  }}</span>
                </div>
              </template>

              <q-list class="min-w-48">
                <q-item
                  clickable
                  v-close-popup
                  class="hover:bg-gray-50 transition-colors duration-200"
                >
                  <q-item-section avatar>
                    <q-icon name="person" class="text-gray-600" />
                  </q-item-section>
                  <q-item-section>
                    <q-item-label class="font-medium">Profile</q-item-label>
                  </q-item-section>
                </q-item>

                <q-item
                  clickable
                  v-close-popup
                  class="hover:bg-gray-50 transition-colors duration-200"
                >
                  <q-item-section avatar>
                    <q-icon name="settings" class="text-gray-600" />
                  </q-item-section>
                  <q-item-section>
                    <q-item-label class="font-medium">Settings</q-item-label>
                  </q-item-section>
                </q-item>

                <q-separator class="my-1" />

                <q-item
                  clickable
                  v-close-popup
                  @click="logout"
                  class="hover:bg-red-50 transition-colors duration-200"
                >
                  <q-item-section avatar>
                    <q-icon name="logout" class="text-red-600" />
                  </q-item-section>
                  <q-item-section>
                    <q-item-label class="font-medium text-red-600"
                      >Logout</q-item-label
                    >
                  </q-item-section>
                </q-item>
              </q-list>
            </q-btn-dropdown>
          </div>
        </nav>
      </q-toolbar>
    </q-header>

    <!-- Mobile Sidebar -->
    <q-drawer
      v-if="isAuthenticated"
      v-model="mobileMenuOpen"
      side="left"
      overlay
      behavior="mobile"
      class="md:hidden"
      :width="280"
    >
      <div class="h-full bg-white flex flex-col">
        <!-- Mobile Menu Header -->
        <div class="p-4 border-b border-gray-200">
          <div class="flex items-center space-x-3">
            <div
              class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center"
            >
              <span class="text-white font-bold">UI</span>
            </div>
            <div>
              <h2 class="text-lg font-bold text-gray-900">UInify</h2>
              <p class="text-sm text-gray-500">Component Library</p>
            </div>
          </div>
        </div>

        <!-- Mobile Navigation -->
        <nav class="flex-1 p-4 space-y-2">
          <q-item
            clickable
            :class="[
              'rounded-lg transition-all duration-200',
              isActiveRoute('/dashboard')
                ? 'bg-blue-50 text-blue-600 border-l-4 border-blue-600'
                : 'text-gray-700 hover:bg-gray-50',
            ]"
            @click="navigateToMobile('/dashboard')"
          >
            <q-item-section avatar>
              <q-icon name="dashboard" />
            </q-item-section>
            <q-item-section>
              <q-item-label class="font-medium">Dashboard</q-item-label>
            </q-item-section>
          </q-item>

          <q-item
            clickable
            :class="[
              'rounded-lg transition-all duration-200',
              isActiveRoute('/share')
                ? 'bg-blue-50 text-blue-600 border-l-4 border-blue-600'
                : 'text-gray-700 hover:bg-gray-50',
            ]"
            @click="navigateToMobile('/share')"
          >
            <q-item-section avatar>
              <q-icon name="share" />
            </q-item-section>
            <q-item-section>
              <q-item-label class="font-medium">Share Component</q-item-label>
            </q-item-section>
          </q-item>

          <q-item
            clickable
            :class="[
              'rounded-lg transition-all duration-200',
              isActiveRoute('/components')
                ? 'bg-blue-50 text-blue-600 border-l-4 border-blue-600'
                : 'text-gray-700 hover:bg-gray-50',
            ]"
            @click="navigateToMobile('/components')"
          >
            <q-item-section avatar>
              <q-icon name="widgets" />
            </q-item-section>
            <q-item-section>
              <q-item-label class="font-medium">Components</q-item-label>
            </q-item-section>
          </q-item>
        </nav>

        <!-- Mobile Menu Footer -->
        <div class="p-4 border-t border-gray-200">
          <q-item
            clickable
            @click="logout"
            class="rounded-lg text-red-600 hover:bg-red-50 transition-colors duration-200"
          >
            <q-item-section avatar>
              <q-icon name="logout" />
            </q-item-section>
            <q-item-section>
              <q-item-label class="font-medium">Logout</q-item-label>
            </q-item-section>
          </q-item>
        </div>
      </div>
    </q-drawer>

    <!-- Page Content -->
    <q-page-container class="bg-gray-50 min-h-screen">
      <!-- Breadcrumb -->
      <div
        v-if="isAuthenticated"
        class="bg-white border-b border-gray-200 px-4 lg:px-6 py-3"
      >
        <div class="flex items-center space-x-2 text-sm">
          <q-icon name="home" class="text-gray-400" />
          <span class="text-gray-400">/</span>
          <span class="text-gray-600 font-medium">{{ pageTitle }}</span>
        </div>
      </div>

      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRoute } from "vue-router";
import { useRouter } from "vue-router";
import { useAuthStore } from "stores/auth";
import { useQuasar } from "quasar";

const $q = useQuasar();
const auth = useAuthStore();
const router = useRouter();
const route = useRoute();

// Mobile menu state
const mobileMenuOpen = ref(false);

// Check if user is authenticated
const isAuthenticated = computed(() => {
  return !!auth?.authData?.user;
});

// Get user information
const userName = computed(() => {
  return auth?.authData?.user?.name || auth?.authData?.user?.username || "User";
});

const userInitials = computed(() => {
  const name = userName.value;
  if (name.includes(" ")) {
    const parts = name.split(" ");
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  }
  return name.substring(0, 2).toUpperCase();
});

// Check if current route is active
const isActiveRoute = (routePath) => {
  return route.path === routePath;
};

// Navigation methods
const navigateTo = (path) => {
  if (route.path !== path) {
    router.push(path);
  }
};

const navigateToMobile = (path) => {
  mobileMenuOpen.value = false;
  navigateTo(path);
};

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value;
};

const logout = () => {
  $q.dialog({
    title: "Confirm Logout",
    message: "Are you sure you want to logout?",
    cancel: true,
    persistent: true,
    class: "text-gray-800",
  }).onOk(() => {
    auth.storageAuthRemove();
    $q.notify({
      type: "positive",
      message: "Logged out successfully",
      position: "top",
    });
    router.push("/login");
  });
};

// Page title for breadcrumb
const pageTitle = computed(() => {
  const titles = {
    "/dashboard": "Dashboard",
    "/share": "Share Component",
    "/components": "Components",
    "/profile": "Profile",
    "/settings": "Settings",
  };
  return titles[route.path] || "UInify";
});

// Theme and responsive utilities
const isDarkMode = ref(false);

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value;
  $q.dark.set(isDarkMode.value);
};
</script>

<style scoped>
/* Custom styles for enhanced animations and effects */
.bg-clip-text {
  -webkit-background-clip: text;
  background-clip: text;
}

/* Smooth transitions for all interactive elements */
* {
  transition-property: color, background-color, border-color,
    text-decoration-color, fill, stroke, opacity, box-shadow, transform, filter,
    backdrop-filter;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

/* Custom scrollbar for mobile drawer */
.q-drawer :deep(.q-scrollarea__content) {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 transparent;
}

.q-drawer :deep(.q-scrollarea__content)::-webkit-scrollbar {
  width: 4px;
}

.q-drawer :deep(.q-scrollarea__content)::-webkit-scrollbar-track {
  background: transparent;
}

.q-drawer :deep(.q-scrollarea__content)::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 2px;
}

.q-drawer :deep(.q-scrollarea__content)::-webkit-scrollbar-thumb:hover {
  background-color: #94a3b8;
}
</style>
