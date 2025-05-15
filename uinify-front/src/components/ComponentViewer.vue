<template>
  <div class="component-viewer bg-gray-50 rounded-lg shadow-md overflow-hidden">
    <!-- Header with title and controls -->
    <div
      class="flex items-center justify-between p-4 bg-gray-100 border-b border-gray-200"
    >
      <h3 class="text-lg font-semibold text-gray-800">Component Preview</h3>
      <div class="flex space-x-2">
        <q-btn
          round
          dense
          flat
          icon="refresh"
          @click="refreshIframe"
          class="text-gray-600 hover:bg-gray-200"
          title="Refresh preview"
        />
        <q-btn
          round
          dense
          flat
          icon="fullscreen"
          @click="toggleFullscreen"
          class="text-gray-600 hover:bg-gray-200"
          title="Toggle fullscreen"
        />
      </div>
    </div>

    <!-- Iframe container with responsive sizing -->
    <div
      class="iframe-container relative w-full bg-white"
      :class="{
        'fixed inset-0 z-50 bg-white !h-screen !w-screen': isFullscreen,
        'h-96': !isFullscreen,
      }"
    >
      <!-- Close button in fullscreen mode -->
      <q-btn
        v-if="isFullscreen"
        round
        dense
        flat
        icon="close"
        @click="toggleFullscreen"
        class="absolute top-4 right-4 z-10 bg-white shadow-md"
        title="Exit fullscreen"
      />

      <!-- The actual iframe -->
      <iframe
        ref="iframeRef"
        :srcdoc="processedContent"
        class="w-full h-full border-0"
        sandbox="allow-scripts allow-same-origin"
        @load="onIframeLoad"
      ></iframe>

      <!-- Loading indicator -->
      <div
        v-if="isLoading"
        class="absolute inset-0 flex items-center justify-center bg-gray-50 bg-opacity-70"
      >
        <q-spinner color="primary" size="3em" />
        <span class="ml-2 text-gray-700">Loading component...</span>
      </div>
    </div>

    <!-- Dimensions info -->
    <div
      v-if="!isFullscreen"
      class="p-2 bg-gray-100 text-xs text-gray-500 text-center"
    >
      {{ iframeDimensions.width }} × {{ iframeDimensions.height }} px
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { useQuasar } from "quasar";

const $q = useQuasar();

const props = defineProps({
  content: {
    type: String,
    required: true,
    default:
      '<div class="p-4 text-center text-gray-500">No component content provided</div>',
  },
  baseStyles: {
    type: String,
    default: "",
  },
  includeTailwind: {
    type: Boolean,
    default: true,
  },
  includeQuasar: {
    type: Boolean,
    default: true,
  },
  framework: {
    type: String,
    default: "vue",
  },
});

const iframeRef = ref(null);
const isLoading = ref(true);
const isFullscreen = ref(false);
const iframeDimensions = ref({ width: 0, height: 0 });

// Process the content to include necessary styles and scripts
const processedContent = computed(() => {
  // Note: Using Tailwind CDN is not recommended for production
  // The warning "cdn.tailwindcss.com should not be used in production" is expected
  // For production, consider using Tailwind as a PostCSS plugin or via the Tailwind CLI
  const tailwindLink = props.includeTailwind
    ? '<script src="https://cdn.tailwindcss.com/3.4.1"><\/script>'
    : "";

  const quasarLinks = props.includeQuasar
    ? '<link href="https://cdn.jsdelivr.net/npm/quasar@2/dist/quasar.dev.css" rel="stylesheet">'
    : "";

  const vueScript =
    props.framework === "vue"
      ? '<script src="https://cdn.jsdelivr.net/npm/vue@3.3.4/dist/vue.global.js"><\/script>'
      : "";

  const quasarScript =
    props.includeQuasar && props.framework === "vue"
      ? '<script src="https://cdn.jsdelivr.net/npm/quasar@2/dist/quasar.umd.js"><\/script>'
      : "";

  const mountScript =
    props.framework === "vue"
      ? `<script>
        // We'll create the mount point with a small delay to ensure the DOM is ready
        // This helps prevent the "Cannot read properties of null (reading 'appendChild')" error
        setTimeout(() => {
          try {
            const mountPoint = document.createElement('div');
            mountPoint.id = 'app-mount-point';
            document.body.appendChild(mountPoint);
            console.log('Mount point created successfully');
          } catch (e) {
            console.error('Error creating mount point:', e);
          }
        }, 10);

        // Wait for both DOM and scripts to be ready
        function tryMount() {
          if (!window.Vue) {
            setTimeout(tryMount, 50);
            return;
          }

          function mountVueApp() {
            try {
              // Make sure the mount point exists
              let mountElement = document.getElementById('app-mount-point');
              if (!mountElement) {
                console.warn('Mount point not found, creating a new one');
                mountElement = document.createElement('div');
                mountElement.id = 'app-mount-point';
                document.body.appendChild(mountElement);
              }

              const app = Vue.createApp({
                template: \`<div>${props.content}</div>\`,
                data() { return {}; }
              });

              // Only use Quasar if it's available
              ${
                props.includeQuasar ? "if (window.Quasar) app.use(Quasar);" : ""
              }

              app.mount('#app-mount-point');
              console.log('Vue app mounted successfully');
            } catch(e) {
              console.error('Error mounting Vue:', e);
              const errorElement = document.getElementById('app-mount-point') || document.body;
              errorElement.innerHTML = \`<div class="p-4 bg-red-50 text-red-600">
                <p>Error rendering component:</p>
                <pre>\${e.message}</pre>
                <p>Check the console for details.</p>
              </div>\`;
            }
          }

          ${
            props.includeQuasar
              ? `
            // Check if Quasar is available, if not wait for it with a timeout
            if (window.Quasar) {
              mountVueApp();
            } else {
              console.log('Waiting for Quasar to load...');
              let attempts = 0;
              const maxAttempts = 20; // 1 second total wait time

              const interval = setInterval(() => {
                attempts++;
                if (window.Quasar) {
                  clearInterval(interval);
                  console.log('Quasar loaded, mounting app');
                  mountVueApp();
                } else if (attempts >= maxAttempts) {
                  clearInterval(interval);
                  console.warn('Quasar failed to load after timeout, attempting to mount without it');
                  mountVueApp(); // Try to mount anyway
                }
              }, 50);
            }
          `
              : `
            // No Quasar needed, mount directly
            mountVueApp();
          `
          }
        }

        // Start the mounting process
        if (document.readyState === 'loading') {
          document.addEventListener('DOMContentLoaded', tryMount);
        } else {
          tryMount();
        }
      <\/script>`
      : "";

  return `
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        ${tailwindLink}
        ${quasarLinks}
        ${vueScript}
        ${quasarScript}
        <style>
          body { margin: 0; padding: 0; font-family: sans-serif; }
          ${props.baseStyles}
        </style>
      </head>
      <body>
        ${props.framework === "vue" ? "" : props.content}
        ${mountScript}
      </body>
    </html>
  `;
});

// Watch for content changes to trigger reload
watch(
  () => props.content,
  () => {
    isLoading.value = true;
  }
);

const onIframeLoad = () => {
  isLoading.value = false;

  try {
    // Try to get dimensions from the iframe content
    const iframeDoc =
      iframeRef.value.contentDocument || iframeRef.value.contentWindow.document;
    const body = iframeDoc.body;
    const html = iframeDoc.documentElement;

    iframeDimensions.value = {
      width: Math.max(
        body.scrollWidth,
        body.offsetWidth,
        html.scrollWidth,
        html.offsetWidth
      ),
      height: Math.max(
        body.scrollHeight,
        body.offsetHeight,
        html.scrollHeight,
        html.offsetHeight
      ),
    };
  } catch (e) {
    console.warn("Could not access iframe dimensions:", e);
    iframeDimensions.value = { width: 0, height: 0 };
  }
};

const refreshIframe = () => {
  if (!iframeRef.value) return;
  isLoading.value = true;

  // Force iframe to reload by temporarily clearing srcdoc
  const currentContent = iframeRef.value.srcdoc;
  iframeRef.value.srcdoc = "";
  setTimeout(() => {
    iframeRef.value.srcdoc = currentContent;
  }, 50);
};

const toggleFullscreen = () => {
  isFullscreen.value = !isFullscreen.value;

  if (isFullscreen.value) {
    document.body.style.overflow = "hidden";
  } else {
    document.body.style.overflow = "";
  }
};

// Cleanup on unmount
onMounted(() => {
  return () => {
    document.body.style.overflow = "";
  };
});
</script>

<style scoped>
.component-viewer {
  transition: all 0.3s ease;
}

.iframe-container {
  transition: all 0.3s ease;
}
</style>
