<template>
  <div class="monaco-editor-container" :style="{ height: height }">
    <div ref="editorContainer" class="editor-instance"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue';
import * as monaco from 'monaco-editor';
import loader from '@monaco-editor/loader';

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  language: {
    type: String,
    default: 'html'
  },
  theme: {
    type: String,
    default: 'vs'
  },
  height: {
    type: String,
    default: '300px'
  },
  options: {
    type: Object,
    default: () => ({})
  }
});

const emit = defineEmits(['update:modelValue', 'editor-mounted']);

const editorContainer = ref(null);
let editor = null;

// Initialize the editor
onMounted(async () => {
  if (!editorContainer.value) return;

  // Load Monaco editor
  await loader.init();
  
  // Create editor with options
  const defaultOptions = {
    value: props.modelValue,
    language: props.language,
    theme: props.theme,
    automaticLayout: true,
    minimap: { enabled: false },
    scrollBeyondLastLine: false,
    lineNumbers: 'on',
    roundedSelection: true,
    scrollbar: {
      useShadows: false,
      verticalScrollbarSize: 10,
      horizontalScrollbarSize: 10,
      alwaysConsumeMouseWheel: false
    },
    fontSize: 14,
    fontFamily: "'Fira Code', 'Courier New', monospace",
    tabSize: 2
  };

  // Merge default options with user options
  const editorOptions = { ...defaultOptions, ...props.options };
  
  // Create the editor instance
  editor = monaco.editor.create(editorContainer.value, editorOptions);
  
  // Handle content changes
  editor.onDidChangeModelContent(() => {
    const value = editor.getValue();
    emit('update:modelValue', value);
  });
  
  // Emit the mounted event with the editor instance
  emit('editor-mounted', editor);
});

// Watch for external value changes
watch(() => props.modelValue, (newValue) => {
  if (editor && newValue !== editor.getValue()) {
    editor.setValue(newValue);
  }
});

// Watch for language changes
watch(() => props.language, (newLanguage) => {
  if (editor) {
    monaco.editor.setModelLanguage(editor.getModel(), newLanguage);
  }
});

// Watch for theme changes
watch(() => props.theme, (newTheme) => {
  if (editor) {
    monaco.editor.setTheme(newTheme);
  }
});

// Clean up on component unmount
onBeforeUnmount(() => {
  if (editor) {
    editor.dispose();
  }
});
</script>

<style scoped>
.monaco-editor-container {
  width: 100%;
  border-radius: 4px;
  overflow: hidden;
}

.editor-instance {
  width: 100%;
  height: 100%;
}
</style>
