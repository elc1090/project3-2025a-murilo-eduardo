<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header Section -->
    <div class="bg-white border-b border-gray-200 px-4 lg:px-6 py-6">
      <div class="max-w-7xl mx-auto">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <q-btn
              flat
              round
              icon="arrow_back"
              @click="goBack"
              class="text-gray-600 hover:text-gray-900 hover:bg-gray-100"
            />
            <div>
              <h1 class="text-2xl font-bold text-gray-900">
                {{ component?.title || component?.name || 'Component View' }}
              </h1>
              <p class="text-gray-600 mt-1">
                {{ component?.description || 'No description available' }}
              </p>
            </div>
          </div>
          
          <div class="flex items-center space-x-3">
            <q-chip 
              :color="getStatusColor(component?.status)" 
              text-color="white" 
              :label="component?.status || 'Unknown'"
              size="md"
            />
            <q-chip 
              color="blue" 
              text-color="white" 
              :label="component?.framework || 'Unknown'"
              size="md"
            />
            <q-btn
              color="orange"
              icon="edit"
              label="Edit"
              @click="editComponent"
              :loading="loading"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <q-spinner-dots size="50px" color="primary" />
      <span class="ml-3 text-gray-600">Loading component...</span>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="flex items-center justify-center py-20">
      <div class="text-center">
        <q-icon name="error_outline" size="64px" class="text-red-500 mb-4" />
        <h3 class="text-xl font-semibold text-gray-900 mb-2">Error Loading Component</h3>
        <p class="text-gray-600 mb-4">{{ error }}</p>
        <q-btn
          color="primary"
          icon="refresh"
          label="Try Again"
          @click="fetchComponent"
        />
      </div>
    </div>

    <!-- Component Content -->
    <div v-else-if="component" class="max-w-7xl mx-auto px-4 lg:px-6 py-6">
      <!-- Component Metadata -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Component Information</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label class="text-sm font-medium text-gray-500">Framework</label>
            <p class="text-gray-900">{{ component.framework || 'N/A' }}</p>
          </div>
          <div>
            <label class="text-sm font-medium text-gray-500">Category</label>
            <p class="text-gray-900">{{ component.category || 'N/A' }}</p>
          </div>
          <div>
            <label class="text-sm font-medium text-gray-500">Created</label>
            <p class="text-gray-900">{{ formatDate(component.created_at) }}</p>
          </div>
          <div>
            <label class="text-sm font-medium text-gray-500">Last Updated</label>
            <p class="text-gray-900">{{ formatDate(component.updated_at) }}</p>
          </div>
        </div>
        
        <!-- Tags -->
        <div v-if="component.tags && component.tags.length > 0" class="mt-4">
          <label class="text-sm font-medium text-gray-500 block mb-2">Tags</label>
          <div class="flex flex-wrap gap-2">
            <q-chip
              v-for="tag in component.tags"
              :key="tag"
              color="blue"
              text-color="white"
              size="sm"
              :label="tag"
            />
          </div>
        </div>
      </div>

      <!-- Component Viewer -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <ComponentViewer
          :content="component.code || defaultComponentCode"
          :framework="component.inputType || component.framework || 'vue'"
          :include-tailwind="component.includeTailwind !== false"
          :include-quasar="component.includeQuasar !== false"
        />
      </div>
    </div>

    <!-- Not Found State -->
    <div v-else class="flex items-center justify-center py-20">
      <div class="text-center">
        <q-icon name="search_off" size="64px" class="text-gray-400 mb-4" />
        <h3 class="text-xl font-semibold text-gray-900 mb-2">Component Not Found</h3>
        <p class="text-gray-600 mb-4">The component you're looking for doesn't exist or has been removed.</p>
        <q-btn
          color="primary"
          icon="arrow_back"
          label="Go Back"
          @click="goBack"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { getComponentById } from 'src/services/DefaultService'
import ComponentViewer from 'src/components/ComponentViewer.vue'

// Props
const props = defineProps({
  id: {
    type: String,
    required: true
  }
})

const $q = useQuasar()
const route = useRoute()
const router = useRouter()

// Reactive data
const component = ref(null)
const loading = ref(true)
const error = ref(null)

// Default component code for fallback
const defaultComponentCode = `<template>
  <div class="p-6 bg-white rounded-lg shadow-lg border border-gray-200">
    <h2 class="text-2xl font-bold text-gray-800 mb-3">Sample Component</h2>
    <p class="text-gray-600 mb-4">This is a default component preview.</p>
    <button class="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded-md transition-colors duration-200">
      Click Me
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const message = ref('Hello from component!')
<\/script>`

// Computed
const componentId = computed(() => {
  return props.id || route.params.id
})

// Methods
const fetchComponent = async () => {
  if (!componentId.value) {
    error.value = 'No component ID provided'
    loading.value = false
    return
  }

  loading.value = true
  error.value = null

  try {
    const { data } = await getComponentById(componentId.value)
    component.value = data
  } catch (err) {
    console.error('Error fetching component:', err)
    error.value = err.response?.data?.message || 'Failed to load component'
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString()
}

const getStatusColor = (status) => {
  switch (status?.toLowerCase()) {
    case 'active':
      return 'positive'
    case 'draft':
      return 'warning'
    case 'archived':
      return 'negative'
    default:
      return 'grey'
  }
}

const editComponent = () => {
  router.push(`/components/${componentId.value}/edit`)
}

const goBack = () => {
  router.back()
}

// Lifecycle
onMounted(() => {
  fetchComponent()
})
</script>

<style scoped>
/* Custom styles for enhanced visual appeal */
.component-metadata {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}
</style>
