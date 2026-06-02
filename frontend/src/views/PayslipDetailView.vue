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

onMounted(() => {
    loadPayslipDetail();
});
</script>


<template>
    <div class="container">
        <button @click="goBack">Back</button>

        <h1>Payslip Detail</h1>

        <p v-if="isLoading">กำลังโหลดข้อมูล...</p>

        <p v-if="errorMessage" class="error">
            {{ errorMessage }}
        </p>

        <div v-if="payslip" class="card">
            <h2>{{ payslip.salary_month }}/{{ payslip.salary_year }}</h2>

            <p><strong>Employee Code:</strong> {{ payslip.employee_code }}</p>
            <p><strong>Department:</strong> {{ payslip.department }}</p>
            <p><strong>Position:</strong> {{ payslip.position }}</p>

            <hr />

            <h3>Income</h3>
            <p>Base Salary: {{ payslip.base_salary }}</p>
            <p>Paid Salary: {{ payslip.paid_salary }}</p>
            <p>Allowance: {{ payslip.allowance }}</p>
            <p>Overtime Pay: {{ payslip.overtime_pay }}</p>
            <p>Bonus: {{ payslip.bonus }}</p>
            <p>Other Income: {{ payslip.other_income }}</p>
            <p>Adjust Amount: {{ payslip.adjust_amount }}</p>
            <p>Special Amount: {{ payslip.special_amount }}</p>

            <hr />

            <h3>Deduction</h3>
            <p>Expense Deduction: {{ payslip.expense_deduction }}</p>
            <p>Social Security: {{ payslip.social_security }}</p>
            <p>Provident Fund: {{ payslip.provident_fund }}</p>
            <p>Tax: {{ payslip.tax }}</p>
            <p>Other Deduction: {{ payslip.other_deduction }}</p>

            <hr />

            <h3>Summary</h3>
            <p><strong>Total Income:</strong> {{ payslip.total_income }}</p>
            <p><strong>Total Deduction:</strong> {{ payslip.total_deduction }}</p>
            <p><strong>Net Salary:</strong> {{ payslip.net_salary }}</p>
        </div>
    </div>
</template>


<style scoped>
.container {
    max-width: 800px;
    margin: 40px auto;
}

.card {
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
}

button {
    margin-bottom: 16px;
    padding: 8px 12px;
}

.error {
    color: red;
}
</style>