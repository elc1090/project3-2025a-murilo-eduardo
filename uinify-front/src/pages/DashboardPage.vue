<template>
  <div class="q-pa-md">
    <div class="row items-center q-mb-md">
      <div class="col">
        <h4 class="text-h4 q-my-none">My Components Dashboard</h4>
        <p class="text-subtitle1 text-grey-7">
          Manage and view all your components
        </p>
      </div>
      <div class="col-auto">
        <q-btn
          color="primary"
          icon="add"
          label="New Component"
          @click="createNewComponent"
        />
      </div>
    </div>

    <q-table
      :rows="components"
      :columns="columns"
      row-key="id"
      :loading="loading"
      :pagination="pagination"
      @request="onRequest"
      binary-state-sort
      grid
      class="my-grid-table"
    >
      <template v-slot:loading>
        <q-inner-loading showing color="primary" />
      </template>

      <template v-slot:no-data="{ message }">
        <div class="full-width row flex-center text-accent q-gutter-sm">
          <q-icon size="2em" name="sentiment_dissatisfied" />
          <span>{{ message }}</span>
        </div>
      </template>

      <template v-slot:item="props">
        <div class="q-pa-xs col-xs-12 col-sm-6 col-md-4 col-lg-3">
          <q-card class="component-card">
            <q-card-section class="text-center">
              <div class="text-h6 q-mb-xs">{{ props.row.name }}</div>
              <div class="text-caption q-mb-sm">ID: {{ props.row.id }}</div>
              <q-chip
                :color="getStatusColor(props.row.status)"
                text-color="white"
                :label="props.row.status || 'Unknown'"
                size="sm"
                class="q-mb-sm"
              />
            </q-card-section>

            <q-card-section class="q-pt-none">
              <div class="text-body2 q-mb-sm">
                <strong>Framework:</strong> {{ props.row.framework || "N/A" }}
              </div>
              <div class="text-body2 q-mb-sm">
                <strong>Created:</strong> {{ formatDate(props.row.created_at) }}
              </div>
              <div class="text-body2 description-text">
                <strong>Description:</strong>
                <div class="q-mt-xs">
                  {{ props.row.description || "No description available" }}
                </div>
              </div>
            </q-card-section>

            <q-separator />

            <q-card-actions align="center" class="q-pa-md">
              <q-btn
                flat
                round
                color="primary"
                icon="visibility"
                @click="viewComponent(props.row)"
                size="sm"
              >
                <q-tooltip>View Component</q-tooltip>
              </q-btn>
              <q-btn
                flat
                round
                color="orange"
                icon="edit"
                @click="editComponent(props.row.id)"
                size="sm"
              >
                <q-tooltip>Edit Component</q-tooltip>
              </q-btn>
              <q-btn
                flat
                round
                color="negative"
                icon="delete"
                @click="deleteComponentConfirm(props.row)"
                size="sm"
              >
                <q-tooltip>Delete Component</q-tooltip>
              </q-btn>
            </q-card-actions>
          </q-card>
        </div>
      </template>
    </q-table>

    <!-- Component View Dialog -->
    <q-dialog v-model="viewDialog" maximized>
      <q-card class="bg-gray-50">
        <q-card-section class="bg-white border-b border-gray-200 p-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <q-icon name="visibility" color="primary" size="md" />
              <div>
                <h2 class="text-xl font-bold text-gray-900">
                  {{
                    selectedComponent?.title ||
                    selectedComponent?.name ||
                    "Component Preview"
                  }}
                </h2>
                <p class="text-sm text-gray-600">
                  {{
                    selectedComponent?.description || "No description available"
                  }}
                </p>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <q-chip
                :color="getStatusColor(selectedComponent?.status)"
                text-color="white"
                :label="selectedComponent?.status || 'Unknown'"
                size="sm"
              />
              <q-chip
                color="blue"
                text-color="white"
                :label="selectedComponent?.framework || 'Unknown'"
                size="sm"
              />
              <q-btn
                flat
                round
                dense
                icon="close"
                @click="closeViewDialog"
                class="text-gray-600 hover:text-gray-900"
              />
            </div>
          </div>
        </q-card-section>

        <q-card-section class="p-6 flex-1 overflow-auto">
          <ComponentViewer
            v-if="selectedComponent"
            :content="selectedComponent.code || defaultComponentCode"
            :framework="
              selectedComponent.inputType ||
              selectedComponent.framework ||
              'vue'
            "
            :include-tailwind="selectedComponent.includeTailwind !== false"
            :include-quasar="selectedComponent.includeQuasar !== false"
            class="w-full"
          />
          <div
            v-else
            class="flex items-center justify-center h-64 text-gray-500"
          >
            <div class="text-center">
              <q-icon name="error_outline" size="lg" class="mb-2" />
              <p>No component data available</p>
            </div>
          </div>
        </q-card-section>

        <q-card-actions class="bg-white border-t border-gray-200 p-4">
          <div class="flex items-center justify-between w-full">
            <div class="flex items-center space-x-4 text-sm text-gray-600">
              <span>
                <q-icon name="schedule" size="xs" class="mr-1" />
                Created: {{ formatDate(selectedComponent?.created_at) }}
              </span>
              <span v-if="selectedComponent?.updated_at">
                <q-icon name="update" size="xs" class="mr-1" />
                Updated: {{ formatDate(selectedComponent?.updated_at) }}
              </span>
            </div>
            <div class="flex items-center space-x-2">
              <q-btn
                flat
                color="orange"
                icon="edit"
                label="Edit"
                @click="editComponentFromDialog"
              />
              <q-btn
                flat
                color="primary"
                icon="close"
                label="Close"
                @click="closeViewDialog"
              />
            </div>
          </div>
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Delete Confirmation Dialog -->
    <q-dialog v-model="deleteDialog" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="warning" color="negative" text-color="white" />
          <span class="q-ml-sm"
            >Are you sure you want to delete this component?</span
          >
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" v-close-popup />
          <q-btn
            flat
            label="Delete"
            color="negative"
            @click="deleteComponent"
            v-close-popup
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "stores/auth";
import {
  getUserComponents,
  deleteComponent as deleteComponentAPI,
} from "src/services/DefaultService";
import { useQuasar } from "quasar";
import ComponentViewer from "src/components/ComponentViewer.vue";

const $q = useQuasar();
const router = useRouter();
const auth = useAuthStore();

// Reactive data
const components = ref([]);
const loading = ref(false);
const deleteDialog = ref(false);
const componentToDelete = ref(null);
const viewDialog = ref(false);
const selectedComponent = ref(null);

// Table configuration
const columns = [
  {
    name: "id",
    required: true,
    label: "ID",
    align: "left",
    field: "id",
    sortable: true,
  },
  {
    name: "name",
    required: true,
    label: "Component Name",
    align: "left",
    field: "name",
    sortable: true,
  },
  {
    name: "description",
    label: "Description",
    align: "left",
    field: "description",
    sortable: false,
  },
  {
    name: "framework",
    label: "Framework",
    align: "center",
    field: "framework",
    sortable: true,
  },
  {
    name: "status",
    label: "Status",
    align: "center",
    field: "status",
    sortable: true,
  },
  {
    name: "created_at",
    label: "Created",
    align: "center",
    field: "created_at",
    sortable: true,
  },
  {
    name: "actions",
    label: "Actions",
    align: "center",
    field: "actions",
    sortable: false,
  },
];

const pagination = ref({
  sortBy: "created_at",
  descending: true,
  page: 1,
  rowsPerPage: 10,
});

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
<\/script>`;

// Computed properties
const userId = computed(() => {
  return auth.authData?.user?.id;
});

// Methods
const fetchComponents = async () => {
  if (!userId.value) {
    $q.notify({
      type: "negative",
      message: "User not authenticated",
    });
    return;
  }

  loading.value = true;
  try {
    const { data } = await getUserComponents(userId.value);
    components.value = data || [];
  } catch (error) {
    console.error("Error fetching components:", error);
    $q.notify({
      type: "negative",
      message: "Failed to load components",
    });
  } finally {
    loading.value = false;
  }
};

const onRequest = (props) => {
  const { page, rowsPerPage, sortBy, descending } = props.pagination;

  pagination.value.page = page;
  pagination.value.rowsPerPage = rowsPerPage;
  pagination.value.sortBy = sortBy;
  pagination.value.descending = descending;

  // In a real app, you would make an API call here with the pagination parameters
  // For now, we'll just update the pagination
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

const viewComponent = (component) => {
  selectedComponent.value = component;
  viewDialog.value = true;
};

const closeViewDialog = () => {
  viewDialog.value = false;
  selectedComponent.value = null;
};

const editComponentFromDialog = () => {
  if (selectedComponent.value) {
    const id = selectedComponent.value.id;
    closeViewDialog();
    editComponent(id);
  }
};

const editComponent = (id) => {
  // Navigate to component edit page
  router.push(`/components/${id}/edit`);
};

const createNewComponent = () => {
  // Navigate to component creation page
  router.push("/share");
};

const deleteComponentConfirm = (component) => {
  componentToDelete.value = component;
  deleteDialog.value = true;
};

const deleteComponent = async () => {
  if (!componentToDelete.value) return;

  try {
    await deleteComponentAPI(componentToDelete.value.id);

    // Remove from local array
    const index = components.value.findIndex(
      (c) => c.id === componentToDelete.value.id
    );
    if (index > -1) {
      components.value.splice(index, 1);
    }

    $q.notify({
      type: "positive",
      message: "Component deleted successfully",
    });
  } catch (error) {
    console.error("Error deleting component:", error);
    $q.notify({
      type: "negative",
      message: "Failed to delete component",
    });
  }

  componentToDelete.value = null;
};

// Lifecycle
onMounted(() => {
  fetchComponents();
});
</script>

<style scoped>
/* Custom styles that can't be easily replaced with Tailwind */
.my-grid-table :deep(.q-table__grid-content) {
  flex-direction: row;
  flex-wrap: wrap;
}

.component-card {
  height: 100%;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border-radius: 12px;
}

.component-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.component-card :deep(.q-card__section:first-child) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.component-card :deep(.q-card__section:first-child .text-h6) {
  font-weight: 600;
  margin-bottom: 8px;
}

.component-card :deep(.q-card__section:first-child .text-caption) {
  opacity: 0.9;
}

.component-card :deep(.q-card__section:first-child .q-chip) {
  background: rgba(255, 255, 255, 0.2) !important;
  color: white !important;
  font-weight: 500;
}

.description-text {
  max-height: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
}

.component-card :deep(.q-card__actions) {
  background-color: #f8f9fa;
}

.component-card :deep(.q-card__actions .q-btn) {
  margin: 0 4px;
  transition: transform 0.2s ease;
}

.component-card :deep(.q-card__actions .q-btn:hover) {
  transform: scale(1.1);
}

/* Responsive adjustments using Tailwind-style media queries */
@media (max-width: 599px) {
  .component-card {
    margin-bottom: 16px;
  }
}

@media (min-width: 600px) and (max-width: 1023px) {
  .component-card {
    margin-bottom: 16px;
  }
}

@media (min-width: 1024px) {
  .component-card {
    margin-bottom: 20px;
  }
}
</style>
