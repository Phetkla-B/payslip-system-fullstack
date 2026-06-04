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

    // Validate month
    if (!salaryMonth.value) {
        errorMessage.value = "กรุณากรอกเดือนที่ต้องการ"
        return;
    }

    // Validate year
    if (!salaryYear.value) {
        errorMessage.value = "กรุณากรอกปีที่ต้องการ"
        return;
    }

    // Validate file
    if (!selectedFile.value) {
        errorMessage.value = "กรุณาเลือกไฟล์ Excel"
        return;
    }

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

        if (error.response?.status === 400) {
            errorMessage.value = error.response.data.detail || "ไฟล์ไม่ถูกต้อง";
        } else if (error.response?.status === 403) {
            errorMessage.value = "คุณไม่มีสิทธิ์ Upload ไฟล์";
        } else {
            errorMessage.value = "Upload ไม่สำเร็จ กรุณาลองใหม่";
        }
    }
}
</script>


<template>
    <div class="page-container">
        <h1 class="page-title">Upload Payslip</h1>
        <p class="page-subtitle">
            Upload Excel file for employee payslip data.
        </p>

        <div class="card upload-card">
            <div class="form-group">
                <label class="form-label">Salary Month</label>

                <input
                    class="form-control"
                    type="number"
                    min="1"
                    max="12"
                    v-model="salaryMonth"
                    placeholder="Example: 1"
                />
            </div>

            <div class="form-group">
                <label class="form-label">Salary Year</label>

                <input
                    class="form-control"
                    type="number"
                    v-model="salaryYear"
                    placeholder="Example: 2026"
                />
            </div>

            <div class="form-group">
                <label class="form-label">Excel File</label>
                <input
                    class="form-control"
                    type="file"
                    accept=".xlsx,.xls"
                    @change="handleFileChange"
                />
            </div>
        

            <button class="btn btn-primary" @click="uploadPayslip">
                Upload Payslip
            </button>

            <p v-if="errorMessage" class="alert-error">
                {{ errorMessage }}
            </p>

            <div
                v-if="uploadResult"
                class="alert-success"
            >
                <h3>Upload Result</h3>

                <p>Total: {{ uploadResult.total_records }}</p>

                <p>Success: {{ uploadResult.success_records }}</p>

                <p>Failed: {{ uploadResult.failed_records }}</p>

                <p>Status: {{ uploadResult.status }}</p>
            </div>
        </div>
    </div>
</template>


<style scoped>
.upload-card {
    max-width: 560px;
    margin: 0 auto;
}

.page-title,
.page-subtitle {
    text-align: center;
}
</style>