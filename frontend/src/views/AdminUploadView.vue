<script setup>
import { ref } from "vue";
import api from "../api/axios.js";

// From data
const salaryMonth = ref("");
const salaryYear = ref("");
const selectedFile = ref(null);

// Upload result
const uploadResult = ref(null);
const errorMessage = ref("");

// Handle file selection
function handleFileChange(event) {
    selectedFile.value = event.target.files[0];
}

// Upload payslip
async function uploadPayslip() {
    errorMessage.value = "";
    uploadResult.value = null;

    try {
        const formData = new FormData();

        formData.append("salary_month", salaryMonth.value);
        formData.append("salary_year", salaryYear.value);
        formData.append("file", selectedFile.value);

        const response = await api.post(
            "/admin/upload-payslip",
            formData,
            {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            }
        );

        uploadResult.value = response.data;

    } catch (error) {
        console.error(error);

        errorMessage.value =
            error.response?.data?.detail ||
            "Upload failed";
    }
}
</script>


<template>
    <div class="container">
        <h1>Upload Payslip</h1>

        <div class="form-group">
            <label>Salary Month</label>

            <input
                type="number"
                min="1"
                max="12"
                v-model="salaryMonth"
            />

        </div>

        <div class="form-group">
            <label>Salary Year</label>

            <input
                type="number"
                v-model="salaryYear"
            />

        </div>

        <dev class="form-group">
            <label>Excel File</label>

            <input
                type="file"
                accept=".xlsx,.xls"
                @change="handleFileChange"
            />

        </dev>

        <button @click="uploadPayslip">
            Upload
        </button>

        <p v-if="errorMessage" class="error">
            {{ errorMessage }}
        </p>

        <div
            v-if="uploadResult"
            class="result"
        >
            <h3>Upload Result</h3>

            <p>Total: {{ uploadResult.total_records }}</p>

            <p>Success: {{ uploadResult.success_records }}</p>

            <p>Failed: {{ uploadResult.failed_records }}</p>

            <p>Status: {{ uploadResult.status }}</p>
        </div>

    </div>
</template>


<style scoped>
.container {
    max-width: 600px;
    margin: 40px auto;
}

.form-group {
    margin-bottom: 16px;
}

input {
    width: 100%;
    padding: 8px;
}

button {
    padding: 10px 16px;
}

.error {
    color: red;
}

.result {
    margin-top: 20px;
    padding: 12px;
    border: 1px solid #ddd;
}
</style>