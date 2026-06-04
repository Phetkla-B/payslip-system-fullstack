<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../api/axios.js"

const route = useRoute();
const router = useRouter();

const payslip = ref(null);
const errorMessage = ref("");
const isLoading = ref(false);

async function loadPayslipDetail() {
    errorMessage.value = "";
    isLoading.value = true;

    try {
        const response = await api.get(`/payslips/${route.params.id}`);
        payslip.value = response.data;
    } catch (error) {
        console.error("Load payslip detail failed:", error);
        errorMessage.value = "ไม่สามารถโหลดรายละเอียดเงินเดือนได้"
    } finally {
        isLoading.value = false;
    }
}

function goBack() {
    router.push("/payslips");
}

// Download PDF
async function downloadPdf() {
    try {
        const response = await api.get(
            `/payslips/${route.params.id}/download`,
            {
                responseType: "blob",
            }
        );

        const fileURL = window.URL.createObjectURL(new Blob([response.data]));
        const fileLink = document.createElement("a");

        fileLink.href = fileURL;
        fileLink.setAttribute(
            "download",
            `payslip_${route.params.id}.pdf`
        );

        document.body.appendChild(fileLink);
        fileLink.click();
        fileLink.remove();

        window.URL.revokeObjectURL(fileURL);
    } catch (error) {
        console.error("Download PDF failed:", error);

        if (error.response?.status === 404) {
            errorMessage.value = "ไม่พบข้อมูลเงินเดือน หรือคุณไม่มีสิทธิ์ดูข้อมูล";
        } else if (!error.response) {
            errorMessage.value = "ไม่สามารถเชื่อมต่อ Server ได้";
        } else {
            errorMessage.value = "ไม่สามารถโหลดรายละเอียดเงินเดือนได้";
        }
        
    }
}

onMounted(() => {
    loadPayslipDetail();
});
</script>


<template>
    <div class="page-container">
        <h1 class="page-title">Payslip Detail</h1>
        <p class="page-subtitle">
            View detail payslip information for selected month.
        </p>

        <div class="action-bar">
            <button class="btn btn-secondary" @click="goBack">
                Back
            </button>

            <button class="btn btn-primary" @click="downloadPdf">
                Download PDF
            </button>
        </div>

        <p v-if="isLoading" class="page-subtitle">
            กำลังโหลดข้อมูล...
        </p>

        <p v-if="errorMessage" class="alert-error">
            {{ errorMessage }}
        </p>

        <div v-if="payslip" class="detail-grid">
            <div class="card">
                <h2>Employee Information</h2>

                <p><strong>Employee Code:</strong> {{ payslip.employee_code }}</p>
                <p><strong>Citizen ID:</strong> {{ payslip.citizen_id }}</p>
                <p><strong>Department:</strong> {{ payslip.department }}</p>
                <p><strong>Position:</strong> {{ payslip.position }}</p>
                <p><strong>Period:</strong> {{ payslip.salary_month }}/{{ payslip.salary_year }}</p>
            </div>

            <div class="card">
                <h2>Summary</h2>
                
                <p><strong>Total Income:</strong> {{ payslip.total_income }}</p>
                <p><strong>Total Deduction:</strong> {{ payslip.total_deduction }}</p>
                <p><strong>Net Salary:</strong> {{ payslip.net_salary }}</p>
            </div>
                
            <div class="card">
                <h2>Income</h2>

                <p>Base Salary: {{ payslip.base_salary }}</p>
                <p>Paid Salary: {{ payslip.paid_salary }}</p>
                <p>Allowance: {{ payslip.allowance }}</p>
                <p>Overtime Pay: {{ payslip.overtime_pay }}</p>
                <p>Bonus: {{ payslip.bonus }}</p>
                <p>Other Income: {{ payslip.other_income }}</p>
                <p>Adjust Amount: {{ payslip.adjust_amount }}</p>
                <p>Special Amount: {{ payslip.special_amount }}</p>
            </div>

            <div class="card">
                <h2>Deduction</h2>

                <p>Expense Deduction: {{ payslip.expense_deduction }}</p>
                <p>Social Security: {{ payslip.social_security }}</p>
                <p>Provident Fund: {{ payslip.provident_fund }}</p>
                <p>Tax: {{ payslip.tax }}</p>
                <p>Other Deduction: {{ payslip.other_deduction }}</p>
            </div>
        </div>
    </div>
</template>


<style scoped>
.page-title,
.page-subtitle {
    text-align: center;
}

.action-bar {
    display: flex;
    justify-content: center;
    gap: 24px;
    margin-bottom: 32px;
}

.action-bar .btn {
    min-width: 140px;
}

.detail-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.card h2 {
    margin-top: 0;
    margin-bottom: 16px;
}

.card p {
    margin: 8px 0;
}

@media (max-width: 768px) {
    .detail-grid {
        grid-template-columns: 1fr;
    }
}
</style>