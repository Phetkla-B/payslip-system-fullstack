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
    <div class="container">
        <h1>Upload History</h1>

        <div class="filters">
            <input
                v-model="searchMonth"
                type="number"
                min="1"
                max="12"
                placeholder="Month"
            />

            <input
                v-model="searchYear"
                type="number"
                placeholder="Year"
            />

            <select v-model="searchStatus">
                <option value="">All Status</option>
                <option value="success">Success</option>
                <option value="partial_failed">Partial Failed</option>
                <option value="failed">Failed</option>
            </select>

            <button @click="clearFilter">
                Clear
            </button>
        </div>

        <p v-if="isLoading">กำลังโหลดข้อมูล...</p>

        <p v-if="errorMessage" class="error">
            {{ errorMessage }}
        </p>

        <table v-if="filteredHistories.length > 0">
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
                    <td>{{ history.status }}</td>
                    <td>{{ history.created_at }}</td>
                </tr>
            </tbody>
        </table>

        <p v-else-if="!isLoading">
            ยังไม่มีประวัติการ Upload
        </p>
    </div>
</template>


<style scoped>
    .container {
        max-width: 1000px;
        margin: 40px auto;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }

    .filters {
        display: flex;
        gap: 12px;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .filters input,
    .filters select {
        padding: 8px;
        border: 1px solid #d0d5dd;
        border-radius: 6px;
    }

    .filters button {
        padding: 8px 12px;
        border: 1px solid #d0d5dd;
        border-radius: 6px;
        cursor: pointer;
    }

    th,
    td {
        padding: 10px;
        border: 1px solid #ddd;
        text-align: left;
    }

    th {
        background: #f3f4f6;
    }

    .error {
        color: red;
    }
</style>