<script setup>
import { ref, onMounted } from "vue";
import api from "../api/axios.js";

// Upload history list
const histories = ref([]);

// UI state
const errorMessage = ref("");
const isLoading = ref(false);

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

// Run when page is opened
onMounted(() => {
    loadUploadHistory();
});
</script>


<template>
    <div class="container">
        <h1>Upload History</h1>

        <p v-if="isLoading">กำลังโหลดข้อมูล...</p>

        <p v-if="errorMessage" class="error">
            {{ errorMessage }}
        </p>

        <table v-if="histories.length > 0">
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
                <tr v-for="history in histories" :key="history.id">
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

    th,
    td {
        padding: 10px;
        border: 1px solid #ddd;
        text-align: left;
    }

    th {
        backgroind: #f3f4f6;
    }

    .error {
        color: red;
    }
</style>