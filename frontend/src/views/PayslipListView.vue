<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../api/axios.js"

// Router is used to navigate to payslip detail page
const router = useRouter();

// Payslip list data
const payslips = ref([]);

// UI state
const isLoading = ref(false);
const errorMessage = ref("");


// Load payslip of current user
async function loadPayslip() {
    errorMessage.value = "";
    isLoading.value = true;

    try {
        const response = await api.get("/payslips");
        payslips.value = response.data;
    } catch (error) {
        console.error("Load payslips failed:", error);
        errorMessage.value = "ไม่สามารถโหลดรายการเงินเดือนได้"
    } finally {
        isLoading.value = false;
    }
}

// Go to payslip detail page
function goToDetail(payslipId) {
    router.push(`/payslips/${payslipId}`);
}

// Load data when page is opened
onMounted(() => {
    loadPayslip();
})
</script>


<template>
    <div class="page-container">
        <h1 class="page-title">My Payslips</h1>
        <p class="page-subtitle">
            View your monthly payslips records.
        </p>

        <p v-if="isLoading" class="page-subtitle">
            กำลังโหลดข้อมูล...
        </p>

        <p v-if="errorMessage" class="alert-error">
            {{ errorMessage }}
        </p>

        <div
            v-if="payslips.length > 0"
            class="table-wrapper"
        >
            <table class="data-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Month</th>
                        <th>Year</th>
                        <th>Total Income</th>
                        <th>Total Deduction</th>
                        <th>Net Salary</th>
                        <th>View Detail</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="payslip in payslips" :key="payslip.id">
                        <td>{{ payslip.id }}</td>
                        <td>{{ payslip.salary_month }}</td>
                        <td>{{ payslip.salary_year }}</td>
                        <td>{{ payslip.total_income }}</td>
                        <td>{{ payslip.total_deduction }}</td>
                        <td>
                            <strong>{{ payslip.net_salary }}</strong>
                        </td>
                        <td>
                            <button @click="goToDetail(payslip.id)">
                                Detail
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <p v-else-if="!isLoading" class="card">
            ยังไม่มีข้อมูลเงินเดือน
        </p>
    </div>
</template>


<style scoped>
.page-title,
.page-subtitle {
    text-align: center;
}
</style>