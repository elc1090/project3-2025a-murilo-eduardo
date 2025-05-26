<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header Section -->
    <div class="bg-white border-b border-gray-200 px-4 lg:px-6 py-6">
      <div class="max-w-7xl mx-auto">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Component Library</h1>
            <p class="text-gray-600 mt-1">
              Discover and explore {{ totalComponents }} components from the
              UInify community
            </p>
            <div class="flex items-center space-x-4 mt-2 text-sm text-gray-500">
              <span class="flex items-center">
                <q-icon name="widgets" size="xs" class="mr-1" />
                {{ filteredComponents.length }} components
              </span>
              <span class="flex items-center">
                <q-icon name="people" size="xs" class="mr-1" />
                {{ uniqueAuthors }} contributors
              </span>
              <span class="flex items-center">
                <q-icon name="code" size="xs" class="mr-1" />
                {{ uniqueFrameworks }} frameworks
              </span>
            </div>
          </div>

          <div class="flex items-center space-x-3">
            <q-btn
              flat
              icon="view_module"
              :color="viewMode === 'grid' ? 'primary' : 'grey'"
              @click="viewMode = 'grid'"
              class="hidden sm:flex"
            >
              <q-tooltip>Grid View</q-tooltip>
            </q-btn>
            <q-btn
              flat
              icon="view_list"
              :color="viewMode === 'list' ? 'primary' : 'grey'"
              @click="viewMode = 'list'"
              class="hidden sm:flex"
            >
              <q-tooltip>List View</q-tooltip>
            </q-btn>
            <q-btn
              color="primary"
              icon="add"
              label="New Component"
              @click="createNewComponent"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="bg-white border-b border-gray-200 px-4 lg:px-6 py-4">
      <div class="max-w-7xl mx-auto">
        <div class="flex flex-col gap-4">
          <!-- Top Row: Search and Sort -->
          <div class="flex flex-col sm:flex-row gap-4">
            <!-- Search -->
            <div class="flex-1">
              <q-input
                v-model="searchQuery"
                placeholder="Search components, descriptions, or authors..."
                outlined
                dense
                class="w-full"
                clearable
              >
                <template v-slot:prepend>
                  <q-icon name="search" />
                </template>
              </q-input>
            </div>

            <!-- Sort -->
            <q-select
              v-model="sortBy"
              :options="sortOptions"
              label="Sort by"
              outlined
              dense
              class="w-full sm:w-48"
            />
          </div>

          <!-- Bottom Row: Filters -->
          <div class="flex flex-col sm:flex-row gap-4">
            <!-- Framework Filter -->
            <q-select
              v-model="selectedFramework"
              :options="frameworkOptions"
              label="Framework"
              outlined
              dense
              clearable
              class="w-full sm:w-48"
            />

            <!-- Category Filter -->
            <q-select
              v-model="selectedCategory"
              :options="categoryOptions"
              label="Category"
              outlined
              dense
              clearable
              class="w-full sm:w-48"
            />

            <!-- Status Filter -->
            <q-select
              v-model="selectedStatus"
              :options="statusOptions"
              label="Status"
              outlined
              dense
              clearable
              class="w-full sm:w-48"
            />

            <!-- Author Filter -->
            <q-select
              v-model="selectedAuthor"
              :options="authorOptions"
              label="Author"
              outlined
              dense
              clearable
              use-input
              input-debounce="300"
              @filter="filterAuthors"
              class="w-full sm:w-48"
            />

            <!-- Clear Filters -->
            <q-btn
              v-if="hasActiveFilters"
              flat
              icon="clear"
              label="Clear"
              @click="clearFilters"
              class="self-start"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <q-spinner-dots size="50px" color="primary" />
      <span class="ml-3 text-gray-600">Loading components...</span>
    </div>

    <!-- Components Content -->
    <div v-else class="max-w-7xl mx-auto px-4 lg:px-6 py-6">
      <!-- Grid View -->
      <div
        v-if="viewMode === 'grid' && paginatedComponents.length > 0"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
      >
        <div
          v-for="component in paginatedComponents"
          :key="component.id"
          class="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-all duration-200 cursor-pointer group"
          @click="viewComponent(component)"
        >
          <!-- Component Header -->
          <div
            class="p-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-t-lg"
          >
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <h3 class="font-semibold text-lg mb-1 line-clamp-1">
                  {{
                    component?.title || component?.name || "Untitled Component"
                  }}
                </h3>
                <p class="text-blue-100 text-sm opacity-90">
                  by
                  {{
                    component?.author ||
                    component?.user?.name ||
                    component?.created_by ||
                    "Unknown"
                  }}
                </p>
              </div>
              <q-chip
                :color="getStatusColor(component.status)"
                text-color="white"
                :label="component.status || 'Draft'"
                size="sm"
                class="ml-2"
              />
            </div>
          </div>

          <!-- Component Body -->
          <div class="p-4">
            <p class="text-gray-600 text-sm mb-3 line-clamp-2">
              {{ component?.description || "No description available" }}
            </p>

            <!-- Tags -->
            <div
              v-if="component?.tags && component.tags.length > 0"
              class="mb-3"
            >
              <div class="flex flex-wrap gap-1">
                <q-chip
                  v-for="tag in component.tags.slice(0, 3)"
                  :key="tag"
                  color="grey-3"
                  text-color="grey-8"
                  size="sm"
                  :label="tag"
                />
                <q-chip
                  v-if="component.tags.length > 3"
                  color="grey-3"
                  text-color="grey-8"
                  size="sm"
                  :label="`+${component.tags.length - 3}`"
                />
              </div>
            </div>

            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <q-chip
                  color="blue"
                  text-color="white"
                  :label="component?.framework || 'Unknown'"
                  size="sm"
                />
                <span class="text-xs text-gray-500">
                  {{ formatDate(component?.created_at) }}
                </span>
              </div>
              <div
                class="flex space-x-1 opacity-0 group-hover:opacity-100 transition-opacity"
              >
                <q-btn
                  flat
                  round
                  dense
                  icon="visibility"
                  @click.stop="viewComponent(component)"
                  class="text-gray-600 hover:text-blue-600"
                  size="sm"
                >
                  <q-tooltip>View Component</q-tooltip>
                </q-btn>
                <q-btn
                  v-if="canEdit(component)"
                  flat
                  round
                  dense
                  icon="edit"
                  @click.stop="editComponent(component)"
                  class="text-gray-600 hover:text-orange-600"
                  size="sm"
                >
                  <q-tooltip>Edit Component</q-tooltip>
                </q-btn>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- List View -->
      <div
        v-else-if="viewMode === 'list' && paginatedComponents.length > 0"
        class="space-y-4"
      >
        <div
          v-for="component in paginatedComponents"
          :key="component.id"
          class="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-all duration-200 cursor-pointer p-6"
          @click="viewComponent(component)"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center space-x-3 mb-2">
                <h3 class="text-xl font-semibold text-gray-900">
                  {{
                    component?.title || component?.name || "Untitled Component"
                  }}
                </h3>
                <q-chip
                  :color="getStatusColor(component?.status)"
                  text-color="white"
                  :label="component?.status || 'Draft'"
                  size="sm"
                />
                <q-chip
                  color="blue"
                  text-color="white"
                  :label="component?.framework || 'Unknown'"
                  size="sm"
                />
              </div>

              <p class="text-gray-600 mb-3 line-clamp-2">
                {{ component?.description || "No description available" }}
              </p>

              <div class="flex items-center space-x-4 text-sm text-gray-500">
                <span class="flex items-center">
                  <q-icon name="person" size="xs" class="mr-1" />
                  {{
                    component?.author ||
                    component?.user?.name ||
                    component?.created_by ||
                    "Unknown"
                  }}
                </span>
                <span class="flex items-center">
                  <q-icon name="schedule" size="xs" class="mr-1" />
                  {{ formatDate(component?.created_at) }}
                </span>
                <span
                  v-if="component?.tags && component.tags.length > 0"
                  class="flex items-center"
                >
                  <q-icon name="local_offer" size="xs" class="mr-1" />
                  {{ component.tags.length }} tags
                </span>
              </div>
            </div>

            <div class="flex space-x-2 ml-4">
              <q-btn
                flat
                icon="visibility"
                label="View"
                @click.stop="viewComponent(component)"
                class="text-gray-600 hover:text-blue-600"
                size="sm"
              />
              <q-btn
                v-if="canEdit(component)"
                flat
                icon="edit"
                label="Edit"
                @click.stop="editComponent(component)"
                class="text-gray-600 hover:text-orange-600"
                size="sm"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div
        v-if="paginatedComponents.length > 0"
        class="flex items-center justify-between mt-8 pt-6 border-t border-gray-200"
      >
        <div class="text-sm text-gray-600">
          Showing {{ startIndex + 1 }} to {{ endIndex }} of
          {{ filteredComponents.length }} components
        </div>
        <q-pagination
          v-model="currentPage"
          :max="totalPages"
          :max-pages="7"
          direction-links
          boundary-links
          color="primary"
          class="q-mt-md"
        />
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-20">
        <q-icon name="widgets" size="64px" class="text-gray-400 mb-4" />
        <h3 class="text-xl font-semibold text-gray-900 mb-2">
          No Components Found
        </h3>
        <p class="text-gray-600 mb-6">
          {{
            hasActiveFilters
              ? "No components match your current filters."
              : "No components available yet."
          }}
        </p>
        <q-btn
          v-if="!hasActiveFilters"
          color="primary"
          icon="add"
          label="Create First Component"
          @click="createNewComponent"
        />
        <q-btn
          v-else
          flat
          color="primary"
          icon="clear"
          label="Clear Filters"
          @click="clearFilters"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useRouter } from "vue-router";
import { useQuasar } from "quasar";
import { useAuthStore } from "stores/auth";
import { getComponents } from "src/services/DefaultService";

const $q = useQuasar();
const router = useRouter();
const auth = useAuthStore();

// Reactive data
const components = ref([]);
const loading = ref(true);
const searchQuery = ref("");
const selectedFramework = ref(null);
const selectedCategory = ref(null);
const selectedStatus = ref(null);
const selectedAuthor = ref(null);
const sortBy = ref({ label: "Newest First", value: "created_at_desc" });
const viewMode = ref("grid");
const currentPage = ref(1);
const itemsPerPage = ref(12);

// Author options for filtering
const authorOptions = ref([]);

// Filter options
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

const statusOptions = [
  { label: "Active", value: "active" },
  { label: "Draft", value: "draft" },
  { label: "Archived", value: "archived" },
];

const sortOptions = [
  { label: "Newest First", value: "created_at_desc" },
  { label: "Oldest First", value: "created_at_asc" },
  { label: "Title A-Z", value: "title_asc" },
  { label: "Title Z-A", value: "title_desc" },
  { label: "Most Popular", value: "popular" },
];

// Computed
const totalComponents = computed(() => components.value.length);

const uniqueAuthors = computed(() => {
  const authors = new Set(
    components.value.map((c) => c.author || "Unknown").filter(Boolean)
  );
  return authors.size;
});

const uniqueFrameworks = computed(() => {
  const frameworks = new Set(
    components.value.map((c) => c.framework).filter(Boolean)
  );
  return frameworks.size;
});

const hasActiveFilters = computed(() => {
  return !!(
    searchQuery.value ||
    selectedFramework.value ||
    selectedCategory.value ||
    selectedStatus.value ||
    selectedAuthor.value
  );
});

const filteredComponents = computed(() => {
  if (!Array.isArray(components.value)) {
    return [];
  }

  let filtered = components.value;

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter((component) => {
      if (!component) return false;

      const title = component.title || component.name || "";
      const description = component.description || "";
      const author =
        component.author || component.user?.name || component.created_by || "";

      return (
        title.toLowerCase().includes(query) ||
        description.toLowerCase().includes(query) ||
        author.toLowerCase().includes(query)
      );
    });
  }

  // Framework filter
  if (selectedFramework.value) {
    filtered = filtered.filter(
      (component) => component?.framework === selectedFramework.value
    );
  }

  // Category filter
  if (selectedCategory.value) {
    filtered = filtered.filter(
      (component) => component?.category === selectedCategory.value
    );
  }

  // Status filter
  if (selectedStatus.value) {
    filtered = filtered.filter(
      (component) => component?.status === selectedStatus.value
    );
  }

  // Author filter
  if (selectedAuthor.value) {
    filtered = filtered.filter((component) => {
      const author =
        component?.author || component?.user?.name || component?.created_by;
      return author === selectedAuthor.value;
    });
  }

  // Sort
  if (sortBy.value) {
    filtered.sort((a, b) => {
      if (!a || !b) return 0;

      switch (sortBy.value.value) {
        case "created_at_desc":
          const dateA = a.created_at ? new Date(a.created_at) : new Date(0);
          const dateB = b.created_at ? new Date(b.created_at) : new Date(0);
          return dateB - dateA;
        case "created_at_asc":
          const dateA2 = a.created_at ? new Date(a.created_at) : new Date(0);
          const dateB2 = b.created_at ? new Date(b.created_at) : new Date(0);
          return dateA2 - dateB2;
        case "title_asc":
          const titleA = a.title || a.name || "";
          const titleB = b.title || b.name || "";
          return titleA.localeCompare(titleB);
        case "title_desc":
          const titleA2 = a.title || a.name || "";
          const titleB2 = b.title || b.name || "";
          return titleB2.localeCompare(titleA2);
        case "popular":
          return (b.views || 0) - (a.views || 0);
        default:
          return 0;
      }
    });
  }

  return filtered;
});

const totalPages = computed(() => {
  return Math.ceil(filteredComponents.value.length / itemsPerPage.value);
});

const startIndex = computed(() => {
  return (currentPage.value - 1) * itemsPerPage.value;
});

const endIndex = computed(() => {
  return Math.min(
    startIndex.value + itemsPerPage.value,
    filteredComponents.value.length
  );
});

const paginatedComponents = computed(() => {
  return filteredComponents.value.slice(startIndex.value, endIndex.value);
});

// Methods
const fetchComponents = async () => {
  loading.value = true;
  try {
    const response = await getComponents();

    // Handle different response structures
    let componentsData = [];
    if (response?.data) {
      componentsData = Array.isArray(response.data) ? response.data : [];
    } else if (Array.isArray(response)) {
      componentsData = response;
    }

    components.value = componentsData;

    // Extract unique authors for filter - with better error handling
    const authors = [
      ...new Set(
        components.value
          .map((c) => c?.author || c?.user?.name || c?.created_by)
          .filter(Boolean)
      ),
    ];

    authorOptions.value = authors.map((author) => ({
      label: author,
      value: author,
    }));

    console.log("Components loaded:", components.value.length);
  } catch (error) {
    console.error("Error fetching components:", error);

    // More specific error messages
    let errorMessage = "Failed to load components";
    if (error.response?.status === 404) {
      errorMessage = "Components endpoint not found";
    } else if (error.response?.status === 500) {
      errorMessage = "Server error while loading components";
    } else if (error.code === "NETWORK_ERROR") {
      errorMessage = "Network error - please check your connection";
    }

    $q.notify({
      type: "negative",
      message: errorMessage,
      caption: error.response?.data?.message || error.message,
    });

    // Set empty array on error to prevent undefined issues
    components.value = [];
  } finally {
    loading.value = false;
  }
};

const formatDate = (dateString) => {
  if (!dateString) return "N/A";
  return new Date(dateString).toLocaleDateString();
};

const getStatusColor = (status) => {
  switch (status?.toLowerCase()) {
    case "active":
      return "positive";
    case "draft":
      return "warning";
    case "archived":
      return "negative";
    default:
      return "grey";
  }
};

const canEdit = (component) => {
  // Users can only edit their own components
  const currentUserId = auth.authData?.user?.id;
  return (
    currentUserId &&
    (component.user_id === currentUserId ||
      component.author_id === currentUserId)
  );
};

const viewComponent = (component) => {
  router.push(`/components/${component.id}`);
};

const editComponent = (component) => {
  router.push(`/components/${component.id}/edit`);
};

const createNewComponent = () => {
  router.push("/share");
};

const clearFilters = () => {
  searchQuery.value = "";
  selectedFramework.value = null;
  selectedCategory.value = null;
  selectedStatus.value = null;
  selectedAuthor.value = null;
  currentPage.value = 1;
};

const filterAuthors = (val, update) => {
  if (val === "") {
    update(() => {
      const authors = [
        ...new Set(components.value.map((c) => c.author).filter(Boolean)),
      ];
      authorOptions.value = authors.map((author) => ({
        label: author,
        value: author,
      }));
    });
    return;
  }

  update(() => {
    const needle = val.toLowerCase();
    const authors = [
      ...new Set(components.value.map((c) => c.author).filter(Boolean)),
    ];
    authorOptions.value = authors
      .filter((author) => author.toLowerCase().includes(needle))
      .map((author) => ({ label: author, value: author }));
  });
};

// Watchers
watch(
  [
    searchQuery,
    selectedFramework,
    selectedCategory,
    selectedStatus,
    selectedAuthor,
    sortBy,
  ],
  () => {
    currentPage.value = 1; // Reset to first page when filters change
  }
);

// Lifecycle
onMounted(() => {
  fetchComponents();
});
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Enhanced hover effects */
.group:hover .group-hover\:opacity-100 {
  opacity: 1;
}

/* Custom scrollbar for better UX */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
