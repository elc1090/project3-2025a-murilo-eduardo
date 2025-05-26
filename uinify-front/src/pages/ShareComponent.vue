<template>
  <q-page class="share-component-page bg-gray-50">
    <div class="max-w-6xl mx-auto px-4 py-8">
      <!-- Header -->
      <div class="text-center mb-8">
        <div class="flex items-center justify-center w-full">
          <img src="assets/uinify-logo.png" class="cursor-pointer h-[50px]" />
        </div>
        <h1 class="text-3xl font-bold text-gray-900 mb-2">
          {{ isEditMode ? "Edit Component" : "Share Your Components" }}
        </h1>
        <p class="text-lg text-gray-600 max-w-2xl mx-auto">
          {{
            isEditMode
              ? "Update your component details and code below."
              : "Upload your Vue, React, or HTML component to the UInify community."
          }}
          <br v-if="!isEditMode" />
          <span v-if="!isEditMode"
            >Help us build a unified library of components.</span
          >
        </p>
      </div>

      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <!-- Sidebar with guidelines -->
        <div class="lg:col-span-1">
          <div class="bg-white p-6 rounded-lg shadow-sm sticky top-8">
            <h3 class="text-lg font-semibold mb-4">Upload Guidelines</h3>
            <ul class="space-y-3 text-sm text-gray-600">
              <li
                class="flex flex-nowrap items-start"
                v-for="(item, idx) in [
                  'Ensure your component is reusable and well-documented',
                  'Use clear, descriptive names and titles',
                  'Add relevant tags for discoverability',
                  'Test your component thoroughly before sharing',
                  'Follow community guidelines and be respectful',
                ]"
                :key="idx"
              >
                <q-icon name="check" class="text-green-500 mt-0.5 mr-2" />
                <span>{{ item }}</span>
              </li>
            </ul>

            <div class="mt-6 pt-6 border-t border-gray-200">
              <h4 class="text-sm font-medium text-gray-900 mb-2">
                Popular Tags
              </h4>
              <div class="flex flex-wrap gap-2">
                <q-chip
                  v-for="tag in popularTags"
                  :key="tag"
                  color="primary"
                  text-color="white"
                >
                  {{ tag }}
                </q-chip>
              </div>
            </div>
          </div>
        </div>

        <!-- Main Form -->
        <div class="lg:col-span-3">
          <ComponentUploadForm
            :component-data="componentData"
            :is-edit-mode="isEditMode"
            :component-id="componentId"
          />
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import ComponentUploadForm from "../components/ComponentUploadForm.vue";
import { useRoute } from "vue-router";
import { getComponentById } from "src/services/DefaultService";

// Props for route parameters
const props = defineProps({
  id: {
    type: String,
    default: null,
  },
});

const route = useRoute();

const popularTags = ref([
  "Vue3",
  "Quasar",
  "Tailwind",
  "UI",
  "Form",
  "Button",
  "Card",
  "Animation",
  "Responsive",
  "Dashboard",
]);

const componentData = ref(null);

// Computed to get component ID from props or route
const componentId = computed(() => {
  return props.id || route.params.id;
});

// Computed to determine if we're in edit mode
const isEditMode = computed(() => {
  return !!componentId.value;
});

const fetchComponentData = async () => {
  if (!componentId.value) return;

  try {
    const { data } = await getComponentById(componentId.value);
    componentData.value = data;
  } catch (error) {
    console.error("Error fetching component data:", error);
  }
};

onMounted(() => {
  if (componentId.value) {
    fetchComponentData();
  }
});
</script>

<style scoped>
.share-component-page {
  min-height: calc(100vh - 64px);
}
</style>
