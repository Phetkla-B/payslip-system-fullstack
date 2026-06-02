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
    <div class="container">
        <h1>รายการเงินเดือน</h1>

        <p v-if="isLoading">กำลังโหลดข้อมูล...</p>

        <p v-if="errorMessage" class="error">
            {{ errorMessage }}
        </p>

        <table v-if="payslips.length > 0">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>เดือน</th>
                    <th>ปี</th>
                    <th>เงินเดือนสุทธิ</th>
                    <th>ดูรายละเอียด</th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="payslip in payslips" :key="payslip.id">
                    <td>{{ payslip.id }}</td>
                    <td>{{ payslip.salary_month }}</td>
                    <td>{{ payslip.salary_year }}</td>
                    <td>{{ payslip.net_salary }}</td>
                    <td>
                        <button @click="goToDetail(payslip.id)">
                            Detail
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>

        <p v-else-if="!isLoading">
            ยังไม่มีข้อมูลเงินเดือน
        </p>
    </div>
</template>


<style scoped>
.container {
    max-width: 900px;
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
    background: #f3f4f6;
}

button {
    padding: 6px 12px;
    cursor: pointer;
}

.error {
    color: red;
}
</style>