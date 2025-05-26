<template>
  <div class="component-upload-form">
    <q-form @submit.prevent="handleSubmit" class="space-y-6">
      <!-- Component Details -->
      <div class="bg-white p-6 rounded-lg shadow-sm">
        <h3 class="text-xl font-semibold mb-4">Component Details</h3>

        <q-input
          v-model="formData.title"
          label="Component Title *"
          outlined
          :rules="[(val) => !!val || 'Title is required']"
          class="mb-4"
        />

        <q-input
          v-model="formData.description"
          label="Description"
          outlined
          type="textarea"
          class="mb-4"
        />

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <q-select
            v-model="formData.framework"
            label="Framework *"
            outlined
            :options="frameworkOptions"
            :rules="[(val) => !!val || 'Framework is required']"
          />

          <q-select
            v-model="formData.category"
            label="Category *"
            outlined
            :options="categoryOptions"
            :rules="[(val) => !!val || 'Category is required']"
          />
        </div>

        <q-input
          v-model="formData.tags"
          label="Tags"
          outlined
          hint="Separate tags with commas"
        >
          <template v-slot:after>
            <q-btn
              round
              dense
              flat
              icon="add"
              @click="addTag"
              title="Add tag"
            />
          </template>
        </q-input>

        <div class="flex flex-wrap gap-2 mt-2">
          <q-chip
            v-for="(tag, index) in formData.tagsArray"
            :key="index"
            removable
            @remove="removeTag(index)"
          >
            {{ tag }}
          </q-chip>
        </div>
      </div>

      <!-- Code Editor Section -->
      <div class="bg-white p-6 rounded-lg shadow-sm">
        <h3 class="text-xl font-semibold mb-4">Component Code</h3>

        <div class="mb-4">
          <q-radio v-model="formData.inputType" val="html" label="HTML" />
          <q-radio
            v-model="formData.inputType"
            val="vue"
            label="Vue SFC"
            class="ml-4"
          />
        </div>

        <div
          class="editor-container border border-gray-200 rounded-lg overflow-hidden"
        >
          <div
            class="editor-toolbar bg-gray-100 px-4 py-2 flex justify-between items-center"
          >
            <span class="text-sm font-medium">Component Code *</span>
            <q-btn
              flat
              dense
              icon="content_copy"
              label="Copy"
              @click="copyToClipboard"
              size="sm"
            />
          </div>
          <MonacoEditor
            v-model="formData.code"
            :language="formData.inputType === 'vue' ? 'vue' : 'html'"
            height="300px"
            theme="vs"
            class="code-editor"
          />
        </div>

        <q-checkbox
          v-model="formData.includeTailwind"
          label="Include Tailwind CSS"
          class="mt-4"
        />

        <!-- Temporarily disabled Quasar option -->
        <!--
        <q-checkbox
          v-model="formData.includeQuasar"
          label="Include Quasar Framework"
          class="mt-2"
        />
        -->
      </div>

      <!-- Preview Section -->
      <div class="bg-white p-6 rounded-lg shadow-sm">
        <h3 class="text-xl font-semibold mb-4">Live Preview</h3>
        <ComponentViewer
          :content="formData.code"
          :framework="formData.inputType === 'vue' ? 'vue' : 'html'"
          :include-tailwind="formData.includeTailwind"
          :include-quasar="formData.includeQuasar"
        />
      </div>

      <!-- Actions -->
      <div class="flex justify-end space-x-4">
        <q-btn
          label="Reset"
          type="reset"
          color="grey"
          flat
          @click="resetForm"
        />
        <q-btn
          label="Upload Component"
          type="submit"
          color="primary"
          :loading="isSubmitting"
        />
      </div>
    </q-form>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import { useQuasar } from "quasar";
import ComponentViewer from "./ComponentViewer.vue";
import MonacoEditor from "./MonacoEditor.vue";
import { saveComponent } from "src/services/DefaultService";
import { useAuthStore } from "stores/auth";

const $q = useQuasar();
const auth = useAuthStore();

const formData = ref({
  title: "",
  description: "",
  framework: "vue",
  category: "ui",
  tags: "",
  tagsArray: [],
  code: `<template>
  <div class="p-6 bg-white rounded-lg shadow-lg border border-gray-200">
    <h2 class="text-2xl font-bold text-gray-800 mb-3">{{ title }}</h2>
    <p class="text-gray-600 mb-4">{{ description }}</p>

    <button
      @click="handleClick"
      class="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded-md transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
    >
      Click Me
    </button>

    <div
      v-if="clicked"
      class="mt-4 inline-block bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium animate-pulse border border-green-200"
    >
      ✅ Button clicked successfully!
    </div>

    <div class="mt-4 flex items-center justify-between">
      <div class="text-sm text-gray-500">
        Count: <span class="font-semibold text-gray-700">{{ clickCount }}</span>
      </div>
      <button
        v-if="clickCount > 0"
        @click="resetCount"
        class="text-xs text-red-500 hover:text-red-700 underline"
      >
        Reset
      </button>
    </div>

    <div v-if="clickCount >= 5" class="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
      <p class="text-sm text-yellow-800">
        🎉 Wow! You've clicked {{ clickCount }} times! You're really testing this component!
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// Reactive data
const title = ref('New Component')
const description = ref('Edit this code to create your component with Vue 3 + Tailwind')
const clicked = ref(false)
const clickCount = ref(0)

// Computed properties
const isActive = computed(() => clickCount.value > 0)

// Methods
const handleClick = () => {
  clicked.value = true
  clickCount.value++

  console.log('Button clicked! Count:', clickCount.value)

  // Reset the clicked state after 3 seconds
  setTimeout(() => {
    clicked.value = false
  }, 3000)
}

const resetCount = () => {
  clickCount.value = 0
  clicked.value = false
  console.log('Count reset!')
}

// Lifecycle
onMounted(() => {
  console.log('Component mounted with Vue 3 Composition API!')
})
<\/script>`,
  inputType: "vue",
  includeTailwind: true,
  includeQuasar: false,
});

const frameworkOptions = [
  { label: "Vue 3", value: "vue" },
  { label: "React", value: "react" },
  { label: "HTML/CSS/JS", value: "html" },
];

const categoryOptions = [
  { label: "UI Elements", value: "ui" },
  { label: "Forms", value: "forms" },
  { label: "Navigation", value: "navigation" },
  { label: "Cards", value: "cards" },
  { label: "Data Display", value: "data" },
  { label: "Layout", value: "layout" },
];

const isSubmitting = ref(false);

const addTag = () => {
  if (formData.value.tags.trim()) {
    const newTags = formData.value.tags
      .split(",")
      .map((tag) => tag.trim())
      .filter((tag) => tag && !formData.value.tagsArray.includes(tag));

    formData.value.tagsArray = [...formData.value.tagsArray, ...newTags];
    formData.value.tags = "";
  }
};

const removeTag = (index) => {
  formData.value.tagsArray.splice(index, 1);
};

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(formData.value.code);
    $q.notify({
      type: "positive",
      message: "Code copied to clipboard!",
    });
  } catch (err) {
    $q.notify({
      type: "negative",
      message: "Failed to copy code",
    });
  }
};

const validateForm = () => {
  const errors = [];

  if (!formData.value.title.trim()) {
    errors.push("Component title is required");
  }

  if (!formData.value.framework) {
    errors.push("Framework selection is required");
  }

  if (!formData.value.category) {
    errors.push("Category selection is required");
  }

  if (!formData.value.code.trim()) {
    errors.push("Component code is required");
  }

  return errors;
};

const resetForm = () => {
  formData.value = {
    title: "",
    description: "",
    framework: "vue",
    category: "ui",
    tags: "",
    tagsArray: [],
    code: `<template>
  <div class="p-6 bg-white rounded-lg shadow-lg border border-gray-200">
    <h2 class="text-2xl font-bold text-gray-800 mb-3">{{ title }}</h2>
    <p class="text-gray-600 mb-4">{{ description }}</p>

    <button
      @click="handleClick"
      class="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded-md transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
    >
      Click Me
    </button>

    <div
      v-if="clicked"
      class="mt-4 inline-block bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium animate-pulse border border-green-200"
    >
      ✅ Button clicked successfully!
    </div>

    <div class="mt-4 flex items-center justify-between">
      <div class="text-sm text-gray-500">
        Count: <span class="font-semibold text-gray-700">{{ clickCount }}</span>
      </div>
      <button
        v-if="clickCount > 0"
        @click="resetCount"
        class="text-xs text-red-500 hover:text-red-700 underline"
      >
        Reset
      </button>
    </div>

    <div v-if="clickCount >= 5" class="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
      <p class="text-sm text-yellow-800">
        🎉 Wow! You've clicked {{ clickCount }} times! You're really testing this component!
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// Reactive data
const title = ref('New Component')
const description = ref('Edit this code to create your component with Vue 3 + Tailwind')
const clicked = ref(false)
const clickCount = ref(0)

// Computed properties
const isActive = computed(() => clickCount.value > 0)

// Methods
const handleClick = () => {
  clicked.value = true
  clickCount.value++

  console.log('Button clicked! Count:', clickCount.value)

  // Reset the clicked state after 3 seconds
  setTimeout(() => {
    clicked.value = false
  }, 3000)
}

const resetCount = () => {
  clickCount.value = 0
  clicked.value = false
  console.log('Count reset!')
}

// Lifecycle
onMounted(() => {
  console.log('Component mounted with Vue 3 Composition API!')
})
<\/script>`,
    inputType: "vue",
    includeTailwind: true,
    includeQuasar: false,
  };
};

const handleSubmit = async () => {
  // Validate form before submitting
  const validationErrors = validateForm();
  if (validationErrors.length > 0) {
    $q.notify({
      type: "negative",
      message: validationErrors.join(", "),
      position: "top",
    });
    return;
  }

  isSubmitting.value = true;

  try {
    // Prepare the payload for the backend
    const payload = {
      title: formData.value.title,
      description: formData.value.description,
      framework: formData.value.framework.value || formData.value.framework,
      category: formData.value.category.value || formData.value.category,
      tags: formData.value.tagsArray,
      code: formData.value.code,
      inputType: formData.value.inputType,
      includeTailwind: formData.value.includeTailwind,
      includeQuasar: formData.value.includeQuasar,
      user_id: auth.authData.user.id,
    };

    console.log("Sending payload to backend:", payload);

    // Call the backend API
    const response = await saveComponent(payload);

    console.log("Component saved successfully:", response.data);

    // Show success message
    $q.notify({
      type: "positive",
      message: "Component uploaded successfully!",
      position: "top",
    });

    // Reset the form after successful upload
    resetForm();
  } catch (error) {
    console.error("Error uploading component:", error);

    // Show error message
    $q.notify({
      type: "negative",
      message:
        error.response?.data?.message ||
        "Failed to upload component. Please try again.",
      position: "top",
    });
  } finally {
    isSubmitting.value = false;
  }
};

// Watch for tag input changes to add tags on comma
watch(
  () => formData.value.tags,
  (newVal) => {
    if (newVal.endsWith(",")) {
      addTag();
    }
  }
);

// Watch for input type changes to update the editor language
watch(
  () => formData.value.inputType,
  () => {
    // The language will be updated automatically through the :language binding
    // This watch is here in case we need to add more logic in the future
  }
);
</script>

<style scoped>
.editor-container {
  transition: all 0.2s ease;
}

.code-editor {
  width: 100%;
  border-radius: 4px;
  overflow: hidden;
}

:deep(.monaco-editor) {
  border-radius: 4px;
  padding: 0;
}
</style>
