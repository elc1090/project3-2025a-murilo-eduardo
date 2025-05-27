<template>
  <div
    class="component-viewer bg-white rounded-lg shadow-lg overflow-hidden border"
  >
    <!-- Enhanced Header with title and controls -->
    <div
      class="flex items-center justify-between p-4 bg-gradient-to-r from-blue-50 to-indigo-50 border-b"
    >
      <div class="flex items-center space-x-3">
        <q-icon name="visibility" color="primary" size="sm" />
        <h3 class="text-lg font-semibold text-gray-800">Live Preview</h3>
        <q-chip
          v-if="renderStatus"
          :color="
            renderStatus === 'success'
              ? 'positive'
              : renderStatus === 'error'
              ? 'negative'
              : 'warning'
          "
          text-color="white"
          size="sm"
          :label="renderStatus"
        />
      </div>
      <div class="flex items-center space-x-2">
        <!-- Device size selector -->
        <q-btn-dropdown
          flat
          dense
          :icon="currentDevice.icon"
          :label="currentDevice.name"
          class="text-gray-600"
        >
          <q-list>
            <q-item
              v-for="device in deviceSizes"
              :key="device.name"
              clickable
              @click="setDevice(device)"
              :class="{ 'bg-blue-50': currentDevice.name === device.name }"
            >
              <q-item-section avatar>
                <q-icon :name="device.icon" />
              </q-item-section>
              <q-item-section>
                <q-item-label>{{ device.name }}</q-item-label>
                <q-item-label caption>{{ device.width }}px</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>

        <q-separator vertical />

        <q-btn
          round
          dense
          flat
          icon="refresh"
          @click="refreshIframe"
          class="text-gray-600 hover:bg-gray-200"
        >
          <q-tooltip>Refresh preview</q-tooltip>
        </q-btn>

        <q-btn
          round
          dense
          flat
          icon="code"
          @click="showCode = !showCode"
          :color="showCode ? 'primary' : 'grey'"
          class="hover:bg-gray-200"
        >
          <q-tooltip>{{ showCode ? "Hide" : "Show" }} code</q-tooltip>
        </q-btn>

        <q-btn
          round
          dense
          flat
          icon="fullscreen"
          @click="toggleFullscreen"
          class="text-gray-600 hover:bg-gray-200"
        >
          <q-tooltip>Toggle fullscreen</q-tooltip>
        </q-btn>
      </div>
    </div>

    <!-- Code display (collapsible) -->
    <q-slide-transition>
      <div v-show="showCode" class="border-b bg-gray-50">
        <div class="p-4">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-medium text-gray-700"
              >Component Code</span
            >
            <q-btn
              flat
              dense
              icon="content_copy"
              label="Copy"
              @click="copyCode"
              size="sm"
              color="primary"
            />
          </div>
          <pre
            class="bg-gray-900 text-green-400 p-4 rounded-lg text-sm overflow-x-auto max-h-40"
          ><code>{{ props.content }}</code></pre>
        </div>
      </div>
    </q-slide-transition>

    <!-- Enhanced Iframe container with device simulation -->
    <div
      class="iframe-container relative bg-gray-100 flex items-center justify-center"
      :class="{
        'fixed inset-0 z-50 bg-gray-100': isFullscreen,
        'min-h-96 p-4': !isFullscreen,
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
        class="absolute top-4 right-4 z-10 bg-white shadow-lg"
      >
        <q-tooltip>Exit fullscreen</q-tooltip>
      </q-btn>

      <!-- Device frame -->
      <div
        class="device-frame bg-white rounded-lg shadow-lg overflow-hidden transition-all duration-300"
        :style="deviceFrameStyle"
      >
        <!-- Device header (optional) -->
        <div
          v-if="currentDevice.showHeader"
          class="device-header bg-gray-800 h-6 flex items-center justify-center"
        >
          <div class="flex space-x-1">
            <div class="w-2 h-2 bg-red-500 rounded-full"></div>
            <div class="w-2 h-2 bg-yellow-500 rounded-full"></div>
            <div class="w-2 h-2 bg-green-500 rounded-full"></div>
          </div>
        </div>

        <!-- The actual iframe -->
        <iframe
          ref="iframeRef"
          :srcdoc="processedContent"
          class="w-full h-full border-0"
          sandbox="allow-scripts allow-same-origin allow-popups allow-modals"
          @load="onIframeLoad"
          @error="onIframeError"
        ></iframe>

        <!-- Error overlay -->
        <div
          v-if="renderError"
          class="absolute inset-0 flex items-center justify-center bg-red-50 bg-opacity-95"
        >
          <div class="text-center p-6">
            <q-icon name="error" color="negative" size="3em" class="mb-4" />
            <h4 class="text-lg font-semibold text-red-800 mb-2">
              Rendering Error
            </h4>
            <p class="text-red-600 mb-4">{{ renderError }}</p>
            <q-btn
              color="negative"
              outline
              label="Retry"
              @click="refreshIframe"
            />
          </div>
        </div>

        <!-- Loading indicator -->
        <div
          v-if="isLoading"
          class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-90"
        >
          <div class="flex flex-col items-center w-full">
            <q-spinner color="primary" size="3em" class="mb-4" />
            <p class="text-gray-700 font-medium">Rendering component...</p>
            <p class="text-gray-500 text-sm">{{ loadingMessage }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Enhanced footer with more info -->
    <div
      v-if="!isFullscreen"
      class="p-3 bg-gray-50 border-t flex items-center justify-between text-sm"
    >
      <div class="flex items-center space-x-4 text-gray-600">
        <span>
          <q-icon name="aspect_ratio" size="xs" class="mr-1" />
          {{ iframeDimensions.width }} × {{ iframeDimensions.height }}px
        </span>
        <span v-if="renderTime">
          <q-icon name="schedule" size="xs" class="mr-1" />
          {{ renderTime }}ms
        </span>
        <span>
          <q-icon name="devices" size="xs" class="mr-1" />
          {{ currentDevice.name }}
        </span>
      </div>
      <div class="flex items-center space-x-2">
        <span
          v-if="props.includeTailwind"
          class="px-2 py-1 text-xs font-medium bg-cyan-500 text-white rounded"
        >
          Tailwind
        </span>
        <span
          class="px-2 py-1 text-xs font-medium bg-green-500 text-white rounded"
        >
          {{ props.framework }}
        </span>
      </div>
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
const showCode = ref(false);
const renderError = ref(null);
const renderStatus = ref(null);
const renderTime = ref(null);
const loadingMessage = ref("Initializing...");

// Device simulation
const deviceSizes = ref([
  {
    name: "Desktop",
    width: "100%",
    height: "auto",
    icon: "desktop_windows",
    showHeader: true,
  },
  {
    name: "Laptop",
    width: "1024px",
    height: "auto",
    icon: "laptop",
    showHeader: true,
  },
  {
    name: "Tablet",
    width: "768px",
    height: "auto",
    icon: "tablet",
    showHeader: false,
  },
  {
    name: "Mobile",
    width: "375px",
    height: "auto",
    icon: "phone_android",
    showHeader: false,
  },
  {
    name: "Mobile Small",
    width: "320px",
    height: "auto",
    icon: "smartphone",
    showHeader: false,
  },
]);

const currentDevice = ref(deviceSizes.value[0]);

const deviceFrameStyle = computed(() => ({
  width:
    currentDevice.value.width === "100%" ? "100%" : currentDevice.value.width,
  maxWidth: "100%",
  height:
    currentDevice.value.height === "auto"
      ? "500px"
      : currentDevice.value.height,
  minHeight: "300px",
}));

// Process the content to include necessary styles and scripts
const processedContent = computed(() => {
  // Enhanced CDN links with better versions and fallbacks
  const tailwindLink = props.includeTailwind
    ? `<script src="https://cdn.tailwindcss.com/3.4.1"><\/script>
       <script>
         tailwind.config = {
           theme: {
             extend: {
               animation: {
                 'fade-in': 'fadeIn 0.5s ease-in-out',
                 'slide-up': 'slideUp 0.3s ease-out',
               }
             }
           }
         }
       <\/script>`
    : "";

  const vueScript =
    props.framework === "vue"
      ? '<script src="https://cdn.jsdelivr.net/npm/vue@3.4.15/dist/vue.global.js"><\/script>'
      : "";

  // Safely encode the content to avoid JavaScript injection issues
  const safeContent = btoa(unescape(encodeURIComponent(props.content)));

  const mountScript =
    props.framework === "vue"
      ? `<script>
        console.log('🚀 Starting component rendering...');
        const startTime = performance.now();

        // Enhanced error handling and status reporting
        function reportStatus(status, message) {
          console.log('📊 Status: ' + status + ' - ' + message);
          window.parent.postMessage({
            type: 'render-status',
            status: status,
            message: message,
            timestamp: Date.now()
          }, '*');
        }

        function reportError(error) {
          console.error('❌ Render Error:', error);
          window.parent.postMessage({
            type: 'render-error',
            error: error.message || error,
            timestamp: Date.now()
          }, '*');
        }

        function reportSuccess(renderTime) {
          console.log('✅ Component rendered successfully in ' + renderTime + 'ms');
          window.parent.postMessage({
            type: 'render-success',
            renderTime: renderTime,
            timestamp: Date.now()
          }, '*');
        }

        // Create mount point with better error handling
        function createMountPoint() {
          try {
            reportStatus('loading', 'Creating mount point...');

            // Remove any existing mount point
            const existingMount = document.getElementById('app-mount-point');
            if (existingMount) {
              existingMount.remove();
            }

            const mountPoint = document.createElement('div');
            mountPoint.id = 'app-mount-point';
            mountPoint.style.cssText = 'width: 100%; min-height: 100px; padding: 0; margin: 0;';

            // Ensure body exists and append
            if (document.body) {
              document.body.appendChild(mountPoint);
              console.log('✅ Mount point created successfully');
              return true;
            } else {
              console.warn('⚠️ Document body not ready, retrying...');
              return false;
            }
          } catch (e) {
            console.error('❌ Error creating mount point:', e);
            reportError(e);
            return false;
          }
        }

        // Wait for DOM to be ready before creating mount point
        function waitForDOM() {
          if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
              if (createMountPoint()) {
                tryMount();
              }
            });
          } else {
            if (createMountPoint()) {
              tryMount();
            }
          }
        }

        // Enhanced mounting function with better error handling
        function tryMount() {
          if (!window.Vue) {
            reportStatus('loading', 'Waiting for Vue.js...');
            setTimeout(tryMount, 50);
            return;
          }

          function mountVueApp() {
            try {
              reportStatus('loading', 'Mounting Vue application...');

              // Ensure mount point exists
              let mountElement = document.getElementById('app-mount-point');
              if (!mountElement) {
                console.warn('⚠️ Mount point not found, creating a new one');
                mountElement = document.createElement('div');
                mountElement.id = 'app-mount-point';
                mountElement.style.width = '100%';
                mountElement.style.minHeight = '100px';
                document.body.appendChild(mountElement);
              }

              // Process the content to handle Vue templates properly
              let processedTemplate = '';
              let componentOptions = {};

              try {
                // Decode the safely encoded content
                const rawContent = decodeURIComponent(escape(atob('${safeContent}')));
                processedTemplate = rawContent;

                // Check if content contains <template> tags (Vue SFC format)
                if (rawContent.includes('<template>')) {
                  console.log('🔍 Detected Vue SFC format, extracting template...');

                  // Extract template content
                  const templateMatch = rawContent.match(/<template[^>]*>([\\s\\S]*?)<\\/template>/);
                  if (templateMatch) {
                    processedTemplate = templateMatch[1].trim();
                    console.log('✅ Template extracted successfully');
                  }

                  // Extract script content if present
                  const scriptMatch = rawContent.match(/<script[^>]*>([\\s\\S]*?)<\\/script>/);
                  if (scriptMatch) {
                    try {
                      const scriptContent = scriptMatch[1].trim();
                      console.log('🔍 Found script section, parsing...');

                      // Check if it's a <script setup> format
                      const scriptTag = rawContent.match(/<script[^>]*>/)[0];
                      const isScriptSetup = scriptTag.includes('setup');

                      if (isScriptSetup) {
                        console.log('📝 Detected Vue 3 <script setup> format');
                        // For script setup, we'll extract reactive variables and functions
                        componentOptions = {
                          isScriptSetup: true,
                          scriptContent: scriptContent
                        };
                      } else {
                        console.log('📝 Detected Options API format');
                        // Handle Options API format
                        let cleanScript = scriptContent;

                        // Remove import statements
                        cleanScript = cleanScript.replace(/import\\s+.*?from\\s+['"][^'"]*['"];?/g, '');

                        // Remove export default and extract the object
                        if (cleanScript.includes('export default')) {
                          cleanScript = cleanScript.replace(/export\\s+default\\s*/, '');
                        }

                        // If it's wrapped in an object, extract it
                        if (cleanScript.trim().startsWith('{') && cleanScript.trim().endsWith('}')) {
                          cleanScript = cleanScript.trim().slice(1, -1);
                        }

                        // Create a safer evaluation with better error handling
                        try {
                          const safeEval = new Function('return {' + cleanScript + '}');
                          componentOptions = safeEval();
                          console.log('✅ Options API parsed successfully:', Object.keys(componentOptions));
                        } catch (evalError) {
                          console.warn('⚠️ Could not parse Options API object, trying alternative approach:', evalError);

                          // Try to extract individual sections
                          componentOptions = {};

                          // Extract data function
                          const dataMatch = cleanScript.match(/data\\s*\\(\\s*\\)\\s*\\{([^}]+)\\}/);
                          if (dataMatch) {
                            try {
                              componentOptions.data = new Function('return function() { ' + dataMatch[1] + ' }')();
                            } catch (e) {
                              console.warn('Could not parse data function:', e);
                            }
                          }

                          // Extract methods
                          const methodsMatch = cleanScript.match(/methods\\s*:\\s*\\{([^}]+)\\}/);
                          if (methodsMatch) {
                            try {
                              componentOptions.methods = new Function('return {' + methodsMatch[1] + '}')();
                            } catch (e) {
                              console.warn('Could not parse methods:', e);
                            }
                          }

                          // Extract computed
                          const computedMatch = cleanScript.match(/computed\\s*:\\s*\\{([^}]+)\\}/);
                          if (computedMatch) {
                            try {
                              componentOptions.computed = new Function('return {' + computedMatch[1] + '}')();
                            } catch (e) {
                              console.warn('Could not parse computed:', e);
                            }
                          }
                        }
                      }

                      console.log('✅ Script options extracted successfully');
                    } catch (e) {
                      console.warn('⚠️ Could not parse script section:', e);
                      componentOptions = {};
                    }
                  }
                }
              } catch (e) {
                console.error('❌ Error processing template:', e);
                processedTemplate = '<div class="p-4 text-red-600">Error processing template: ' + e.message + '</div>';
                componentOptions = {};
              }

              // Enhanced Vue app creation with better error handling
              const { createApp, ref, reactive, onMounted, computed } = Vue;

              const app = createApp({
                template: '<div class="component-wrapper">' + processedTemplate + '</div>',
                setup() {
                  console.log('🔧 Setting up Vue component...');

                  if (componentOptions.isScriptSetup) {
                    console.log('⚡ Using script setup approach');

                    // For script setup, we need to execute the script content in the setup context
                    try {
                      // Create a safe execution context with Vue 3 APIs
                      const setupContext = {
                        ref, reactive, computed, onMounted, watch: Vue.watch,
                        nextTick: Vue.nextTick, watchEffect: Vue.watchEffect,
                        console: console
                      };

                      // Clean and prepare the script content
                      let cleanScriptContent = componentOptions.scriptContent;

                      // Remove import statements (they won't work in this context)
                      cleanScriptContent = cleanScriptContent.replace(/import\\s+.*?from\\s+['"][^'"]*['"];?/g, '');

                      // Remove defineProps, defineEmits calls and capture them
                      const propsMatch = cleanScriptContent.match(/const\\s+props\\s*=\\s*defineProps\\s*\\(([^)]+)\\)/);
                      const emitsMatch = cleanScriptContent.match(/const\\s+emits\\s*=\\s*defineEmits\\s*\\(([^)]+)\\)/);

                      cleanScriptContent = cleanScriptContent.replace(/const\\s+props\\s*=\\s*defineProps\\s*\\([^)]+\\);?/g, '');
                      cleanScriptContent = cleanScriptContent.replace(/const\\s+emits\\s*=\\s*defineEmits\\s*\\([^)]+\\);?/g, '');

                      // Extract all variable declarations and function definitions with improved patterns
                      const variableMatches = cleanScriptContent.match(/(?:const|let|var)\\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\\s*=/g) || [];
                      const arrowFunctionMatches = cleanScriptContent.match(/(?:const|let|var)\\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\\s*=\\s*(?:\\([^)]*\\)\\s*=>|\\([^)]*\\)\\s*=>\\s*\\{|[a-zA-Z_$][a-zA-Z0-9_$]*\\s*=>)/g) || [];
                      const regularFunctionMatches = cleanScriptContent.match(/(?:const|let|var)\\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\\s*=\\s*function/g) || [];
                      const directFunctionMatches = cleanScriptContent.match(/function\\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\\s*\\(/g) || [];

                      // Also look for reactive/ref declarations
                      const refMatches = cleanScriptContent.match(/(?:const|let|var)\\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\\s*=\\s*ref\\s*\\(/g) || [];
                      const reactiveMatches = cleanScriptContent.match(/(?:const|let|var)\\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\\s*=\\s*reactive\\s*\\(/g) || [];
                      const computedMatches = cleanScriptContent.match(/(?:const|let|var)\\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\\s*=\\s*computed\\s*\\(/g) || [];

                      // Extract variable names
                      const extractedVars = new Set();

                      // Helper function to extract variable name from match
                      const extractVarName = (match, pattern) => {
                        try {
                          const result = match.match(pattern);
                          return result ? result[1] : null;
                        } catch (e) {
                          console.warn('Error extracting variable name from:', match, e);
                          return null;
                        }
                      };

                      // Process all variable declarations
                      variableMatches.forEach(match => {
                        const varName = extractVarName(match, /(?:const|let|var)\\s+([a-zA-Z_$][a-zA-Z0-9_$]*)/);
                        if (varName) extractedVars.add(varName);
                      });

                      // Process arrow functions
                      arrowFunctionMatches.forEach(match => {
                        const funcName = extractVarName(match, /(?:const|let|var)\\s+([a-zA-Z_$][a-zA-Z0-9_$]*)/);
                        if (funcName) extractedVars.add(funcName);
                      });

                      // Process regular functions
                      regularFunctionMatches.forEach(match => {
                        const funcName = extractVarName(match, /(?:const|let|var)\\s+([a-zA-Z_$][a-zA-Z0-9_$]*)/);
                        if (funcName) extractedVars.add(funcName);
                      });

                      // Process direct function declarations
                      directFunctionMatches.forEach(match => {
                        const funcName = extractVarName(match, /function\\s+([a-zA-Z_$][a-zA-Z0-9_$]*)/);
                        if (funcName) extractedVars.add(funcName);
                      });

                      // Process reactive declarations
                      refMatches.forEach(match => {
                        const varName = extractVarName(match, /(?:const|let|var)\\s+([a-zA-Z_$][a-zA-Z0-9_$]*)/);
                        if (varName) extractedVars.add(varName);
                      });

                      reactiveMatches.forEach(match => {
                        const varName = extractVarName(match, /(?:const|let|var)\\s+([a-zA-Z_$][a-zA-Z0-9_$]*)/);
                        if (varName) extractedVars.add(varName);
                      });

                      computedMatches.forEach(match => {
                        const varName = extractVarName(match, /(?:const|let|var)\\s+([a-zA-Z_$][a-zA-Z0-9_$]*)/);
                        if (varName) extractedVars.add(varName);
                      });

                      // Create dynamic return statement
                      const returnVars = Array.from(extractedVars).join(', ');
                      const returnStatement = returnVars ? 'return { ' + returnVars + ' };' : 'return {};';

                      console.log('🔍 Detected variables/functions:', Array.from(extractedVars));

                      // Execute the script setup content with dynamic return
                      const setupFunction = new Function(
                        'ref', 'reactive', 'computed', 'onMounted', 'watch', 'nextTick', 'watchEffect', 'console',
                        cleanScriptContent + '; ' + returnStatement
                      );

                      const setupResult = setupFunction(
                        ref, reactive, computed, onMounted,
                        Vue.watch, Vue.nextTick, Vue.watchEffect, console
                      );

                      // Setup lifecycle for render time tracking
                      onMounted(() => {
                        const endTime = performance.now();
                        const renderTime = Math.round(endTime - startTime);
                        reportSuccess(renderTime);
                      });

                      console.log('✅ Script setup executed successfully with result:', Object.keys(setupResult));
                      return setupResult;

                    } catch (e) {
                      console.warn('⚠️ Could not execute script setup, using fallback:', e);
                      console.log('Script content that failed:', componentOptions.scriptContent);
                      // Fallback to default setup
                      return createDefaultSetup();
                    }
                  } else {
                    console.log('📋 Using Options API approach');
                    return createOptionsAPISetup();
                  }

                  function createDefaultSetup() {
                    // Default reactive data
                    const title = ref('New Component');
                    const description = ref('Edit this code to create your component');
                    const clicked = ref(false);
                    const clickCount = ref(0);

                    // Default computed
                    const isActive = computed(() => clickCount.value > 0);

                    // Toast notification function
                    const showToast = (message, type = 'success') => {
                      const toast = document.createElement('div');
                      toast.className = 'toast-notification';
                      toast.textContent = message;

                      if (type === 'error') {
                        toast.style.background = '#ef4444';
                      } else if (type === 'warning') {
                        toast.style.background = '#f59e0b';
                      }

                      document.body.appendChild(toast);

                      // Auto remove after 3 seconds
                      setTimeout(() => {
                        toast.classList.add('fade-out');
                        setTimeout(() => {
                          if (toast.parentNode) {
                            toast.parentNode.removeChild(toast);
                          }
                        }, 300);
                      }, 3000);
                    };

                    // Default methods
                    const handleClick = () => {
                      console.log('Button clicked!');
                      clicked.value = true;
                      clickCount.value++;

                      // Show toast notification instead of alert (sandbox safe)
                      showToast('✅ Button clicked successfully!');
                      console.log('✅ Button clicked successfully!');

                      // Reset after 3 seconds
                      setTimeout(() => {
                        clicked.value = false;
                      }, 3000);
                    };

                    const resetCount = () => {
                      clickCount.value = 0;
                      clicked.value = false;
                      console.log('Count reset!');
                    };

                    // Setup lifecycle
                    onMounted(() => {
                      const endTime = performance.now();
                      const renderTime = Math.round(endTime - startTime);
                      reportSuccess(renderTime);
                      console.log('Component mounted with Vue 3 Composition API!');
                    });

                    return {
                      title, description, clicked, clickCount, isActive,
                      handleClick, resetCount
                    };
                  }

                  function createOptionsAPISetup() {
                    // Create reactive data from Options API
                    let componentData = reactive({
                      message: 'Hello from component!',
                      clicked: false,
                      title: 'New Component',
                      description: 'Edit this code to create your component'
                    });

                    // Merge any data from extracted script
                    if (componentOptions.data && typeof componentOptions.data === 'function') {
                      try {
                        const extractedData = componentOptions.data();
                        componentData = reactive({ ...componentData, ...extractedData });
                        console.log('✅ Merged Options API data:', Object.keys(extractedData));
                      } catch (e) {
                        console.warn('⚠️ Could not execute data function:', e);
                      }
                    }

                    // Toast notification function
                    const showToast = (message, type = 'success') => {
                      const toast = document.createElement('div');
                      toast.className = 'toast-notification';
                      toast.textContent = message;

                      if (type === 'error') {
                        toast.style.background = '#ef4444';
                      } else if (type === 'warning') {
                        toast.style.background = '#f59e0b';
                      }

                      document.body.appendChild(toast);

                      // Auto remove after 3 seconds
                      setTimeout(() => {
                        toast.classList.add('fade-out');
                        setTimeout(() => {
                          if (toast.parentNode) {
                            toast.parentNode.removeChild(toast);
                          }
                        }, 300);
                      }, 3000);
                    };

                    // Create default methods
                    const defaultMethods = {
                      handleClick: () => {
                        console.log('Button clicked!');
                        componentData.clicked = true;

                        // Show toast notification instead of alert (sandbox safe)
                        showToast('✅ Button clicked successfully!');
                        console.log('✅ Button clicked successfully!');

                        // Reset after 3 seconds
                        setTimeout(() => {
                          componentData.clicked = false;
                        }, 3000);
                      }
                    };

                    // Merge any methods from extracted script
                    const extractedMethods = componentOptions.methods || {};

                    // Bind extracted methods to the component data context
                    const boundMethods = {};
                    Object.keys(extractedMethods).forEach(methodName => {
                      if (typeof extractedMethods[methodName] === 'function') {
                        boundMethods[methodName] = extractedMethods[methodName].bind({
                          ...componentData,
                          ...defaultMethods,
                          showToast
                        });
                      }
                    });

                    const methods = {
                      ...defaultMethods,
                      ...boundMethods
                    };

                    console.log('✅ Methods prepared:', Object.keys(methods));

                    // Setup lifecycle
                    onMounted(() => {
                      const endTime = performance.now();
                      const renderTime = Math.round(endTime - startTime);
                      reportSuccess(renderTime);

                      // Call original mounted if exists
                      if (componentOptions.mounted) {
                        componentOptions.mounted.call({ ...componentData, ...methods });
                      }
                    });

                    // Process computed properties
                    const extractedComputed = componentOptions.computed || {};
                    const processedComputed = {};

                    Object.keys(extractedComputed).forEach(computedName => {
                      if (typeof extractedComputed[computedName] === 'function') {
                        // Convert computed function to Vue 3 computed
                        processedComputed[computedName] = computed(() => {
                          return extractedComputed[computedName].call({
                            ...componentData,
                            ...methods
                          });
                        });
                      }
                    });

                    console.log('✅ Computed properties prepared:', Object.keys(processedComputed));

                    // Return everything to template
                    return {
                      ...componentData,
                      ...methods,
                      ...processedComputed
                    };
                  }
                },
                errorCaptured(err, instance, info) {
                  console.error('Vue Error Captured:', err, info);
                  reportError(err);
                  return false;
                }
              });

              // No Quasar configuration - using only Vue and Tailwind
              console.log('✅ Vue app configured (Tailwind + Vue only)');

              // Mount the app
              app.mount('#app-mount-point');
              console.log('✅ Vue app mounted successfully');

            } catch(e) {
              console.error('❌ Error mounting Vue:', e);
              reportError(e);

              // Show user-friendly error
              const errorElement = document.getElementById('app-mount-point') || document.body;
              errorElement.innerHTML =
                '<div style="padding: 20px; background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; color: #dc2626; font-family: system-ui, sans-serif;">' +
                  '<h3 style="margin: 0 0 10px 0; font-size: 16px; font-weight: 600;">⚠️ Component Rendering Error</h3>' +
                  '<p style="margin: 0 0 10px 0; font-size: 14px;">' + e.message + '</p>' +
                  '<details style="margin-top: 10px;">' +
                    '<summary style="cursor: pointer; font-size: 12px; color: #991b1b;">Show Details</summary>' +
                    '<pre style="margin: 10px 0 0 0; padding: 10px; background: #fee2e2; border-radius: 4px; font-size: 11px; overflow-x: auto;">' + (e.stack || 'No stack trace available') + '</pre>' +
                  '</details>' +
                '</div>';
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

        // Start the mounting process with proper DOM waiting
        waitForDOM();
      <\/script>`
      : "";

  return `
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Component Preview</title>
        ${tailwindLink}
        <style>
          * { box-sizing: border-box; }
          html, body {
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            line-height: 1.5;
            background: #ffffff;
          }
          .component-wrapper {
            width: 100%;
            min-height: 100px;
          }
          /* Simple button styles for non-Quasar buttons */
          .btn {
            display: inline-flex;
            align-items: center;
            padding: 8px 16px;
            background-color: #3b82f6;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 500;
            transition: background-color 0.2s;
          }
          .btn:hover {
            background-color: #2563eb;
          }
          .btn-primary {
            background-color: #3b82f6;
          }
          .btn-primary:hover {
            background-color: #2563eb;
          }

          /* Toast notification styles */
          .toast-notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #10b981;
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            z-index: 1000;
            animation: slideInRight 0.3s ease-out;
            font-family: system-ui, sans-serif;
            font-size: 14px;
            font-weight: 500;
          }

          @keyframes slideInRight {
            from {
              transform: translateX(100%);
              opacity: 0;
            }
            to {
              transform: translateX(0);
              opacity: 1;
            }
          }

          .toast-notification.fade-out {
            animation: fadeOut 0.3s ease-out forwards;
          }

          @keyframes fadeOut {
            from {
              opacity: 1;
              transform: translateX(0);
            }
            to {
              opacity: 0;
              transform: translateX(100%);
            }
          }
          ${props.baseStyles}
        </style>
      </head>
      <body>
        ${props.framework === "vue" ? "" : props.content}
        ${vueScript}
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
    renderError.value = null;
    renderStatus.value = null;
    loadingMessage.value = "Reloading component...";
  }
);

// Listen for messages from iframe
const handleMessage = (event) => {
  if (event.data && event.data.type) {
    switch (event.data.type) {
      case "render-status":
        renderStatus.value = event.data.status;
        loadingMessage.value = event.data.message;
        break;
      case "render-error":
        renderError.value = event.data.error;
        renderStatus.value = "error";
        isLoading.value = false;
        break;
      case "render-success":
        renderStatus.value = "success";
        renderTime.value = event.data.renderTime;
        isLoading.value = false;
        break;
    }
  }
};

const onIframeLoad = () => {
  loadingMessage.value = "Calculating dimensions...";

  // Add message listener for iframe communication
  window.addEventListener("message", handleMessage);

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

  // Set a timeout to hide loading if no message is received
  setTimeout(() => {
    if (isLoading.value && !renderError.value) {
      isLoading.value = false;
      renderStatus.value = "warning";
    }
  }, 5000);
};

const onIframeError = () => {
  renderError.value = "Failed to load component iframe";
  renderStatus.value = "error";
  isLoading.value = false;
};

const refreshIframe = () => {
  if (!iframeRef.value) return;
  isLoading.value = true;
  renderError.value = null;
  renderStatus.value = null;
  loadingMessage.value = "Refreshing component...";

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

// Device switching
const setDevice = (device) => {
  currentDevice.value = device;
  $q.notify({
    message: `Switched to ${device.name} view`,
    color: "primary",
    position: "top",
    timeout: 1000,
  });
};

// Copy code functionality
const copyCode = async () => {
  try {
    await navigator.clipboard.writeText(props.content);
    $q.notify({
      message: "Code copied to clipboard!",
      color: "positive",
      position: "top",
      timeout: 2000,
      icon: "content_copy",
    });
  } catch (err) {
    console.error("Failed to copy code:", err);
    $q.notify({
      message: "Failed to copy code",
      color: "negative",
      position: "top",
      timeout: 2000,
    });
  }
};

// Cleanup on unmount
onMounted(() => {
  return () => {
    document.body.style.overflow = "";
    window.removeEventListener("message", handleMessage);
  };
});
</script>

<style scoped>
.component-viewer {
  transition: all 0.3s ease;
  font-family: "Roboto", sans-serif;
}

.iframe-container {
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.device-frame {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
}

.device-frame:hover {
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.device-header {
  background: linear-gradient(90deg, #374151 0%, #1f2937 100%);
}

/* Enhanced code display */
pre code {
  font-family: "Monaco", "Menlo", "Ubuntu Mono", monospace;
  line-height: 1.5;
}

/* Loading animation */
@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.q-spinner {
  animation: pulse 2s infinite;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .device-frame {
    width: 100% !important;
    max-width: 100% !important;
  }

  .iframe-container {
    padding: 8px !important;
  }
}

/* Fullscreen mode */
.iframe-container.fixed {
  background: #f9fafb;
}

/* Status chip animations */
.q-chip {
  transition: all 0.2s ease;
}

/* Button hover effects */
.q-btn {
  transition: all 0.2s ease;
}

.q-btn:hover {
  transform: translateY(-1px);
}

/* Error state styling */
.bg-red-50 {
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0%,
  100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-5px);
  }
  75% {
    transform: translateX(5px);
  }
}

/* Success state styling */
.render-success {
  border-left: 4px solid #10b981;
}

/* Code syntax highlighting enhancement */
.bg-gray-900 {
  background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%) !important;
}
</style>
