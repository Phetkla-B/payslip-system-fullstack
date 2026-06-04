<script setup>
import { ref, onMounted, computed } from "vue";
import api from "../api/axios.js";

// Upload history list
const histories = ref([]);
const searchMonth = ref("");
const searchYear = ref("");
const searchStatus = ref("");

// UI state
const errorMessage = ref("");
const isLoading = ref(false);

// search history
const filteredHistories = computed(() => {
    return histories.value.filter((history) => {
        const matchMonth = 
            searchMonth.value === "" ||
            String(history.salary_month) === String(searchMonth.value);
        
        const matchYear = 
            searchYear.value === "" ||
            String(history.salary_year) === String(searchYear.value);

        const matchStatus = 
            searchStatus.value === "" ||
            history.status === searchStatus.value;

        return matchMonth && matchYear && matchStatus;
    });
});

// Load upload history from backend
async function loadUploadHistory() {
    errorMessage.value = "";
    isLoading.value = true;

    try {
        const response = await api.get("/admin/upload-history");
        histories.value = response.data;
    } catch (error) {
        console.error(error);
        errorMessage.value = "ไม่สามารถโหลดประวัติการ Upload ได้";
    } finally {
        isLoading.value = false;
    }    
}

function clearFilter() {
    searchMonth.value = "";
    searchYear.value = "";
    searchStatus.value = "";
}

// Run when page is opened
onMounted(() => {
    loadUploadHistory();
});
</script>


<template>
    <div class="page-container">
        <h1 class="page-title">Upload History</h1>
        <p class="page-subtitle">
            View uploaded Excel files and import result.
        </p>

        <div class="card filter-card">
            <div class="filters">
                <input
                    class="form-control"
                    v-model="searchMonth"
                    type="number"
                    min="1"
                    max="12"
                    placeholder="Month"
                />

                <input
                    class="form-control"
                    v-model="searchYear"
                    type="number"
                    placeholder="Year"
                />

                <select 
                    class="form-control"
                    v-model="searchStatus"
                >
                    <option value="">All Status</option>
                    <option value="success">Success</option>
                    <option value="partial_failed">Partial Failed</option>
                    <option value="failed">Failed</option>
                </select>

                <button class="btn btn-secondary" @click="clearFilter">
                    Clear
                </button>
            </div>
        </div>

        <p v-if="isLoading" class="page-subtitle">
            กำลังโหลดข้อมูล...
        </p>

        <p v-if="errorMessage" class="alert-error">
            {{ errorMessage }}
        </p>

        <div
            v-if="filteredHistories.length > 0"
            class="table-wrapper"
        >
            <table class="data-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>File Name</th>
                        <th>Month</th>
                        <th>Year</th>
                        <th>Total</th>
                        <th>Success</th>
                        <th>Failed</th>
                        <th>Status</th>
                        <th>Created At</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="history in filteredHistories" :key="history.id">
                        <td>{{ history.id }}</td>
                        <td>{{ history.file_name }}</td>
                        <td>{{ history.salary_month }}</td>
                        <td>{{ history.salary_year }}</td>
                        <td>{{ history.total_records }}</td>
                        <td>{{ history.success_records }}</td>
                        <td>{{ history.failed_records }}</td>
                        <td>
                            <span
                                class="badge"
                                :class="{
                                    'badge-success': history.status === 'success',
                                    'badge-warning': history.status === 'partial_failed',
                                    'badge-danger': history.status === 'failed',
                                }"
                            >
                                {{ history.status }}
                            </span>
                        </td>
                        <td>{{ history.created_at }}</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div v-else-if="!isLoading" class="card">
            ยังไม่มีประวัติการ Upload
        </div>
    </div>
</template>


<style scoped>
.filter-card {
    margin-bottom: 20px;
}

.filters {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr auto;
    gap: 12px;
    align-items: center;
}

.table-wrapper {
    margin-top: 20px;
}

.page-title,
.page-subtitle {
    text-align: center;
}

@media (max-width: 768px) {
    .filters {
        grid-template-columns: 1fr;
    }
}
</style>