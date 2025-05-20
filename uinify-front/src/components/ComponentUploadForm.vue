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

        <q-checkbox
          v-model="formData.includeQuasar"
          label="Include Quasar Framework"
          class="mt-2"
        />
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

const $q = useQuasar();

const formData = ref({
  title: "",
  description: "",
  framework: "vue",
  category: "ui",
  tags: "",
  tagsArray: [],
  code: `<template>
  <div class="p-4 bg-white rounded-lg shadow-sm">
    <h2 class="text-xl font-semibold mb-2">New Component</h2>
    <p class="text-gray-600">Edit this code to create your component</p>
    <q-btn
      color="primary"
      label="Click Me"
      class="mt-4"
    />
  </div>
</template>`,
  inputType: "vue",
  includeTailwind: true,
  includeQuasar: true,
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

const resetForm = () => {
  formData.value = {
    title: "",
    description: "",
    framework: "vue",
    category: "ui",
    tags: "",
    tagsArray: [],
    code: `<template>
  <div class="p-4 bg-white rounded-lg shadow-sm">
    <h2 class="text-xl font-semibold mb-2">New Component</h2>
    <p class="text-gray-600">Edit this code to create your component</p>
    <q-btn
      color="primary"
      label="Click Me"
      class="mt-4"
    />
  </div>
</template>`,
    inputType: "vue",
    includeTailwind: true,
    includeQuasar: true,
  };
};

const handleSubmit = () => {
  isSubmitting.value = true;

  // Simulate API call
  setTimeout(() => {
    $q.notify({
      type: "positive",
      message: "Component uploaded successfully!",
    });
    isSubmitting.value = false;
    // In a real app, you would redirect to the component page or reset the form
  }, 1500);
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
