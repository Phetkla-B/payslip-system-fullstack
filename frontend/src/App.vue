<script setup>
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

// Check current page
const isLoginPage = computed(() => route.path === "/login");

// Read user role from localStorage
const userName = computed(() => localStorage.getItem("user_name"));
const userRole = computed(() => localStorage.getItem("user_role"));

// Logout user
function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("user_name");
  localStorage.removeItem("user_role");

  router.push("/login");
}
</script>


<template>
  <dev>
    <nav v-if="!isLoginPage" class="navbar">
      <div class="nav-left">
        <strong class="brand">Payslip System</strong>

        <router-link v-if="userRole === 'admin'" to="/admin/upload">
          Upload
        </router-link>

        <router-link v-if="userRole === 'admin'" to="/admin/upload-history">
          Upload History
        </router-link>

        <router-link v-if="userRole === 'employee'" to="/payslips">
          My Payslips
        </router-link>
        
      </div>

      <div class="nav-right">
        <span class="user-info">
          {{ userName }} ({{ userRole }})
        </span>

        <button class="btn btn-secondary logout-button" @click="logout">
          Logout
        </button>

      </div>
    </nav>

    <router-view />
  </dev>
</template>


<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-item: center;
  padding: 14px 32px;
  background: #111827;
  color: white;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
}

.nav-left,
.nav-right {
  display: flex;
  align-item: center;
  gap: 20px;
}

.brand {
  font-size: 18px;
  margin-right: 8px;
}

a {
  color: #e5e7eb;
  text-decoration: none;
  padding: 8px 10px;
  border-radius: 6px;
  font-weight: 600;
}

a.router-link-active {
  color: #2563eb;
  background: white;
}

.user-info {
  font-size: 14px;
  color: #d1d5db;
}

.logout-button {
  background: white;
  color: #111827;
}

@media (max-width: 768px) {
  .navbar a:hover {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .nav-left.
  .nav-right {
    flex-wrap: wrap;
    gap: 12px;
  }

}
</style>